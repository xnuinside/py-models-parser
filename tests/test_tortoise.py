from py_models_parser import parse


def test_tortoise_two_models():
    models_str = """from tortoise import Tortoise, fields, run_async
    from tortoise.models import Model


    class Event(Model):
        id = fields.IntField(pk=True)
        name = TextField()
        datetime = fields.DatetimeField(null=True)

        class Meta:
            table = "event"


    class Event2(Model):
        id = fields.IntField(pk=True)
        name = fields.TextField(description="Name of the event that corresponds to an action")
        datetime = fields.DatetimeField(
            null=True, description="Datetime of when the event was generated"
        )

        class Meta:
            table = "event"
            table_description = "This table contains a list of all the example events"

        def __str__(self):
            return self.name

    """
    result = parse(models_str)
    excepted = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"pk": "True"},
                    "type": "Int",
                },
                {"default": None, "name": "name", "properties": {}, "type": "Text"},
                {
                    "default": None,
                    "name": "datetime",
                    "properties": {"null": "True"},
                    "type": "Datetime",
                },
            ],
            "name": "Event",
            "parents": ["Model"],
            "properties": {"table": '"event"'},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"pk": "True"},
                    "type": "Int",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {
                        "description": '"Name of the event that '
                        'corresponds to an action"'
                    },
                    "type": "Text",
                },
                {
                    "default": None,
                    "name": "datetime",
                    "properties": {
                        "description": '"Datetime of when the event was ' 'generated"',
                        "null": "True",
                    },
                    "type": "Datetime",
                },
            ],
            "name": "Event2",
            "parents": ["Model"],
            "properties": {
                "table": '"event"',
                "table_description": '"This table contains a list of all the '
                'example events"',
            },
        },
    ]
    assert result == excepted


def test_full_tortoise_example_from_docs():
    models_str = '''
    """
    This example demonstrates most basic operations with single model
    and a Table definition generation with comment support
    """
    from tortoise import Tortoise, fields, run_async
    from tortoise.models import Model


    class Event(Model):
        id = fields.IntField(pk=True)
        name = fields.TextField(description="Name of the event that corresponds to an action")
        datetime = fields.DatetimeField(
            null=True, description="Datetime of when the event was generated"
        )

        class Meta:
            table = "event"
            table_description = "This table contains a list of all the example events"

        def __str__(self):
            return self.name


    async def run():
        await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
        await Tortoise.generate_schemas()

        event = await Event.create(name="Test")
        await Event.filter(id=event.id).update(name="Updated name")

        print(await Event.filter(name="Updated name").first())

        await Event(name="Test 2").save()
        print(await Event.all().values_list("id", flat=True))
        print(await Event.all().values("id", "name"))


    if __name__ == "__main__":
        run_async(run())
    '''
    result = parse(models_str)
    excepted = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "id",
                    "properties": {"pk": "True"},
                    "type": "Int",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {
                        "description": '"Name of the event that '
                        'corresponds to an action"'
                    },
                    "type": "Text",
                },
                {
                    "default": None,
                    "name": "datetime",
                    "properties": {
                        "description": '"Datetime of when the event was ' 'generated"',
                        "null": "True",
                    },
                    "type": "Datetime",
                },
            ],
            "name": "Event",
            "parents": ["Model"],
            "properties": {
                "table": '"event"',
                "table_description": '"This table contains a list of all the '
                'example events"',
            },
        }
    ]
    assert result == excepted
