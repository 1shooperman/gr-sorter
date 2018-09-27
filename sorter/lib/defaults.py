'''
App defaults:

    https://www.goodreads.com/book/show/453444.xml?key=[key]
    http://localhost:8081/simple/book_by_id.xml?id=%s % book_id

    https://www.goodreads.com/search?q=8811667739&format=xml&key=[key]
    http://localhost:8081/simple/book_by_isbn.xml?isbn=%s % isbn
'''
import os

class Defaults(object):
    '''
    Set up APP defaults
    '''
    def __init__(self, base, api_key=None, per_page=40, shelves=None):
        self.base = base

        self.__api_key = api_key
        self.__api_urls = {
            'SEARCH_URL': self.base + '/search?q=%s&format=xml&key=%s',
            'BOOK_URL': self.base + '/book/show/%s.xml?key=%s',
            'SHELF_URL': self.base + '/review/list/%s.xml?key=%s&v=2&shelf=%s&per_page=%s'
        }
        self.__per_page = per_page

        if shelves is None:
            self.__shelves = ['to-read']
        else:
            self.__shelves = shelves

    def get_search_url(self, search_term, uri=None):
        '''
        Return the well formed search url
        '''
        if uri is None:
            uri = self.__api_urls['SEARCH_URL']

        formed_url = uri % (search_term, self.__api_key)

        return formed_url

    def get_book_url(self, book_id, uri=None):
        '''
        Return the well formed book url
        '''
        if uri is None:
            uri = self.__api_urls['BOOK_URL']

        formed_url = uri % (book_id, self.__api_key)

        return formed_url

    def get_shelf_url(self, user_id, shelves=None, per_page=None, uri=None):
        '''
        Return the well formed review url used for bulk import
        '''
        if shelves is None:
            shelves = self.__shelves

        if per_page is None:
            per_page = self.__per_page

        if uri is None:
            uri = self.__api_urls['SHELF_URL']

        formed_url = uri % (user_id, self.__api_key, shelves[0], per_page)

        return formed_url

    def get_key(self):
        '''
        API KEY getter
        '''
        return self.__api_key

    @staticmethod
    def is_test():
        '''
        Determine if we are running in the test environment
        '''
        if 'WEBPY_ENV' in os.environ:
            return os.environ['WEBPY_ENV'] == 'test'

        return False
