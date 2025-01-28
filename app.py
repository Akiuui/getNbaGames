import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def fetchGames(date):
    url = f"https://v2.nba.api-sports.io/games?date={date}"
    headers = {
        'x-rapidapi-host': "v2.nba.api-sports.io",
        'x-rapidapi-key': os.environ.get("API-KEY")
    }
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        return res.json()
    else:
        return None

def fetchPlayersStats():
    return None

def formatGameData(data):
    delete = [  
                "league",
                "season",
                "stage",
                "status",
                "periods",
                "arena",
                "officials",
                "timesTied",
                "leadChanges",
                "nugget"
            ]

    for item in delete:
        if item in data:
            del data[item]

    return data

#START

DTnow = datetime.now()
DTformatted = DTnow.strftime("%Y-%m-%d")

resJson = fetchGames(DTformatted) #We get json

if resJson is None:
    print("resJson is None")
    exit()

games = []
for item in resJson["response"]:
     games.append(formatGameData(item))

for i in games:
    print(i)
