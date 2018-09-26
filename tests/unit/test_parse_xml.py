# pylint: skip-file
from sorter.lib.parse_xml import parse, get_book_data, get_total_pages, parse_id_response, parse_isbn13_response
from tests.utils.get_element import get_file_as_string
import pytest
import os

class fake_generator(object):
    def find(self, foo):
        return foo_object(10)

class foo_object(object):
    def __init__(self, retval):
        self.text = retval
    
class fake_generator2(object):
    def find(self, foo):
        if foo == 'book/published':
            return None
        elif foo == 'book/publication_year':
            return foo_object(13)
        else:
            return foo_object(10)

class TestParseXml(object):
    def test_parse(self):
        xml_File = os.path.abspath('tests/fixtures/sample.1.xml')
        with open(xml_File, 'r') as myfile:
            data = myfile.read()

        myfile.close()
        
        foo = parse(data)

        assert foo == [
            (453444, 
            '1562828991', 
            '9781562828998', 
            "Disney's Art of Animation #1", 
            'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png', 
            '1992',
            622, 
            '4.29', 
            'Bob Thomas',
            'https://www.goodreads.com/book/show/453444.Disney_s_Art_of_Animation_1')
        ]

    def test_parse_exception(self):
        with pytest.raises(TypeError):
            parse(None)

    def test_get_book_data(self):
        foo = get_book_data(fake_generator())

        assert foo == (10,10,10,10,10,10,10,10,10,10)

    def test_get_book_data_none_pubyear(self):
        foo = get_book_data(fake_generator2())

        assert foo == (10,10,10,10,10,13,10,10,10,10)

    def test_get_total_pages(self):
        xml_string = '<foo><reviews start="1" end="20" total="400"></reviews></foo>'
        pages, current_page = get_total_pages(xml_string)

        assert pages == 20
        assert current_page == 1

    def test_get_total_pages_page5(self):
        xml_string = '<foo><reviews start="81" end="100" total="400"></reviews></foo>'
        pages, current_page = get_total_pages(xml_string)

        assert pages == 20
        assert current_page == 5

    def test_get_total_pages_raises_exception_type(self):
        with pytest.raises(TypeError):
            get_total_pages(None)

    def test_get_total_pages_raises_exception_zerodiv(self):
        with pytest.raises(ZeroDivisionError):
            xml_string = '<foo><reviews start="0" end="0" total="0"></reviews></foo>'
            get_total_pages(xml_string)

    def test_parse_isbn13_response(self):
        xml_string = get_file_as_string('tests/fixtures/book_by_isbn.xml')
        foo = parse_isbn13_response(xml_string)

        assert foo == (1417331, None, None, 'My Book Title', 
                        'http://some.fake.gltd/fake.png', '1975', '457', 
                        '4.13', 'Fake Author', None)

    def test_parse_isbn13_response_excepts(self):
        with pytest.raises(TypeError):
            parse_isbn13_response(None)

    def test_parse_id_response(id):
        xml_string = get_file_as_string('tests/fixtures/book_by_id.xml')
        foo = parse_id_response(xml_string)

        assert foo == (453444, '1562828991', '9781562828998', "Disney's Art of Animation #1", 
                        'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png', '1992',
                        '622', '4.29', 'Bob Thomas', 'https://www.goodreads.com/book/show/453444.Disney_s_Art_of_Animation_1')

    def test_parse_id_response_alt_year(id):
        xml_string = get_file_as_string('tests/fixtures/book_by_id.1.xml')
        foo = parse_id_response(xml_string)

        assert foo == (453444, '1562828991', '9781562828998', "Disney's Art of Animation #1", 
                        'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png', '1991',
                        '622', '4.29', 'Bob Thomas', 'https://www.goodreads.com/book/show/453444.Disney_s_Art_of_Animation_1')

    def test_parse_id_response_excepts(self):
        with pytest.raises(TypeError):
            parse_id_response(None)
