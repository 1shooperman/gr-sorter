''' parse_xml.py '''
import xml.etree.ElementTree as ElementTree       

def parse(xml_string):
    ''' parse a provided goodreads api xml response as a string '''
    if xml_string is None:
        raise TypeError('expected string, got %s' % type(xml_string))

    root = ElementTree.fromstring(xml_string)
    books = map(get_book_data, root.findall('reviews/review'))

    return books

def get_book_data(generator):
    ''' private method used for pulling book data from the provided xml generator '''
    book = (
        int(generator.find('id').text),
        generator.find('book/isbn').text,
        generator.find('book/isbn13').text,
        generator.find('book/title_without_series').text,
        generator.find('book/image_url').text,
        generator.find('book/publication_year').text,
        int(generator.find('book/ratings_count').text),
        generator.find('book/average_rating').text,
        generator.find('book/authors/author/name').text
    )

    return book
