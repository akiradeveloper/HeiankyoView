install:
	python setup.py install

runtest:
	cd test; \
	python runtest.py; \
	cd -
