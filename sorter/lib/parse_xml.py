''' parse_xml.py '''
import xml.etree.ElementTree as ElementTree
import math

def parse(xml_string):
    ''' parse a provided goodreads api xml response as a string '''
    if xml_string is None:
        raise TypeError('expected string, got %s' % type(xml_string))

    root = ElementTree.fromstring(xml_string)
    books = map(get_book_data, root.findall('reviews/review'))

    return books

def parse_isbn13_response(xml_string):
    ''' get book data from the isbn search response '''
    if xml_string is None:
        raise TypeError('expected string, got %s' % type(xml_string))

    root = ElementTree.fromstring(xml_string)
    book = get_book_data_from_isbn_response(root.find('search/results/work'))

    return book

def parse_id_response(xml_string):
    ''' get book data from the id search response '''
    if xml_string is None:
        raise TypeError('expected string, got %s' % type(xml_string))

    root = ElementTree.fromstring(xml_string)
    book = get_book_data_from_id_response(root.find('book'))

    return book

def get_book_data(generator):
    ''' private method used for pulling book data from the provided xml generator '''
    utils = GrDataUtils(generator)

    book = (
        utils.get_id(),
        utils.get_isbn(),
        utils.get_isbn13(),
        utils.get_title(),
        utils.get_image_url(),
        utils.get_year(),
        utils.get_ratings_count(),
        utils.get_average_rating(),
        utils.get_author(),
        utils.get_link(),
    )

    return book

def get_book_data_from_isbn_response(element): # pylint: disable=invalid-name
    ''' Given a goodreads search response, parse book data '''
    book_id = int(element.find('id').text)
    title = element.find('best_book/title').text
    image_url = element.find('best_book/image_url').text
    year = element.find('original_publication_year').text
    ratings_count = element.find('ratings_count').text
    average_rating = element.find('average_rating').text
    author = element.find('best_book/author/name').text

    return (
        book_id,
        None,
        None,
        title,
        image_url,
        year,
        ratings_count,
        average_rating,
        author,
        None
    )

def get_book_data_from_id_response(element):
    ''' Given a goodreads search response, parse book data '''
    book_id = int(element.find('id').text)
    title = element.find('title').text
    isbn = element.find('isbn').text
    isbn13 = element.find('isbn13').text
    image_url = element.find('image_url').text
    year = element.find('publication_year').text
    ratings_count = element.find('work/ratings_count').text
    average_rating = element.find('average_rating').text
    author = element.find('authors/author/name').text
    link = element.find('link').text

    return (
        book_id,
        isbn,
        isbn13,
        title,
        image_url,
        year,
        ratings_count,
        average_rating,
        author,
        link
    )

def get_total_pages(xml_string):
    '''
    Calculate total pages and current page based on reviews element attributes
    '''
    if xml_string is None:
        raise TypeError('expected string, got %s' % type(xml_string))

    root = ElementTree.fromstring(xml_string)
    reviews = root.find('reviews')
    attribs = reviews.attrib

    total = float(attribs['total'])
    start = float(attribs['start'])
    end = float(attribs['end'])

    if end > 0:
        per_page = float(end - start + 1)
    else:
        per_page = 0

    pages = int(math.ceil(total / per_page))
    current_page = int(math.ceil(start / per_page))

    return (pages, current_page)


class GrDataUtils(object):
    ''' utility methods for pulling data from the xml object '''
    def __init__(self, generator):
        self.generator = generator

    def get_id(self):
        ''' get the book id from the goodreads data set '''
        return int(self.generator.find('book/id').text)

    def get_isbn(self):
        ''' get the book isbn from the goodreads data set '''
        isbn = self.generator.find('book/isbn')
        if isbn != None:
            isbn = isbn.text
        return isbn

    def get_isbn13(self):
        ''' get the book isbn13 from the goodreads data set '''
        isbn13 = self.generator.find('book/isbn13')
        if isbn13 != None:
            isbn13 = isbn13.text
        return isbn13

    def get_title(self):
        ''' get the book title from the goodreads data set '''
        title = self.generator.find('book/title_without_series')
        if title != None:
            title = title.text
        return title

    def get_image_url(self):
        ''' get the book cover from the goodreads data set '''
        image_url = self.generator.find('book/image_url')
        if image_url != None:
            image_url = image_url.text

        return image_url

    def get_year(self):
        ''' get the book publication year from the goodreads data set '''
        pub_year = self.generator.find('book/published')
        if pub_year != None:
            pub_year = pub_year.text
        else:
            pub_year = self.generator.find('book/publication_year')
            if pub_year != None:
                pub_year = pub_year.text

        return pub_year

    def get_ratings_count(self):
        ''' get the book ratings count from the goodreads data set '''
        ratings = self.generator.find('book/ratings_count')
        if ratings is not None:
            ratings = int(ratings.text)
        return ratings

    def get_average_rating(self):
        ''' get the book average rating from the goodreads data set '''
        avg_rating = self.generator.find('book/average_rating')
        if avg_rating is not None:
            avg_rating = avg_rating.text # TODO: should we cast this to a float?

        return avg_rating

    def get_author(self):
        ''' get the book author from the goodreads data set '''
        author = self.generator.find('book/authors/author/name')
        if author is not None:
            author = author.text
        return author

    def get_link(self):
        ''' get the book link from the goodreads data set '''
        book_link = self.generator.find('book/link')
        if book_link is not None:
            book_link = book_link.text

        return book_link
