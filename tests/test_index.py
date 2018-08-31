from sorter.__main__ import APP

class TestIndex(object):
    def test_status(self):
        resp = APP.request("/")
        assert resp.status == "200 OK"

    def test_body(self):
        resp = APP.request("/")
        assert "<body>" in resp.data
