from bs4 import BeautifulSoup
import requests
from transformers import pipeline
from thefuzz import fuzz

# set headers for web scraper
headers = {
        'accept':'application/json, text/plain, */*',
        'origin':'https://opencritic.com',
        'referer':'https://opencritic.com/',
        'user-agent':'Chrome/109.0.0.0'
        }

# Get review page and parse with beautifulsoup
def getPage(gameid, game, headers):
    url = f"https://opencritic.com/game/{gameid}/{game}/reviews"
    try:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        return soup
    except Exception as e:
        print(f"LOG --> SENTIMENT --> \tError opening page {e}")

# Get game id from opencritic
def getGameId(game, headers):
    searchUrl = f'https://api.opencritic.com/api/meta/search?criteria={game}'
    results = requests.get(searchUrl,headers=headers)
    resultsJson = results.json()
    found_id = -1

    # find game in results - title not always exact between datasets so fuzz ratio is used for similarity ratio
    for r in resultsJson:
        ratio = fuzz.ratio(game.lower(), r['name'].lower())
        if game.lower() in r['name'].lower():
            print(f'LOG --> SENTIMENT --> \t{r["name"]} found!')
            found_id = r['id']
            return found_id
        elif ratio > 80:
            print(f'LOG --> SENTIMENT --> \t{game} not found exactly, getting review for closest result: {r["name"]}')
            found_id = r["id"]
            return found_id
    return found_id

# Get all reviews on review page
def getReviews(game):
    id = getGameId(game, headers=headers)
    if(id == -1):
        print("LOG --> SENTIMENT --> \tNo game found")
        return -1
    page = getPage(id, game, headers)
    reviews = page.find_all("app-review-row")
    result = []
    for r in reviews:
        if(r.find("p")):
            result.append(r.find("p").text)
    
    return result

# Get overall average sentiment for a game's reviews
def averageSentiment(values):
    score = 0
    for v in values:
        if(v['label'] == "POSITIVE"):
            score += v['score']
        if(v['label'] == "NEGATIVE"):
            score -= v['score']
    if(len(values) != 0):
        score = score / len(values)
    return score

# Calculate sentiment of all of a game's reviews
def getSentiment(game):
    reviews = getReviews(game)
    if(reviews == -1):
        return -1
    pipe = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    values = pipe(reviews)
    return averageSentiment(values)
