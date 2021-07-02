from py_models_parser import parse


def test_simple_pony_model():
    model = """
class Person(db.Entity):
     name = Required(str)
     age = Required(int)
     cars = Set('Car')

class Car(db.Entity):
     make = Required(str)
     model = Required(str)
     owner = Required(Person)

"""

    result = parse(model)
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "name",
                    "properties": {"nullable": False},
                    "type": "str",
                },
                {
                    "default": None,
                    "name": "age",
                    "properties": {"nullable": False},
                    "type": "int",
                },
                {
                    "default": None,
                    "name": "cars",
                    "properties": {"foreign_key": "'Car'", "relationship": True},
                    "type": "'Car'",
                },
            ],
            "name": "Person",
            "parents": ["db.Entity"],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "make",
                    "properties": {"nullable": False},
                    "type": "str",
                },
                {
                    "default": None,
                    "name": "model",
                    "properties": {"nullable": False},
                    "type": "str",
                },
                {
                    "default": None,
                    "name": "owner",
                    "properties": {"nullable": False},
                    "type": "Person",
                },
            ],
            "name": "Car",
            "parents": ["db.Entity"],
            "properties": {},
        },
    ]
    assert result == expected


def test_primary_and_optional():

    model = """
    from pony.orm import *

    db = Database()


    class Product(db.Entity):
        id = PrimaryKey(int, auto=True)
        name = Required(str)
        info = Required(Json)
        tags = Optional(Json)


    db.bind('sqlite', ':memory:', create_db=True)
    db.generate_mapping(create_tables=True)
    """

    result = parse(model)
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"auto": "True", "primary_key": True},
                    "type": "int",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {"nullable": False},
                    "type": "str",
                },
                {
                    "default": None,
                    "name": "info",
                    "properties": {"nullable": False},
                    "type": "Json",
                },
                {
                    "default": None,
                    "name": "tags",
                    "properties": {"nullable": True},
                    "type": "Json",
                },
                {"default": None, "name": "db.bind", "type": None},
            ],
            "name": "Product",
            "parents": ["db.Entity"],
            "properties": {},
        }
    ]
    assert result == expected
