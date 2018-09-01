# Book Sorter
I am an avid reader.  Crowd sourced tools like [goodreads](https://www.goodreads.com/) help maintain my reading list.  It's a fantastic piece 
of software that allows me to quickly add books, read synopses, and read reviews.  The only thing it was missing was the ability
to add custom weights to the sorting.  This started off as an excel sheet and some weighting algorithms developed by my fantastic wife (who 
also happens to be a data analyst).

## Tech
* SQLite (to import the CSV exports from goodreads)
* Python because I chose to learn Python in 2018

## Weighting Algorithm
* WEIGHT = Number of Ratings/Total Ratings + (TO_PERCENT((2010 - Publication Year) * 0.00001)) + Preference Adjustment
* SCORE = (Avg Rating * WEIGHT) * 100

### Key
* *Number of Ratings* is the number of ratings for a book on goodreads
* *Total Ratings* is the total number of ratings across all books on my reading list(s)
* *Avg Rating* is the community sourced average rating for a book on goodreads
* *2010* is an arbitrary fixed year I picked

### Reasoning
* Since newer books frequently build on older texts, publication year is factored into the rating.
* There is a preference adjustment to weight topics/genres I am more interested in. 

## References
1. Directory structure - https://docs.python-guide.org/writing/structure/
1. Pip requirements file - https://pip.pypa.io/en/stable/user_guide/#requirements-files
1. Pylint - https://www.pylint.org/#install
1. Makefile - https://www.gnu.org/software/make/manual/html_node/Simple-Makefile.html
1. goodreads - https://www.goodreads.com/
