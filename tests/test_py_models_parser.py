import pathlib

from py_models_parser import parse_from_file
from py_models_parser.core import pre_processing


def test_pre_processing():
    models_str = """
from gino import Gino

db = Gino()


class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    db = db.Column(db.String())
    created_at = db.Column(db.TIMESTAMP())
    updated_at = db.Column(db.TIMESTAMP())
    country_code = db.Column(db.Integer())
    default_language = db.Column(db.Integer())
"""
    result = pre_processing(models_str)
    excepted = """class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    db = db.Column(db.String())
    created_at = db.Column(db.TIMESTAMP())
    updated_at = db.Column(db.TIMESTAMP())
    country_code = db.Column(db.Integer())
    default_language = db.Column(db.Integer())"""
    assert result == excepted


def test_parse_from_file_gino():
    file_path = pathlib.Path(__file__).parent / "data" / "gino_models.py"
    result = parse_from_file(file_path)
    expected = [
        {
            "attrs": [
                {
                    "default": "'article'",
                    "name": "article",
                    "properties": {},
                    "type": None,
                },
                {"default": "'video'", "name": "video", "properties": {}, "type": None},
            ],
            "name": "MaterialType",
            "parents": ["Enum"],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"autoincrement": "True", "primary_key": "True"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "title",
                    "properties": {"nullable": "False"},
                    "type": "db.String()",
                },
                {
                    "default": None,
                    "name": "description",
                    "properties": {},
                    "type": "db.Text()",
                },
                {
                    "default": None,
                    "name": "link",
                    "properties": {"nullable": "False"},
                    "type": "db.String()",
                },
                {
                    "default": None,
                    "name": "type",
                    "properties": {},
                    "type": "db.Enum(MaterialType)",
                },
                {
                    "default": None,
                    "name": "additional_properties",
                    "properties": {},
                    "type": "JSON()",
                },
                {
                    "default": None,
                    "name": "created_at",
                    "properties": {"server_default": "func.now()"},
                    "type": "db.TIMESTAMP()",
                },
                {
                    "default": None,
                    "name": "updated_at",
                    "properties": {},
                    "type": "db.TIMESTAMP()",
                },
            ],
            "name": "Material",
            "parents": ["db.Model"],
            "properties": {"table_name": "'material'"},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"autoincrement": "True", "primary_key": "True"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {},
                    "type": "db.String()",
                },
                {
                    "default": None,
                    "name": "link",
                    "properties": {},
                    "type": "db.String()",
                },
            ],
            "name": "Author",
            "parents": ["db.Model"],
            "properties": {"table_name": "'author'"},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "category",
                    "properties": {"foreign_key": "'author.id'"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "material",
                    "properties": {"foreign_key": "'material.id'"},
                    "type": "db.Integer()",
                },
            ],
            "name": "MaterialAuthors",
            "parents": ["db.Model"],
            "properties": {"table_name": "'material_authors'"},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "category",
                    "properties": {"foreign_key": "'platform.id'"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "material",
                    "properties": {"foreign_key": "'material.id'"},
                    "type": "db.Integer()",
                },
            ],
            "name": "MaterialPlatforms",
            "parents": ["db.Model"],
            "properties": {"table_name": "'material_platforms'"},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"autoincrement": "True", "primary_key": "True"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {"nullable": "False"},
                    "type": "db.String()",
                },
                {
                    "default": None,
                    "name": "link",
                    "properties": {"nullable": "False"},
                    "type": "db.String()",
                },
            ],
            "name": "Platform",
            "parents": ["db.Model"],
            "properties": {"table_name": "'platform'"},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "category",
                    "properties": {"foreign_key": "'category.id'"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "material",
                    "properties": {"foreign_key": "'material.id'"},
                    "type": "db.Integer()",
                },
            ],
            "name": "MaterialCategories",
            "parents": ["db.Model"],
            "properties": {"table_name": "'material_categories'"},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"autoincrement": "True", "primary_key": "True"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {"nullable": "False"},
                    "type": "db.String()",
                },
                {
                    "default": None,
                    "name": "description",
                    "properties": {},
                    "type": "db.Text()",
                },
                {
                    "default": None,
                    "name": "created_at",
                    "properties": {"server_default": "func.now()"},
                    "type": "db.TIMESTAMP()",
                },
                {
                    "default": None,
                    "name": "updated_at",
                    "properties": {},
                    "type": "db.TIMESTAMP()",
                },
            ],
            "name": "Category",
            "parents": ["db.Model"],
            "properties": {"table_name": "'category'"},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "category",
                    "properties": {"foreign_key": "'category.id'"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "channels",
                    "properties": {},
                    "type": "ARRAY(db.String())",
                },
                {
                    "default": None,
                    "name": "words",
                    "properties": {},
                    "type": "ARRAY(db.String())",
                },
                {
                    "default": None,
                    "name": "created_at",
                    "properties": {"server_default": "func.now()"},
                    "type": "db.TIMESTAMP()",
                },
                {
                    "default": None,
                    "name": "updated_at",
                    "properties": {},
                    "type": "db.TIMESTAMP()",
                },
            ],
            "name": "ContentFilters",
            "parents": ["db.Model"],
            "properties": {"table_name": "'content_filters'"},
        },
    ]
    assert result == expected


