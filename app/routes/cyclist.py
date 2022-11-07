from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.cyclist import Cyclist
from app.models.bike import Bike



cyclist_bp = Blueprint("cyclist_bp", __name__, url_prefix="/cyclist") #don't need to understand the __name__ piece
# #dont need to understand the "cyclist_bp" specifically, just something python keeps track of, doesn't need to be the same name as the variable either (even though they have the same name here)


#could go ahead and put helper fxns like this one in it's own file
#better to store this in a separate file since we may use it for classes other than cyclist
def get_one_obj_or_abort(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        response_str = f"Invalid ID: `{obj_id}`. ID must be an integer"
        #want to raise abort here instead of the return value. Abort needs to be imported
        abort(make_response(jsonify({"message":response_str}), 400))
    #     return jsonify({"message": response_str}), 400
    # #after the try-except: cyclist_id will be a valid int
    matching_obj = cls.query.get(obj_id) #returns None if no matching cyclist_id

    if matching_obj is None:
        response_str = f"{cls.__name__} '{obj_id}' was not found in database"
        abort(make_response(jsonify({"message":response_str}), 404)) #jsonify is just taking something and converting it into JSON. Make response can be sometihng much larger- returning something under a decorator is doing make rsponse under the hood

    return matching_obj 
#  -------------------------------------------------POST-----------------------------------------   
@cyclist_bp.route("", methods=["POST"])
def add_cyclist():
    request_body = request.get_json()

    new_cyclist = Cyclist.from_dict(request_body) #cyclist(
 
    db.session.add(new_cyclist) 
    db.session.commit() #CRUCIAL !!!!! Must do a commit here! #to make changes to our DB

    return {"id": new_cyclist.id}, 201

@cyclist_bp.route("/<cyclist_id>/bike", methods=["POST"])
def post_bike_belonging_to_cyclist(cyclist_id):
    parent_cyclist = get_one_obj_or_abort(Cyclist, cyclist_id)

    request_body = request.get_json()

    new_bike = Bike.from_dict(request_body)
    new_bike.cyclist = parent_cyclist #setting the Bike attribute of cyclist to parent_cyclist (which sets the bikes attrb in Cyclist)

    db.session.add(new_bike)
    db.session.commit()

    return jsonify({"message": f"Bike {new_bike.name} belonging to {new_bike.cyclist.name} successfully added"}), 201


#  -------------------------------------------------GET-----------------------------------------   

@cyclist_bp.route("", methods=["GET"])
def get_all_cyclists():
    name_param = request.args.get("name")  #request.args is a dict that has all the... attributes?
    
    if name_param is None:
        cyclists = Cyclist.query.all() #Inherited from db.Model
    else:
        cyclists = Cyclist.query.filter_by(name=name_param) #filter_by --> only cyclists that fit this condition

    response = [cyclist.to_dict() for cyclist in cyclists]
    return jsonify(response), 200 #abort:

@cyclist_bp.route("/<cyclist_id>", methods=["GET"])
def get_one_cyclist(cyclist_id):
    chosen_cyclist = get_one_obj_or_abort(Cyclist, cyclist_id)

    cyclist_dict = chosen_cyclist.to_dict() #{

    return jsonify(cyclist_dict), 200 #.to_dict() changes variable into a dictionary format. ???Jsonify only works on dicts????

@cyclist_bp.route("/<cyclist_id>/bike", methods=["GET"])
def get_all_bikes_belonging_to_cyclist(cyclist_id):
    cyclist = get_one_obj_or_abort(Cyclist, cyclist_id)

    bikes_response = [bike.to_dict() for bike in cyclist.bikes] #loops through bikes of cyclists

    return jsonify(bikes_response)

# @cyclist_bp.route("/<cyclist_id>", methods=["PUT"])
# def update_cyclist_with_new_vals(cyclist_id):
#     chosen_cyclist = get_one_obj_or_abort(cyclist, cyclist_id)

#     request_body = request.get_json()

#     if "name" not in request_body or \
#         "size" not in request_body or \
#         "price" not in request_body or \
#         "type" not in request_body:
#             return jsonify({"message":"Request must include name, size, price, and type"})

#     chosen_cyclist.name = request_body["name"]
#     chosen_cyclist.size = request_body["size"]
#     chosen_cyclist.price = request_body["price"]
#     chosen_cyclist.type = request_body["type"]

#     db.session.commit()

#     return jsonify({"message": "Successfully replaced cyclist with id '{cyclist_id}'"}), 200

# @cyclist_bp.route("/<cyclist_id>", methods=["DELETE"])
# def delete_one_cyclist(cyclist_id):
#     chosen_cyclist = get_one_obj_or_abort(cyclist, cyclist_id)

#     db.session.delete(chosen_cyclist)
#     db.session.commit()

#     return jsonify({"Message": "Successfully deleted cyclist with id '{cyclist_id}'"}), 200
