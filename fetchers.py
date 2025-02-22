import requests
import os

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
    
def fetchTeamId(teamCode):
    url = f"moj teams api"

    res = requests.get(url)
    print(res)

    # FROM RES GET ID AND RETURN IT