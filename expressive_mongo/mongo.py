#   Copyright 2020 John Yu
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.k

#!/usr/bin/env python
import ast
import code
import copy
import pdb
import argparse

from pymongo import MongoClient

def document_matches_boolop(document, expr):
    assert isinstance(expr, ast.BoolOp)

    if isinstance(expr.op, ast.And):
        is_and = True
        for value in expr.values:
            if isinstance(value, ast.BoolOp):
                if not document_matches_boolop(document, value):
                    is_and = False
                    break
            elif isinstance(value, ast.Compare):
                if not document_matches_compare(document, value):
                    is_and = False
                    break
            else:
                raise Exception("can't process", value)

        return is_and

    elif isinstance(expr.op, ast.Or):
        is_or = False
        for value in expr.values:
            if isinstance(value, ast.BoolOp):
                if document_matches_boolop(document, value):
                    is_or = True
                    break
            elif isinstance(value, ast.Compare):
                if document_matches_compare(document, value):
                    is_or = True
                    break
            else:
                raise Exception("can't process", value)
        return is_or
    else:
        return "Unable to parse boolop"


def document_matches_compare(document, expr):
    assert isinstance(expr, ast.Compare)

    assert len(expr.ops) == 1, expr.ops
    op = expr.ops[0]

    assert len(expr.comparators) == 1, expr.comparators
    comparator = expr.comparators[0]

    def _get_fields(fields):
        left = copy.copy(document)
        for field in fields:
            left = left[field]
        return left

    #pdb.set_trace()
    if isinstance(expr.left, ast.Attribute):
        fields = [expr.left.value.id, expr.left.attr]
        left = _get_fields(fields)
    elif isinstance(expr.left, ast.Name):
        fields = [expr.left.id]
        left = _get_fields(fields)
    elif isinstance(expr.left, ast.Str):
        left = expr.left.s
    elif isinstance(expr.left, ast.Subscript):
        index = expr.left.slice.value.n
        fields= [expr.left.value.id]
        value = _get_fields(fields)
        left = value[index]
    elif isinstance(expr.left, ast.Call):
        func_name = expr.left.func.id
        assert func_name == 'len', func_name
        field = expr.left.args[0].id
        left = len(document[field])
    else:
        raise Exception("Can't parse left")


    if isinstance(op, ast.Eq):
        # what's the other value?
        if isinstance(comparator, ast.Str):
            right = comparator.s
        elif isinstance(comparator, ast.Num):
            right = comparator.n
        elif isinstance(comparator, ast.Dict):
            right = {}
            for key, value_node in zip(comparator.keys, comparator.values):
                assert isinstance(key, ast.Name)
                if isinstance(value_node, ast.Num):
                    value = value_node.n
                elif isinstance(value_node, ast.Str):
                    value = value_node.s
                else:
                    raise Exception(value_node)

                right[key.id] = value
            #pdb.set_trace()
        elif isinstance(comparator, ast.List):
            #pdb.set_trace()
            right = []
            for elt in comparator.elts:
                assert isinstance(elt, ast.Str)
                right.append(elt.s)
        else:
            raise Exception(comparator)

        # we have everything we need now.
        return left == right

    elif isinstance(op, ast.In):

        in_list = []
        if isinstance(comparator, ast.List):
            for elt in comparator.elts:
                assert isinstance(elt, ast.Str)
                in_list.append(elt.s)
        elif isinstance(comparator, ast.Name):
            in_list = document[comparator.id]

        return left in in_list

    elif isinstance(op, ast.Lt):
        assert isinstance(comparator, ast.Num)
        number = comparator.n
        return left < number
    elif isinstance(op, ast.Gt):
        assert isinstance(comparator, ast.Num)
        number = comparator.n
        return left > number
    else:
        raise Exception("Unable to parse expression")


#class Collection(object):
#    def __init__(self, collection):
#        self.collection = collection
#
#    def find(self, text=None):
#        results = self._find(text)
#        for result in results:
#            print(result)
#
#    def _find(self, text):
#        if text is None:
#            return self.collection
#        if len(text) == 0:
#            return self.collection
#
#        module = ast.parse(text)
#        expr = module.body[0].value
#
#        # ex. 'status == "D"', 'qty < 30'
#        if isinstance(expr, ast.Compare):
#            result = []
#            for document in self.collection:
#                if document_matches_compare(document, expr):
#                    result.append(document)
#            return result
#
#        # ex. 'status == "A" and qty < 30'
#        elif isinstance(expr, ast.BoolOp):
#            result = []
#            for document in self.collection:
#                if document_matches_boolop(document, expr):
#                    result.append(document)
#
#            return result
#
#        else:
#            return "unable to parse and run the expression"


#class DB(object):
#    def __init__(self, client):
#        collection = [s for s in client.tutorial.inventory.find()]
#        self.inventory = Collection(collection)
#        collection = [s for s in client.tutorial.inventory2.find()]
#        self.inventory2 = Collection(collection)

