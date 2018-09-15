''' book_utils.py '''
from sorter.lib.request_data import read_url
from sorter.lib.defaults import get_book_url, get_search_url

def get_by_id(book_id):
    '''
    Get book given a goodreads book id
    '''
    url = get_book_url(book_id, 'http://localhost:8081/simple/book_by_id.xml?id=%s&key=%s')
    xml_string = read_url(url)

    return xml_string

def get_by_isbn(isbn):
    '''
    Get book info given a search term
    note: expects isbn or isbn13, support for other terms is limited
    '''
    url = get_search_url(isbn, 'http://localhost:8081/simple/book_by_isbn.xml?isbn=%s&key=%s')
    xml_string = read_url(url)

    return xml_string
