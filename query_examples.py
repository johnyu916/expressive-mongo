db.inventory.find( {} )
jdb.inventory.find( '')


db.inventory.find( { 'status': "D" } )
db.inventory.find({$expr: {$eq: ["$status", "D"]}})
jdb.inventory.find('status == "D"')


db.inventory.find( { 'status': { '$in': [ "A", "D" ] } } )
db.inventory.find({$expr: {$in: ["$status", ["A", "D"]]}})
jdb.inventory.find( 'status in [ "A", "D" ]' )


db.inventory.find( { 'status': "A", 'qty': { '$lt': 30 } } )
db.inventory.find({$expr: {$and: [{"$eq": ["$status", "A"]}, {$lt: ["$qty", 30]}]}})
jdb.inventory.find( 'status == "A" and qty < 30' )


db.inventory.find( { '$or': [ { 'status': "A" }, { 'qty': { '$lt': 30 } } ] } )
db.inventory.find({$expr: {$or: [{"$eq": ["$status", "A"]}, {$lt: ["$qty", 30]}]}})
jdb.inventory.find( 'status == "A" or qty < 30' )


db.inventory.find( {
    'status': "A",
    '$or': [ { 'qty': { '$lt': 30 } }, { 'item': 'paper' } ]
} )
db.inventory.find({$expr: {$and: [{"$eq": ["$status", "A"]}, {$or :[{$eq:["$item", "paper"]}, {$lt: ["$qty", 30]}]}]}})
jdb.inventory.find('(status == "A") and (qty < 30 or item == "paper")')


db.inventory.find( { 'size': { 'h': 14, 'w': 21, 'uom': "cm" } } )
db.inventory.find({$expr: {$eq: ["$size", { 'h': 14, 'w': 21, 'uom': "cm"}]}})
jdb.inventory.find('size == { h: 14, w: 21, uom: "cm" }')


db.inventory.find( { "size.uom": "in" } )
db.inventory.find({$expr: { $eq: ["$size.uom", "in"] }} )
jdb.inventory.find('size.uom == "in"')


db.inventory.find( { "size.h": { '$lt': 15 } } )
db.inventory.find({$expr: { $eq: ["$size.uom", "in"] }} )
jdb.inventory.find('size.h < 15 ')


db.inventory.find( { "size.h": { $lt: 15 }, "size.uom": "in", status: "D" } )
jdb.inventory.find('size.h < 15 and size.uom == "in" and status == "D"')

# arrays
db.inventory2.find( { tags: ["red", "blank"] } )
db.inventory2.find({$expr: { $eq: ["$tags", ["red", "blank"]] }} )
jdb.inventory2.find( 'tags == ["red", "blank"]' )

# If you wish to find an array that contains both the elements "red" and "blank", without regard to order or other elements in the array, use the $all operator:
db.inventory2.find( { tags: { $all: ["red", "blank"] } } )
db.inventory2.find({$expr: { $and: [{$in: ["red", "$tags"]}, {$in: ["blank", "$tags"] }]} })
#db.inventory.find('all(tags, ["red", "blank"])')
jdb.inventory2.find('"red" in tags and "blank" in tags')

db.inventory2.find( { tags: "red" } )
db.inventory2.find({$expr: {$in: ["red", "$tags"]} })
jdb.inventory2.find('"red" in tags')


# match any document where the dim_cm array has at least 
# one element that is greater than 25
db.inventory2.find( { dim_cm: { $gt: 25 } } )
#db.inventory.find('len(filter(lambda x: x > 25, dim_cm)) > 0')
db.inventory2.find( { $expr: { $gt: [ {$size:{$filter: { input: "$dim_cm", as: "x", cond: { $gt: ["$$x", 25]}}}}, 0]}})
jdb.inventory2.find('len([for element in dim_cm if element > 25]) > 0')


# satisfy one or the other or both conditions
db.inventory2.find( { dim_cm: { $gt: 15, $lt: 20 } } )
db.inventory2.find( { $expr: { $gt: [ {$size:{$filter: { input: "$dim_cm", as: "x", cond: { $or: [{'$gt': ["$$x", 15]}, {'$lt': ["$$x", 20]}] }}}}, 0]}})
jdb.inventory2.find('len(filter(lambda x: x < 20 or x > 15, dim_cm)) > 0')
jdb.inventory2.find('len([for x in dim_cm if x <20 or x > 15]) > 0')


db.inventory2.find( { dim_cm: { $elemMatch: { $gt: 22, $lt: 30 } } } )
# don't need special elemMatch
db.inventory2.find( { $expr: { $gt: [ {$size:{$filter: { input: "$dim_cm", as: "x", cond: { $and: [{'$gt': ["$$x", 22]}, {'$lt': ["$$x", 30]}] }}}}, 0]}})
db.inventory.find('len(filter(lambda x: x > 22 and x > 30, dim_cm)) > 0')
db.inventory.find('len([for element in dim_cm if element > 22 and element < 30]) > 0')


# second element is greater than 25
db.inventory2.find( { "dim_cm.1": { $gt: 25 } } )
db.inventory2.find({$expr: {$gt: [{$arrayElemAt: ["$dim_cm", 1]}, 25]}})
jdb.inventory2.find('dim_cm[1] > 25')


db.inventory.find( { "tags": { $size: 3 } } )
db.inventory2.find({$expr: {$eq: [{$size: "$tags"}, 3]}} )
jdb.inventory2.find('len(tags) == 3')

# mql: ?
db.inventory2.find({$expr: {$lt: [{$size: "$tags"}, 3]}} )
jdb.inventory2.find('len(tags) < 3')

db.inventory.find( { item: null } )
db.inventory.find({$expr: {$eq: ["$item", null]}})
db.inventory.find('item == None')


db.inventory.find( { item : { $exists: false } } )
db.inventory.find({$expr: {$eq: ["$size", "$missing"]}})
db.inventory.find('item in document')





























##########
# DEMO
#########

# where status is D
db.inventory.find( { 'status': "D" } )
jdb.inventory.find('status == "D"')


# where status is one of "A" and "D"
db.inventory.find( { 'status': { '$in': [ "A", "D" ] } } )
jdb.inventory.find( 'status in [ "A", "D" ]' )


# where status is A and qty < 30
db.inventory.find( { 'status': "A", 'qty': { '$lt': 30 } } )
jdb.inventory.find( 'status == "A" and qty < 30' )


# status is A and (qty < 30 or item is paper)
db.inventory.find( {
    'status': "A",
    '$or': [ { 'qty': { '$lt': 30 } }, { 'item': 'paper' } ]
} )
jdb.inventory.find('(status == "A") and (qty < 30 or item == "paper")')


# size.h is less than 15
db.inventory.find( { "size.h": { '$lt': 15 } } )
jdb.inventory.find('size.h < 15 ')


# tag array is equal to ['red', 'blank']
db.inventory2.find( { tags: ["red", "blank"] } )
jdb.inventory2.find( 'tags == ["red", "blank"]' )


# find an array that contains both the elements "red" and "blank", without regard to order.
db.inventory2.find( { tags: { $all: ["red", "blank"] } } )
jdb.inventory2.find('"red" in tags and "blank" in tags')


# second element of dim_cm is greater than 25
db.inventory2.find( { "dim_cm.1": { $gt: 25 } } )
jdb.inventory2.find('dim_cm[1] > 25')


# size of the tags array is 3
db.inventory2.find( { "tags": { $size: 3 } } )
jdb.inventory2.find('len(tags) == 3')


# size of the tags array is less than 3
?
jdb.inventory2.find('len(tags) < 3')
