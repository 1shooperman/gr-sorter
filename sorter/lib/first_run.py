from lib.db import DB

def init(db_file):
    db = DB(db_file)
   
    db.get_connection()

    qry = '''CREATE TABLE rankings
             (id PRIMARY KEY, isbn UNIQUE, isbn13 UNIQUE, title, image_url, 
              publication_year INTEGER, ratings_count INTEGER, average_rating FLOAT,
              author)'''
    
    db.execute(qry)
    
    db.close_connection()

