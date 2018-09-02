# pylint: skip-file
from sorter.lib.request_data import read_url

class fake_urllib(object):
    def __init__(self):
        pass

    def urlopen(self):
        pass

    def read(self):
        return "fake body"

    def close(self):
        pass

class fake_logger(object):
    def info(self, bar, baz):
        pass

class TestRequestData(object):

    def test_read_url(self, monkeypatch):
        monkeypatch.setattr("urllib2.urlopen", lambda foo: fake_urllib())
        monkeypatch.setattr("sorter.lib.request_data.LOGGER", fake_logger())

        body = read_url("fakeurl")

        assert body == "fake body"


        
