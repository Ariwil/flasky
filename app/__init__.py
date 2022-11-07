from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy() #in global scope so we can import it to other places
migrate = Migrate() #migrate is ways we take ourselves from an empty DB to something that has the schema I want, to something that has the tables and relationships I want
load_dotenv() #finds .env file nearby and takes those key-value pairs we have in them and make them available as environment variables

def create_app(testing=None): #add the parameter to be able to change whether we're in testing mode or not 
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    #setting some config things in our app
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #dont need to remember why we dont want this but we just want our sqla operate in a dif way without this piece
    if testing is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI") #dictionary that has dif environments
        # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/bikes_development"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    from app.models.bike import Bike #importing the Bike class/model from app.models.bike #needs to come before the next two lines #later on Jerica said not sure why we added this line

    db.init_app(app) #where we connect our DB to our application. init_app is the connector
    migrate.init_app(app, db) #tool to set up our DB

    from .routes.bike import bike_bp
    app.register_blueprint(bike_bp)
    from .routes.cyclist import cyclist_bp
    app.register_blueprint(cyclist_bp)

    return app