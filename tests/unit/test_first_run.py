# pylint: skip-file
from sorter.lib.first_run import init

class fake_db(object):
    def __init__(self):
        self.query = ""

    def create_connection(self):
        pass

    def execute(self, foo):
        self.query = foo
    
    def close_connection(self):
        pass

    def get_qry(self):
        return self.query

class TestFirstRun(object):
    def test_init(self, monkeypatch):
        DB = fake_db()
        monkeypatch.setattr("sorter.lib.first_run.DB", lambda x: DB)

        init("")

        foo = DB.get_qry()

        assert foo == '''CREATE TABLE rankings
             (id PRIMARY KEY, isbn UNIQUE, isbn13 UNIQUE, title, image_url, 
              publication_year INTEGER, ratings_count INTEGER, average_rating FLOAT,
              author, link)'''
