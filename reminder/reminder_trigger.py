from datetime import datetime
from reminder.reminder import fetch_all_location_reminders, reminder_trigger
from model.reminder_model import Reminder
from model.user_model import User_Profile
from thirdparty.mail import send_email

def trigger_notification(reminder_id):
    """
    Triggers notification for a specific reminder.
    Sends an email if notification type is 'mail'.
    """
    reminder_response = Reminder.get_reminder(reminder_id)
    if reminder_response["status"] == "failed":
        return reminder_response
    
    reminder = reminder_response["reminder"]
    user_response = User_Profile.get_user(reminder["user_id"])

    if user_response["status"] == "failed":
        return user_response
    
    user = user_response["user"]

    if reminder["notification_type"] == "mail":
        send_email(user["user_mail"], reminder["description"])
        print("Notification sent via email.")
        return {"status": "success", "message": "Notification sent successfully."}

    return {"status": "failed", "message": "Unsupported notification type."}

def process_reminders(reminders, latitude=None, longitude=None):
    """
    Processes reminders and triggers notifications based on time or location.
    """
    if not reminders:
        return 
    current_time = datetime.now()

    for rem_id, reminder in reminders.items():
        if latitude is not None and longitude is not None:
            if reminder["latitude"] != latitude or reminder["longitude"] != longitude:
                continue
            if "time_trigger" in reminder and reminder["time_trigger"] > current_time:
                continue
        elif reminder["time_trigger"] > current_time:
            continue

        response = trigger_notification(rem_id)

        if response["status"] == "success":
            reminder_response = Reminder.notification_sent(rem_id)
            print(reminder_response["message"])
        else:
            print(f"Failed to send notification for reminder {rem_id}: {response['message']}")
    else:
        print("No Reminder found!")
        
def check_reminders_trigger():
    """
    Checks time-based reminders and triggers notifications if necessary.
    """
    print("Checking reminders...")
    process_reminders(reminder_trigger)

def check_location_trigger(latitude, longitude):
    """
    Checks location-based reminders and triggers notifications if necessary.
    """
    location_reminder = fetch_all_location_reminders()
    print("Checking location reminders...")
    process_reminders(location_reminder, latitude, longitude)
