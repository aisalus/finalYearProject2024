from flask import Flask, make_response, jsonify, request
import requests, json
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId
import datetime, time
import recommendationEngine as eng

# Endpoints go here

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017")
db = client.project
coll = db.games
userColl = db.users
suggestionColl = db.suggestions

# --- Get all games/query games --- #
@app.route("/api/v1.0/games", methods=["GET"])
def show_all_games():
    value = ""
    page_num, page_size = 1, 10

    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))

    page_start = (page_size * (page_num - 1))
    data_to_return = []

    for game in coll.find().sort("num_votes", -1 ) \
        .skip(page_start).limit(page_size):
        game['_id'] = str(game['_id'])
        data_to_return.append(game)

    return make_response( jsonify(data_to_return), 200 )

# --- Search game by title --- #
@app.route("/api/v1.0/games/search/<string:title>", methods=["GET"])
def search_game_by_title(title):
    returnData = []
    query = {'title':{'$regex':'.*'+title+'.*', '$options' :'i'}}
    games = coll.find(query, {"title": 1}).sort('num_votes', -1).limit(10)
    count = coll.count_documents(query)

    if count > 0:
        for game in games:
            game['_id'] = str(game['_id'])
            returnData.append(game)
        return make_response( jsonify(returnData), 200 )
    else:
        return make_response( jsonify( { "error" : "No games found" } ), 404 )

# --- Get a sample of games using context --- #
@app.route("/api/v1.0/games", methods=["POST"])
def games_by_attribute():
    data_to_return = []
    data = json.loads(request.data.decode())
    terms = []

    for itemK, itemV in data.items():
        terms.append({"attributes."+ itemK : {'$regex':'.*'+itemV+'.*', '$options' :'i'}})
    # Query to match where 'Basic Genres' contains any of the provided genres
    query = {"$or" : terms}

    # Aggregation pipeline to match the query and get a random sample for processing
    pipeline = [{"$match":query},{"$sample": {"size": 500}}]

    games = coll.aggregate(pipeline)
    for game in games:
        game['_id'] = str(game['_id'])
        data_to_return.append(game)
    return make_response(data_to_return)

# --- Get game by id --- #
@app.route("/api/v1.0/games/<string:id>/info", methods=["GET"])
def get_game_by_id(id):
    game = coll.find_one({'_id':ObjectId(id)})
    if game is not None:
        game['_id'] = str(game['_id'])
        return make_response(jsonify(game), 200)
    else:
        return make_response(jsonify({"error" : "Invalid game ID" }), 404)

# --- Get attributes of game --- #
@app.route("/api/v1.0/games/<string:id>/attributes", methods=["GET"])
def get_game_attributes(id):
    game = coll.find_one({'_id':ObjectId(id)})
    if game is not None:
        game['_id'] = str(game['_id'])
        returnData = {"id":game['_id'], "attributes":game['attributes']}
        return make_response(jsonify(returnData), 200)
    else:
        return make_response(jsonify({"error" : "Invalid game ID" }), 404)

# --- Get platforms of game --- #
@app.route("/api/v1.0/games/<string:id>/platforms", methods=["GET"])
def get_game_platforms(id):
    game = coll.find_one({'_id':ObjectId(id)})
    if game is not None:
        game['_id'] = str(game['_id'])
        returnData = {"id":game['_id'], "title":game['title'], "platforms":game['platforms']}
        return make_response(jsonify(returnData), 200)
    else:
        return make_response(jsonify({"error" : "Invalid game ID" }), 404)

# --- Get recommendations from id --- #
@app.route("/api/v1.0/games/rec/<string:id>", methods=["GET"])
def get_recommendations(id):
    sentiment = request.args.get('useSentiment') == "true"
    library = request.args.get('useLibrary') == "true"
    if (request.args.get('userId')):
        return make_response( jsonify(eng.recommendMain(id, sentiment, library, request.args.get('userId'))), 200 )
    return make_response( jsonify(eng.recommendMain(id, sentiment, library)), 200 )

# --- Add user info --- #
@app.route("/api/v1.0/users", methods=["PUT"])
def addUserId():
    req = json.loads(request.data.decode())
    user = userColl.find_one({'_id': req["user_id"]})
    if user is not None:
        return make_response( jsonify( {"message":"user exists"}), 200 )
    newUser = {
        "_id": req["user_id"],
        "history": [],
        "library": [],
        "blocklist": [],
        "name": req["name"]
    }
    userColl.insert_one(newUser)
    return make_response( jsonify({"message":"success"}), 200 )

# --- Get user history --- #
@app.route("/api/v1.0/users/<string:id>/history", methods=["GET"])
def getUserHistory(id):
    user = userColl.find_one({'_id':id})
    if user is not None:
        targetData = user['history']
        for item in targetData:
            item['_id'] = str(item['_id'])
        return make_response( jsonify( targetData ), 200 )
    else:
        return make_response( jsonify( { "error" : "Invalid user ID" } ), 404 )

# --- Add to/set user history --- #
@app.route("/api/v1.0/users/<string:id>/history", methods=["PUT"])
def setUserHistory(id):
    req = json.loads(request.data.decode())
    item = coll.find_one({'_id':ObjectId(req['id'])})
    if(item is None):
        return make_response( jsonify( { "error" : "Invalid Game ID" } ), 404 )
    newEntry = {
        "_id": item['_id'],
        "moby_url": item['moby_url'],
        "title": item['title'],
        "reasoning": req['reasoning'],
        "timestamp": datetime.datetime.now()
    }
    userColl.update_one( { "_id" : id }, \
        { "$push": { "history" : newEntry } } )
    return make_response( jsonify( {"message":"success"}), 200 )

