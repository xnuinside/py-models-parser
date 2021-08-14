## Py-Models-Parser

![badge1](https://img.shields.io/pypi/v/py-models-parser) ![badge2](https://img.shields.io/pypi/l/py-models-parser) ![badge3](https://img.shields.io/pypi/pyversions/py-models-parser) ![workflow](https://github.com/xnuinside/py-models-parser/actions/workflows/main.yml/badge.svg)

It's as second Parser that done by me, first is a https://github.com/xnuinside/simple-ddl-parser for SQL DDL with different dialects.

Py-Models-Parser can parse & extract information from models & table definitions:

- Sqlalchemy ORM (https://docs.sqlalchemy.org/en/14/orm/),
- Gino ORM (https://python-gino.org/),
- Tortoise ORM (https://tortoise-orm.readthedocs.io/en/latest/),
- Django ORM Model (https://docs.djangoproject.com/en/3.2/topics/db/queries/),
- Pydantic (https://pydantic-docs.helpmanual.io/),
- Python Enum (https://docs.python.org/3/library/enum.html),
- Pony ORM (https://ponyorm.org/),
- Pydal Tables definitions (http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#The-DAL-A-quick-tour),
- Python Dataclasses (https://docs.python.org/3/library/dataclasses.html),
- pure Python Classes (https://docs.python.org/3/tutorial/classes.html#class-objects)

Number of supported models will be increased, check 'TODO' section, if you want to have support of different models types - please open the issue.

Py-Models-Parser written with PEG parser and it's python implementation - parsimonious. It's pretty new and I did not cover all possible test cases, so if you will have an issue  - please just open an issue in this case with example, I will fix it as soon as possible.

Py-Models-Parser take as input different Python code with Models and provide output in standard form:

```python

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
```

For ORM models 'attrs' contains Columns of course.

3 keys - 'type', 'name', 'default' exists in parse result 'attrs' of all Models
'properties' key contains additional information for attribut or column depend on Model type, for example, in ORM models it can contains 'foreign_key' key if this column used ForeignKey, or 'server_default' if it is a SqlAlchemy model or GinoORM.

Model level 'properties' contains information relative to model, for example, if it ORM model - table_name

NOTE: it's is a text parser, so it don't import or load your code, parser work with source code as text, not objects in Python. So to run parser you DO NOT NEED install dependencies for models, that you tries to parse - only models.

## How to install

```bash

    pip install py-models-parser

```

## How to use

Library detect automaticaly that type of models you tries to parse. You can check a lot of examples in test/ folder on the GitHub

1. You can parse models from python string:

```python

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

```

2. Parse models from file:

```python

    from py_models_parser import parse_from_file


    file_path = "path/to/your/models.py"
    # for example: tests/data/dataclass_defaults.py
    result = parse_from_file(file_path)
```

3. Parse models from file with command line

```bash

    pmp path_to_models.py 

    # for example: pmp tests/data/dataclass_defaults.py

```

Output from cli can be dumped in 'output_models.json' file - use flag '-d' '--dump' if you want to change target file name, provide it after argument like '-d target_file.json'

```bash

    # example how to dump output from cli

    pmp path_to_models.py -d target_file.json

```

### Output example

You can find a lot of output examples in tests - https://github.com/xnuinside/py-models-parser/tree/main/tests

For model from point 1 (above) library will produce the result:

```python

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
```

## TODO: in next Release

1. Add more tests for supported models (and fix existed not covered cases): Django ORM, Pydantic, Enums, Dataclasses, SQLAlchemy Models, GinoORM models, TortoiseORM models, PonyORM, for lists
2. Add support for SQLAlchemy Core Tables
3. Add support for Piccolo ORM models


## Changelog
**v0.5.1**
Fixes:
1. Sometimes multiple parents names in "parents" output was joined in one string - fixed.

**v0.5.0**
1. Added base support for Pydal tables definitions
2. Added support for python list syntax like []

**v0.4.0**
1. return tuples (multiple values) is parsed correctly now
2. symbols like `*&^%$#!±~`§<>` now does not cause any errors
3. classes without any args does not cause an error anymore

**v0.3.0**
1. Added cli - `pmp` command with args -d, --dump  
2. Added support for simple Django ORM models
3. Added base support for pure Python Classes

**v0.2.0**
1. Added support for Dataclasses
2. Added parse_from_file method
3. Added correct work with types with comma inside, like: Union[dict, list] or Union[dict, list, tuple, anything] 

**v0.1.1**
1. Added base parser logic & tests for Pydantic, Enums, SQLAlchemy Models, GinoORM models, TortoiseORM models 
