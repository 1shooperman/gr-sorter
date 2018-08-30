import xml.etree.ElementTree as ElementTree       

class Xml(object):
    """ Xml class """
    def __init__(self):
        pass

    @staticmethod
    def parse(xmlString):
        root = ElementTree.fromstring(xmlString)

        stats = root[1].attrib

        totalRatings = 0
        books = {}
        for review in root.findall('reviews/review'):
            goodreads_id = review.find('id').text
            ratings = int(review.find('book/ratings_count').text)
            book = {
                'isbn': review.find('book/isbn').text,
                'isbn13': review.find('book/isbn13').text,
                'title': review.find('book/title_without_series').text,
                'image_url': review.find('book/image_url').text,
                'publication_year': review.find('book/publication_year').text,
                'ratings_count': ratings,
                'average_rating': review.find('book/average_rating').text,
                'author': review.find('book/authors/author/name').text
            }
            books[goodreads_id] = book
            totalRatings += ratings

        return (books,totalRatings)

    @staticmethod
    def rank(jsonData):
       pass 
