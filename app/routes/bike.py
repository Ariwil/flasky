from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.bike import Bike

# class Bike:
#     def __init__(self, id, name, price, size, type):
#         self.id = id
#         self.name = name
#         self.price = price
#         self.size = size
#         self.type = type

bike_bp = Blueprint("bike_bp", __name__, url_prefix="/bike") #don't need to understand the __name__ piece
# #dont need to understand the "bike_bp" specifically, just something python keeps track of, doesn't need to be the same name as the variable either (even though they have the same name here)

#helper fxn - don't need decorator bc we don't want client to directly access this
def get_one_bike_or_abort(bike_id):
    #see if bike_id can be converted to an integer
    #try-except: try to convert to an int, if error occurs, catch it and raise 400 error with message
    try:
        bike_id = int(bike_id)
    except ValueError:
        response_str = f"Invalid bike_id: `{bike_id}`. ID must be an integer"
        #want to raise abort here instead of the return value. Abort needs to be imported
        abort(make_response(jsonify({"message":response_str}), 400))
    #     return jsonify({"message": response_str}), 400
    # #after the try-except: bike_id will be a valid int
    matching_bike = Bike.query.get(bike_id) #returns None if no matching bike_id

    if matching_bike is None:
        response_str = f"Bike with id '{bike_id}' was not found in database"
        abort(make_response(jsonify({"message":response_str}), 404)) #jsonify is just taking something and converting it into JSON. Make response can be sometihng much larger- returning something under a decorator is doing make rsponse under the hood

    return matching_bike
    # #looping through data to find a bike with matching bike_id
    # #if found: return that bike's data with 200 response code
    # for bike in bikes:
    #     if bike.id == bike_id:
    #         bike_dict = {
    #             "id": bike.id,
    #             "name": bike.name,
    #             "price": bike.price,
    #             "size": bike.size,
    #             "type": bike.type
    #             }
    #         #return in the if block
    #         return jsonify(bike_dict), 200
        
    # #after the loop: the bike with matching bike_id was not found, we will raise 404 error with message
    # response_message = f"Could not find bike with ID {bike_id}"
    # return jsonify({"message":response_message}), 404

# bikes = [
#     Bike(5, "Nina", 100, 48, "gravel"),
#     Bike(8, "Bike 3000", 1000, 50, "hybrid"),
#     Bike(2, "Auberon", 2000, 52, "electonic")
#]

@bike_bp.route("", methods=["GET"])
def get_all_bikes():
    name_param = request.args.get("name")  #request.args is a dict that has all the... attributes?
    
    if name_param is None:
        bikes = Bike.query.all() #Inherited from db.Model
    else:
        bikes = Bike.query.filter_by(name=name_param) #filter_by --> only bikes that fit this condition

    response = []
    for bike in bikes:
        bike_dict = {
            "id": bike.id,
            "name": bike.name,
            "price": bike.price,
            "size": bike.size,
            "type": bike.type
        }
        response.append(bike_dict)
    return jsonify(response), 200 #abort: 
    


@bike_bp.route("/<bike_id>", methods=["GET"])
def get_one_bike(bike_id):
    chosen_bike = get_one_bike_or_abort(bike_id)

    bike_dict = {
            "id": chosen_bike.id,
            "name": chosen_bike.name,
            "price": chosen_bike.price,
            "size": chosen_bike.size,
            "type": chosen_bike.type
        }

    return jsonify(bike_dict), 200 #.to_dict() changes variable into a dictionary format. ???Jsonify only works on dicts????

@bike_bp.route("", methods=["POST"])
def add_bike():
    request_body = request.get_json()

    new_bike = Bike(
        name=request_body["name"],
        price=request_body["price"],
        size=request_body["size"],
        type=request_body["type"]
    )
        
        
    db.session.add(new_bike) 
    db.session.commit() #CRUCIAL !!!!! Must do a commit here! #to make changes to our DB

    return {"id": new_bike.id}, 201

@bike_bp.route("/<bike_id>", methods=["PUT"])
def update_bike_with_new_vals(bike_id):
    chosen_bike = get_one_bike_or_abort(bike_id)

    request_body = request.get_json()

    if "name" not in request_body or \
        "size" not in request_body or \
        "price" not in request_body or \
        "type" not in request_body:
            return jsonify({"message":"Request must include name, size, price, and type"})

    chosen_bike.name = request_body["name"]
    chosen_bike.size = request_body["size"]
    chosen_bike.price = request_body["price"]
    chosen_bike.type = request_body["type"]

    db.session.commit()

    return jsonify({"message": "Successfully replaced bike with id '{bike_id}'"}), 200

@bike_bp.route("/<bike_id>", methods=["DELETE"])
def delete_one_bike(bike_id):
    chosen_bike = get_one_bike_or_abort(bike_id)

    db.session.delete(chosen_bike)
    db.session.commit()

    return jsonify({"Message": "Successfully deleted bike with id '{bike_id}'"}), 200
# @bike_bp.route("/<bike_id>", methods=["GET"])
# def get_one_bike(bike_id):
#     #see if bike_id can be converted to an integer
#     #try-except: try to convert to an int, if error occurs, catch it and raise 400 error with message
#     try:
#         bike_id = int(bike_id)
#     except ValueError:
#         response_str = f"Invalid bike_id: `{bike_id}`. ID must be an integer"
#         return jsonify({"message": response_str}), 400
#     #after the try-except: bike_id will be a valid int

#     #looping through data to find a bike with matching bike_id
#     #if found: return that bike's data with 200 response code
#     for bike in bikes:
#         if bike.id == bike_id:
#             bike_dict = {
#                 "id": bike.id,
#                 "name": bike.name,
#                 "price": bike.price,
#                 "size": bike.size,
#                 "type": bike.type
#                 }
#             #return in the if block
#             return jsonify(bike_dict), 200
        
#     #after the loop: the bike with matching bike_id was not found, we will raise 404 error with message
#     response_message = f"Could not find bike with ID {bike_id}"
#     return jsonify({"message":response_message}), 404