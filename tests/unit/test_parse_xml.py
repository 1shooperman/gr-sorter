# pylint: skip-file
from sorter.lib.parse_xml import parse, get_book_data
import pytest
import os

class fake_generator(object):
    def find(self, foo):
        return foo_object()

class foo_object(object):
    text = 10

class TestParseXml(object):
    def test_parse(self):
        xml_File = os.path.abspath('tests/fixtures/sample.1.xml')
        with open(xml_File, 'r') as myfile:
            data = myfile.read()

        foo = parse(data)

        assert foo == [
            (2503817653, 
            '1562828991', 
            '9781562828998', 
            "Disney's Art of Animation #1", 
            'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png', 
            '1992',
            622, 
            '4.29', 
            'Bob Thomas')
        ]

    def test_parse_exception(self):
        with pytest.raises(TypeError):
            parse(None)

    def test_get_book_data(self):
        foo = get_book_data(fake_generator())

        assert foo == (10,10,10,10,10,10,10,10,10)
