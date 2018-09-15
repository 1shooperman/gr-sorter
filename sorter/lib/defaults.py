'''
App defaults:

    https://www.goodreads.com/book/show/453444.xml?key=[key]
    http://localhost:8081/simple/book_by_id.xml?id=%s % book_id

    https://www.goodreads.com/search?q=8811667739&format=xml&key=[key]
    http://localhost:8081/simple/book_by_isbn.xml?isbn=%s % isbn
'''
import os

__KEY_FILE = './goodreads_api_key'

__API_URLS = {
    'SEARCH_URL': 'https://www.goodreads.com/search?q=%s&format=xml&key=%s',
    'BOOK_URL': 'https://www.goodreads.com/book/show/%s.xml?key=%s'
}

def get_key(secret=__KEY_FILE):
    '''
    Get API key from given file
    '''
    key = None
    key_file = os.path.abspath(secret)
    if os.path.isfile(key_file) is True:
        with open(key_file, 'r') as myfile:
            key = myfile.read()

        myfile.close()

    return key

def get_search_url(search_term, uri=__API_URLS['SEARCH_URL']):
    '''
    Return the well formed search url
    '''
    formed_url = uri % (search_term, __API_KEY)

    return formed_url

def get_book_url(book_id, uri=__API_URLS['BOOK_URL']):
    '''
    Return the well formed book url
    '''
    formed_url = uri % (book_id, __API_KEY)

    return formed_url

def is_test():
    '''
    Determine if we are running in the test environment
    '''
    if 'WEBPY_ENV' in os.environ: # TODO not really happy with this check
        return os.environ['WEBPY_ENV'] == 'test'

    return False


# initialize the api key variable
if not is_test():
    __API_KEY = get_key(__KEY_FILE) # pragma: no cover
else:
    __API_KEY = None
