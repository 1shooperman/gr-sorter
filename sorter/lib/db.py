'''
db.py
'''
import sqlite3

class DB(object):
    '''
    Class wrapping SQLite3, providing helper methods as needed.
    Initialized with a string containing path to new or existing db file
    '''
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        ''' get or create a sql connection '''
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_file)

        return self.conn

    def close_connection(self):
        ''' close the database connection '''
        self.conn.close()
        self.conn = None

    def insertupdate(self, qry, values):
        ''' insert/update data in the database '''
        cur = self.conn.cursor()
        cur.execute(qry, values)
        self.conn.commit()

    def query(self, qry):
        ''' run a query against the database '''
        return self.conn.execute(qry).fetchall()

    def execute(self, qry):
        ''' execute arbitrary command against the database '''
        cur = self.conn.cursor()
        cur.execute(qry)
        self.conn.commit()
