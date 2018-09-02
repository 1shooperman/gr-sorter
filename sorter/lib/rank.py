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
            if books[j][score_key] > books[j+1][score_key]:
                books[j], books[j+1] = books[j+1], books[j]

    # careful: we overwrote books here!
    return books

def score_book(book, total_ratings):
    '''
    score the books:
        book[5] = pub year
        book[6] = Total Ratings
        book[7] = avg rating
    '''
    base_year = 2010
    rating_weight = book[6] / total_ratings
    year_weight = (base_year - book[5]) * 0.00001 # issue here since python does not support % as a data type
    preference_adjustment = 0 #not yet implemented
    weight = rating_weight + year_weight + preference_adjustment
    score = (book[7] * weight) * 100

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
