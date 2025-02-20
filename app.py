import os
from datetime import datetime
from pymongo import MongoClient
from flask import Flask, jsonify

from fetchers import fetchGames, fetchPlayersStats
from formatters import deletePropsFromStruct, drillForProp

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def service():
    #We take todays date and format it to the needed format
    DTnow = datetime.now() 
    DTformatted = DTnow.strftime("%Y-%m-%d")
    # DTformatted = "2025-02-20"
    #Fetches games based on the date
    res = fetchGames(DTformatted)

    if res is None:
        return jsonify({"error": "Response is None"}), 404

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
                return jsonify({"success": "Success"}), 200
            else:
                return jsonify({"error": "Failed!"})

        else: 
            return jsonify({"success": "No new games"})

    except Exception as e:
        return jsonify({"error": f"Error: {e}"})
    finally:
        client.close()



if __name__ == '__main__':
    from waitress import serve
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 8008))
    serve(app, host="0.0.0.0", port=port)
