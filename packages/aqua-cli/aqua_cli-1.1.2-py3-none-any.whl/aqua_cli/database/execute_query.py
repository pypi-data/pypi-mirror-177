import sqlite3

from sqlite3 import OperationalError
from aqua_cli.utils import files_location

def execute_query(query, parameters='', return_value=False, return_all=False):
    connection = None
    
    try:
        connection = sqlite3.connect(files_location.db_file)
        cursor = connection.cursor()

        cursor.execute(query, parameters)
        
        if return_value and return_all:
            return cursor.fetchall()
        if return_value:
            return cursor.fetchone()

        connection.commit()
    except OperationalError as sqlite_error:
        print(f'FATAL ERROR: {sqlite_error}. Couldn\'t complete the query, report it on GitHub.')
    finally:
        if connection != None:
            connection.close()