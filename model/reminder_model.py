from mysql.connector import Error
from model.db_connection import get_connection
from reminder.reminder import fetch_all_reminders

class Reminder:
    """
    This class provides CRUD operations for the `reminders` table.
    """

    @staticmethod
    def create_reminder(user_id, description, rem_type, loc_id, time_trigger, noti_type) -> dict:
        """
        Adds a reminder to the `reminders` table.
        Parameters:
            user_id (int): ID of the user creating the reminder.
            description (str): Description of the reminder.
            rem_type (str): Type of reminder (time, location, etc.).
            loc_id (int): Location ID associated with the reminder.
            time_trigger (datetime): Time trigger for the reminder.
            noti_type (str): Notification type.
        Returns:
            dict: Contains a message and status of the operation.
        """
        query = "INSERT INTO reminders (user_id, description, reminder_type, location_id, time_trigger, notification_type) VALUES (%s, %s, %s, %s, %s, %s)"
        con = get_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(query, (user_id, description, rem_type, loc_id, time_trigger, noti_type))
                con.commit()
                if cursor.rowcount > 0:
                    fetch_all_reminders()
                    return {"message": "Reminder creation successful!", "status": "success"}
        except Error as e:
            print(f"Error: {e}")
            return {"message": "Error creating reminder!", "status": "failed"}
        finally:
            con.close()
        return {"message": "Reminder creation failed!", "status": "failed"}

    @staticmethod
    def get_reminders_of_user(user_id) -> dict:
        """
        Fetches all reminders associated with a user.
        Parameters:
            user_id (int): ID of the user.
        Returns:
            dict: Contains a message, status, and reminders (if found).
        """
        query = "SELECT * FROM reminders WHERE user_id = %s"
        con = get_connection()
        try:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute(query, (user_id,))
                reminders = cursor.fetchall()
                if reminders:
                    return {"message": "Reminders fetched successfully!", "status": "success", "reminders": reminders}
        except Error as e:
            print(f"Error: {e}")
            return {"message": "Error fetching reminders!", "status": "failed"}
        finally:
            con.close()
        return {"message": "No reminders found!", "status": "failed"}

    @staticmethod
    def get_all_reminders_time() -> dict:
        """
        Fetches all reminders with time triggers where notifications are not sent and not completed.
        Returns:
            dict: Contains a message, status, and reminders (if found).
        """
        query = "SELECT reminder_id, time_trigger FROM reminders WHERE is_completed = 0 AND notification_sent = 0 AND reminder_type = 'time'"
        con = get_connection()
        try:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                reminders = cursor.fetchall()
                if reminders:
                    return {"message": "All reminders time fetched successfully!", "status": "success", "reminders": reminders}
        except Error as e:
            print(f"Error: {e}")
            return {"message": "Error fetching reminders!", "status": "failed"}
        finally:
            con.close()
        return {"message": "No reminders found!", "status": "failed"}

    @staticmethod
    def get_reminder(rem_id) -> dict:
        """
        Fetches a specific reminder by ID.
        Parameters:
            rem_id (int): ID of the reminder.
        Returns:
            dict: Contains a message, status, and reminder (if found).
        """
        query = "SELECT * FROM reminders WHERE reminder_id = %s"
        con = get_connection()
        try:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute(query, (rem_id,))
                reminder = cursor.fetchone()
                if reminder:
                    return {"message": "Reminder fetched successfully!", "status": "success", "reminder": reminder}
        except Error as e:
            print(f"Error: {e}")
            return {"message": "Error fetching reminder!", "status": "failed"}
        finally:
            con.close()
        return {"message": "Reminder not found!", "status": "failed"}

    @staticmethod
    def update_reminder(rem_id, description, rem_type, loc_id, time_trigger, noti_type) -> dict:
        """
        Updates a specific reminder by ID.
        Parameters:
            rem_id (int): ID of the reminder.
            description (str): New description of the reminder.
            rem_type (str): New type of the reminder.
            loc_id (int): New location ID.
            time_trigger (datetime): New time trigger.
            noti_type (str): New notification type.
        Returns:
            dict: Contains a message and status of the operation.
        """
        query = "UPDATE reminders SET description = %s, reminder_type = %s, location_id = %s, time_trigger = %s, notification_type = %s, notification_sent = 0 WHERE reminder_id = %s"
        con = get_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(query, (description, rem_type, loc_id, time_trigger, noti_type, rem_id))
                con.commit()
                if cursor.rowcount > 0:
                    fetch_all_reminders()
                    return {"message": "Reminder updated successfully!", "status": "success"}
        except Error as e:
            print(f"Error: {e}")
            return {"message": "Error updating reminder!", "status": "failed"}
        finally:
            con.close()
        return {"message": "Reminder update failed!", "status": "failed"}

    @staticmethod
    def delete_reminder(rem_id) -> dict:
        """
        Deletes a specific reminder by ID.
        Parameters:
            rem_id (int): ID of the reminder.
        Returns:
            dict: Contains a message and status of the operation.
        """
        query = "DELETE FROM reminders WHERE reminder_id = %s"
        con = get_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(query, (rem_id,))
                con.commit()
                if cursor.rowcount > 0:
                    fetch_all_reminders()
                    return {"message": "Reminder deleted successfully!", "status": "success"}
        except Error as e:
            print(f"Error: {e}")
            return {"message": "Error deleting reminder!", "status": "failed"}
        finally:
            con.close()
        return {"message": "Reminder deletion failed!", "status": "failed"}

    @staticmethod
    def delete_all_reminders(user_id) -> dict:
        """
        Deletes all reminders associated with a user.
        Parameters:
            user_id (int): ID of the user.
        Returns:
            dict: Contains a message and status of the operation.
        """
        query = "DELETE FROM reminders WHERE user_id = %s"
        con = get_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(query, (user_id,))
                con.commit()
                if cursor.rowcount > 0:
                    fetch_all_reminders()
                    return {"message": "All reminders deleted successfully!", "status": "success"}
        except Error as e:
            print(f"Error: {e}")
            return {"message": "Error deleting reminders!", "status": "failed"}
        finally:
            con.close()
        return {"message": "No reminders deleted!", "status": "success"}

    @staticmethod
    def reminder_completed(rem_id) -> dict:
        """
        Marks a reminder as completed.
        Parameters:
            rem_id (int): ID of the reminder.
        Returns:
            dict: Contains a message and status of the operation.
        """
        query = "UPDATE reminders SET is_completed = 1 WHERE reminder_id = %s"
        con = get_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(query, (rem_id,))
                con.commit()
                if cursor.rowcount > 0:
                    fetch_all_reminders()
                    return {"message": "Reminder marked as completed!", "status": "success"}
        except Error as e:
            print(f"Error: {e}")
            return {"message": "Error updating completion status!", "status": "failed"}
        finally:
            con.close()
        return {"message": "Failed to mark reminder as completed!", "status": "failed"}

    @staticmethod
    def notification_sent(rem_id) -> dict:
        """
        Marks a reminder's notification as sent.
        Parameters:
            rem_id (int): ID of the reminder.
        Returns:
            dict: Contains a message and status of the operation.
        """
        query = "UPDATE reminders SET notification_sent = 1 WHERE reminder_id = %s"
        con = get_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(query, (rem_id,))
                con.commit()
                if cursor.rowcount > 0:
                    fetch_all_reminders()
                    return {"message": "Notification marked as sent!", "status": "success"}
        except Error as e:
            print(f"Error: {e}")
            return {"message": "Error updating notification status!", "status": "failed"}
        finally:
            con.close()
        return {"message": "Failed to mark notification as sent!", "status": "failed"}

    @staticmethod
    def get_all_reminders_location_time() -> dict:
        """
        Fetches all reminders with location and time triggers where notifications are not sent and not completed.
        Returns:
            dict: Contains a message, status, and reminders (if found).
        """
        query = """
    SELECT reminder_id, time_trigger, location_id
    FROM reminders
    WHERE is_completed = 0
      AND notification_sent = 0
      AND reminder_type IN ('loc', 'time&loc')
    """
        con = get_connection()
        try:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                reminders = cursor.fetchall()
                if reminders:
                    return {"message": "All reminders fetched successfully!", "status": "success", "reminders": reminders}
        except Error as e:
            print(f"Error: {e}")
            return {"message": "Error fetching reminders!", "status": "failed"}
        finally:
            con.close()
        return {"message": "No reminders found!", "status": "failed"}
