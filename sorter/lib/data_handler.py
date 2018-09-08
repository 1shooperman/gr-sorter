''' store_data.py '''
import os
from sorter.lib.db import DB

def store_data(books, db_file):
    '''
    Store the book data in the provided database
    '''
    database = DB(db_file)
    database.create_connection()

    for book in books:
        query = '''INSERT INTO rankings(id, isbn, isbn13, title,
                image_url, publication_year, ratings_count, average_rating, 
                author) VALUES(?,?,?,?,?,?,?,?,?)'''

        database.insertupdate(query, book)

    database.close_connection()

def get_books(db_file):
    '''
    Get the previously stored books data
    '''
    database = DB(db_file)

    database.create_connection()

    books = database.query('select * from rankings')

    database.close_connection()

    return books

def dump_data(db_file):
    '''
    Delete the provided data file
    '''
    if os.path.isfile(db_file):
        os.remove(db_file)
