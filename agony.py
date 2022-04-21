import requests
import json

#Script for Guild Wars 2 to calculate profitability between crafting 2^n Agony Infusions and merging them vs buying intermediate steps

THERMO_COST = 150
BUY = 86
SELL = 91


payload = {"query":{"craftable":{"$eq":True},"name":{"$like":"%AGONY infusion%"},"rarity":{"$eq":6}},"sort":{"craftProfit.sellProfit":-1},"skip":0,"limit":24}
headers = {'content-type': 'application/json'}
url = 'https://api.gw2efficiency.com/items/query'
#url = "https://httpbin.org/post"
r = requests.post(url, headers=headers, data=json.dumps(payload))

output = r.json()

results = output["results"]
results.sort(key=lambda x: x["id"])
results = results[0:16]



parsed = [{"id": i["id"], "name": i["name"], "buy": i["buy"]["price"], "sell": i["sell"]["price"]} for i in results]
parsed.insert(0, {"id": 0, "name": "+1 Agony Infusion", "buy": BUY, "sell": SELL})

output = {}
for idxS, source in enumerate(parsed):
    out = {}
    agonyIdxS = idxS + 1
    #print("Starting +{0} simulation".format(agonyIdxS))
    for idxT, target in enumerate(parsed[idxS+1::]):
        agonyIdxT = idxS + idxT + 2
        #print("Running for +{0}".format(agonyIdxT))
        thermoNeeded = ((2**(agonyIdxT-agonyIdxS)) - 1)
        thermoCost = thermoNeeded * THERMO_COST

        agonyNeeded = (2**(agonyIdxT-agonyIdxS))
        agonyCost = agonyNeeded * source["buy"]

        totalCost = agonyCost + thermoCost
        profit = (target["sell"] * 0.85 - totalCost)
        out[agonyIdxT] = profit
    output[agonyIdxS] = out

outFile = open("out.csv", "w")
outFile.write("source," + "".join("+{0},".format(i) for i in range(1, 18)) + "\n")


for k, v in output.items():
    outFile.write(str(k) + ",")
    for i in range(1,18):
        if i > k:
            outFile.write(str(output[k][i]) + ",")
        else:
            outFile.write(",")
    outFile.write("\n")
