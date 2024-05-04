from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests as r
import re
from thefuzz import fuzz

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.project
coll = db.games

token = r.post("https://id.twitch.tv/oauth2/token?client_id=gijlxy2a6uo0yo06wyx0hu9gdlqpi8&client_secret=ob5gdpnhduel6istj9rfs8ul51gq3z&grant_type=client_credentials")
auth = token.json()['access_token']
def cleanDescriptions():
    cursor = coll.find()
    index = 0
    count = coll.count_documents({})
    while index != count:
        doc = cursor[index]
        print('updating doc', index)
        cleantext = BeautifulSoup(doc["description"], "lxml").text
        coll.update_one({"_id": doc["_id"]},{"$set": {"description": cleantext}})
        index += 1

def fixGenreNames():
    cursor = coll.find()
    index = 0
    count = coll.count_documents({})
    
    while index != count:
        doc = cursor[index]
        print('updating doc', index)
        newAttributes = {}
        try:
            for att in doc['attributes']:
                if(att['genre_category'] in  newAttributes.keys()):
                    print("Adding to", att['genre_category'], "... ")
                    newAttributes[att['genre_category']].append(att['genre_name'])
                else:
                    newAttributes.update({att['genre_category']: [att['genre_name']]})
            coll.update_one({"_id": doc["_id"]},{"$set": {"attributes": newAttributes}})
        except Exception as e:
            print("Exception:", e)
        finally:
            index += 1

def fillEmptyDescriptions():
    cursor = coll.find({"description": ""})
    notFound = 0
    processed = 0
    for doc in cursor:
        try:
            newDesc = queryIGDB(doc['title'])
            if(newDesc == -1):
                notFound += 1
            else:
                print('updating doc', doc['title'])
                coll.update_one({"_id": doc["_id"]},{"$set": {"description": newDesc}})
        except Exception as e:
            print("Exception:", e)
            notFound += 1
        finally:
            processed += 1
            print("Processed:", processed)     
    print("Not found:", notFound)

def queryIGDB(title):
    title = title.replace("é", "e")
    title = re.sub('[^A-Za-z0-9 ]+', ' ', title)
    res = r.post("https://api.igdb.com/v4/games", **{"headers": {"Client-ID": "gijlxy2a6uo0yo06wyx0hu9gdlqpi8", "charset": "utf-8", "Authorization": "Bearer " + auth}, "data":"search \""+ title +"\"; fields summary, name;"})
    resultingGames = res.json()
    for game in resultingGames:
        if('name' in game.keys() and 'summary' in game.keys()):
            ratio = fuzz.ratio(game['name'].lower(), title.lower())
            if(ratio >= 70):
                return game['summary']
    return -1

fillEmptyDescriptions()