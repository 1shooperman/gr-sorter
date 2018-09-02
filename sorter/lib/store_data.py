''' store_data.py '''
from sorter.lib.db import DB

def store_data(books, db_file):
    ''' store the book data in the provided database '''
    database = DB(db_file)

    database.create_connection()

    for book in books:
        query = '''INSERT INTO rankings(id, isbn, isbn13, title,
                image_url, publication_year, ratings_count, average_rating, 
                author) VALUES(?,?,?,?,?,?,?,?,?)'''

        database.insertupdate(query, book)

    database.close_connection()
