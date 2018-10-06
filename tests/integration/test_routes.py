# pylint: skip-file
from paste.fixture import TestApp as app_fixture # pytest will try to collect "Test*"
import sqlite3
from sorter.__main__ import APP as app
from tests.utils.get_element import get_file_as_string

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
            author, link, preference_adjustment FLOAT DEFAULT 0.0)'''

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

class FakeDefaults(object):
    def __init__(*args):
        pass

    def get_list_url(self, *args):
        return "faker.gtld"

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
        monkeypatch.setattr("sorter.__main__.page_vars", lambda *args: ('foo', 6, 5, 4))
        monkeypatch.setattr("sorter.__main__.read_url", fake_read_url)
        monkeypatch.setattr("sorter.__main__.page_loop", lambda *args: True)
        monkeypatch.setattr("sorter.__main__.clean_data", lambda *args: None)
        monkeypatch.setattr("sorter.__main__.Defaults", FakeDefaults)

        resp = test_app.post("/import", [('data_file', 'fake.faker')])

        assert resp.status is 200
        assert "200 OK" in resp

    def test_import_new(self, monkeypatch):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        monkeypatch.setattr("sorter.__main__.page_vars", lambda *args: ('foo', 6, 5, 4))
        monkeypatch.setattr("sorter.__main__.read_url", fake_read_url)
        monkeypatch.setattr("sorter.__main__.page_loop", lambda *args: True)
        monkeypatch.setattr("sorter.__main__.clean_data", lambda *args: None)
        monkeypatch.setattr("sorter.__main__.Defaults", FakeDefaults)

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

    def test_admin(self):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        resp = test_app.get("/admin")

        assert resp.status is 200

    def test_admin_advanced_get(self, monkeypatch):
        monkeypatch.setattr("sorter.__main__.DB_NAME", "")
        books = bootstrap_data("")
        monkeypatch.setattr("sorter.__main__.get_books", lambda foo: books)
        monkeypatch.setattr("sorter.__main__.rank", lambda foo: books)
        monkeypatch.setattr("sorter.__main__.os.path.isfile", lambda foo: True)

        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        resp = test_app.get("/admin/advanced")

        assert resp.status is 200
        assert "<tr>" in resp

    def test_admin_advanced_post(self, monkeypatch):
        monkeypatch.setattr("sorter.__main__.DB_NAME", "")
        books = bootstrap_data("")
        monkeypatch.setattr("sorter.__main__.get_books", lambda foo: books)
        monkeypatch.setattr("sorter.__main__.rank", lambda foo: books)
        monkeypatch.setattr("sorter.__main__.os.path.isfile", lambda foo: True)
        monkeypatch.setattr("sorter.__main__.from_post", lambda *args: ('foo', None))
        monkeypatch.setattr("sorter.__main__.manually_update_books", lambda *args: ('foo', None))

        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        resp = test_app.post("/admin/advanced", "some_query_string")

        assert resp.status is 200
        assert "<tr>" in resp

    def test_admin_getshelves_post(self, monkeypatch):
        monkeypatch.setattr("sorter.__main__.DB_NAME", "")
        monkeypatch.setattr("sorter.__main__.page_vars", lambda *args: (1,2,3,4))
        monkeypatch.setattr("sorter.__main__.read_url", lambda *args: get_file_as_string('tests/fixtures/shelf_list.xml'))

        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        resp = test_app.post("/admin/getshelves", "some_query_string")

        assert resp.status is 200
        assert '["foo-shelf", "bar-shelf", "baz-shelf"]' == resp.body

    def test_clean(self, monkeypatch):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        monkeypatch.setattr("sorter.__main__.clean_data", lambda *args: None)
        monkeypatch.setattr("sorter.__main__.Defaults", FakeDefaults)
        monkeypatch.setattr("sorter.__main__.query_vars", lambda *args: ('foo', None))

        resp = test_app.get("/clean")

        assert resp.status is 200
        assert "200 OK" in resp
