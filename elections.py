import requests
import time

#Script made for the 2021 PT Presidential elections. Outputs...... something, probably.

root = "LOCAL-500000"

BASE_TERRITORY_URL = "https://www.presidenciais2021.mai.gov.pt/frontend/data/TerritoryChildren?territoryKey={0}"
BASE_RESULTS_URL = "https://www.presidenciais2021.mai.gov.pt/frontend/data/TerritoryResults?electionId=PR&territoryKey={0}"

baseTerritories = requests.get(BASE_TERRITORY_URL.format(root)).json()

out = open('out.txt', 'w')

#CSV HEADERS
#Distrito
#CodDistrito
#Concelho
#CodConcelho
#Freguesia
#CodFreguesia
#Nulo
#NuloPercent
#Branco
#BrancoPercent
#MaxVoters
#Voters
#VotersPercent
#MRSVotes
#MRSPercent
#AGVotes
#AGPercent
#AVVotes
#AVPercent
#MMVotes
#MMPercent
#JFVotes
#JFPercent
#TMVotes
#TMPercent
#VSVotes
#VSPercent
out.write('Distrito;CodDistrito;Concelho;CodConcelho;Freguesia;CodFreguesia;Nulo;NuloPercent;Branco;BrancoPercent;MaxVoters;Voters;VotersPercent;MRSVotes;MRSPercent;AGVotes;AGPercent;AVVotes;AVPercent;MMVotes;MMPercent;JFVotes;JFPercent;TMVotes;TMPercent;VSVotes;VSPercent;\n')

for dist in baseTerritories:
    distTerritories = requests.get(BASE_TERRITORY_URL.format(dist['territoryKey'])).json()
    for conc in distTerritories:
        concTerritories = requests.get(BASE_TERRITORY_URL.format(conc['territoryKey'])).json()
        time.sleep(0.1)
        for freg in concTerritories:
            results = requests.get(BASE_RESULTS_URL.format(freg['territoryKey'])).json()['currentResults']

            party = {}
            for cdt in results['resultsParty']:
                party[cdt['acronym']] = {'votes': cdt['votes'], 'percentage': cdt['validVotesPercentage']}

            l = [
                    dist['name'], 
                    dist['territoryKey'], 
                    conc['name'],
                    conc['territoryKey'],
                    freg['name'], 
                    freg['territoryKey'], 
                    results['nullVotes'], 
                    results['nullVotesPercentage'], 
                    results['blankVotes'], 
                    results['blankVotesPercentage'], 
                    results['subscribedVoters'], 
                    results['numberVoters'], 
                    results['percentageVoters'],
                    party['Marcelo Rebelo de Sousa']['votes'],
                    party['Marcelo Rebelo de Sousa']['percentage'],
                    party['Ana Gomes']['votes'],
                    party['Ana Gomes']['percentage'],
                    party['André Ventura']['votes'],
                    party['André Ventura']['percentage'],
                    party['Marisa Matias']['votes'],
                    party['Marisa Matias']['percentage'],
                    party['João Ferreira']['votes'],
                    party['João Ferreira']['percentage'],
                    party['Tiago Mayan Gonçalves']['votes'],
                    party['Tiago Mayan Gonçalves']['percentage'],
                    party['Vitorino Silva']['votes'],
                    party['Vitorino Silva']['percentage']
                    ]
            l = list(map(lambda x: str(x), l))
            out.write(';'.join(l) + '\n')
            #print('{0}[{1}] -> {2}[{3}] -> {4}[{5}]'.format(dist['name'], dist['territoryKey'], conc['name'], conc['territoryKey'], freg['name'], freg['territoryKey']))
        print(conc['name'] + " completed.")
    print('DISTRITO: ' + dist['name'] + " completed")
