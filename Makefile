init: 
	pip install -r requirements.txt
	npm install

test:
	-npm run lint
	-pylint sorter
	-coverage run -m pytest -vv
	coverage report -m
	
start:
	python -m sorter

clean:
	-find . -name "*.pyc" -type f -delete
	-rm .coverage
