install:
	python2.6 setup.py install
	python setup.py install

runtest:
	cd test; \
	python runtest.py; \
	cd -

release:
	python setup.py sdist upload
