init: 
	pip install -r requirements.txt

test:
	@export WEBPY_ENV=test
	-pylint sorter
	-coverage run -m pytest
	coverage report -m
	@export WEBPY_ENV=
	
start:
	python -m sorter

clean:
	-find . -name "*.pyc" -type f -delete
	-rm .coverage

# requires: virtualenv
# https://docs.python-guide.org/dev/virtualenvs/
dev:
	source environment/bin/activate
