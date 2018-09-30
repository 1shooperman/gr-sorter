# pylint: skip-file
from sorter.lib.data_handler import *
import sqlite3

from sorter.lib.defaults import Defaults

defaults = Defaults('FOO_KEY', 1, ['BAR-SHELF'])

CREATE_RANKINGS = '''CREATE TABLE rankings
            (id PRIMARY KEY, isbn UNIQUE, isbn13 UNIQUE, title, image_url, 
            publication_year INTEGER, ratings_count INTEGER, average_rating FLOAT,
            author, link, preference_adjustment FLOAT DEFAULT 0.0)'''

class fake_os(object):
    def __init__(self):
        self.called_remove = None
    
    def remove(self, file):
        self.called_remove = file

class fake_db(object):
    def __init__(self, foo):
        self.conn = foo

    def create_connection(self):
        pass

    def insertupdate(self, foo, bar):
        pass
    
    def close_connection(self):
        pass

    def query(self):
        pass

class wrapped_db(object):
    def __init__(self, database):
        self.database = database

    def create_connection(self):
        pass

    def insertupdate(self, query, vals):
        self.database.insertupdate(query, vals)
    
    def close_connection(self):
        pass

    def query(self):
        pass 

class fake_data_handler(object):
    def __init__(self):
        self.called_get_books_with_missing_data = False
        self.called_update_book = False
        self.called_get_by_isbn = False
        self.called_parse_isbn13_response = False
        self.called_get_by_id = False
        self.called_parse_id_response = False

    def get_books_with_missing_data(self, *args):
        self.called_get_books_with_missing_data = True
        return [[1],[2],[3],[4],[5]]

    def update_book(self, *args):
        self.called_update_book = True
        return None

    def get_by_isbn(self, *args):
        self.called_get_by_isbn = True

    def parse_isbn13_response(self, *args):
        self.called_parse_isbn13_response = True

    def get_by_id(self, *args):
        self.called_get_by_id = True

    def parse_id_response(self, *args):
        self.called_parse_id_response = True

