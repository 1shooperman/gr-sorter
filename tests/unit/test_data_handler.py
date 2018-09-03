# pylint: skip-file
from sorter.lib.data_handler import store_data, get_books, dump_data
import sqlite3

class fake_os(object):
    def __init__(self):
        self.called_remove = None
    
    def remove(self, file):
        self.called_remove = file

class fake_db(object):
    def __init__(self, foo):
        pass

    def create_connection(self):
        pass

    def insertupdate(self, foo, bar):
        pass
    
    def close_connection(self):
        pass

    def query(self):
        pass

class TestDataHandler(object):
    def test_store_data(self, monkeypatch):
        database = sqlite3.connect(':memory:')

        qry = '''CREATE TABLE rankings
            (id PRIMARY KEY, isbn UNIQUE, isbn13 UNIQUE, title, image_url, 
            publication_year INTEGER, ratings_count INTEGER, average_rating FLOAT,
            author)'''

        database.execute(qry)

        monkeypatch.setattr("sorter.lib.data_handler.DB", fake_db)
        monkeypatch.setattr("sorter.lib.data_handler.DB.create_connection", lambda foo: database)
        monkeypatch.setattr("sorter.lib.data_handler.DB.insertupdate", lambda self, foo, bar: database.execute(foo,bar))

        fake_data = [(1,2,3,4,5,6,7,8,9)]
        store_data(fake_data, "foo")

        fake_data_returned = database.execute("select * from rankings").fetchall()

        database.close()
        database = None

        assert fake_data == fake_data_returned

    def test_get_books(self, monkeypatch):
        database = sqlite3.connect(':memory:')

        qry = '''CREATE TABLE rankings
            (id PRIMARY KEY, isbn UNIQUE, isbn13 UNIQUE, title, image_url, 
            publication_year INTEGER, ratings_count INTEGER, average_rating FLOAT,
            author)'''

        database.execute(qry)

        monkeypatch.setattr("sorter.lib.data_handler.DB", fake_db)
        monkeypatch.setattr("sorter.lib.data_handler.DB.create_connection", lambda foo: database)
        monkeypatch.setattr("sorter.lib.data_handler.DB.query", lambda self, foo: database.execute(foo).fetchall())

        fake_book = (1,2,3,4,5,6,7,8,9)
        
        query = '''INSERT INTO rankings(id, isbn, isbn13, title,
                image_url, publication_year, ratings_count, average_rating, 
                author) VALUES(?,?,?,?,?,?,?,?,?)'''

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
