# pylint: skip-file
from paste.fixture import TestApp as app_fixture # pytest will try to collect "Test*" 
import pytest
import mock
from sorter.__main__ import APP as app 

import os

def fake_parse_qs(my_file):
    return {
        'data_file': ['http://some.fake.gtld/sample.xml']
    }

def fake_read_url(url_string):
    with open('tests/fixtures/sample.xml', 'r') as myfile:
        data = myfile.read()

    return data

def clean_test_db(db_file):
    if os.path.isfile(db_file) is True:
        os.remove(db_file)

def fake_asset_handler(asset_path):
    return (asset_path, 'bar')

class TestRoutes(object):  

    def test_index(self):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        resp = test_app.get("/")

        assert resp.status is 200
        assert "Book ID" in resp

    def test_import(self, monkeypatch):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        monkeypatch.setattr("sorter.__main__.parse_qs", fake_parse_qs)
        monkeypatch.setattr("sorter.__main__.read_url", fake_read_url)
        
        DB_FILE = os.path.abspath("tests/test.db")
        clean_test_db(DB_FILE)
        from sorter.lib.first_run import init
        monkeypatch.setattr("sorter.__main__.DB_FILE", DB_FILE)
        
        init(DB_FILE)
        
        resp = test_app.post("/import", [('data_file', 'fake.txt')])
        clean_test_db(DB_FILE)

        assert resp.status is 200
        assert "200 OK" in resp

    def test_asset_js(self, monkeypatch):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        monkeypatch.setattr("sorter.__main__.asset", fake_asset_handler)
        resp = test_app.get("/assets/js/foo.js")

        assert resp.status is 200
        assert "assets/js/foo.js" in resp

    def test_assset_css(self, monkeypatch):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        monkeypatch.setattr("sorter.__main__.asset", fake_asset_handler)
        resp = test_app.get("/assets/css/foo.css")

        assert resp.status is 200
        assert "assets/css/foo.css" in resp
    
    def test_asset_default(self, monkeypatch):
        middleware = []
        test_app = app_fixture(app.wsgifunc(*middleware))
        monkeypatch.setattr("sorter.__main__.asset", fake_asset_handler)
        resp = test_app.get("/assets/foo/bar.baz")

        assert resp.status is 200
        assert "assets/foo/bar.baz" in resp