# --- Get user library --- #
@app.route("/api/v1.0/users/<string:id>/library", methods=["GET"])
def getUserLibrary(id):
    user = userColl.find_one({'_id':id})
    if user is not None:
        targetData = user['library']
        for item in targetData:
            item['_id'] = str(item['_id'])
        return make_response( jsonify( targetData ), 200 )
    else:
        return make_response( jsonify( { "error" : "Invalid user ID" } ), 404 )

# --- Add to/set user library --- #
@app.route("/api/v1.0/users/<string:id>/library", methods=["PUT"])
def setUserLibrary(id):
    req = json.loads(request.data.decode())
    item= coll.find_one({'_id':ObjectId(req['gameId'])})
    newEntry = {
        "_id": item['_id'],
        "moby_url": item['moby_url'],
        "title": item['title'],
        "timestamp": datetime.datetime.now()
    }
    userColl.update_one( { "_id" : id }, \
        { "$push": { "library" : newEntry } } )
    return make_response( jsonify( {"message":"success"}), 200 )

# --- Delete one from user library --- #
@app.route("/api/v1.0/users/<string:id>/library/delete/<string:lid>", methods=["DELETE"])
def deleteOneInLibrary(id, lid):
    libraryItem = userColl.find({"_id" :  id, 'library._id' : ObjectId(lid)})
    if libraryItem is not None:
        print(userColl.update_one( \
        { "_id" :  id }, \
        { "$pull" : {"library" : {"_id" : ObjectId(lid)}}} ))
        return make_response( jsonify( { "message" : "success" } ), 204 )
    else:
        return make_response( jsonify( { "error" : "Invalid user ID" } ), 404 )

# --- Clear history --- #
@app.route("/api/v1.0/users/<string:id>/history/clear", methods=["DELETE"])
def clearUserHistory(id):
    userColl.update_one( { "_id" : id }, \
        { "$set": { "history" : [] } } )
    return make_response( jsonify( {"message":"success"}), 204 )

# --- Clear library --- #
@app.route("/api/v1.0/users/<string:id>/library/clear", methods=["DELETE"])
def clearUserLibrary(id):
    userColl.update_one( { "_id" : id }, \
        { "$set": { "library" : [] } } )
    return make_response( jsonify( {"message":"success"}), 204 )

# --- Get auth0 token --- #
def getUserToken():
    headers = { 'content-type': "application/json" }
    data = "{\"client_id\":\"4Ngnua8oTEmtfB6A2JspHn1dX3lIlLQ6\",\"client_secret\":\"3Gx8gOfI8F2XqXOPBm6ti9ojFYXcON727ukvYZA2-QH4D4q-qKF2HGjMPcKk6j2P\",\"audience\":\"https://dev-x4savaa1u24lh134.us.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"
    token = requests.post("https://dev-x4savaa1u24lh134.us.auth0.com/oauth/token", data, headers=headers)
    return json.loads(token.content.decode())["access_token"]

# --- Delete user --- #
@app.route("/api/v1.0/users/<string:id>/deactivate", methods=["DELETE"])
def deactivateUser(id):
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxMdkN2RVlGTVM1N29XVXR1YkE3dyJ9.eyJpc3MiOiJodHRwczovL2Rldi14NHNhdmFhMXUyNGxoMTM0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiI0TmdudWE4b1RFbXRmQjZBMkpzcEhuMWRYM2xJbExRNkBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYteDRzYXZhYTF1MjRsaDEzNC51cy5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTcxMzAyMTM4MSwiZXhwIjoxNzEzMTA3NzgxLCJzY29wZSI6ImRlbGV0ZTp1c2VycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IjROZ251YThvVEVtdGZCNkEySnNwSG4xZFgzbElsTFE2In0.dTxNhcKezW9F3CSip1a4-B8zasL-loE2zfI9eyvnlBbu2kKhNABhU6DpY12yfCgV-Q7AV4bzsRFDt4N8xfJPHSVOb-snguP-rmyK79apF-M88Te6vlZlhCJAiq1fv41RkWjY-6fCVHKfrZqonBH6oy0BGCfjGXcFsxGzWHtg3SYBlbEwqMfBKTpTnbx1KB5b5XhFRbVxyzWdGjB5ASnJTijvu5Uc5Bb01aX-46DBQmPgX5lwYV-NdT7Fa0qk87F8DE1cHcAYDu0Kw_UDN8nAkWO81AROLtYvhaQc7eeuLk_QWHO3sUF5Uls1dnc7vhzJGSuRKrbpWWGTZw33yLeS2g"
    headers = {'authorization': "Bearer " + token}
    res = requests.delete("https://dev-x4savaa1u24lh134.us.auth0.com/api/v2/users/"+id, headers=headers)
    userColl.delete_one({"_id" : id.split("|")[1]})
    return make_response( jsonify( res.text ), 204 )

# --- Add to suggestions --- #
@app.route("/api/v1.0/suggestions", methods=["PUT"])
def addSuggestion():
    req = json.loads(request.data.decode())
    suggestion = {
        "_id": ObjectId(),
        "text": str(req['suggestionMessage']),
        "timestamp": datetime.datetime.now()
    }
    suggestionColl.insert_one(suggestion)
    return make_response( jsonify({"message":"success"}), 200 )

if(__name__ == "__main__"):
    app.run(debug="true")