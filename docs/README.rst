
Py-Models-Parser
----------------


.. image:: https://img.shields.io/pypi/v/py-models-parser
   :target: https://img.shields.io/pypi/v/py-models-parser
   :alt: badge1
 
.. image:: https://img.shields.io/pypi/l/py-models-parser
   :target: https://img.shields.io/pypi/l/py-models-parser
   :alt: badge2
 
.. image:: https://img.shields.io/pypi/pyversions/py-models-parser
   :target: https://img.shields.io/pypi/pyversions/py-models-parser
   :alt: badge3
 
.. image:: https://github.com/xnuinside/py-models-parser/actions/workflows/main.yml/badge.svg
   :target: https://github.com/xnuinside/py-models-parser/actions/workflows/main.yml/badge.svg
   :alt: workflow


It's as second Parser that done by me, first is a https://github.com/xnuinside/simple-ddl-parser for SQL DDL with different dialects.

Py-Models-Parser can parse & extract information from models & table definitions:


* Sqlalchemy ORM (https://docs.sqlalchemy.org/en/14/orm/),
* Gino ORM (https://python-gino.org/),
* Tortoise ORM (https://tortoise-orm.readthedocs.io/en/latest/),
* Encode ORM (https://github.com/encode/orm)
* Django ORM Model (https://docs.djangoproject.com/en/3.2/topics/db/queries/),
* Pydantic (https://pydantic-docs.helpmanual.io/),
* Python Enum (https://docs.python.org/3/library/enum.html),
* Pony ORM (https://ponyorm.org/),
* Piccolo ORM models (https://piccolo-orm.readthedocs.io/en/latest/piccolo/schema/defining.html),
* Pydal Tables definitions (http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#The-DAL-A-quick-tour),
* Python Dataclasses (https://docs.python.org/3/library/dataclasses.html),
* pure Python Classes (https://docs.python.org/3/tutorial/classes.html#class-objects)

Number of supported models will be increased, check 'TODO' section, if you want to have support of different models types - please open the issue.

Py-Models-Parser written with PEG parser and it's python implementation - parsimonious. It's pretty new and I did not cover all possible test cases, so if you will have an issue  - please just open an issue in this case with example, I will fix it as soon as possible.

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


#. You can parse models from python string:

.. code-block:: python


   from py_models_parser import parse

   models_str =  """from gino import Gino

   db = Gino()


   class OrderItems(db.Model):

       __tablename__ = 'order_items'

       product_no = db.Column(db.Integer(), db.ForeignKey('products.product_no'), ondelete="RESTRICT", primary_key=True)
       order_id = db.Column(db.Integer(), db.ForeignKey('orders.order_id'), ondelete="CASCADE", primary_key=True)
       type = db.Column(db.Integer(), db.ForeignKey('types.type_id'), ondelete="RESTRICT", onupdate="CASCADE")

       """
   result = parse(models_str)


#. Parse models from file:

.. code-block:: python


       from py_models_parser import parse_from_file


       file_path = "path/to/your/models.py"
       # for example: tests/data/dataclass_defaults.py
       result = parse_from_file(file_path)


#. Parse models from file with command line

.. code-block:: bash


       pmp path_to_models.py 

       # for example: pmp tests/data/dataclass_defaults.py

Output from cli can be dumped in 'output_models.json' file - use flag '-d' '--dump' if you want to change target file name, provide it after argument like '-d target_file.json'

.. code-block:: bash


       # example how to dump output from cli

       pmp path_to_models.py -d target_file.json

Output example
^^^^^^^^^^^^^^

You can find a lot of output examples in tests - https://github.com/xnuinside/py-models-parser/tree/main/tests

For model from point 1 (above) library will produce the result:

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


#. Add more tests for supported models
#. Add support for SQLAlchemy Core Tables

Changelog
---------

**v0.6.0**
Features:


#. Added support for Encode ORM models https://github.com/encode/orm
#. Added support for Piccolo ORM models https://piccolo-orm.readthedocs.io/en/latest/piccolo/schema/defining.html

**v0.5.1**
Fixes:


#. Sometimes multiple parents names in "parents" output was joined in one string - fixed.

**v0.5.0**


#. Added base support for Pydal tables definitions
#. Added support for python list syntax like []

**v0.4.0**


#. return tuples (multiple values) is parsed correctly now
#. symbols like ``*&^%$#!±~``\ §<>` now does not cause any errors
#. classes without any args does not cause an error anymore

**v0.3.0**


#. Added cli - ``pmp`` command with args -d, --dump  
#. Added support for simple Django ORM models
#. Added base support for pure Python Classes

**v0.2.0**


#. Added support for Dataclasses
#. Added parse_from_file method
#. Added correct work with types with comma inside, like: Union[dict, list] or Union[dict, list, tuple, anything] 

**v0.1.1**


#. Added base parser logic & tests for Pydantic, Enums, SQLAlchemy Models, GinoORM models, TortoiseORM models 
