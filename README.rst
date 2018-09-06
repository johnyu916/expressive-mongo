================
expressive-mongo
================
MongoDB queries with expressions

:Author: John Yu

About
=====

expressive-mongo is an alternative interactive shell for MongoDB. It can parse a different query language based in programming language expressions (in python) rather than a javascript object.

Examples
========

.. code-block:: python

    $ python mongo.py
    Query with Expression
    >>> db.inventory.find('status == "D"')  # the default db is "test"
    query: {'$expr': {'$eq': ['$status', 'D']}}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd8'), 'item': 'paper', 'qty': 100.0, 'size': {'h': 8.5, 'w': 11.0, 'uom': 'in'}, 'status': 'D'}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd9'), 'item': 'planner', 'qty': 75.0, 'size': {'h': 22.85, 'w': 30.0, 'uom': 'cm'}, 'status': 'D'}
    >>> db = client.market  # change db to "market"
    >>> db.items.find({})
    query: {}
    {'_id': ObjectId('5b9164ff73556ec902b1e269'), 'name': 'iPhone 7', 'type': 'phone'}
    >>> db = client.test  # go back to test DB
    >>> db.inventory.find('status == "A" and qty < 30')
    query: {'$expr': {'$and': [{'$eq': ['$status', 'A']}, {'$lt': ['$qty', 30]}]}}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd6'), 'item': 'journal', 'qty': 25.0, 'size': {'h': 14.0, 'w': 21.0, 'uom': 'cm'}, 'status': 'A'}
    >>> db.inventory.find('status == "A" or qty < 30')
    query: {'$expr': {'$or': [{'$eq': ['$status', 'A']}, {'$lt': ['$qty', 30]}]}}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd6'), 'item': 'journal', 'qty': 25.0, 'size': {'h': 14.0, 'w': 21.0, 'uom': 'cm'}, 'status': 'A'}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd7'), 'item': 'notebook', 'qty': 50.0, 'size': {'h': 8.5, 'w': 11.0, 'uom': 'in'}, 'status': 'A'}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcda'), 'item': 'postcard', 'qty': 45.0, 'size': {'h': 10.0, 'w': 15.25, 'uom': 'cm'}, 'status': 'A'}
    >>> db.inventory.find('(status == "A") and (qty < 30 or item == "paper")')
    query: {'$expr': {'$and': [{'$eq': ['$status', 'A']}, {'$or': [{'$lt': ['$qty', 30]}, {'$eq': ['$item', 'paper']}]}]}}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd6'), 'item': 'journal', 'qty': 25.0, 'size': {'h': 14.0, 'w': 21.0, 'uom': 'cm'}, 'status': 'A'}
    >>> db.inventory.find('size == { h: 14, w: 21, uom: "cm" }')
    query: {'$expr': {'$eq': ['$size', {'h': 14, 'w': 21, 'uom': 'cm'}]}}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd6'), 'item': 'journal', 'qty': 25.0, 'size': {'h': 14.0, 'w': 21.0, 'uom': 'cm'}, 'status': 'A'}
    >>> db.inventory.find('size.uom == "in"')

    >>> db.inventory.find('size.h < 15 ')

    # arrays
    >>> db.inventory2.find( 'tags == ["red", "blank"]' )

    >>> db.inventory2.find('"red" in tags')

    >>> db.inventory2.find('dim_cm[1] > 25')
    >>> db.inventory2.find('len(tags) == 3')
    >>> db.inventory2.find('len(tags) < 3')
    >>> db.inventory3.find('item == None')
    >>> db.inventory.find('item == missing')

Installation
============

1. Install MongoDB (3.6 or above), python 3, and virtualenv
2. Run the following::

    $ virtualenv venv/
    $ pip install -r reqiurements.txt #this installs pymongo
