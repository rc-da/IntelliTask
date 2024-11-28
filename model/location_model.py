from model.db_connection import get_connection
from mysql.connector import Error


class Location:
    '''
        Allow us to create, read Location from location table
    '''

    # Read
    @staticmethod
    def get_loc_id(lat, long, user_id) -> int:
        '''
            Fetches the location_id from the locations table
            Parameters (lat, long, user_id)
            Returns loc_id
        '''

        query = "SELECT location_id FROM locations WHERE lat = %s, long = %s, user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (lat, long, user_id))
            loc_id = cursor.fetchone()

            if loc_id:
                return loc_id[0]
        
        except Error as e:
            print(f"Error occured when getting location_id error is \n{e}")

        finally:
            cursor.close()
            con.close()

        return 0

  # Create location
    @staticmethod
    def create_location(user_id, loc_details, lat, long) -> dict:
        """
        Creates a location entry in the locations table using user_id, latitude, longitude, 
        and other details. Returns a dictionary with the result.
        """
        query = "INSERT INTO locations (user_id, location_detail, latitude, longitude) VALUES (%s, %s, %s, %s)"
        
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (user_id, loc_details, lat, long))
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message": "Location creation successful!",
                    "status": "success"
                }
            
        except Error as e:
            print(f"Error occurred when adding location: {e}")
            return {
                "message": "Error occurred when creating location!",
                "status": "failed"
            }

        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()

        return {
            "message": "Location creation failed!",
            "status": "failed"
        }
    # Read
    @staticmethod
    def get_all_locations_of_user(user_id) -> dict:
        '''
            Fetches all the location of a user in locations table 
            Parameter (user_id)
            Returns a dictionary with a message, status, locations(dict)
        '''

        query = "SELECT * FROM locations WHERE user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            locations = cursor.fetchall()

            if locations:
                return {
                    "message" : "Locations fetch successful!",
                    "status" : "success",
                    "locations" : locations
                }
            
        except Error as e:
            print(f"Error occured when fetching location error = \n{e}")
            return {
            "message" : "Error fetching all location!",
            "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()

        return {
            "message" : "All Location fetch failed!",
            "status" : "failed"
        }
    
    # Read
    @staticmethod
    def get_location(loc_id) -> dict:
        '''
            Fetches the location in locations table 
            Parameter (loc_id)
            Returns a dictionary with a message, status, location(dict)
        '''

        query = "SELECT * FROM locations WHERE location_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(query, (loc_id,))
            location = cursor.fetchone()

            if location:
                return {
                    "message" : "Location fetch successful!",
                    "status" : "success",
                    "location" : location
                }
            
        except Error as e:
            print(f"Error occured when fetching location error = \n{e}")
            return {
            "message" : "Error fetching location!",
            "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()

        return {
            "message" : "Location fetch failed!",
            "status" : "failed"
        }
    
    # Update
    @staticmethod
    def update_location(loc_id, loc_details, latitude, longitude, radius) -> dict:
        '''
            Updates latitude , longitude and radius in locations table
            Parameters (loc_id, loc_details, latitude, longitude, radius)
            Returns a dictionary with a message, status
        '''

        query = "UPDATE locations SET location_details = %s, latitude = %s, longitude = %s, radius =%s WHERE location_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (loc_details, latitude, longitude, radius, loc_id))
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message" : "Location updation successful!",
                    "status" : "success"
                }
        
        except Error as e:
            print(f"Error occured when updating locations error:\n{e}")
            return {
            "message" : "Error updating location!",
            "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()

        return {
            "message" : "Location updation failed!",
            "status" : "failed"
        }
    
    # Delete
    def delete_location(loc_id) -> dict:
        '''
            Deletes the location in locations table
            Parameter (loc_id)
            Returns a dictionary with a message, status
        '''

        query = "DELETE FROM locations WHERE location_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (loc_id,))
            con.commit()
            
            if cursor.rowcount > 0: 
                return {
                    "message" : "Location deletion successful!",
                    "status" : "success"
                }
            
        except Error as e:
            print(f"Error deleting location error:\n{e}")
            return {
                "message" : "Error deleting location!",
                "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()

        return {
            "message" : "Location deletion failed!",
            "status" : "failed"
        }
    
    # Delete
    def delete_all_locations(user_id) -> dict:
        '''
            Deletes all the locations related to user_id 
            Parameter (user_id)
            Returns a dictionary with a message, status
        '''

        query = "DELETE FROM locations WHERE user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (user_id,))
            con.commit()

            if cursor.rowcount > 0:
                return {
                "message" : "Locations deletion successful!",
                "status" : "success"
                }
            
            elif cursor.rowcount == 0:
                return {
                    "message" : "No locations deleted!",
                    "status" : "success"
                }
        
        except Error as e:
            print(f"Error occured when deleting all locations, error : \n{e}")
            return {
            "message" : "Error deleting location!",
            "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()

        return {
            "message" : "Locations deletion failed!",
            "status" : "failed"
        }
