# manage your database connections here, low level actions only
import sqlite3


class DatabaseContext:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.database_name = "database.db"
        self.database_path = "data/database.db"

    def connect(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
        self.cursor.close()

    def execute(self,query):
        self.cursor.execute(query)
        self.connection.commit()

    def fetchall(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetchone(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetchmany(self,query,size):
        self.cursor.execute(query)
        return self.cursor.fetchmany(size)
