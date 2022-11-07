from app import db
#only need to update migrations if you change the entities of the table (not for adding something like the to_dict fxn)
class Bike(db.Model): #All stuff from SQLA is bc we inherit from the Model
    #db.Model means we don't need to put stuff inside a dunder init
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #id INT GENERATE ALWAYS... #Column turns info into column in DB
    name = db.Column(db.String) #
    price = db.Column(db.Integer) 
    size = db.Column(db.Integer)
    type = db.Column(db.String)
    cyclist_id = db.Column(db.Integer, db.ForeignKey('cyclist.id'))
    cyclist = db.relationship("Cyclist", back_populates="bikes")

    def to_dict(self):
        bike_dict = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "size": self.size,
            "type": self.type
        }
        return bike_dict

    #Want to creat a new bike object
    @classmethod
    def from_dict(cls, data_dict): #or cls.__init__()
        #check data_dict has all valid bike attrbs
        if "name" in data_dict and "price" in data_dict and "size" in data_dict and "type" in data_dict:
            new_obj = cls(name=data_dict["name"], 
            price=data_dict["price"], 
            size=data_dict["size"], 
            type=data_dict["type"]) 

        return new_obj