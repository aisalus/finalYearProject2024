import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import databaseOps as db
import sentimentAnalysis as snt
import json

# Main WIPs here:
# slow
# How do I show the reasoning?
# Output format - this will make more sense when building front end - id needed?
# Search tool - Game id lookup thingy - frontend? keep this id based? API endpoint?
# accuracy - how is this measurable?
# search endpoint - punctuation problems

def prepDataframe(game):
    genreStr = "-".join(game['attributes']['Basic Genres']).replace("/", "-")

    # get games of genre of game
    genreResponse = json.loads(db.games_by_genre(genreStr))

    # put that data into dataframe
    print("Stage 1: Initialising dataframes...")
    data = pd.json_normalize(genreResponse)
    data2 = pd.json_normalize(game)
    data = pd.concat([data2, data])
    data = data.reset_index()
    return data

def processAttributes(data):
    # Put all attributes into one column as string
    print("Stage 2: Processing attributes...")
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

def recommendGame(gameId):
    gameData = json.loads(db.get_game_by_id(gameId))
    print("Input game:", gameData['title'])

    data = prepDataframe(gameData)
    data = processAttributes(data)

    # Limit dataset to necessary columns
    data = data[['description','title','_id']]
    data = data.drop_duplicates(subset=['title'], keep="first")
    data = data.reset_index()
    data = data.drop('index',axis=1)

    # Clean description text
    print("Stage 3: Processing description...")
    data['description'] = data['description'].apply(clean_text)

    # Find cosine similarity between games
    print("Stage 4: Calculating similarity...")
    v = CountVectorizer(stop_words="english")
    vector = v.fit_transform(data['description'])
    similarities = cosine_similarity(vector)

    # Put similarity calcs into dataframe and use to find highest similarity of chosen game
    df2 = pd.DataFrame(similarities, columns=data['title'], index=data['title']).reset_index()
    recommendations = pd.DataFrame(df2.nlargest(4,gameData['title'])['title'])
    recommendations = recommendations[recommendations['title']!=gameData['title']]
    recommendations = list(recommendations['title'].to_dict().values())

    recTitle = sentimentCalc(recommendations)
    recId = data[data['title']==recTitle]['_id'].values[0]
    result = {"title":recTitle, "id":recId}
    return result

# print(recommendGame("6602db59301d967bf44b6f06"))