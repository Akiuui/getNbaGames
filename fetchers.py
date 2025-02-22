import requests
import os
import logging

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
        
    url = f"https://getnbateams.onrender.com/getIdByCode?teamCode={teamCode}"
    try:
        res = requests.get(url)
    except Exception as e:
        logging.error("Exception: While fetching a team id")
        
    return int(res.text)