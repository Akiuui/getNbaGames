from flask import jsonify
from datetime import datetime
from pymongo import MongoClient, UpdateOne
from fetchers import fetchGames
from formatters import formatGames
import os
import logging

def getTodaysDate():
    DTnow = datetime.now() 
    DTformatted = DTnow.strftime("%Y-%m-%d")
    return DTformatted

def ConnectToMongo():
    try:
        client = MongoClient(os.environ.get("MONGO-KEY"), tls=True)
    except Exception as e:
        logging.info(f"There has been an exception! {e.args}")
        return jsonify({"error": "Could not connect to MongoDB"}), 500

    return client

def getGames():

    todaysDate = getTodaysDate()
    logging.info(f"The day used for fetching data is {todaysDate}")

    client = ConnectToMongo()
    logging.info("Succesfully connected to mongoDb")

    db = client["NbaGames"]
    collection = db["NbaGames"]

    found = collection.find({"dateStart": todaysDate})
    found = list(found)

    if len(found) == 0:
        logging.info("No games found for this date")
        return jsonify({"Failed": "No games found for this date"}), 400
    
    return found 

def fetchAndSaveGames():
    
    todaysDate = getTodaysDate()
    logging.info(f"The day used for fetching data is {todaysDate}")

    logging.info("Trying to fetchGames")
    res = fetchGames(todaysDate)
    games = res["response"]

    if res is None or res is []:
        logging.error("Response is empty")
        return jsonify({"error": "Response is empty"}), 404
        
    logging.info("Successfully fetched the games")
        
    # We connect and save the data to db
    client = ConnectToMongo()

    logging.info("Succesfully connected to mongoDb")
    db = client["NbaGames"]
    collection = db["NbaGames"]

    #Formats all the data
    games = formatGames(games)

    logging.info("Trying to save my games")

    operations = [
        UpdateOne({"_id": game["_id"]}, {"$set": game}, upsert=True) for game in games
    ]

    # Perform bulk update (insert new, overwrite existing)
    if operations:
        result = collection.bulk_write(operations)
        logging.info(f"Matched: {result.matched_count}, Upserted: {result.upserted_count}, Modified: {result.modified_count}")

    return [result.matched_count, result.upserted_count, result.modified_count]