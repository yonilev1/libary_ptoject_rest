import mysql.connector

class DbConnection:
    def __init__(self):
        self.user='root'
        self.password='root'
        self. host='127.0.0.1'
        self.port=3306
        self.database='library_db'


    def get_connection(self):
        return mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
            port=self.port
        )
        