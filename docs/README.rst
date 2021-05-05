
Py-Models-Parser
----------------

It's as second Parser that done by me, first is a https://github.com/xnuinside/simple-ddl-parser for SQL DDL with different dialects.
Py-Models-Parser supports now ORM Sqlalchemy, Gino, Tortoise; Pydantic, Python Enum models & in nearest feature I plan to add Dataclasses & pure pyton classes. And next will be added other ORMs models.

Py-Models-Parser written with PEG parser and it's python implementation - parsimonious.
Py-Models-Parser take as input different Python code with Models and provide output in standard form:

.. code-block:: python


       [
           'name': 'ModelName',
           'parents': ['BaseModel'], # class parents that defined in (), for example: `class MaterialType(str, Enum):` parents - str, Enum
           'attrs':
       {
           'type': 'integer',
           'name': 'attr_name',
           'default': 'default_value',
           'properties': {
               ...
           }
       },
       'properties': {
           'table_name': ...
       }
       ]

For ORM models 'attrs' contains Columns of course.

3 keys - 'type', 'name', 'default' exists in parse result 'attrs' of all Models
'properties' key contains additional information for attribut or column depend on Model type, for example, in ORM models it can contains 'foreign_key' key if this column used ForeignKey, or 'server_default' if it is a SqlAlchemy model or GinoORM.

Model level 'properties' contains information relative to model, for example, if it ORM model - table_name

NOTE: it's is a text parser, so it don't import or load your code, parser work with source code as text, not objects in Python. So to run parser you DO NOT NEED install dependencies for models, that you tries to parse - only models.

How to install
--------------

.. code-block:: bash


       pip install py-models-parser

How to use
----------

Library detect automaticaly that type of models you tries to parse. You can check a lot of examples in test/ folder on the GitHub

You can parse models from python string:

.. code-block:: python


   from py_models_parser.core import parse

   models_str =  """from gino import Gino

   db = Gino()


   class OrderItems(db.Model):

       __tablename__ = 'order_items'

       product_no = db.Column(db.Integer(), db.ForeignKey('products.product_no'), ondelete="RESTRICT", primary_key=True)
       order_id = db.Column(db.Integer(), db.ForeignKey('orders.order_id'), ondelete="CASCADE", primary_key=True)
       type = db.Column(db.Integer(), db.ForeignKey('types.type_id'), ondelete="RESTRICT", onupdate="CASCADE")

       """
   result = parse(models_str)

It will produce the result:

.. code-block:: python


       [
           {
               "attrs": [
                   {
                       "default": None,
                       "name": "product_no",
                       "properties": {
                           "foreign_key": "'products.product_no'",
                           "ondelete": '"RESTRICT"',
                           "primary_key": "True",
                       },
                       "type": "db.Integer()",
                   },
                   {
                       "default": None,
                       "name": "order_id",
                       "properties": {
                           "foreign_key": "'orders.order_id'",
                           "ondelete": '"CASCADE"',
                           "primary_key": "True",
                       },
                       "type": "db.Integer()",
                   },
                   {
                       "default": None,
                       "name": "type",
                       "properties": {
                           "foreign_key": "'types.type_id'",
                           "ondelete": '"RESTRICT"',
                           "onupdate": '"CASCADE"',
                       },
                       "type": "db.Integer()",
                   },
               ],
               "name": "OrderItems",
               "parents": ["db.Model"],
               "properties": {"table_name": "'order_items'"},
           }
       ]

TODO: in next Release
---------------------


#. Parse from file method
#. Add cli
#. Add more tests for supported models (and fix existed not covered cases): Pydantic, Enums, Dataclasses, SQLAlchemy Models, GinoORM models, TortoiseORM models 
#. Add support for pure Python classes
#. Add support for pure SQLAlchemy Core Tables

Changelog
---------

**v0.1.0**


#. Added base parser logic & tests for Pydantic, Enums, SQLAlchemy Models, GinoORM models, TortoiseORM models 
