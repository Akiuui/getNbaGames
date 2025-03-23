import os
import logging
from pymongo import MongoClient
from flask import Flask, jsonify
from flask_cors import CORS

from fetchers import fetchGames
from formatters import formatGames
from utils import getTodaysDate

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

@app.route('/saveTodays', methods=['POST'])
def saveGames():

    todaysDate = getTodaysDate()
    logging.info(f"The day used for fetching data is {todaysDate}")

    logging.info("Trying to fetchGames")
    res = fetchGames(todaysDate)

    if res is None or res is []:
        logging.error("Response is empty")
        return jsonify({"error": "Response is empty"}), 404
        
    logging.info("Successfully fetched the games")
        
    # We connect and save the data to db
    try:
        logging.info("Trying to connect to Mongo")
        client = MongoClient(os.environ.get("MONGO-URI"), tls=True)
    except Exception as e:
        logging.info(f"There has been an exception! {e.args}")
        logging.info(f"The class! {e.__class__}")

    logging.info("Succesfully connected to mongoDb")
    db = client["NbaGames"]
    collection = db["NbaGames"]

    #Filtering duplicates
    logging.info("Trying to find a duplicate")
    filterGames = []
    found = 0
    games = res["response"]

    for game in games:
        if not collection.find_one({"_id": game["id"]}):
            filterGames.append(game)
        else:
            found+=1
            
    if found == 0:
        logging.info("Didnt find any duplicates")
    else:
        logging.info(f"Found: {found} duplicates")

    #Formats all the data
    games = formatGames(filterGames)

    if filterGames:
        logging.info("Trying to save my games")
        result = collection.insert_many(games)

        if result.acknowledged:
            logging.info("Successfuly saved!")
            return jsonify({"success": "Success"}), 200
            # return jsonify(games), 200
        else:
            logging.error("There has been an erorr with saving the results to mongoDb!")
            return jsonify({"error": "Failed!"})

    client.close()
    logging.info("There wasnt anything to save")
    return jsonify({"Success": "There wasnt anything to save"})

@app.route("/getTodays", methods=["GET"])
def getGames():

    todaysDate = getTodaysDate()
    logging.info(f"The day used for fetching data is {todaysDate}")

    try:
        logging.info("Trying to connect to Mongo")
        client = MongoClient(os.environ.get("MONGO-URI"), tls=True)
    except Exception as e:
        logging.info(f"There has been an exception! {e.args}")
        logging.info(f"The class! {e.__class__}")

    logging.info("Succesfully connected to mongoDb")
    db = client["NbaGames"]
    collection = db["NbaGames"]

    found = collection.find({"start": {"$regex": todaysDate}})
    found = list(found)

    if len(found) == 0:
        logging.info("No games found for this date")
        return jsonify({"Failed": "No games found for this date"}), 400
    
    client.close()
    logging.info("We found "+str(len(found))+" games")
    return jsonify({"res": found})


if __name__ == '__main__':
    from waitress import serve
    # app.run(debug=True)
    # port = int(os.environ.get("PORT", 8008))
    serve(app, host="0.0.0.0", port=8008)
