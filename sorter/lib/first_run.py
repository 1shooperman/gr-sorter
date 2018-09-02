''' app initializion methods '''
from lib.db import DB

def init(db_file):
    ''' initializa the app '''
    database = DB(db_file)

    database.create_connection()

    qry = '''CREATE TABLE rankings
             (id PRIMARY KEY, isbn UNIQUE, isbn13 UNIQUE, title, image_url, 
              publication_year INTEGER, ratings_count INTEGER, average_rating FLOAT,
              author)'''

    database.execute(qry)

    database.close_connection()
