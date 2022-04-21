import html5lib
import requests
import bs4
from bs4 import BeautifulSoup
import time
import json

#Taking a list of youtube video url sections ("/watch?v=dQw4w9WgXcQ"), return get URL, Title and tags and output them to a file.

def getVideoTags(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html5lib')
        tags = [meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"})]
        title = soup.find("meta", {"property": "og:title"}).get("content")
        return {"url": url, "title": title, "tags": tags}
    except:
        return None



urls = open('urls.txt', 'r').readlines()
videos = []

raw = open('data.txt', 'w')

start = 0
try:
    for urlIdx in range(start, len(urls)-1):
        url = "https://youtube.com" + urls[urlIdx]
        data = getVideoTags(url)
        print(str(urlIdx) + "/1388: " + data["title"])
        videos.append(data)
        raw.write(str(json.dumps(data))+"\n")
        time.sleep(0.1)
except (Exception, KeyboardInterrupt) as e:
    print("Last Parsed:" + urlIdx)

result = open('final.txt', 'w')
result.write(json.dumps(videos))
result.close()
