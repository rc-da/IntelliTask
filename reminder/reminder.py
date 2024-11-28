reminder_trigger = {}

def fetch_all_reminders():
    global reminder_trigger

    from model.reminder_model import Reminder
    response = Reminder.get_all_reminders_time()

    if response["status"] == "failed":
        print(response["message"])
        return
    
    reminders = response["reminders"]
    reminder_trigger.clear()
    
    for reminder in reminders:
            reminder_trigger[reminder["reminder_id"]] = {
                "time_trigger": reminder["time_trigger"]
            }

    print("Reminders loaded successfully into reminder_trigger.", reminder_trigger)


def fetch_all_location_reminders():
    location_reminder = {}

    from model.reminder_model import Reminder
    from model.location_model import Location
    response = Reminder.get_all_reminders_location_time()
    print("The response loaded:", response)

    if response["status"] == "failed":
        print("Failed to fetch reminders:", response["message"])
        return
    
    reminders = response["reminders"]
    location_reminder.clear()
    
    for reminder in reminders:
        location_id = reminder["location_id"]
        if not location_id:
            print(f"Reminder {reminder['reminder_id']} does not have a location_id.")
            continue

        location_response = Location.get_location(location_id)
        print(f"Fetching location for ID {location_id}: {location_response}")

        
        if location_response["status"] == "success":
            location_coords = location_response["location"]
            latitude = location_coords["latitude"]
            longitude = location_coords["longitude"]

            if reminder.get("time_trigger"):
                location_reminder[reminder["reminder_id"]] = {
                    "time_trigger": reminder["time_trigger"],
                    "latitude": latitude,
                    "longitude": longitude,
                }
            else:
                location_reminder[reminder["reminder_id"]] = {
                    "latitude": latitude,
                    "longitude": longitude,
                }
        else:
            print(f"Error when getting location for reminder ID {reminder['reminder_id']}: {location_response.get('message', 'Unknown error')}")

    print("Checking location reminders...", location_reminder)

    if not location_reminder:
        print("No Reminder found!")

    return location_reminder

