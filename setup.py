from distutils.core import setup
setup(
  name = 'expressive-mongo',
  packages = ['expressive_mongo'],
  version = '0.0.2',
  license= 'Apache License, Version 2.0',
  description = 'Easy MongoDB queries with Python expressions',
  author = 'John Yu',
  author_email = 'johnyu916@hotmail.com',
  url = 'https://github.com/johnyu916/expressive-mongo',
  download_url = 'https://github.com/johnyu916/expressive-mongo/archive/0.0.1.tar.gz',
  keywords = ['MongoDB', 'Database', 'Query'],
  install_requires=['pymongo',],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Database',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
