from py_models_parser import parse


def test_multiple_class_defs():
    models_str = """from gino import Gino

    db = Gino()

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

    class User4:

        __tablename__ = 'users4'
        id = db.Column(db.Integer)

    class User3():

        __tablename__ = 'users3'
        id = db.Column(db.Integer)

    class Users2(db.Model):

        __tablename__ = 'users2'
        id = db.Column
    """
    result = parse(models_str)
    excepted = [
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
                    "name": "db",
                    "properties": {},
                    "type": "db.String()",
                },
                {
                    "default": None,
                    "name": "created_at",
                    "properties": {},
                    "type": "db.TIMESTAMP()",
                },
                {
                    "default": None,
                    "name": "updated_at",
                    "properties": {},
                    "type": "db.TIMESTAMP()",
                },
                {
                    "default": None,
                    "name": "country_code",
                    "properties": {},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "default_language",
                    "properties": {},
                    "type": "db.Integer()",
                },
            ],
            "name": "Users",
            "parents": ["db.Model"],
            "properties": {"table_name": "'users'"},
        },
        {
            "attrs": [
                {"default": None, "name": "id", "properties": {}, "type": "db.Integer"}
            ],
            "name": "User4",
            "parents": [],
            "properties": {"table_name": "'users4'"},
        },
        {
            "attrs": [
                {"default": None, "name": "id", "properties": {}, "type": "db.Integer"}
            ],
            "name": "User3",
            "parents": [],
            "properties": {"table_name": "'users3'"},
        },
        {
            "attrs": [
                {"default": "db.Column", "name": "id", "properties": {}, "type": None}
            ],
            "name": "Users2",
            "parents": ["db.Model"],
            "properties": {"table_name": "'users2'"},
        },
    ]
    assert result == excepted


def test_complex_syntax_in_columns_and_table_args():

    models_str = """from gino import Gino

        db = Gino()

        from gino import Gino

        db = Gino()

    class Languages(db.Model):

        __tablename__ = 'languages'

        id = db.Column(db.Integer(), primary_key=True)
        code = db.Column(db.String(2), nullable=False)
        name = db.Column(db.String(), nullable=False)
        field_3 = db.Column(ARRAY(db.String()), nullable=False, server_default=func.now())
        squares = db.Column(ARRAY(db.Integer()), nullable=False, server_default='{1}')
        schedule = db.Column(ARRAY(db.Text()))

    class Table(db.Model):

        __tablename__ = 'table'

        _id = db.Column(UUID, primary_key=True)
        one_more_id = db.Column(db.Integer())

        __table_args__ = (

        UniqueConstraint(one_more_id, name='table_pk'),
        Index('table_ix2', _id),
        dict(schema="prefix--schema-name")
                )

    """
    result = parse(models_str)
    excepted = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "code",
                    "properties": {"nullable": "False"},
                    "type": "db.String(2)",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {"nullable": "False"},
                    "type": "db.String()",
                },
                {
                    "default": None,
                    "name": "field_3",
                    "properties": {"nullable": "False", "server_default": "func.now()"},
                    "type": "ARRAY(db.String())",
                },
                {
                    "default": None,
                    "name": "squares",
                    "properties": {"nullable": "False", "server_default": "'{1}'"},
                    "type": "ARRAY(db.Integer())",
                },
                {
                    "default": None,
                    "name": "schedule",
                    "properties": {},
                    "type": "ARRAY(db.Text())",
                },
            ],
            "name": "Languages",
            "parents": ["db.Model"],
            "properties": {"table_name": "'languages'"},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "_id",
                    "properties": {"primary_key": "True"},
                    "type": "UUID",
                },
                {
                    "default": None,
                    "name": "one_more_id",
                    "properties": {},
                    "type": "db.Integer()",
                },
            ],
            "name": "Table",
            "parents": ["db.Model"],
            "properties": {
                "__table_args__": "(\n"
                "        UniqueConstraint(one_more_id, "
                "name='table_pk'),\n"
                "        Index('table_ix2', _id),\n"
                "        "
                'dict(schema="prefix--schema-name")\n'
                "                )",
                "table_name": "'table'",
            },
        },
    ]

    assert result == excepted


def test_with_foreign_keys_with_params():
    models_str = """from gino import Gino

db = Gino()


class OrderItems(db.Model):

    __tablename__ = 'order_items'

    product_no = db.Column(db.Integer(), db.ForeignKey('products.product_no'), ondelete="RESTRICT", primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('orders.order_id'), ondelete="CASCADE", primary_key=True)
    type = db.Column(db.Integer(), db.ForeignKey('types.type_id'), ondelete="RESTRICT", onupdate="CASCADE")
    """
    result = parse(models_str)
    excepted = [
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
    assert result == excepted


def test_foreign_keys():
    models_str = """
    class MaterialAttachments(db.Model):

        __tablename__ = 'material_attachments'

        material_id = db.Column(db.Integer(), db.ForeignKey('materials.id'), default=1)
        attachment_id = db.Column(db.Integer(), db.ForeignKey('attachments.id'))


    class Attachments(db.Model):

        __tablename__ = 'attachments'

        id = db.Column(db.Integer(), primary_key=True)
        title = db.Column(db.String())
        description = db.Column(db.String())
        created_at = db.Column(db.TIMESTAMP())
        updated_at = db.Column(db.TIMESTAMP())
    """
    result = parse(models_str)
    excepted = [
        {
            "attrs": [
                {
                    "default": "1",
                    "name": "material_id",
                    "properties": {"foreign_key": "'materials.id'"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "attachment_id",
                    "properties": {"foreign_key": "'attachments.id'"},
                    "type": "db.Integer()",
                },
            ],
            "name": "MaterialAttachments",
            "parents": ["db.Model"],
            "properties": {"table_name": "'material_attachments'"},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "db.Integer()",
                },
                {
                    "default": None,
                    "name": "title",
                    "properties": {},
                    "type": "db.String()",
                },
                {
                    "default": None,
                    "name": "description",
                    "properties": {},
                    "type": "db.String()",
                },
                {
                    "default": None,
                    "name": "created_at",
                    "properties": {},
                    "type": "db.TIMESTAMP()",
                },
                {
                    "default": None,
                    "name": "updated_at",
                    "properties": {},
                    "type": "db.TIMESTAMP()",
                },
            ],
            "name": "Attachments",
            "parents": ["db.Model"],
            "properties": {"table_name": "'attachments'"},
        },
    ]
    assert result == excepted
