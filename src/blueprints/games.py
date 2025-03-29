from flask import Blueprint, jsonify, abort, request
from services import fetchAndSaveGames, getGames
import logging
import os

games_bp = Blueprint("games", __name__)

@games_bp.route("/saveTodays", methods=["POST"])
def saveGames():

    authKey = request.headers.get("Authorization", "").strip()

    if not authKey or authKey != os.environ.get("AUTH").strip():
        abort(401, description="Unauthorized access")

    logging.info("Passed the authorization")

    asd = fetchAndSaveGames()

    return jsonify({"SUcces: ": f"Matched: {asd[0]}, Upserted: {asd[1]}, Modified: {asd[2]}"})

@games_bp.route("/getTodays", methods=["GET"])
def fetchGames():

    found = getGames()

    logging.info("We found "+str(len(found))+" games")
    return jsonify({"res": found})