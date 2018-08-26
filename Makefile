init: 
	pip install -r requirements.txt

test:
	-pylint sorter
	nosetests --with-coverage

clean:
	-rm *.pyc
	-rm sorter/*.pyc
	-rm tests/*.pyc
