from app import db

class Bike(db.Model): #All stuff from SQLA is bc we inherit from the Model
    #db.Model means we don't need to put stuff inside a dunder init
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #id INT GENERATE ALWAYS... #Column turns info into column in DB
    name = db.Column(db.String) #
    price = db.Column(db.Integer) 
    size = db.Column(db.Integer)
    type = db.Column(db.String)
