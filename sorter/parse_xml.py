import xml.etree.ElementTree as ElementTree       

tree = ElementTree.parse('tests/fixtures/sample.xml')
root = tree.getroot() 

stats = root[1].attrib

books = {}
for review in root.findall('reviews/review'):
    goodreads_id = review.find('id').text
    book = {
        'isbn': review.find('book/isbn').text,
        'isbn13': review.find('book/isbn13').text,
        'title': review.find('book/title_without_series').text,
        'image_url': review.find('book/image_url').text,
        'publication_year': review.find('book/publication_year').text,
        'ratings_count': review.find('book/ratings_count').text,
        'average_rating': review.find('book/average_rating').text,
        'author': review.find('book/authors/author/name').text
    }
    books[goodreads_id] = book

print books
