# pylint: skip-file
import tempfile
import os
from urlparse import parse_qs, urlsplit
from sorter.lib.defaults import get_book_url, get_key, get_search_url, is_test


class TestDefaults(object):
    def test_get_key(self):
        foo = tempfile.NamedTemporaryFile()
        foo.write('FOO_KEY')
        foo.flush()

        bar = get_key(foo.name)

        foo.close()
        
        assert bar == 'FOO_KEY'

    def test_get_book_url(self):
        api_url = get_book_url(12345, 'http://FAKE.GLTD/FAKER?id=%s&key=%s')
        _, _, path, query, _ = urlsplit(api_url)
        params = parse_qs(query)

        assert params['id'][0] == '12345'
        assert params['key'][0] == 'None'

    def test_get_search_url(self):
        api_url = get_search_url(54321, 'http://FAKE.GLTD/FAKER?isbn=%s&key=%s')
        _, _, path, query, _ = urlsplit(api_url)
        params = parse_qs(query)

        assert params['isbn'][0] == '54321'
        assert params['key'][0] == 'None'

    def test_is_test(self, monkeypatch):
        monkeypatch.setattr('os.environ', {'WEBPY_END': 'foo'})

        bar = is_test()

        assert bar is False
