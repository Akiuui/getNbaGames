from flask import Flask
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)
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

DTnow = datetime.now()
DTformatted = DTnow.strftime("%Y-%m-%d")
fetchGames(DTformatted)

# @app.route('/')
# def home():
#     return "Hello, Flask!"

# if __name__ == '__main__':
#     app.run(debug=True)