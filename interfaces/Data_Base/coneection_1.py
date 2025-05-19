import mysql.connector as mysql
from mysql.connector import Error


def get_db():
    try:
    
        connection = mysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='guilherme',
            database='drone_project'
        )

        if connection.is_connected():
            return connection
    
    except Error as e:
        return None
    
    