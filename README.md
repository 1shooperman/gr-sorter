# Book Sorter
I am an avid reader.  Crowd sourced tools like [goodreads](https://www.goodreads.com/) help maintain my reading list.  It (goodreads) is a fantastic piece 
of software that allows me to quickly add books, read synopses, and read reviews.  The only thing it was missing was the ability
to add custom weights to the sorting.  This started off as an excel sheet and some weighting algorithms developed by my fantastic wife (who 
also happens to be a data analyst).

## Basic Guide
The application consists of three main screens: Main, Admin, and Advanced Admin.  From these three screens you can do everything from view your book list, to tweaking a few things, to updating every piece of data bit by bit.

### The _Main_ Screen
![Main Screen](docs/screenshots/main.png "Main Screen")
From this screen you can view all of your books, ordered by "score".  You can also link back to the book on Goodreads.

### The _Admin_ Screen
![Admin Screen](docs/screenshots/basic_admin.png "Admin Screen")
From this screen you have a few options.  You can enter your API Key and User ID, select which shelves to pull from, update the list of available shelves, and import all of your data.  Please note that nothing will work without the User Id and API Key being added.

### The _Advanced Admin_ Screen
![Advanced Screen](docs/screenshots/adv_admin.png "Advanced Screen")
From this screen, you have full control over your data.  You can do everything from the basic admin screen, as well as manually update individual pieces of data.

## References / Tech
1. Learn Python the Hard Way - https://learnpythonthehardway.org/
1. Directory structure - https://docs.python-guide.org/writing/structure/
1. Pip requirements file - https://pip.pypa.io/en/stable/user_guide/#requirements-files
1. Pylint - https://www.pylint.org/#install
1. Makefile - https://www.gnu.org/software/make/manual/html_node/Simple-Makefile.html
1. goodreads - https://www.goodreads.com/
1. Python (2.7) - https://www.python.org/
1. SQLite - https://www.sqlite.org/
1. Pytest - https://docs.pytest.org/en/latest/
1. ESLint - https://eslint.org/
1. Bootstrap - http://getbootstrap.com/docs/4.1/getting-started/introduction/


## Powered by
[![Goodreads](http://s.gr-assets.com/assets/icons/goodreads_icon_50x50-823139ec9dc84278d3863007486ae0ac.png)](http://www.goodreads.com)