import os
from datetime import datetime
from pymongo import MongoClient
from flask import Flask, jsonify

from fetchers import fetchGames, fetchPlayersStats
from formatters import deletePropsFromStruct, drillForProp

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

@app.route('/')
def service():
    #We take todays date and format it to the needed format
    DTnow = datetime.now() 
    DTformatted = DTnow.strftime("%Y-%m-%d")

    #Fetches games based on the date
    res = fetchGames(DTformatted)

    if res is None:
        return jsonify({"error": "Response is None"}), 404
        # print("resJson is None")
        # exit()

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
                return jsonify({"success": f"Inserted {len(result.inserted_ids)} new games, into MongoDB"}), 200
                # print(f"Inserted {len(result.inserted_ids)} new games, into MongoDB")
            else:
                return jsonify({"error": "Insertion failed!"})
        else: 
            return jsonify({"success": "No new games to insert"})
            # print("No new games to insert.!")
    except Exception as e:
        return jsonify({"error": f"Error: {e}"})
        # print(f"Error: {e}")
    finally:
        client.close()



if __name__ == '__main__':
    from waitress import serve

    port = int(os.environ.get("PORT", 8008))
    serve(app, port=port)
    # app.run(debug=True)