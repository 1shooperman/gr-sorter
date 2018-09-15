# pylint: skip-file
import tempfile
import os
from urlparse import parse_qs, urlsplit
from sorter.lib.defaults import Defaults

class TestDefaults(object):
    def test_get_book_url(self):
        defaults = Defaults('http://FAKE.GLTD')

        api_url = defaults.get_book_url(12345, 'http://FAKE.GLTD/FAKER?id=%s&key=%s')
        _, _, path, query, _ = urlsplit(api_url)
        params = parse_qs(query)

        assert params['id'][0] == '12345'
        assert params['key'][0] == 'None'

    def test_get_search_url(self):
        defaults = Defaults('http://FAKE.GLTD')

        api_url = defaults.get_search_url(54321, 'http://FAKE.GLTD/FAKER?isbn=%s&key=%s')
        _, _, path, query, _ = urlsplit(api_url)
        params = parse_qs(query)

        assert params['isbn'][0] == '54321'
        assert params['key'][0] == 'None'

    def test_get_book_url_nouri(self):
        defaults = Defaults('http://FAKE.GLTD')

        api_url = defaults.get_book_url(12345)
        _, _, path, query, _ = urlsplit(api_url)

        assert path == "/book/show/12345.xml"
        assert query == "key=None"

    def test_get_search_url_nouri(self):
        defaults = Defaults('http://FAKE.GLTD')

        api_url = defaults.get_search_url(54321)
        _, _, path, query, _ = urlsplit(api_url)

        assert path == "/search"
        assert query == "q=54321&format=xml&key=None"

    def test_is_test(self, monkeypatch):
        defaults = Defaults('http://FAKE.GLTD', 'FOO_KEY')

        monkeypatch.setattr('os.environ', {'WEBPY_END': 'foo'})

        bar = Defaults.is_test()

        assert bar is False

    def test_get_shelf_url(self):
        defaults = Defaults('http://FAKE.GLTD')
        api_url = defaults.get_shelf_url(98765, ['foo-shelf'], 9, 'http://FAKE.GLTD/FAKER?user_id=%s&key=%s&shelf=%s&per_page=%s')
        _, _, path, query, _ = urlsplit(api_url)
        params = parse_qs(query)

        assert params['user_id'][0] == '98765'
        assert params['key'][0] == 'None'
        assert params['shelf'][0] == 'foo-shelf'
        assert params['per_page'][0] == '9'

    def test_getset_key(self):
        defaults = Defaults('FAKER.GTLD', 'FOO_KEY')

        assert defaults.get_key() == 'FOO_KEY'

