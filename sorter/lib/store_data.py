from lib.db import DB

def store_data(books, db_file):
    db = DB(db_file)

    db.get_connection()
    
    for book in books:
        qry_base = '''INSERT INTO rankings(id, isbn, isbn13, title, 
                      image_url, publication_year, ratings_count, average_rating 
                      , author) VALUES'''
        
        qry_values = "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (book['goodreads_id'], book['isbn'], book['isbn13'], book['title'], book['image_url'], book['publication_year'], book['ratings_count'], book['average_rating'], book['author'])

        qry = qry_base + qry_values
        print qry
        print "++++++++++++++++++++"
        db.insert(qry)

    db.close_connection()
    