def translate_object(obj, is_filter_cond=False):
    if isinstance(obj, ast.Name):
        if is_filter_cond:
            prefix = '$$'
        else:
            prefix = '$'
        return prefix + obj.id
    elif isinstance(obj, ast.Attribute):
        # ex. animal.name
        return "$" + obj.value.id + '.' + obj.attr

    elif isinstance(obj, ast.Str):
        return obj.s
    elif isinstance(obj, ast.Num):
        return obj.n
    elif isinstance(obj, ast.List):
        in_list = []
        for elt in obj.elts:
            in_list.append(translate_object(elt))
        return in_list
    elif isinstance(obj, ast.Dict):
        in_dict = {}
        for key, value_node in zip(obj.keys, obj.values):
            assert isinstance(key, ast.Name)
            in_dict[key.id] = translate_object(value_node)
        return in_dict
    elif isinstance(obj, ast.Call):
        name = obj.func.id
        if name == "len":
            # use size
            arg = translate_object(obj.args[0])
            return {'$size': arg}
        elif name == "filter":
            assert len(obj.args) == 2, "filter() should have 2 parameters"
            _lambda = obj.args[0]
            arg = _lambda.args.args[0].arg
            _input = translate_object(obj.args[1])
            return {'$filter': {'input': _input, 'as': arg, 'cond': translate_boolop(_lambda.body, is_filter_cond=True)} }
        else:
            pdb.set_trace()
            raise Exception("Don't know call" + name)
    elif isinstance(obj, ast.Subscript):
        parent = obj.value.id
        index = obj.slice.value.n
        return {'$arrayElemAt': ["$" + parent, index]}
    elif isinstance(obj, ast.NameConstant):
        if obj.value is None:
            return None
        else:
            pdb.set_trace()
            raise Exception("Don't know name constant")
    elif isinstance(obj, ast.ListComp):
        raise Exception("Not implemented yet")
    else:
        pdb.set_trace()
        raise Exception("Don't know comparator")


def translate_compare(expr, is_filter_cond=False):
    assert isinstance(expr, ast.Compare)

    assert len(expr.ops) == 1, expr.ops
    op = expr.ops[0]

    assert len(expr.comparators) == 1, expr.comparators
    comparator = expr.comparators[0]

    left = translate_object(expr.left, is_filter_cond)

    operators = {
        'Eq': '$eq',
        'Lt': '$lt',
        'Gt': '$gt',
        'In': '$in',
    }

    operands = [left, translate_object(comparator, is_filter_cond)]

    return { operators[op.__class__.__name__]: operands }


def translate_boolop(expr, is_filter_cond=False):
    assert isinstance(expr, ast.BoolOp)

    if isinstance(expr.op, ast.And):
        operator = "$and"
    else:
        operator = "$or"

    operands = []
    for value in expr.values:
        if isinstance(value, ast.BoolOp):
            operands.append(translate_boolop(value, is_filter_cond))
        elif isinstance(value, ast.Compare):
            operands.append(translate_compare(value, is_filter_cond))
        else:
            raise Exception("Can't")

    return {operator: operands}


def to_mongo(text=''):
    """
    Translate a python expression inside a string to a MongoDB expression query.
    """
    if len(text) == 0:
        return {}

    module = ast.parse(text)
    expr = module.body[0].value

    # ex. 'status == "D"'
    # 'qty < 30'
    if isinstance(expr, ast.Compare):
        return {
            '$expr': translate_compare(expr)
        }
    # ex. 'status == "A" and qty < 30'
    elif isinstance(expr, ast.BoolOp):
        return {
            '$expr': translate_boolop(expr)
        }
    else:
        raise Exception("Don't know")

class ExpressiveCollection:
    def __init__(self, name, mongo_collection, verbose):
        self.name = name
        self.mongo_collection = mongo_collection
        self.verbose = verbose

    def find(self, expression=''):
        # convert arguemnt to $expr query and run it
        translated = to_mongo(expression)
        if self.verbose:
            print("query: {}".format(translated))
        cursor = self.mongo_collection.find(translated)

        for document in cursor:
            print(document)

class ExpressiveDatabase:
    def __init__(self, name, mongo_db, verbose):
        self.name = name
        self.mongo_db = mongo_db
        self.verbose = verbose

    def __getattr__(self, name):
        # construct a DB object
        return ExpressiveCollection(name, self.mongo_db[name], self.verbose)

class ExpressiveClient:
    def __init__(self, verbose):
        self.mongo_client = MongoClient()
        self.verbose = verbose

    def __getattr__(self, name):
        # construct a DB object
        return ExpressiveDatabase(name, self.mongo_client[name], self.verbose)


def repl(verbose):
    client = ExpressiveClient(verbose)
    db = client.test
    code.interact(
        banner="Query with Expressions. Try 'db'",
        local=locals(),
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run expressive MongoDB queries')
    parser.add_argument('--verbose', action='store_true', help='verbose output')
    args = parser.parse_args()
    repl(args.verbose)
