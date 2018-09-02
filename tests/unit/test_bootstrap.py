# pylint: skip-file
from sorter.lib.bootstrap import bootstrap

class fake_logger(object):
    def info(self, msg):
        pass

class TestBootstrap(object):
    def test_bootstrap(self, monkeypatch):
        monkeypatch.setattr("sorter.lib.bootstrap.init", lambda foo: None)

        foo = bootstrap('fake.db.file', fake_logger())

        assert foo == "/Users/bshoop/workspace/python/readingSorter/fake.db.file"
