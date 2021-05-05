from py_models_parser.core import parse

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

import pprint

pprint.pprint(result)
