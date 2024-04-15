import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import sentimentAnalysis as snt
import json

# Main WIPs here:
# How do I show the reasoning?
# accuracy - how is this measurable?
# break code down more and comment - readability
apiUrl = "http://127.0.0.1:5000"
def prepDataframe(gameData, userLibrary = 0):
    data = {}
    for attK, attV in gameData['attributes'].items():
        data.update({attK: "|".join(attV)})
    
    if (userLibrary != 0):
        print("LOG --> REC ENGINE --> \tOPTIONAL: Processing user library...")
        for game in userLibrary:
            attributes = json.loads(requests.get(apiUrl + "/api/v1.0/games/" + game["_id"] +"/attributes").content.decode())
            attributes = attributes["attributes"].items()
            for attK, attV in attributes:
                if(data.get(attK) != None):
                    data.update({attK: data.get(attK) + "|" + "|".join(attV)})
                else:
                    data.update({attK: "|".join(attV)})

    # get games of genre of game
    genreResponse = requests.post(apiUrl + "/api/v1.0/games", data=json.dumps(data), headers={"content-type": "application/json"})

    # put that data into dataframe
    print("LOG --> REC ENGINE --> \tStage 1: Initialising dataframes...")
    data = pd.json_normalize(json.loads(genreResponse.content.decode()))
    data2 = pd.json_normalize(gameData)
    data = pd.concat([data2, data])
    data = data.reset_index()
    return data

def processAttributes(data):
    # Put all attributes into one column as string
    print("LOG --> REC ENGINE --> \tStage 2: Processing attributes...")
    attributeNames = [col for col in data if col.startswith('attributes')]
    for att in attributeNames:
        data[att] = data[att].apply(attToStr)
    data.insert(4,"newAttributes", None)
    data['newAttributes'] = data[[att for att in attributeNames]].agg(" ".join, axis=1)

    # Add attribute string to description string
    data['description'] = data['description'] + " " + data['newAttributes']
    return data

def clean_text(text):
    result = str(text).lower()
    return(result)

def attToStr(att):
    if(not isinstance(att, list)):
        result = ""
        return result
    att = [a.replace(" ", "") for a in att]
    result = " ".join(att)
    return result

def sentimentCalc(recs):
    topRated = ""
    prevScore = 0
    for r in recs:
        score = snt.getSentiment(r)
        if(score > prevScore):
            topRated = r
        prevScore = score
    if(topRated == ""):
        return recs[0]
    return topRated

def recommendGame(gameId, sentiment, library, userId = 0):
    gameData = json.loads(requests.get(apiUrl + "/api/v1.0/games/" + gameId + "/info").content.decode())
    print("LOG --> REC ENGINE --> \tInput game:", gameData['title'])

    if(library):
        library = requests.get(apiUrl + "/api/v1.0/users/" + userId + "/library")
        library = json.loads(library.content.decode())
        data = prepDataframe(gameData, library)
    else:
        data = prepDataframe(gameData)
    data = processAttributes(data)

    # Limit dataset to necessary columns
    data = data[['description','title','_id']]
    data = data.drop_duplicates(subset=['title'], keep="first")
    data = data.reset_index()
    data = data.drop('index',axis=1)

    # Clean description text
    print("LOG --> REC ENGINE --> \tStage 3: Processing description...")
    data['description'] = data['description'].apply(clean_text)

    # Find cosine similarity between games
    print("LOG --> REC ENGINE --> \tStage 4: Calculating similarity...")
    v = CountVectorizer(stop_words="english")
    vector = v.fit_transform(data['description'])
    similarities = cosine_similarity(vector)

    # Put similarity calcs into dataframe and use to find highest similarity of chosen game
    df2 = pd.DataFrame(similarities, columns=data['title'], index=data['title']).reset_index()
    recommendations = pd.DataFrame(df2.nlargest(4,gameData['title'])[['title',gameData['title']]])
    recommendations = recommendations[recommendations['title']!=gameData['title']]
    recList = list(recommendations['title'].to_dict().values())

    recTitle = sentimentCalc(recList) if sentiment else recList[0]
    recId = data[data['title']==recTitle]['_id'].values[0]
    similarity = recommendations[recommendations['title']==recTitle][gameData['title']].values[0]
    result = {"title":recTitle, "id":recId, "similarity":similarity}
    print(f"LOG --> REC ENGINE --> \tResulting game: {result['title']}")
    reasoning = compareInputAndResult(result, gameData)
    result.update({"reasoning":reasoning})
    result.pop("similarity")
    return result

def compareInputAndResult(result, inputData):
    resultInfo = json.loads(requests.get(apiUrl + f"/api/v1.0/games/{result['id']}/info").content.decode())
    resultAttributes = resultInfo['attributes']
    inputAttributes = inputData['attributes']
    matchingAttributes = []

    for attKres, attVres in resultAttributes.items():
        for attKin, attVin in inputAttributes.items():
            foundAttrs = [att for att in attVres if att in attVin]
            [matchingAttributes.append(item) for item in foundAttrs]

    descriptionSimilarityScore = result['similarity']
    if(descriptionSimilarityScore > 0.7):
        similarityLevel = "Very high"
    elif(descriptionSimilarityScore > 0.5):
        similarityLevel = "High"
    elif(descriptionSimilarityScore > 0.3):
        similarityLevel = "Medium"
    else:
        similarityLevel = "Low"

    resData = {
        "matchingAttributes": matchingAttributes,
        "similarityLevel": similarityLevel
    }
    return resData