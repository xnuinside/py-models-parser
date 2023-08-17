from py_models_parser import parse


def test_simple_example():
    models_str = """
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __repr__(self):
            return '<User %r>' % self.username
    """
    result = parse(models_str)
    excepted = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "db.Integer",
                },
                {
                    "default": None,
                    "name": "username",
                    "properties": {"nullable": "False", "unique": "True"},
                    "type": "db.String(80)",
                },
                {
                    "default": None,
                    "name": "email",
                    "properties": {"nullable": "False", "unique": "True"},
                    "type": "db.String(120)",
                },
            ],
            "name": "User",
            "parents": ["db.Model"],
            "properties": {},
        }
    ]
    assert result == excepted


def test_foreign_keys():
    models_str = """
    class Person(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        addresses = db.relationship('Address', backref='person', lazy=True)

    class Address(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), nullable=False)
        person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
            nullable=False)
    """
    result = parse(models_str)
    excepted = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "db.Integer",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {"nullable": "False"},
                    "type": "db.String(50)",
                },
                {
                    "default": None,
                    "name": "addresses",
                    "properties": {
                        "backref": "'person'",
                        "lazy": "True",
                        "relationship": True,
                    },
                    "type": "'Address'",
                },
            ],
            "name": "Person",
            "parents": ["db.Model"],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "db.Integer",
                },
                {
                    "default": None,
                    "name": "email",
                    "properties": {"nullable": "False"},
                    "type": "db.String(120)",
                },
                {
                    "default": None,
                    "name": "person_id",
                    "properties": {"foreign_key": "'person.id'", "nullable": "False"},
                    "type": "db.Integer",
                },
            ],
            "name": "Address",
            "parents": ["db.Model"],
            "properties": {},
        },
    ]
    assert result == excepted


def test_with_relationship():
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "db.Integer",
                },
                {
                    "default": None,
                    "name": "tags",
                    "properties": {
                        "backref": "db.backref('pages', lazy=True)",
                        "lazy": "'subquery'",
                        "relationship": True,
                        "secondary": "tags",
                    },
                    "type": "'Tag'",
                },
            ],
            "name": "Page",
            "parents": ["db.Model"],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "db.Integer",
                }
            ],
            "name": "Tag",
            "parents": ["db.Model"],
            "properties": {},
        },
    ]
    models_str = """
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('pages', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
"""
    result = parse(models_str)
    assert result == expected
