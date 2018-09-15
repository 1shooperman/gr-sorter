# pylint: skip-file
import xml.etree.ElementTree as ElementTree
from sorter.lib.book_utils import get_by_id, get_by_isbn
from tests.utils.get_element import get_element, get_file_as_string
from sorter.lib.defaults import Defaults

defaults = Defaults('FOO_KEY', 1, ['BAR-SHELF'])

class TestBookUtils(object):
    def test_get_by_id(self, monkeypatch):
        id = get_element('tests/fixtures/book_by_id.xml', 'book/id')

        monkeypatch.setattr('sorter.lib.book_utils.read_url', lambda *args: get_file_as_string('tests/fixtures/book_by_id.xml'))

        foo = get_by_id(1234, defaults)

        root = ElementTree.fromstring(foo)

        _id = root.find('book/id').text

        assert id == _id

    def test_get_by_isbn(self, monkeypatch):
        id = get_element('tests/fixtures/book_by_isbn.xml', 'search/results/work/id')

        monkeypatch.setattr('sorter.lib.book_utils.read_url', lambda *args: get_file_as_string('tests/fixtures/book_by_isbn.xml'))

        foo = get_by_isbn(54321, defaults)

        root = ElementTree.fromstring(foo)

        _id = root.find('search/results/work/id').text

        assert id == _id