def test_parse_from_file_dataclass():
    file_path = pathlib.Path(__file__).parent / "data" / "dataclass_defaults.py"
    result = parse_from_file(file_path)
    expected = [
        {
            "attrs": [
                {
                    "default": "'article'",
                    "name": "article",
                    "properties": {},
                    "type": None,
                },
                {"default": "'video'", "name": "video", "properties": {}, "type": None},
            ],
            "name": "MaterialType",
            "parents": ["str, Enum"],
            "properties": {},
        },
        {
            "attrs": [
                {"default": None, "name": "id", "type": "int"},
                {"default": None, "name": "title", "type": "str"},
                {"default": None, "name": "link", "type": "str"},
                {
                    "default": "None",
                    "name": "description",
                    "properties": {},
                    "type": "str",
                },
                {
                    "default": "None",
                    "name": "type",
                    "properties": {},
                    "type": "MaterialType",
                },
                {
                    "default": "None",
                    "name": "additional_properties",
                    "properties": {},
                    "type": "Union[dict, list]",
                },
                {
                    "default": "datetime.datetime.now()",
                    "name": "created_at",
                    "properties": {},
                    "type": "datetime.datetime",
                },
                {
                    "default": "None",
                    "name": "updated_at",
                    "properties": {},
                    "type": "datetime.datetime",
                },
            ],
            "name": "Material",
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {"default": None, "name": "id", "type": "int"},
                {"default": "None", "name": "name", "properties": {}, "type": "str"},
                {"default": "None", "name": "link", "properties": {}, "type": "str"},
            ],
            "name": "Author",
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": "None",
                    "name": "category",
                    "properties": {},
                    "type": "int",
                },
                {
                    "default": "None",
                    "name": "material",
                    "properties": {},
                    "type": "int",
                },
            ],
            "name": "MaterialAuthors",
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": "None",
                    "name": "category",
                    "properties": {},
                    "type": "int",
                },
                {
                    "default": "None",
                    "name": "material",
                    "properties": {},
                    "type": "int",
                },
            ],
            "name": "MaterialPlatforms",
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {"default": None, "name": "id", "type": "int"},
                {"default": None, "name": "name", "type": "str"},
                {"default": None, "name": "link", "type": "str"},
            ],
            "name": "Platform",
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": "None",
                    "name": "category",
                    "properties": {},
                    "type": "int",
                },
                {
                    "default": "None",
                    "name": "material",
                    "properties": {},
                    "type": "int",
                },
            ],
            "name": "MaterialCategories",
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {"default": None, "name": "id", "type": "int"},
                {"default": None, "name": "name", "type": "str"},
                {
                    "default": "None",
                    "name": "description",
                    "properties": {},
                    "type": "str",
                },
                {
                    "default": "datetime.datetime.now()",
                    "name": "created_at",
                    "properties": {},
                    "type": "datetime.datetime",
                },
                {
                    "default": "None",
                    "name": "updated_at",
                    "properties": {},
                    "type": "datetime.datetime",
                },
            ],
            "name": "Category",
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": "None",
                    "name": "category",
                    "properties": {},
                    "type": "int",
                },
                {
                    "default": "None",
                    "name": "channels",
                    "properties": {},
                    "type": "List[str]",
                },
                {
                    "default": "None",
                    "name": "words",
                    "properties": {},
                    "type": "List[str]",
                },
                {
                    "default": "datetime.datetime.now()",
                    "name": "created_at",
                    "properties": {},
                    "type": "datetime.datetime",
                },
                {
                    "default": "None",
                    "name": "updated_at",
                    "properties": {},
                    "type": "datetime.datetime",
                },
            ],
            "name": "ContentFilters",
            "parents": [],
            "properties": {},
        },
    ]
    assert result == expected
