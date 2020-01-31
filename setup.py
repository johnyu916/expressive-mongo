from distutils.core import setup
setup(
  name = 'expressive-mongo',         # How you named your package folder (MyLib)
  packages = ['expressive_mongo'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license= 'Apache License, Version 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Easy MongoDB queries with Python expressions',   # Give a short description about your library
  author = 'John Yu',                   # Type in your name
  author_email = 'johnyu916@hotmail.com',      # Type in your E-Mail
  url = 'https://github.com/johnyu916/expressive-mongo',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/johnyu916/expressive-mongo/archive/0.0.1.tar.gz',
  keywords = ['MongoDB', 'Database', 'Query'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pymongo',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Database',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
