from distutils.core import setup

setup(
	name = 'HeiankyoView',
	version = '1.0',
	description = 'An Fast algorithm to visualize Tree structure',
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
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"Topic :: Scientific/Engineering :: Visualization",
	]
)
