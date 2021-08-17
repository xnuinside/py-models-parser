from py_models_parser import parse


def test_simple_piccolo():

    model = """
    class Band(Table, tablename="music_band"):
        id = UUID(primary_key=True)
        name = Varchar(length=100)
    """

    result = parse(model)
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"primary_key": "True"},
                    "type": "UUID",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {"length": "100"},
                    "type": "Varchar",
                },
            ],
            "name": "Band",
            "parents": ["Table"],
            "properties": {"table_name": '"music_band"'},
        }
    ]
    assert result == expected
