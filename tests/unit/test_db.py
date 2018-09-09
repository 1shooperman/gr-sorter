# pylint: skip-file
from sorter.lib.db import DB
from sqlite3 import IntegrityError

class fake_sqlite3(object):
    def connect(self, file):
        return file

class fake_failed_connection(object):
    def __init__(self):
        self.called_close = False
        self.called_commit = False
        self.called_execute = False
        self.fake_failed_cursor = None
        self.conn = None

    def close(self):
        self.called_close = True
        called_close = True

    def commit(self):
        self.called_commit = True

    def execute(self, foo):
        self.called_execute = True
        return fake_failed_cursor()

    def cursor(self):
        self.fake_failed_cursor = fake_failed_cursor()
        return self.fake_failed_cursor

class fake_failed_cursor(object):
    def __init__(self):
        self.called_execute = False

    def execute(self, foo, bar):
        raise IntegrityError('123456')

    def fetchall(self):
        return True   

class fake_connection(object):
    def __init__(self):
        self.called_close = False
        self.called_commit = False
        self.called_execute = False
        self.fake_cursor = None
        self.conn = None

    def close(self):
        self.called_close = True
        called_close = True

    def commit(self):
        self.called_commit = True

    def execute(self, foo):
        self.called_execute = True
        return fake_cursor()

    def cursor(self):
        self.fake_cursor = fake_cursor()
        return self.fake_cursor

class fake_connection_2(object):
    def __init__(self):
        self.called_close = False
        self.called_commit = False
        self.called_execute = False
        self.fake_cursor = None
        self.conn = None

    def close(self):
        self.called_close = True
        called_close = True

    def commit(self):
        self.called_commit = True

    def execute(self, foo):
        self.called_execute = True
        return fake_cursor()

    def cursor(self):
        self.fake_cursor = fake_cursor_2()
        return self.fake_cursor

class fake_cursor(object):
    def __init__(self):
        self.called_execute = False

    def execute(self, foo, bar):
        self.called_execute = True

    def fetchall(self):
        return True

class fake_cursor_2(object):
    def __init__(self):
        self.called_execute = False

    def execute(self, foo):
        self.called_execute = True

    def fetchall(self):
        return True

class TestDb(object):
    def test_init(self):
        foo = DB("bar")

        assert foo.conn is None
        assert foo.db_file == "bar"

    def test_create_connection(self, monkeypatch):
        foo = DB("bar")
        monkeypatch.setattr("sorter.lib.db.sqlite3", fake_sqlite3())

        bar = foo.create_connection()

        assert bar == "bar"

    def test_close_connection(self):
        foo = DB("bar")
        foo.conn = fake_connection()

        foo.close_connection()

        assert foo.conn is None

    def test_insertupdate(self):
        foo = DB("bar")
        foo.conn = fake_connection()

        foo.insertupdate("some query", ["val1", "val2"])

        assert foo.conn.called_close == False
        assert foo.conn.called_commit == True
        assert foo.conn.fake_cursor.called_execute == True

    def test_insertupdate_catches_exception(self):
        foo = DB("bar")
        foo.conn = fake_failed_connection()

        bar = foo.insertupdate("some query", ["val1", "val2"])
        assert bar == None

    def test_query(self):
        foo = DB("bar")
        foo.conn = fake_connection()

        bar = foo.query("some query")

        assert bar == True
        assert foo.conn.called_execute == True


    def test_execute(self):
        foo = DB("bar")
        foo.conn = fake_connection_2()

        foo.execute("fake query")

        assert foo.conn.called_close == False
        assert foo.conn.called_commit == True
        assert foo.conn.called_execute == False
        assert foo.conn.fake_cursor.called_execute == True
