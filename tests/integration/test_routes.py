# pylint: skip-file
from paste.fixture import TestApp as app_fixture # pytest will try to collect "Test*"
import sqlite3
from sorter.__main__ import APP as app

def fake_parse_qs(my_file):
    return {
        'data_file': ['http://some.fake.gtld/sample.xml']
    }

def fake_parse_qs_newdata(my_file):
    return {
        'data_file': ['http://some.fake.gtld/sample.xml'],
        'new': [1]
    }

def fake_read_url(url_string):
    with open('tests/fixtures/sample.xml', 'r') as myfile:
        data = myfile.read()

    myfile.close()
    
    return data

def fake_asset_handler(asset_path):
    return (asset_path, 'bar')

def bootstrap_data(foo):
    database = sqlite3.connect(':memory:')

    qry = '''CREATE TABLE rankings
            (id PRIMARY KEY, isbn UNIQUE, isbn13 UNIQUE, title, image_url, 
            publication_year INTEGER, ratings_count INTEGER, average_rating FLOAT,
            author, link)'''

    database.execute(qry)

    fake_xml = fake_read_url("")
    from sorter.lib.parse_xml import parse
    fake_data = parse(fake_xml)

    for book in fake_data:
        query = '''INSERT INTO rankings(id, isbn, isbn13, title,
                image_url, publication_year, ratings_count, average_rating, 
                author, link) VALUES(?,?,?,?,?,?,?,?,?,?)'''

        cur = database.cursor()
        cur.execute(query, book)
        database.commit()

    books = database.execute("select * from rankings").fetchall()

    database.close()
    database = None

    return books

class TestRoutes(object):

    def test_index(self, monkeypatch):
        monkeypatch.setattr("sorter.__main__.DB_NAME", "")
        books = bootstrap_data("")
        monkeypatch.setattr("sorter.__main__.get_books", lambda foo: books)
        monkeypatch.setattr("sorter.__main__.rank", lambda foo: books)
        monkeypatch.setattr("sorter.__main__.os.path.isfile", lambda foo: True)

        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        resp = test_app.get("/")

        assert resp.status is 200
        assert "Book ID" in resp

    def test_index_nodata(self, monkeypatch):
        monkeypatch.setattr("sorter.__main__.DB_NAME", "")
        books = bootstrap_data("")
        monkeypatch.setattr("sorter.__main__.get_books", lambda foo: books)
        monkeypatch.setattr("sorter.__main__.rank", lambda foo: books)

        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        resp = test_app.get("/")

        assert resp.status is 200
        assert "<body>" in resp

    def test_import(self, monkeypatch):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        monkeypatch.setattr("sorter.__main__.parse_qs", fake_parse_qs)
        monkeypatch.setattr("sorter.__main__.read_url", fake_read_url)
        monkeypatch.setattr("sorter.__main__.page_loop", lambda *args: True)
        monkeypatch.setattr("sorter.__main__.verify_data", lambda *args: None)

        resp = test_app.post("/import", [('data_file', 'fake.faker')])

        assert resp.status is 200
        assert "200 OK" in resp

    def test_import_new(self, monkeypatch):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        monkeypatch.setattr("sorter.__main__.parse_qs", fake_parse_qs_newdata)
        monkeypatch.setattr("sorter.__main__.read_url", fake_read_url)
        monkeypatch.setattr("sorter.__main__.page_loop", lambda *args: True)
        monkeypatch.setattr("sorter.__main__.verify_data", lambda *args: None)

        resp = test_app.post("/import", [('data_file', 'fake.faker')])

        assert resp.status is 200
        assert "200 OK" in resp

    def test_asset(self, monkeypatch):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        monkeypatch.setattr("sorter.__main__.asset", fake_asset_handler)
        resp = test_app.get("/assets/js/foo.js")

        assert resp.status is 200
        assert "assets/js/foo.js" in resp
