# pylint: skip-file
from sorter.lib.book_utils import get_by_id, get_by_isbn
from tests.utils.get_element import get_element

class TestBookUtils(object):
    def test_get_by_id(self, monkeypatch):
        id = get_element('tests/fixtures/book_by_id.xml', 'book/id')

        monkeypatch.setattr('sorter.lib.book_utils.read_url', lambda *args: id)

        foo = get_by_id(1234)

        assert id == False # 453444

    def test_get_by_isbn(self, monkeypatch):
        id = get_element('tests/fixtures/book_by_isbn.xml', 'search/results/work/id')

        monkeypatch.setattr('sorter.lib.book_utils.read_url', lambda *args: id)

        foo = get_by_isbn(54321)

        assert id == False  # 1417331
