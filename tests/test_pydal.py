from py_models_parser import parse


def test_simple_pydal_example():
    expected = [
        {
            "attrs": [
                {"default": None, "name": "'name'", "properties": {}, "type": None},
                {
                    "default": None,
                    "name": "'price'",
                    "properties": {},
                    "type": "'integer'",
                },
            ],
            "name": "'cars'",
            "parents": [],
            "properties": {},
        }
    ]

    model = """
    #!/usr/bin/env python3

    from pydal import DAL, Field

    db = DAL('sqlite://test.db', folder='dbs')

    try:
        db.define_table('cars', Field('name'), Field('price', type='integer'))
        db.cars.insert(name='Audi', price=52642)
        db.cars.insert(name='Skoda', price=9000)
        db.cars.insert(name='Volvo', price=29000)
        db.cars.insert(name='Bentley', price=350000)
        db.cars.insert(name='Citroen', price=21000)
        db.cars.insert(name='Hummer', price=41400)
        db.cars.insert(name='Volkswagen', price=21600)

    finally:

        if db:
            db.close()
    """

    result = parse(model)
    assert result == expected


def test_two_tables_type_in_args():
    model = """
    #!/usr/bin/env python3

    from pydal import DAL, Field

    db = DAL('sqlite://test.db', folder='dbs')

    try:
        db.define_table('cars', Field('name'), Field('price', type='integer'))
        db.define_table('cars2', Field('name'), Field('price', 'integer'))
        db.cars.insert(name='Audi', price=52642)

    finally:

        if db:
            db.close()
    """

    result = parse(model)
    expected = [
        {
            "attrs": [
                {"default": None, "name": "'name'", "properties": {}, "type": None},
                {
                    "default": None,
                    "name": "'price'",
                    "properties": {},
                    "type": "'integer'",
                },
            ],
            "name": "'cars'",
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {"default": None, "name": "'name'", "properties": {}, "type": None},
                {
                    "default": None,
                    "name": "'price'",
                    "properties": {},
                    "type": "'integer'",
                },
            ],
            "name": "'cars2'",
            "parents": [],
            "properties": {},
        },
    ]
    assert result == expected


def test_table_properties():
    model = """
    #!/usr/bin/env python3

    from pydal import DAL, Field

    db = DAL('sqlite://test.db', folder='dbs')

    try:
        db.define_table('cars2', Field('name'), Field('price', 'integer'))
        db.define_table('cars_with_table_properties', Field('name'),
        Field('price', 'integer'), rname = 'db1.dbo.table1', format=lambda r: r.name or 'anonymous')
        db.cars.insert(name='Audi', price=52642)

    finally:

        if db:
            db.close()
    """

    result = parse(model)
    expected = [
        {
            "attrs": [
                {"default": None, "name": "'name'", "properties": {}, "type": None},
                {
                    "default": None,
                    "name": "'price'",
                    "properties": {},
                    "type": "'integer'",
                },
            ],
            "name": "'cars2'",
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {"default": None, "name": "'name'", "properties": {}, "type": None},
                {
                    "default": None,
                    "name": "'price'",
                    "properties": {
                        "format": "lambda r: r.name or 'anonymous'",
                        "rname ": " 'db1.dbo.table1'",
                    },
                    "type": "'integer'",
                },
            ],
            "name": "'cars_with_table_properties'",
            "parents": [],
            "properties": {
                "format": "lambda r: r.name or 'anonymous'",
                "rname": "'db1.dbo.table1'",
            },
        },
    ]
    assert result == expected


def test_order_params_in_field():
    model = """

    from pydal import DAL, Field

    db = DAL('sqlite://test.db', folder='dbs')

    try:
        db.define_table('cars2', Field('name'), Field('price', 'integer'))
        db.define_table('cars_with_table_properties', Field('name'),
        Field('price', 'integer', 20, 1990, True),
        rname = 'db1.dbo.table1', format=lambda r: r.name or 'anonymous')
        db.cars.insert(name='Audi', price=52642)

    finally:

        if db:
            db.close()
    """

    result = parse(model)

    expected = [
        {
            "attrs": [
                {"default": None, "name": "'name'", "properties": {}, "type": None},
                {
                    "default": None,
                    "name": "'price'",
                    "properties": {},
                    "type": "'integer'",
                },
            ],
            "name": "'cars2'",
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {"default": None, "name": "'name'", "properties": {}, "type": None},
                {
                    "default": "1990",
                    "name": "'price'",
                    "properties": {
                        "format": "lambda r: r.name or 'anonymous'",
                        "length": "20",
                        "required": "True",
                        "rname ": " 'db1.dbo.table1'",
                    },
                    "type": "'integer'",
                },
            ],
            "name": "'cars_with_table_properties'",
            "parents": [],
            "properties": {
                "format": "lambda r: r.name or 'anonymous'",
                "rname": "'db1.dbo.table1'",
            },
        },
    ]
    assert result == expected


def test_definition_inside_methods_works_well():
    model = """
    from pydal import DAL, Field


    def model(dbinfo="sqlite://storage.sqlite", dbfolder="./dados"):
        db = DAL(dbinfo, folder=dbfolder, pool_size=1)
        table(db)
        return db


    def table(db):
        db.define_table("populacao_total",
                        Field("uf", type="string"),
                        Field("populacao", type="double")
                        )
        db.define_table("uf_nome",
                        Field("uf", type="string"),
                        Field("nome", type="string")
                        )


    DB = model()
    """

    result = parse(model)
    expected = [
        {
            "attrs": [
                {"default": None, "name": '"uf"', "properties": {}, "type": '"string"'},
                {
                    "default": None,
                    "name": '"populacao"',
                    "properties": {},
                    "type": '"double"',
                },
            ],
            "name": '"populacao_total"',
            "parents": [],
            "properties": {},
        },
        {
            "attrs": [
                {"default": None, "name": '"uf"', "properties": {}, "type": '"string"'},
                {
                    "default": None,
                    "name": '"nome"',
                    "properties": {},
                    "type": '"string"',
                },
            ],
            "name": '"uf_nome"',
            "parents": [],
            "properties": {},
        },
    ]
    assert result == expected


def test_list_in_primary_key():
    model = """
    db.define_table('account',
                    Field('accnum', 'integer'),
                    Field('acctype'),
                    Field('accdesc'),
                    primarykey=['accnum', 'acctype'],
                    migrate=False)
    """
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "'accnum'",
                    "properties": {},
                    "type": "'integer'",
                },
                {"default": None, "name": "'acctype'", "properties": {}, "type": None},
                {
                    "default": None,
                    "name": "'accdesc'",
                    "properties": {
                        "length": "'acctype']",
                        "migrate": "False",
                        "primarykey": "['accnum'",
                    },
                    "type": None,
                },
            ],
            "name": "'account'",
            "parents": [],
            "properties": {"migrate": "False", "primarykey": "['accnum', 'acctype']"},
        }
    ]

    result = parse(model)
    assert result == expected
