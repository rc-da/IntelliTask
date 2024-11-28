from flask import Blueprint, jsonify, request, session
from model.location_model import Location
from reminder.reminder_trigger import check_location_trigger

location_bp = Blueprint("location", __name__)

# Create
@location_bp.route("/create", methods=["POST"])
def create_location():
    details = request.get_json()
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    if all(key in details for key in ["location_detail", "latitude", "longitude"]):
        response = Location.create_location(
            user_id,
            details["location_detail"],
            details["latitude"],
            details["longitude"]
        )

        if response["status"]:
            return jsonify(response), 200
        
        return jsonify(response), 401

    # Return an error if required fields are missing
    return jsonify({
        "message": "Missing required fields!",
        "status": "failed"
    }), 400

# Read
@location_bp.route("/all", methods = ["GET", ])
def all_locations():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    response = Location.get_all_locations_of_user(user_id)

    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify({
        "message" : response["message"],
        "status" : "failed"
    }), 401

# Read
@location_bp.route("/<int:id>", methods = ["GET"])
def get_location(id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    response = Location.get_location(id)

    if response["status"]:
        return jsonify({
            "message" : response["message"],
            "status" : "success",
            "location" : response["location"]
        }), 200
    
    return jsonify({
        "message" : response["message"],
        "status" : "failed",
    }), 401

# Delete
@location_bp.route("/delete/<id>", methods= ["DELETE"])
def delete_location(id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    response = Location.delete_location(id)

    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401

# Update
@location_bp.route("/update", methods= ["PUT"])
def update_location():
    details = request.get_json()
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    if all(key in details for key in ["loc_id", "loc_details", "lat", "long", "radius"]):

        response = Location.update_location(
            details["loc_id"], 
            details["loc_details"],
            details["lat"],
            details["long"],
            details["radius"],
        )

        if response["status"]:
            return jsonify({
                "message" : response["message"],
                "status" : "success"
            }), 200
        
        return jsonify({
            "message" : response["message"],
            "status" : "failed"
        }), 401
    
    return jsonify({
        "message" : "Missing required fields!",
        "status" : "failed"
    }), 400

#Check Location
@location_bp.route("/check", methods=["POST"])
def check_location():
    details = request.get_json()
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401

    if "latitude" in details and "longitude" in details:
        check_location_trigger(details["latitude"], details["longitude"])
    return jsonify({
        "message" : "Location reminder if present sent",
        "status" : "success"
    }), 200