init: 
	pip install -r requirements.txt

test:
	-pylint .
	nosetests
