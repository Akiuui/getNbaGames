import os
from datetime import datetime
import schedule
from pymongo import MongoClient

from fetchers import fetchGames, fetchPlayersStats
from formatters import deletePropsFromStruct, drillForProp

from dotenv import load_dotenv
load_dotenv()

def Service():
    #We take todays date and format it to the needed format
    DTnow = datetime.now() 
    DTformatted = DTnow.strftime("%Y-%m-%d")

    #Fetches games based on the date
    res = fetchGames(DTformatted)

    if res is None:
        print("resJson is None")
        exit()

    #Formats all the data
    propsToDelete = [  
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

    games = []
    for item in res["response"]:
        formatted = deletePropsFromStruct(item, propsToDelete)
        formatted = drillForProp(formatted, "date", "start")
        games.append(formatted)

    # We connect and save the data to db
    try:
        client = MongoClient(os.environ.get("MONGO-URI"))
        db = client["NbaGames"]
        collection = db["NbaGames"]

        #Filtering duplicates
        filterGames = []
        for game in games:
            if not collection.find_one({"_id": game["id"]}):
                filterGames.append(game)

        for game in filterGames:
            game["_id"] = game["id"]
            game.pop("id", None)

        if filterGames:
            result = collection.insert_many(filterGames)
            if result.acknowledged:
                print(f"Inserted {len(result.inserted_ids)} new games, into MongoDB")
            else:
                print("Insertion failed!")
        else: 
            print("No new games to insert.!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

schedule.every().day.at("19:35").do(Service)

import time
while True:
    schedule.run_pending()  # Run the scheduled tasks
    time.sleep(1)  # Sleep for a second between checks