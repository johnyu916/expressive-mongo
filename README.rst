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
    ...

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
    ...

    >>> db.inventory.find('(status == "A") and (qty < 30 or item == "paper")')
    query: {'$expr': {'$and': [{'$eq': ['$status', 'A']}, {'$or': [{'$lt': ['$qty', 30]}, {'$eq': ['$item', 'paper']}]}]}}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd6'), 'item': 'journal', 'qty': 25.0, 'size': {'h': 14.0, 'w': 21.0, 'uom': 'cm'}, 'status': 'A'}

    >>> db.inventory.find('size == { h: 14, w: 21, uom: "cm" }')
    query: {'$expr': {'$eq': ['$size', {'h': 14, 'w': 21, 'uom': 'cm'}]}}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd6'), 'item': 'journal', 'qty': 25.0, 'size': {'h': 14.0, 'w': 21.0, 'uom': 'cm'}, 'status': 'A'}

    >>> db.inventory.find('size.uom == "in"')
    query: {'$expr': {'$eq': ['$size.uom', 'in']}}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd7'), 'item': 'notebook', 'qty': 50.0, 'size': {'h': 8.5, 'w': 11.0, 'uom': 'in'}, 'status': 'A'}
    ...

    >>> db.inventory.find('size.h < 15 ')
    query: {'$expr': {'$lt': ['$size.h', 15]}}
    {'_id': ObjectId('5b5a45738507c4e0b7f2bcd6'), 'item': 'journal', 'qty': 25.0, 'size': {'h': 14.0, 'w': 21.0, 'uom': 'cm'}, 'status': 'A'}
    ...

    # arrays
    >>> db.inventory2.find( 'tags == ["red", "blank"]' )
    query: {'$expr': {'$eq': ['$tags', ['red', 'blank']]}}
    {'_id': ObjectId('5b5f7cf05d8d5e3f5d167119'), 'item': 'notebook', 'qty': 50.0, 'tags': ['red', 'blank'], 'dim_cm': [14.0, 21.0]}
    ...

    >>> db.inventory2.find('"red" in tags')
    query: {'$expr': {'$in': ['red', '$tags']}}
    {'_id': ObjectId('5b5f7cf05d8d5e3f5d167118'), 'item': 'journal', 'qty': 25.0, 'tags': ['blank', 'red'], 'dim_cm': [14.0, 21.0]}
    ...

    >>> db.inventory2.find('dim_cm[1] > 25')
    query: {'$expr': {'$gt': [{'$arrayElemAt': ['$dim_cm', 1]}, 25]}}
    {'_id': ObjectId('5b5f7cf05d8d5e3f5d16711b'), 'item': 'planner', 'qty': 75.0, 'tags': ['blank', 'red'], 'dim_cm': [22.85, 30.0]}
    ...

    >>> db.inventory2.find('len(tags) == 3')
    query: {'$expr': {'$eq': [{'$size': '$tags'}, 3]}}
    {'_id': ObjectId('5b5f7cf05d8d5e3f5d16711a'), 'item': 'paper', 'qty': 100.0, 'tags': ['red', 'blank', 'plain'], 'dim_cm': [14.0, 21.0]}

    >>> db.inventory2.find('len(tags) < 3')
    query: {'$expr': {'$lt': [{'$size': '$tags'}, 3]}}
    {'_id': ObjectId('5b5f7cf05d8d5e3f5d167118'), 'item': 'journal', 'qty': 25.0, 'tags': ['blank', 'red'], 'dim_cm': [14.0, 21.0]}
    ...

    >>> db.inventory3.find('item == None')
    query: {'$expr': {'$eq': ['$item', None]}}

    >>> db.inventory.find('item == missing')
    query: {'$expr': {'$eq': ['$item', '$missing']}}

    >>> db.inventory2.find('len(filter(lambda x: x < 20 or x > 15, dim_cm)) > 0')
    query: {'$expr': {'$gt': [{'$size': {'$filter': {'input': '$dim_cm', 'as': 'x', 'cond': {'$or': [{'$lt': ['$$x', 20]}, {'$gt': ['$$x', 15]}]}}}}, 0]}}

Installation
============

1. Install MongoDB (3.6 or above).
2. Install Python 3 (if needed) and run virtualenv at the root of the git repository::

    $ python3 -m venv venv
    
3. Activate virtualenv::

    $ . venv/bin/activate
    
4. Install required python packages::

    $ pip install -r reqiurements.txt #this installs pymongo
