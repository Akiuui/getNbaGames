from flask import Blueprint, jsonify, abort, request
from services import fetchAndSaveGames, getGames
import logging
import os

games_bp = Blueprint("games", __name__)

@games_bp.route("/saveTodays", methods=["GET"])
def saveGames():

    logging.info(f"All headers: {dict(request.environ)}")
    if request.headers.get("Auth"):
        authKey = request.headers.get("Auth")
    else:
        authKey = request.environ.get("Auth")

    # logging.info(f"Header kljuc: {authKey}")
    # logging.info(f"Sifra: {os.environ.get('AUTH')}")
    if not authKey or authKey != os.environ.get("AUTH").strip():
        abort(401, description="Unauthorized access: AUTH header is empty")

    logging.info("Passed the authorization")

    asd = fetchAndSaveGames()

    return jsonify({"SUcces: ": f"Matched: {asd[0]}, Upserted: {asd[1]}, Modified: {asd[2]}"})

@games_bp.route("/getTodays", methods=["GET"])
def fetchGames():

    found = getGames()

    logging.info("We found "+str(len(found))+" games")
    return jsonify({"res": found})