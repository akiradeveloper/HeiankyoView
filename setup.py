from distutils.core import setup

setup(
	name = 'HeiankyoView',
	version = '0.9',
	url = 'https://github.com/akiradeveloper/HeiankyoView',
	description = 'A fast algorithm to visualize tree structures',
	author = 'Akira Hayakawa',
	author_email = 'ruby.wktk@gmail.com',
	package_dir = {'':'lib'},
	packages = [''],
	scripts = [
		'bin/heiankyoview',
	],
	platforms = ['POSIX'],
	classifiers = [
		"Operating System :: POSIX :: Linux",	
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"Topic :: Scientific/Engineering :: Visualization",
	]
)
