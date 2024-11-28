from configuration.get_config import config
import mysql.connector

def get_connection():
    '''
        Gets the database connection
    '''
    return mysql.connector.connect(**config("db_config"))

