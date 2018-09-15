''' book_utils.py '''
from sorter.lib.request_data import read_url

def get_by_id(book_id, defaults):
    '''
    Get book given a goodreads book id
    '''
    url = defaults.get_book_url(book_id)
    xml_string = read_url(url)

    return xml_string

def get_by_isbn(isbn, defaults):
    '''
    Get book info given a search term
    note: expects isbn or isbn13, support for other terms is limited
    '''
    url = defaults.get_search_url(isbn)
    xml_string = read_url(url)

    return xml_string
