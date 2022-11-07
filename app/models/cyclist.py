from app import db
#only need to update migrations if you change the entities of the table (not for adding something like the to_dict fxn)
class Cyclist(db.Model): #All stuff from SQLA is bc we inherit from the Model
    #db.Model means we don't need to put stuff inside a dunder init
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #id INT GENERATE ALWAYS... #Column turns info into column in DB
    name = db.Column(db.String) #
    bikes = db.relationship("Bike", back_populates="cyclist")

    def to_dict(self):
        bikes_list = [bike.to_dict() for bike in self.bikes]
        cyclist_dict = {
            "id": self.id,
            "name": self.name,  
            "bikes": bikes_list
        }
        return cyclist_dict

    #Want to creat a new bike object
    @classmethod
    def from_dict(cls, data_dict): #or cls.__init__()
        #check data_dict has all valid bike attrbs
        if "name" in data_dict:
            new_obj = cls(name=data_dict["name"]) 

        return new_obj
        #if not, can look into raising an error and abort