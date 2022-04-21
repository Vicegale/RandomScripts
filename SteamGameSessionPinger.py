import requests
import json
import time
import boto3
from boto3.dynamodb.conditions import Key

#Lambda function made to continuously ping the steam API for game change events in order to create a game log in DynamoDB

def get_steam_secret():

    secret_name = "prod/steam/apikey"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return json.loads(get_secret_value_response["SecretString"])["SteamAPIKey"]
    except:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            

def createSession(playerID, playerName, appID, gameName, dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb')
	
	table = dynamodb.Table('GameSessions')
	response = table.put_item(
		Item={
			#'partitionID': str(playerID) +"-"+ str(timestamp),
			'timestampCreated': int(time.time()),
			'playerID': playerID,
			'playerName': playerName,
			'game': {
				'appID': appID,
				'gameName': gameName
			},
			'timeStart': int(time.time()),
			'timeEnd': 0,
            'sessionStatus': "In Progress"
			})
	return response

def getSession(playerID, dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('GameSessions')
	r = table.query(KeyConditionExpression=Key('playerID').eq(playerID), FilterExpression=Key('timeEnd').eq(0))
	return r["Items"]
    
    
def closeSession(playerID, timestamp, dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb')
	
	table = dynamodb.Table('GameSessions')
	item = table.update_item(
		Key={
			'playerID': playerID,
			'timestampCreated': timestamp
		},
        ConditionExpression="sessionStatus = :sts",
		UpdateExpression="set timeEnd=:e, sessionStatus=:newsts",
		ExpressionAttributeValues={
            ':e': int(time.time()),
            ':sts': "In Progress",
            ':newsts': "Closed"
        },
	)

personaStates = {"0": "Offline", "1":"Online", "2":"Busy", "3":"Away", "4":"Snooze", "5":"Looking to trade", "6":"Looking to play"}

accessKey = get_steam_secret()


#Steam IDs to be looked up go here (must not be private)
steamids = "76561197960287930" #Gabe Newell's profile


# #Get player data
url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}".format(accessKey, steamids)

while(True):
    r = requests.get(url)

    results = r.json()["response"]["players"]
        
    timestamp = int(time.time())
    for player in results:
        name = player["personaname"]
        steamID = player["steamid"]
        state = personaStates[str(player["personastate"])]
        game = "Not in game"
        if "gameextrainfo" in player:
            appID = player["gameid"]
            game = player["gameextrainfo"]
            #check dynamo if there's an existing session
            sessions = getSession(player["steamid"])
            if len(sessions) == 0:
                createSession(steamID, name, appID, game)
        else:
            sessions = getSession(player["steamid"])
            if len(sessions) != 0:
                timestamp = sessions[0]["timestampCreated"]
                closeSession(steamID, timestamp)
    time.sleep(3)
