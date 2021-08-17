from py_models_parser import parse


def test_encode_orm():
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "Integer",
                },
                {
                    "default": None,
                    "name": "text",
                    "properties": {"index": "True", "max_length": "100"},
                    "type": "String",
                },
                {
                    "default": "False",
                    "name": "completed",
                    "properties": {},
                    "type": "Boolean",
                },
            ],
            "name": "Note",
            "parents": ["orm.Model"],
            "properties": {
                "__database__": "database",
                "__metadata__": "metadata",
                "table_name": '"notes"',
            },
        }
    ]

    model = """
    import databases
    import orm
    import sqlalchemy

    database = databases.Database("sqlite:///db.sqlite")
    metadata = sqlalchemy.MetaData()


    class Note(orm.Model):
        __tablename__ = "notes"
        __database__ = database
        __metadata__ = metadata

        id = orm.Integer(primary_key=True)
        text = orm.String(max_length=100, index=True)
        completed = orm.Boolean(default=False)

    """

    result = parse(model)
    assert result == expected


def test_encode_foreign_keys():
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "Integer",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {"max_length": "100"},
                    "type": "String",
                },
            ],
            "name": "Album",
            "parents": ["orm.Model"],
            "properties": {
                "__database__": "database",
                "__metadata__": "metadata",
                "table_name": '"album"',
            },
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "Integer",
                },
                {
                    "default": None,
                    "name": "album",
                    "properties": {"foreign_key": "Album"},
                    "type": "Integer",
                },
                {
                    "default": None,
                    "name": "title",
                    "properties": {"max_length": "100"},
                    "type": "String",
                },
                {
                    "default": None,
                    "name": "position",
                    "properties": {},
                    "type": "Integer",
                },
            ],
            "name": "Track",
            "parents": ["orm.Model"],
            "properties": {
                "__database__": "database",
                "__metadata__": "metadata",
                "table_name": '"track"',
            },
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "Integer",
                },
                {
                    "default": None,
                    "name": "ident",
                    "properties": {"max_length": "100"},
                    "type": "String",
                },
            ],
            "name": "Organisation",
            "parents": ["orm.Model"],
            "properties": {
                "__database__": "database",
                "__metadata__": "metadata",
                "table_name": '"org"',
            },
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "Integer",
                },
                {
                    "default": None,
                    "name": "org",
                    "properties": {"foreign_key": "Organisation"},
                    "type": "Integer",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {"max_length": "100"},
                    "type": "String",
                },
            ],
            "name": "Team",
            "parents": ["orm.Model"],
            "properties": {
                "__database__": "database",
                "__metadata__": "metadata",
                "table_name": '"team"',
            },
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "Integer",
                },
                {
                    "default": None,
                    "name": "team",
                    "properties": {"foreign_key": "Team"},
                    "type": "Integer",
                },
                {
                    "default": None,
                    "name": "email",
                    "properties": {"max_length": "100"},
                    "type": "String",
                },
            ],
            "name": "Member",
            "parents": ["orm.Model"],
            "properties": {
                "__database__": "database",
                "__metadata__": "metadata",
                "table_name": '"member"',
            },
        },
    ]

    model = """

    class Album(orm.Model):
        __tablename__ = "album"
        __metadata__ = metadata
        __database__ = database

        id = orm.Integer(primary_key=True)
        name = orm.String(max_length=100)


    class Track(orm.Model):
        __tablename__ = "track"
        __metadata__ = metadata
        __database__ = database

        id = orm.Integer(primary_key=True)
        album = orm.ForeignKey(Album)
        title = orm.String(max_length=100)
        position = orm.Integer()


    class Organisation(orm.Model):
        __tablename__ = "org"
        __metadata__ = metadata
        __database__ = database

        id = orm.Integer(primary_key=True)
        ident = orm.String(max_length=100)


    class Team(orm.Model):
        __tablename__ = "team"
        __metadata__ = metadata
        __database__ = database

        id = orm.Integer(primary_key=True)
        org = orm.ForeignKey(Organisation)
        name = orm.String(max_length=100)


    class Member(orm.Model):
        __tablename__ = "member"
        __metadata__ = metadata
        __database__ = database

        id = orm.Integer(primary_key=True)
        team = orm.ForeignKey(Team)
        email = orm.String(max_length=100)
    """

    result = parse(model)
    assert result == expected
