# Py-Models-Parser

[![PyPI version](https://img.shields.io/pypi/v/py-models-parser)](https://pypi.org/project/py-models-parser/)
[![License](https://img.shields.io/pypi/l/py-models-parser)](https://github.com/xnuinside/py-models-parser/blob/main/LICENSE)
[![Python versions](https://img.shields.io/pypi/pyversions/py-models-parser)](https://pypi.org/project/py-models-parser/)
[![Tests](https://github.com/xnuinside/py-models-parser/actions/workflows/main.yml/badge.svg)](https://github.com/xnuinside/py-models-parser/actions/workflows/main.yml)

It's a second parser that I've created. The first is [simple-ddl-parser](https://github.com/xnuinside/simple-ddl-parser) for SQL DDL with different dialects.

Py-Models-Parser can parse & extract information from models & table definitions:

- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [Gino ORM](https://python-gino.org/)
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/)
- [Encode ORM](https://github.com/encode/orm)
- [Django ORM](https://docs.djangoproject.com/en/3.2/topics/db/queries/)
- [Pydantic v1 and v2](https://docs.pydantic.dev/)
- [Python Enum](https://docs.python.org/3/library/enum.html)
- [Pony ORM](https://ponyorm.org/)
- [Piccolo ORM](https://piccolo-orm.readthedocs.io/en/latest/piccolo/schema/defining.html)
- [PyDAL Tables](http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#The-DAL-A-quick-tour)
- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Pure Python Classes](https://docs.python.org/3/tutorial/classes.html#class-objects)
- [OpenAPI 3.0/Swagger](https://swagger.io/specification/)

Number of supported models will be increased. Check the 'TODO' section. If you want support for different model types, please open an issue.

Py-Models-Parser is written with PEG parser and its Python implementation - parsimonious. It's pretty new and I did not cover all possible test cases, so if you have an issue - please just open an issue with an example, I will fix it as soon as possible.

**NOTE:** This is a text parser, so it doesn't import or load your code. The parser works with source code as text, not objects in Python. So to run the parser you DO NOT NEED to install dependencies for models that you're trying to parse - only the models themselves.

## Output Format

Py-Models-Parser takes different Python code with Models as input and provides output in a standard form:

```python
[
    {
        'name': 'ModelName',
        'parents': ['BaseModel'],  # class parents defined in ()
        'attrs': [
            {
                'name': 'attr_name',
                'type': 'integer',
                'default': 'default_value',
                'properties': {
                    # additional info like foreign_key, server_default, etc.
                }
            }
        ],
        'properties': {
            'table_name': '...'  # model-level properties
        }
    }
]
```

For ORM models, 'attrs' contains columns. Three keys - 'type', 'name', 'default' - exist in all parsed model attrs. The 'properties' key contains additional information depending on Model type.

## Installation

```bash
pip install py-models-parser
```

## Usage

### Parse from string

```python
from py_models_parser import parse

models_str = """
from gino import Gino

db = Gino()

class OrderItems(db.Model):
    __tablename__ = 'order_items'

    product_no = db.Column(db.Integer(), db.ForeignKey('products.product_no'), ondelete="RESTRICT", primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('orders.order_id'), ondelete="CASCADE", primary_key=True)
"""

result = parse(models_str)
```

### Parse from file

```python
from py_models_parser import parse_from_file

result = parse_from_file("path/to/your/models.py")
```

### Parse OpenAPI/Swagger specifications

```python
from py_models_parser import parse_openapi, parse_openapi_file

# Parse from string
openapi_spec = """
openapi: "3.0.0"
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
"""
result = parse_openapi(openapi_spec)

# Or parse from file (supports both YAML and JSON)
result = parse_openapi_file("path/to/openapi.yaml")
```

### CLI

```bash
pmp path_to_models.py

# Dump output to JSON file
pmp path_to_models.py -d target_file.json
```

## Output Example

For the GinoORM model above, the library produces:

```python
[
    {
        "name": "OrderItems",
        "parents": ["db.Model"],
        "attrs": [
            {
                "name": "product_no",
                "type": "db.Integer()",
                "default": None,
                "properties": {
                    "foreign_key": "'products.product_no'",
                    "ondelete": '"RESTRICT"',
                    "primary_key": "True",
                },
            },
            {
                "name": "order_id",
                "type": "db.Integer()",
                "default": None,
                "properties": {
                    "foreign_key": "'orders.order_id'",
                    "ondelete": '"CASCADE"',
                    "primary_key": "True",
                },
            },
        ],
        "properties": {"table_name": "'order_items'"},
    }
]
```

You can find more output examples in [tests](https://github.com/xnuinside/py-models-parser/tree/main/tests).

## TODO

1. Add more tests for supported models
2. Add support for SQLAlchemy Core Tables
