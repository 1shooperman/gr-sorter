import xml.etree.ElementTree as ElementTree       

def parse(xmlString):
    if (xmlString == None):
        raise TypeError('expected string, got %s' % type(xmlString))

    root = ElementTree.fromstring(xmlString)

    stats = root[1].attrib
    totalRatings = 0

    books = map(get_book_data, root.findall('reviews/review'))
    #totalRatings = reduce(lambda acc, it: acc + it['ratings_count'], books, 0)

    #return (books,totalRatings)
    return books

def get_book_data(generator):
    book = {
        'goodreads_id': generator.find('id').text,    
        'isbn': generator.find('book/isbn').text,
        'isbn13': generator.find('book/isbn13').text,
        'title': generator.find('book/title_without_series').text,
        'image_url': generator.find('book/image_url').text,
        'publication_year': generator.find('book/publication_year').text,
        'ratings_count': int(generator.find('book/ratings_count').text),
        'average_rating': generator.find('book/average_rating').text,
        'author': generator.find('book/authors/author/name').text
    }

    return book
