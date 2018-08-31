import sqlite3
from sqlite3 import Error
 
class DB(object):
    def __init__(self, db_file):
        self.db_file = db_file

    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print e

    def get_connection(self):
        return self.conn

    def close_connection(self):
        try:
            self.conn.close()
        except Error as e:
            print e

#if __name__ == '__main__':
#    create_connection("data/sqlite.db")
