''' data_handler.py '''
import os
from sorter.lib.db import DB
from sorter.lib.book_utils import get_by_id, get_by_isbn
from sorter.lib.parse_xml import parse_isbn13_response, parse_id_response

def store_data(books, db_file):
    '''
    Store the book data in the provided database
    '''
    database = DB(db_file)
    database.create_connection()

    query = '''INSERT INTO rankings(id, isbn, isbn13, title,
        image_url, publication_year, ratings_count, average_rating, 
        author, link) VALUES(?,?,?,?,?,?,?,?,?,?)'''

    for book in books:
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

def get_books_with_missing_data(db_file):
    '''
    Get the previously stored books data
    '''
    database = DB(db_file)

    database.create_connection()

    books = database.query('select * from rankings where publication_year is null')

    database.close_connection()

    return books

def dump_data(db_file):
    '''
    Delete the provided data file
    '''
    if os.path.isfile(db_file):
        os.remove(db_file)

def clean_data(db_name, defaults):
    '''
    Plug in missing data:
        book[0] = ID
        book[1] = ISBN
        book[2] = ISBN13
        book[3] = title
        book[4] = image url
        book[5] = pub year
        book[6] = Total Ratings
        book[7] = avg rating
        book[8] = author
        book[9] = link
    '''
    db_file = os.path.abspath(db_name)

    if os.path.isfile(db_file):
        books = get_books_with_missing_data(db_file)
        map(update_book, books, ([db_file] * len(books)), ([defaults] * len(books)))

def update_book(book, db_file, defaults):
    '''
    Add the missing book data
    '''
    qry = None
    if book[2] is not None:
        xml_response = get_by_isbn(book[2], defaults)
        new_book = parse_isbn13_response(xml_response)
        qry = 'UPDATE rankings set publication_year = ? where isbn13 = ?'
        vals = [new_book[5], book[2]]

    elif book[0] is not None:
        xml_response = get_by_id(book[0], defaults)
        new_book = parse_id_response(xml_response)
        qry = 'UPDATE rankings set publication_year = ?, isbn = ?, isbn13 = ? where id = ?'
        vals = [new_book[5], new_book[1], new_book[2], book[0]]

    if qry is not None:
        database = DB(db_file)

        database.create_connection()

        database.insertupdate(qry, vals)

        database.close_connection()
