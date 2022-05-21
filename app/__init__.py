from flask import Flask
from flask_cors import CORS
from app.configs import database, migrates, jwt
from os import getenv
from app import routes


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["JSON_SORT_KEYS"] = False

    CORS(app)
    database.init_app(app)
    migrates.init_app(app)
    jwt.init_app(app)
    routes.init_app(app)

    return app