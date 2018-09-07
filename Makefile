init: 
	pip install -r requirements.txt

test:
	-pylint sorter
	-coverage run -m pytest
	coverage report -m
	
start:
	python -m sorter

clean:
	-find . -name "*.pyc" -type f -delete
	-rm .coverage
