import json

#Take outputs from two executions of import.py and print out any tag that is different.

in1 = open('datanew.txt', 'r')
lines1 = [json.loads(line) for line in in1.readlines()]
in2 = open('dataold.txt', 'r')
lines2 = [json.loads(line) for line in in2.readlines()]

for i in lines1:
    for j in lines2:
        if i["url"] == j["url"]:
            if len(i["tags"]) != len(j["tags"]):
                print(i["title"])
            break
