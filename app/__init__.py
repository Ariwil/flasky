from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy() #in global scope so we can import it to other places
migrate = Migrate() #migrate is ways we take ourselves from an empty DB to something that has the schema I want, to something that has the tables and relationships I want


def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    #setting some config things in our app
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #dont need to remember why we dont want this but we just want our sqla operate in a dif way without this piece
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/bikes_development" #

    from app.models.bike import Bike #importing the Bike class/model from app.models.bike #needs to come before the next two lines

    db.init_app(app) #where we connect our DB to our application. init_app is the connector
    migrate.init_app(app, db) #tool to set up our DB

    from .routes.bike import bike_bp
    app.register_blueprint(bike_bp)

    return app