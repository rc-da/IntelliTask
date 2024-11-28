from flask import Blueprint, request, jsonify, session
from model.user_model import User_Profile
from thirdparty.mail import send_email
from datetime import datetime 
import requests

user_bp = Blueprint('user', __name__)

# Create
@user_bp.route("/signup", methods = ["POST"])
def signup():
    '''
        Create new user
        Data required ("user_name", "user_mail", "user_phno", "password")
        Returns json with a message, status and status code
    '''

    details = request.get_json()
    if all(key in details for key in ["user_name", "user_mail", "user_phno", "password"]):

        signup_response = User_Profile.create_user(
            details["user_name"],
            details["user_mail"],
            details["user_phno"], 
            details["password"]
        )

        if signup_response["status"] == "success":
            
            return jsonify(signup_response), 200
        
        return jsonify(signup_response), 401
    
    return jsonify({
        "message" : "Missing required fields!",
        "status" : "failed"
    }), 400


# Read
@user_bp.route("/login", methods = ["POST"])
def login():
    '''
        Authenticate user
        Data required (mail, password)
        Returns json with a message, status, user_name, user_id and status code  
    '''

    details = request.get_json()
    
    if "user_mail" in details and "password" in details:

        auth_response = User_Profile.authenticate_user(
            details["user_mail"],
            details["password"]
            )

        if auth_response["status"] == "success":
            session["user_id"] = auth_response["user_id"]
            session["user_name"] = auth_response["user_name"]
            user_name = auth_response["user_name"]

            now = datetime.now()
            current_date = now.strftime("%d-%m-%Y")
            current_time = now.strftime("%H:%M:%S")
            subject = "New Login Detected on your Intellitask Account"
            body = f''' Hi {user_name},\n\n We noticed a new login to your Intellitask account on {current_date} at {current_time}\n\n If it was you no further action required.'''

            send_email(details["user_mail"], body, subject)
            print(auth_response, session.get("user_id"))
            return jsonify(auth_response), 200
        
        return jsonify(auth_response), 401
    
    return jsonify({
        "message" : "Missing required fields!" ,
        "status" : "failed"    
    }), 400

# Update
@user_bp.route("/logout", methods = ["POST"])
def logout():
    '''
        Clears the session
    '''
    session.clear()

    return jsonify({
        "message" : "Logged out successfully!",
        "status" : "success"
    }), 200

# Read
@user_bp.route("/fetch", methods = ["GET"])
def get_user():
    '''
        Fetches the user details
        Data required session user_id
        Returns a json with a message, status, user(dict) and status code
    '''

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User not authenticated!",
            "status" : "failed"
        }), 401
    
    user_response = User_Profile.get_user(user_id)

    if user_response["status"] == "success":
        return jsonify(user_response), 200
    
    return jsonify(user_response), 401

# Delete
@user_bp.route("/delete", methods = ["DELETE"])
def delete_user():
    '''
        Deletes the user
        Data required session user_id
        Returns a json with a message, status and status code
    '''

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    delete_response = User_Profile.delete_user(user_id)
    
    if delete_response["status"] == "success":
        return jsonify(delete_response), 200
    
    return jsonify(delete_response), 401

# Update
@user_bp.route("/update", methods = ["PUT"])
def update_user():
    '''
        Update the user details
        Data required ("name", "mail", "phno", "telegram_id", "password")
        Returns a json with a message, status and status code
    '''

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    details = request.get_json()
    if all(key in details for key in ["user_name", "user_mail", "user_phno", "password"]):

        update_response = User_Profile.update_user(
            user_id, 
            details["user_name"], 
            details["user_mail"],
            details["user_phno"],
            details["password"]
            )
        
        if update_response["status"]:
            return jsonify(update_response), 200
        
        return jsonify(update_response), 401
    
    return jsonify({
        "message" : "Missing required fields!",
        "status" : "failed"
    }), 400

    
