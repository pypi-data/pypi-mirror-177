import sqlite3

from os import makedirs, path
from sqlite3 import OperationalError
from aqua_cli.utils import files_location

def create_connection():
    connection = None

    try:
        if not(path.exists(files_location.app_folder)):
            makedirs(files_location.app_folder)
        if not(path.exists(files_location.db_file)):
            connection = sqlite3.connect(database=files_location.db_file)
            cursor = connection.cursor()

            cursor.execute('''
            CREATE TABLE aqua 
                (day INT PRIMARY KEY NOT NULL, 
                intake INT NOT NULL, 
                goal INT NOT NULL)
            '''
            )
            cursor.execute('INSERT INTO aqua VALUES(1, 0, 0)')
            connection.commit()
    except OSError as mkdir_error:
        print(f'FATAL ERROR: {mkdir_error}.\nReport it on GitHub. It was not possible to create the application folder.')
    except OperationalError as sqlite_error:
        print(f'FATAL ERROR: {sqlite_error}.\nReport it on GitHub. Your system is incompatible or the application is getting the wrong folder to store the database.')
    finally:
        if connection != None:
            connection.close()