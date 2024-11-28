from flask import Blueprint, request, jsonify, session, render_template
from model.reminder_model import Reminder
from model.location_model import Location

reminder_bp = Blueprint("reminder", __name__)

# Create
@reminder_bp.route("/create", methods=["POST", "GET"])
def create_reminder():
    '''
        Creates a reminder
        Data required ("latitude", "longitude", "loc_details", "radius", "description", "reminder_type", "time_trigger", "notification_type")
        Returns a json with a message, status and status code
    '''

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "message": "User not authenticated", 
            "status": "failed"
            }), 401
    details = request.get_json()

    if all(key in details for key in ["description", "reminder_type", 
    "time_trigger", "notification_type"]):

        loc_id = None
        if "location_id" in details:
            loc_id = details["location_id"]
        response = Reminder.create_reminder(
           user_id,
           details["description"],
           details["reminder_type"],
           loc_id,
           details["time_trigger"],
           details["notification_type"]
        ) 

        if response["status"] == "success":

            return jsonify(response),200
        
        return jsonify(response), 401
    
    return jsonify({
        "message": "Missing required fields",
        "status": "failed"
    }), 400

# Delete
@reminder_bp.route("/delete", methods=["DELETE"])
def delete_reminder():
    '''
        Deletes the reminder
        Data required (reminder_id)
        Returns a json with a message, status and status code
    '''

    details = request.get_json()
    if not "reminder_id" in details:
        return jsonify({
            "message" : "Missing Reminder id!",
            "status" : "failed"
        }), 400
    
    response = Reminder.delete_reminder(details["reminder_id"])
    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401

# Read
@reminder_bp.route("/all-time", methods=["GET"])
def get_all_reminders_time():
    '''
        Fetches all the reminder_id, time_trigger, is_completed 
        Data required None
        Returns a json with a message, status, reminders(dict) and status code
    '''

    response = Reminder.get_all_reminders_time()
    if response["status"] == "success":
        return jsonify(response), 200

    return jsonify(response), 400

# Read
@reminder_bp.route("/all", methods=["GET"])
def all_reminders():
    '''
        Fetches all the reminders associated with user_id
        Data required user_id from session
        Returns a json with a message, status, reminders(dict) and status code
    '''
    
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated",
            "status" : "failed"
        }), 401
    

    
    response = Reminder.get_reminders_of_user(user_id )

    if response["status"] == "success":
        return jsonify(response), 200

    return jsonify(response), 400

# Read
@reminder_bp.route("/<id>", methods = ["GET"])
def get_reminder(id):
    '''
        Fetches the reminder
        Data required reminder_id
        Returns a json with a message, status, reminder and status code
    '''
    
    response = Reminder.get_reminder(id)
    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401

# Update
@reminder_bp.route("/update", methods=["PUT"])
def update_reminder():
    '''
        Updates the reminder
        Data required ("reminder_id", "description", "notification_type", "time_trigger", "reminder_type")
        Returns a json with a messaage, status and status code
    '''

    details = request.get_json()   
    
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated",
            "status" : "failed"
        }), 401
    
    loc_id = None
    if "loc_id" in details:
        loc_id = details["loc_id"]
    
    if all(key in details for key in ["reminder_id", "description", "notification_type", "time_trigger", "reminder_type"]):
        response = Reminder.update_reminder(
            details["reminder_id"],
            details["description"],
            details["reminder_type"],
            loc_id,
            details["time_trigger"],
            details["notification_type"]
        )

        if response["status"] == "success":
            return jsonify(response), 200
        
        return jsonify(response), 401
    
    return jsonify({
        "message" : "Missing values",
        "status" : "failed"
    }), 400
        
@reminder_bp.route("/notification-sent", methods = ["GET"])
def update_notification_sent():
    '''
        Updates notification_sent in reminders
        Data required (reminder_id)
        Returns a json with a message, status and status code
    '''

    details = request.get_json()

    if not "reminder_id" in details:
        return jsonify({
            "message" : "Missing reminder id!",
            "status" : "failed"
        }), 401
    
    response = Reminder.notification_sent(details["reminder_id"])
    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401


@reminder_bp.route("/complete/<id>", methods = ["POST"])
def reminder_completed(id):
    '''
        Updates notification_sent in reminders
        Data required (reminder_id)
        Returns a json with a message, status and status code
    '''

    response = Reminder.reminder_completed(id)
    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401

@reminder_bp.route("/create-reminder")
def render_create_reminder():
    return render_template("reminder_creation.html")

@reminder_bp.route("/update-reminder")
def render_update_reminder():
    return render_template("reminder_updation.html")



    