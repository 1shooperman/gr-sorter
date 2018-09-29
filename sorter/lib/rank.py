'''
rank.py

Weighting Algorithm
    * WEIGHT =
        Number of Ratings/Total Ratings +
        (TO_PERCENT((2010 - Publication Year) * 0.00001)) +
        Preference Adjustment
    * SCORE = (Avg Rating * WEIGHT) * 100

Key
    * Number of Ratings is the number of ratings for a book on goodreads
    * Total Ratings is the total number of ratings across all books on my reading list(s)
    * Avg Rating is the community sourced average rating for a book on goodreads
    * 2010 is an arbitrary fixed year I picked

Reasoning
    * Since newer books frequently build on older texts, pub year is factored into the rating.
    * There is a preference adjustment to weight topics/genres I am more interested in.
'''
from sorter.lib.sorter_logger import sorter_logger
LOGGER = sorter_logger(__name__)

def rank(books):
    '''rank books based on sorting algorithm developed by my wonderful (data scientist) wife. :)'''
    N = len(books) # pylint: disable=invalid-name
    total_ratings = get_total_ratings(books)

    # score the books outside of the sort for efficiency
    for key, book in enumerate(books):
        books[key] = books[key] + (score_book(book, total_ratings),)

    score_key = len(books[0]) - 1
    for i in range(N):
        for j in range(N-i-1):
            if books[j+1][score_key] > books[j][score_key]:
                books[j], books[j+1] = books[j+1], books[j]

    # careful: we mutated books here!
    return books

def score_book(book, total_ratings):
    '''
    score the books:
        book[1] = ISBN
        book[5] = pub year
        book[6] = Total Ratings
        book[7] = avg rating
        book[10] = preference adjustment
    '''
    book_title = book[3]
    book_id = book[1] # ISBN
    id_type = 'ISBN'
    if book_id is None:
        book_id = book[2] # ISBN13
        id_type = 'ISBN13'
        if book_id is None:
            book_id = book[0] # Goodreads Id
            id_type = 'ID'

    base_year = 2000

    book_ratings = book[6]
    if book_ratings is None:
        LOGGER.warn('book {%s}: {%s} missing ratings!', id_type, book_id)
        LOGGER.warn('book title: {%s}', book_title)
        book_ratings = 0
    rating_weight = book_ratings / total_ratings

    book_year = book[5]
    if book_year is None:
        LOGGER.warn('book {%s}: {%s} missing year!', id_type, book_id)
        LOGGER.warn('book title: {%s}', book_title)
        book_year = base_year
    year_weight = (base_year - book_year) * 0.001

    preference_adjustment = book[10]
    weight = rating_weight + year_weight + preference_adjustment

    book_avg_rating = book[7]
    if book_avg_rating is None:
        LOGGER.warn('book {%s}: {%s} missing averag ratings!', id_type, book_id)
        LOGGER.warn('book title: {%s}', book_title)
        book_avg_rating = 0.0

    score = (book_avg_rating * weight) * 100

    return score

def get_total_ratings(books):
    '''
    calculate total ratings
        book[6] = total ratings
    '''
    total = 0
    for book in books:
        total += book[6]

    return total
