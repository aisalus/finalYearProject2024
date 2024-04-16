import requests as r
from pymongo import MongoClient

apiKey = "moby_gWTqhqU5J8btYyvyS3i8z6Xqu7z"
apiUrl = "https://api.mobygames.com/v1/games"
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.project
coll = db.games

offset = 0
for i in range(1):
    params = {"api_key": apiKey, "offset": offset}
    res = r.get(apiUrl, params=params)
    if res.status_code != 200:
        print(res.status_code)
        print(res.content)
        quit()
    for game in res.json()["games"]:
        coll.insert_one(game)
    offset = offset + 100
    print(i)

print(offset)