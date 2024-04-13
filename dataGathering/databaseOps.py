from pymongo import MongoClient
from bson import ObjectId
import json

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.project
coll = db.games

# --- Get a sample of games of genre --- #
def games_by_genre(genres):
    data_to_return = []

    # Separate individual genre names with the 'or' operator
    genres = genres.replace("-", "|")

    # Query to match where 'Basic Genres' contains any of the provided genres
    query = {"attributes.Basic Genres" : {'$regex':'.*'+genres+'.*', '$options' :'i'}}

    # Aggregation pipeline to match the query and get a random sample for processing
    pipeline = [{"$match":query},{"$sample": {"size": 1000}}]
    games = coll.aggregate(pipeline)

    for game in games:
        game['_id'] = str(game['_id'])
        data_to_return.append(game)
    return json.dumps(data_to_return)

# --- Get game by id --- #
def get_game_by_id(id):
    game = coll.find_one({'_id':ObjectId(id)})
    if game is not None:
        game['_id'] = str(game['_id'])
        return json.dumps(game)
    else:
        return json.dumps({ "error" : "Invalid game ID" })

# --- Get attributes of game --- #
def get_game_attributes(id):
    game = coll.find_one({'_id':ObjectId(id)})
    if game is not None:
        game['_id'] = str(game['_id'])
        returnData = {"id":game['_id'], "attributes":game['attributes']}
        return json.dumps(returnData)
    else:
        return json.dumps({ "error" : "Invalid game ID" })

# --- Get platforms of game --- #
def get_game_platforms(id):
    game = coll.find_one({'_id':ObjectId(id)})
    if game is not None:
        game['_id'] = str(game['_id'])
        returnData = {"id":game['_id'], "title":game['title'], "platforms":game['platforms']}
        return json.dumps(returnData)
    else:
        return json.dumps({"error" : "Invalid game ID" })