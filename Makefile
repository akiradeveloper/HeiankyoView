install:
	python setup.py install

runtest:
	cd test; \
	python runtest.py; \
	cd -

release:
	python setup.py sdist upload
