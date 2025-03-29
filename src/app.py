import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from blueprints.games import games_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

app.register_blueprint(games_bp)
    
if __name__ == '__main__':
    from waitress import serve
    # app.run(debug=True)
    # port = int(os.environ.get("PORT", 8008))
    serve(app, host="0.0.0.0", port=8008)
