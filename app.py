from flask import Flask
from flask import jsonify
from flask_restful import Api
from flask_bcrypt import Bcrypt


from resources.recommendations import RecommendationAPI

import os


app = Flask(__name__, instance_relative_config=True)

# Loads configuration from config.py
app.config.from_object('config')


api = Api(app)
Bcrypt(app)

api.add_resource(RecommendationAPI, '/recommendations')


@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World from Food Buy API"})

if __name__ == "__main__":
    app.run(debug=True, port=3000)