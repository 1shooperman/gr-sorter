init: 
	pip install -r requirements.txt

test:
	-pylint sorter
	-coverage run -m pytest
	coverage report -m
	

clean:
	-rm *.pyc
	-rm sorter/*.pyc
	-rm tests/*.pyc
	-rm .coverage
