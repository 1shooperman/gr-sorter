''' book_utils.py '''
from sorter.lib.request_data import read_url

def get_by_id(book_id):
    ''' https://www.goodreads.com/book/show/453444.xml?key=[key] '''
    xml_string = read_url('http://localhost:8081/simple/book_by_id.xml?id=%s' % book_id)

    return xml_string

def get_by_isbn(isbn):
    ''' https://www.goodreads.com/search?q=8811667739&format=xml&key=[key] '''
    xml_string = read_url('http://localhost:8081/simple/book_by_isbn.xml?isbn=%s' % isbn)

    return xml_string
