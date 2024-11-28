from mysql.connector import Error
from model.db_connection import get_connection
from model.reminder_model import Reminder
from model.location_model import Location

class User_Profile:
    '''
        Allow us to do crud operation in user_credentials table
    '''

    # Read
    @staticmethod
    def get_user(id) -> dict:
        ''' 
            Fetches user info from user_credentials table  
            Parameter (id)
            Returns a dictionary with a status, message, user(dict)
        '''

        query = "SELECT * FROM user_credentials WHERE user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(query, (id,))
            user = cursor.fetchone()
            return {
                "message" : "User fetch successful!",
                "status" : "success",
                "user" : user
            }
        except Error as e:
            print(f"Error occured while fetching user error:\n{e}")

        finally:
            cursor.close()
            con.close()
        return {
            "message" : "User fetch failed!",
            "status" : "success"
        }
    
    # Read
    @staticmethod
    def check_new_user(identifier) ->bool:
        '''
            Check whether the new user exists in the user_credentials
            Parameter (identifier)
            Returns boolean
        '''

        query = "SELECT * FROM user_credentials WHERE user_id = %s or user_mail = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (identifier, identifier))
            if cursor.fetchone():
                return False
            
            return True
            
        except Error as e:
            print(f"Error occured while checking user error:\n{e}")
            return True

        finally:
            cursor.close()
            con.close()
        

    # Create
    @staticmethod
    def create_user(name, email, phno, password) -> dict:
        '''
            Adds user to user_credentials 
            Parameters (name, email, phno, password)
            Returns a dictionary with a message and status.
        '''
        
        if not User_Profile.check_new_user(email):
            return {
                "message": "User already exists!",
                "status": "failed"
            }

        query = """
            INSERT INTO user_credentials (user_name, user_mail, user_phno, password) 
            VALUES (%s, %s, %s, %s)
        """

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (name, email, phno, password))
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message": "User signup Successful!",
                    "status": "success"
                }
            
            
            return {
                "message": "User signup failed!",
                "status": "failed"
            }

        except Error as e:
            print(f"Error occurred while adding user: {e}")
            return {
                "message": "Error signing up!",
                "status": "failed"
            }

        finally:
                cursor.close()
                con.close()

    # Delete  
    @staticmethod 
    def delete_user(user_id) -> dict:
        '''
            Deletes the user from the user_credentials table
            Parameter (user_id)
            Returns a dictionary with a message, status
        '''

        if User_Profile.check_new_user(user_id):
            return {
                "message" : "User doesn't exist!",
                "status" : "failed"
            }
        
        reminder_response = Reminder.delete_all_reminders(user_id)
        
        if reminder_response["status"] == "failed":
            return reminder_response
        
        location_response = Location.delete_all_locations(user_id)
        
        if location_response["status"] == "failed":
            return location_response

        query = "DELETE FROM user_credentials WHERE user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (user_id,)) 
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message" : "User deletion Successful!",
                    "status" : "success"
                }

        except Error as e:
            print(f"Error occured while deleting user error:\n{e}")
            return {
                "message" : "Error Deleting User!",
                "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()

        return {
                "message" : "User deletion failed!",
                "status" : "failed"
            }
    
    # Update
    @staticmethod
    def update_user(user_id, name, mail, phno, password) -> dict:
        '''
            Updates user details in user_credentials table
            Parameters (user_id, name, mail, phno,password)
            Returns a dictionary with a message, status
        '''

        query = "UPDATE user_credentials SET user_name = %s, user_mail = %s, user_phno = %s, password = %s WHERE user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (name, mail, phno, password, user_id))
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message" : "User updation successful!",
                    "status" : "success"
                }
        
        except Error as e:
            print(f"Error while updating user details: {e}")
            return {
            "message" : "Error updating user!",
            "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()
            
        return {
            "message" : "User updation failed!",
            "status" : "failed"
        }
    
    # Read
    @staticmethod
    def authenticate_user(user_mail, password) -> dict:
        '''
            Authenticates user
            Parameter (user_mail, password)
            Returns a dictionary witha message, status, user_name, user_id
        '''

        new_user = User_Profile.check_new_user(user_mail)

        if new_user:
            return {
                "message" : "User Doesn't Exist in the System!",
                "status" : "failed"
                }
        
        query = "SELECT user_id, user_name FROM user_credentials WHERE user_mail = %s and password = %s"

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (user_mail, password))
            aunthenticated = cursor.fetchone()

            if aunthenticated:
                return {
                    "message" : "Login successful!",
                    "status" : "success",
                    "user_id" : aunthenticated[0],
                    "user_name" : aunthenticated[1]
                    }
            
        except Error as e:
            print(f"Error occured when authenticating the User error is \n{e}")
            return {
            "message" : "Error authenticating user!",
            "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()
        
        return {
        "message" : "Wrong Password!",
        "status" : "failed"
        }

if __name__ == "__main__":
    print(User_Profile.check_new_user("jobyj_a21@velhightech.com"))