from py_models_parser.core import parse


def test_simple_enum():
    excepted = [
        {
            "attrs": [
                {"default": "'HTML'", "name": "HTML", "properties": {}, "type": None},
                {
                    "default": "'MARKDOWN'",
                    "name": "MARKDOWN",
                    "properties": {},
                    "type": None,
                },
                {"default": "'TEXT'", "name": "TEXT", "properties": {}, "type": None},
            ],
            "name": "ContentType",
            "parents": ["Enum"],
            "properties": {},
        }
    ]

    models_str = """
    from enum import Enum

    class ContentType(Enum):

        HTML = 'HTML'
        MARKDOWN = 'MARKDOWN'
        TEXT = 'TEXT'

    """
    result = parse(models_str)
    assert result == excepted


def test_int_enum():
    expected = [
        {
            "attrs": [
                {"default": "'HTML'", "name": "HTML", "properties": {}, "type": None},
                {
                    "default": "'MARKDOWN'",
                    "name": "MARKDOWN",
                    "properties": {},
                    "type": None,
                },
                {"default": "'TEXT'", "name": "TEXT", "properties": {}, "type": None},
            ],
            "name": "ContentType",
            "parents": ["str, Enum"],
            "properties": {},
        },
        {
            "attrs": [
                {"default": "0", "name": "zero", "properties": {}, "type": None},
                {"default": "1", "name": "one", "properties": {}, "type": None},
                {"default": "2", "name": "two", "properties": {}, "type": None},
            ],
            "name": "Period",
            "parents": ["IntEnum"],
            "properties": {},
        },
    ]

    models_str = """    from enum import IntEnum,Enum
from typing import Optional
from pydantic import BaseModel


class ContentType(str, Enum):

    HTML = 'HTML'
    MARKDOWN = 'MARKDOWN'
    TEXT = 'TEXT'


class Period(IntEnum):

    zero = 0
    one = 1
    two = 2

"""
    result = parse(models_str)
    assert result == expected
