from sorter.index import app

class TestIndex(object):
    def test_status(self):
        resp = app.request("/")
        assert resp.status == "200 OK"

    def test_body(self):
        resp = app.request("/")
        assert "<body>" in resp.data