class TestDataHandler(object):
    def test_store_data(self, monkeypatch):
        database = sqlite3.connect(':memory:')

        qry = CREATE_RANKINGS

        database.execute(qry)

        monkeypatch.setattr("sorter.lib.data_handler.DB", fake_db)
        monkeypatch.setattr("sorter.lib.data_handler.DB.create_connection", lambda foo: database)
        monkeypatch.setattr("sorter.lib.data_handler.DB.insertupdate", lambda self, foo, bar: database.execute(foo,bar))

        fake_data = [(1,2,3,4,5,6,7,8,9,10)]
        store_data(fake_data, "foo")

        fake_data_returned = database.execute("select * from rankings").fetchall()

        database.close()
        database = None

        assert [fake_data[0] + (0.0,)] == fake_data_returned

    def test_get_books(self, monkeypatch):
        database = sqlite3.connect(':memory:')

        qry = CREATE_RANKINGS

        database.execute(qry)

        monkeypatch.setattr("sorter.lib.data_handler.DB", fake_db)
        monkeypatch.setattr("sorter.lib.data_handler.DB.create_connection", lambda foo: database)
        monkeypatch.setattr("sorter.lib.data_handler.DB.query", lambda self, foo: database.execute(foo).fetchall())

        fake_book = (1,2,3,4,5,6,7,8,9,10,1.2)
        
        query = '''INSERT INTO rankings(id, isbn, isbn13, title,
                image_url, publication_year, ratings_count, average_rating, 
                author, link, preference_adjustment) VALUES(?,?,?,?,?,?,?,?,?,?,?)'''

        database.execute(query, fake_book)

        fake_data_returned = get_books("foo")

        database.close()
        database = None

        assert fake_data_returned == [fake_book]

    def test_dump_data(self, monkeypatch):
        faker = fake_os()
        monkeypatch.setattr("sorter.lib.data_handler.os.remove", lambda file: faker.remove(file))
        monkeypatch.setattr("sorter.lib.data_handler.os.path.isfile", lambda file: True)

        dump_data("fake.file")
        
        assert faker.called_remove == "fake.file"

    def test_get_books_with_missing_data(self, monkeypatch):
        database = sqlite3.connect(':memory:')

        qry = CREATE_RANKINGS

        database.execute(qry)

        monkeypatch.setattr("sorter.lib.data_handler.DB", fake_db)
        monkeypatch.setattr("sorter.lib.data_handler.DB.create_connection", lambda foo: database)
        monkeypatch.setattr("sorter.lib.data_handler.DB.query", lambda self, foo: database.execute(foo).fetchall())

        fake_books = [(1,2,3,4,5,6,7,8,9,10), 
                      (11,12,13,14,15,None,17,18,19,20),
                      (21,22,23,24,25,26,27,28,29,30),
                      (31,32,33,34,35,None,37,38,39,40)]
        
        query = '''INSERT INTO rankings(id, isbn, isbn13, title,
                image_url, publication_year, ratings_count, average_rating, 
                author, link) VALUES(?,?,?,?,?,?,?,?,?,?)'''

        for fake_book in fake_books:
            database.execute(query, fake_book)

        fake_data_returned = get_books_with_missing_data("foo")

        database.close()
        database = None

        assert fake_data_returned == [fake_books[1] + (0.0,), fake_books[3] + (0.0,)]

    def test_clean_data(self, monkeypatch):
        fdh = fake_data_handler()

        monkeypatch.setattr('sorter.lib.data_handler.os.path.abspath', lambda *args: "Foo")
        monkeypatch.setattr('sorter.lib.data_handler.os.path.isfile', lambda *args: True)
        monkeypatch.setattr('sorter.lib.data_handler.update_book', fdh.update_book)
        monkeypatch.setattr('sorter.lib.data_handler.get_books_with_missing_data', fdh.get_books_with_missing_data)

        clean_data('Bar', defaults)

        assert fdh.called_get_books_with_missing_data is True
        assert fdh.called_update_book is True

    def test_update_book_given_isbn(self, monkeypatch):
        fdh = fake_data_handler()

        monkeypatch.setattr('sorter.lib.data_handler.get_by_isbn', fdh.get_by_isbn)
        monkeypatch.setattr('sorter.lib.data_handler.parse_isbn13_response', lambda *args: (11,12,13,14,15,4242,17,18,19,20))
        monkeypatch.setattr('sorter.lib.data_handler.get_by_id', fdh.get_by_id)
        monkeypatch.setattr('sorter.lib.data_handler.parse_id_response', fdh.parse_id_response)

        from sorter.lib.db import DB
        database = DB(':memory:')
        database.create_connection()

        monkeypatch.setattr("sorter.lib.data_handler.DB", lambda *args: wrapped_db(database))

        qry = CREATE_RANKINGS

        database.execute(qry)

        fake_books = [( 1, 2, 3, 4, 5, 6, 7, 8, 9,10), 
                      (11,12,13,14,15,16,17,18,19,20),
                      (21,22,23,24,25,26,27,28,29,30),
                      (31,32,33,34,35,36,37,38,39,40)]
        
        query = '''INSERT INTO rankings(id, isbn, isbn13, title,
                image_url, publication_year, ratings_count, average_rating, 
                author, link) VALUES(?,?,?,?,?,?,?,?,?,?)'''

        for fake_book in fake_books:
            database.insertupdate(query, fake_book)

        update_book((11,12,13,14,15,16,17,18,19,20), 'foo', defaults)

        test_books = database.query('select * from rankings where id = 11')

        database.close_connection()
        database = None

        assert test_books[0][0] == 11
        assert test_books[0][1] == 12
        assert test_books[0][2] == 13
        assert test_books[0][3] == 14
        assert test_books[0][4] == 15
        assert test_books[0][5] == 4242
        assert test_books[0][6] == 17
        assert test_books[0][7] == 18
        assert test_books[0][8] == 19
        assert test_books[0][9] == 20

        assert fdh.called_get_by_isbn is True
        assert fdh.called_get_by_id is False
        assert fdh.called_parse_id_response is False

    def test_update_book_given_id(self, monkeypatch):
        fdh = fake_data_handler()

        monkeypatch.setattr('sorter.lib.data_handler.get_by_isbn', fdh.get_by_isbn)
        monkeypatch.setattr('sorter.lib.data_handler.parse_isbn13_response', fdh.parse_isbn13_response)
        monkeypatch.setattr('sorter.lib.data_handler.get_by_id', fdh.get_by_id)
        monkeypatch.setattr('sorter.lib.data_handler.parse_id_response', lambda *args: (1,999,9999,4,5,1942,7,8,9,10))

        from sorter.lib.db import DB
        database = DB(':memory:')
        database.create_connection()

        monkeypatch.setattr("sorter.lib.data_handler.DB", lambda *args: wrapped_db(database))

        qry = CREATE_RANKINGS

        database.execute(qry)

        fake_books = [( 1, 2, 3, 4, 5, 6, 7, 8, 9,10), 
                      (11,12,13,14,15,16,17,18,19,20),
                      (21,22,23,24,25,26,27,28,29,30),
                      (31,32,33,34,35,36,37,38,39,40)]
        
        query = '''INSERT INTO rankings(id, isbn, isbn13, title,
                image_url, publication_year, ratings_count, average_rating, 
                author, link) VALUES(?,?,?,?,?,?,?,?,?,?)'''

        for fake_book in fake_books:
            database.insertupdate(query, fake_book)

        update_book((1,None,None,4,5,6,7,8,9,10), 'foo', defaults)

        test_books = database.query('select * from rankings where id = 1')

        database.close_connection()
        database = None

        assert test_books[0][0] == 1
        assert test_books[0][1] == 999
        assert test_books[0][2] == 9999
        assert test_books[0][3] == 4
        assert test_books[0][4] == 5
        assert test_books[0][5] == 1942
        assert test_books[0][6] == 7
        assert test_books[0][7] == 8
        assert test_books[0][8] == 9
        assert test_books[0][9] == 10

        assert fdh.called_get_by_isbn is False
        assert fdh.called_parse_isbn13_response is False
        assert fdh.called_get_by_id is True

    def test_manually_update_book_all_fields(self, monkeypatch):
        from sorter.lib.db import DB
        database = DB(':memory:')
        database.create_connection()

        monkeypatch.setattr("sorter.lib.data_handler.DB", lambda *args: wrapped_db(database))
        
        qry = CREATE_RANKINGS

        database.execute(qry)

        fake_books = [( 1, 2, 3, 4, 5, 6, 7, 8, 9,10), 
                      (11,12,13,14,15,16,17,18,19,20),
                      (21,22,23,24,25,26,27,28,29,30),
                      (31,32,33,34,35,36,37,38,39,40)]
        
        query = '''INSERT INTO rankings(id, isbn, isbn13, title,
                image_url, publication_year, ratings_count, average_rating, 
                author, link) VALUES(?,?,?,?,?,?,?,?,?,?)'''

        for fake_book in fake_books:
            database.insertupdate(query, fake_book)

        to_update = [
            {
                'book_id': 1,
                'attr': 'isbn',
                'value': 'foo'
            },
            {
                'book_id': 1,
                'attr': 'isbn13',
                'value': 'bar'
            },
            {
                'book_id': 1,
                'attr': 'title',
                'value': 'baz'
            },
            {
                'book_id': 1,
                'attr': 'image_url',
                'value': 'bang'
            },
                        {
                'book_id': 1,
                'attr': 'publication_year',
                'value': 1980
            },
            {
                'book_id': 1,
                'attr': 'ratings_count',
                'value': 56
            },
            {
                'book_id': 1,
                'attr': 'average_rating',
                'value': 57
            },
            {
                'book_id': 1,
                'attr': 'author',
                'value': 'ipsum'
            },
                        {
                'book_id': 1,
                'attr': 'link',
                'value': 'dolet'
            },
            {
                'book_id': 1,
                'attr': 'preference_adjustment',
                'value': 12
            },
            {
                'book_id': 11,
                'attr': 'ISBN13',
                'value': 'brown'
            }
        ]    

        manually_update_books(to_update, 'foo')

        test_books = database.query('select * from rankings where id in (1,11,21,31)')

        database.close_connection()
        database = None

        assert test_books[0] == (1, 'foo', 'bar', 'baz', 'bang', 1980, 56, 57, 'ipsum', 'dolet', 12.0)

        assert test_books[1] == (11,12,'brown',14,15,16,17,18,19,20,0.0)

        assert test_books[2] == (21,22,23,24,25,26,27,28,29,30,0.0)

        assert test_books[3] == (31,32,33,34,35,36,37,38,39,40,0.0)

    def test_manually_update_book_id_noupdate(self, monkeypatch):
        from sorter.lib.db import DB
        database = DB(':memory:')
        database.create_connection()

        monkeypatch.setattr("sorter.lib.data_handler.DB", lambda *args: wrapped_db(database))
        
        qry = CREATE_RANKINGS

        database.execute(qry)

        fake_books = [( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)]
        
        query = '''INSERT INTO rankings(id, isbn, isbn13, title,
                image_url, publication_year, ratings_count, average_rating, 
                author, link) VALUES(?,?,?,?,?,?,?,?,?,?)'''

        for fake_book in fake_books:
            database.insertupdate(query, fake_book)

        to_update = [
            {
                'book_id': 1,
                'attr': 'id',
                'value': 'foo'
            }
        ]    

        manually_update_books(to_update, 'foo')

        test_books = database.query('select * from rankings where id = 1')

        database.close_connection()
        database = None

        assert test_books[0] == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10,0.0)
