import sqlite3
from sqlite3 import Error
 
class DB(object):
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        if (self.conn == None):
            """ create a database connection to a SQLite database """
            self.conn = sqlite3.connect(self.db_file)

        return self.conn

    def get_connection(self):
        if (self.conn == None):
            self.conn = self.create_connection()
     
        return self.conn

    def close_connection(self):
        try:
            self.conn.close()
        except Error as e:
            print e

    def insert(self, qry):
        c = self.conn.cursor()
        c.execute(qry)
        self.conn.commit()

    def update(self, qry):
        self.insert(qry)

    def query(self, qry):
        return self.conn.execute(qry).fetchall()

    def execute(self, qry):
        self.insert(qry)
