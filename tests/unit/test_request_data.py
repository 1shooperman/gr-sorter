# pylint: skip-file
from sorter.lib.request_data import read_url
from urllib2 import HTTPError

class fake_urllib(object):
    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    def urlopen(self, uri):
        if self.should_fail == True:
            raise HTTPError('FAKER.GTLD', 404, 'Four Oh Four', None, None)

    def read(self):
        return "fake body"

    def close(self):
        pass

class fake_logger(object):
    def __init__(self):
        self.msg = None

    def info(self, msg, *args):
        pass

    def warn(self, msg, *args):
        self.msg = msg.reason

class TestRequestData(object):

    def test_read_url(self, monkeypatch):
        monkeypatch.setattr("urllib2.urlopen", lambda foo: fake_urllib())
        monkeypatch.setattr("sorter.lib.request_data.LOGGER", fake_logger())

        body = read_url("fakeurl")

        assert body == "fake body"

    def test_read_url_404(self, monkeypatch):
        faker = fake_logger()
        monkeypatch.setattr("sorter.lib.request_data.urllib2", fake_urllib(True))
        monkeypatch.setattr("sorter.lib.request_data.LOGGER", faker)

        body = read_url("fakeurl")
        
        assert body == None
        assert faker.msg == 'Four Oh Four'
