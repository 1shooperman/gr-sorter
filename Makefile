init: 
	pip install -r requirements.txt

test:
	-pylint sorter
	nosetests --with-coverage
