# databasemanager.py

import config
from mysql.connector import connect, Error


class DatabaseManager:
    def __init__(self):
        self._host = config.database_conn['host']
        self._user = config.database_conn['username']
        self._password = config.database_conn['password']
        self._database = config.database_conn['database']

    def get_dataset(self, query):
        result = []
        try:
            with connect(host=self._host, user=self._user, password=self._password, database=self._database) as \
                    connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
        except Error as error:
            print(error)
        return result
