''' app initializion methods '''
from sorter.lib.db import DB

def init(db_file):
    ''' initializa the app '''
    database = DB(db_file)

    database.create_connection()

    qry = '''CREATE TABLE rankings
             (id PRIMARY KEY, isbn UNIQUE, isbn13 UNIQUE, title, image_url, 
              publication_year INTEGER, ratings_count INTEGER, average_rating FLOAT,
              author, link, preference_adjustment FLOAT DEFAULT 0.0)'''

    database.execute(qry)

    database.close_connection()
