from py_models_parser import parse


def test_model_with_foreign():

    model = """from django.db import models

    class Musician(models.Model):
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        instrument = models.CharField(max_length=100)

    class Album(models.Model):
        artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
        name = models.CharField(max_length=100)
        release_date = models.DateField()
        num_stars = models.IntegerField()
        """
    result = parse(model)
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "first_name",
                    "properties": {"max_length": "50"},
                    "type": "Char",
                },
                {
                    "default": None,
                    "name": "last_name",
                    "properties": {"max_length": "50"},
                    "type": "Char",
                },
                {
                    "default": None,
                    "name": "instrument",
                    "properties": {"max_length": "100"},
                    "type": "Char",
                },
            ],
            "name": "Musician",
            "parents": ["models.Model"],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "artist",
                    "properties": {
                        "foreign_key": "Musician",
                        "on_delete": "models.CASCADE",
                    },
                    "type": "serial",
                },
                {
                    "default": None,
                    "name": "name",
                    "properties": {"max_length": "100"},
                    "type": "Char",
                },
                {
                    "default": None,
                    "name": "release_date",
                    "properties": {},
                    "type": "Date",
                },
                {
                    "default": None,
                    "name": "num_stars",
                    "properties": {},
                    "type": "Integer",
                },
            ],
            "name": "Album",
            "parents": ["models.Model"],
            "properties": {},
        },
    ]
    assert result == expected


def test_many_to_many():
    expected = [
        {
            "attrs": [{"default": None, "name": "pass", "type": None}],
            "name": "Topping",
            "parents": ["models.Model"],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "toppings",
                    "properties": {"foreign_key": "Topping"},
                    "type": "ManyToMany",
                }
            ],
            "name": "Pizza",
            "parents": ["models.Model"],
            "properties": {},
        },
    ]
    model = """from django.db import models

class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)"""
    result = parse(model)
    assert result == expected


def test_many_to_many_combine():
    model = """from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)"""
    result = parse(model)
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "name",
                    "properties": {"max_length": "128"},
                    "type": "Char",
                }
            ],
            "name": "Person",
            "parents": ["models.Model"],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "name",
                    "properties": {"max_length": "128"},
                    "type": "Char",
                },
                {
                    "default": None,
                    "name": "members",
                    "properties": {"foreign_key": "Person", "through": "'Membership'"},
                    "type": "ManyToMany",
                },
            ],
            "name": "Group",
            "parents": ["models.Model"],
            "properties": {},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "person",
                    "properties": {
                        "foreign_key": "Person",
                        "on_delete": "models.CASCADE",
                    },
                    "type": "serial",
                },
                {
                    "default": None,
                    "name": "group",
                    "properties": {
                        "foreign_key": "Group",
                        "on_delete": "models.CASCADE",
                    },
                    "type": "serial",
                },
                {
                    "default": None,
                    "name": "date_joined",
                    "properties": {},
                    "type": "Date",
                },
                {
                    "default": None,
                    "name": "invite_reason",
                    "properties": {"max_length": "64"},
                    "type": "Char",
                },
            ],
            "name": "Membership",
            "parents": ["models.Model"],
            "properties": {},
        },
    ]
    assert result == expected


def test_simple_table_meta():
    model = """
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"
"""
    result = parse(model)
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "horn_length",
                    "properties": {},
                    "type": "Integer",
                }
            ],
            "name": "Ox",
            "parents": ["models.Model"],
            "properties": {
                "ordering": '["horn_length"]',
                "verbose_name_plural": '"oxen"',
            },
        }
    ]
    assert result == expected


def test_two_tables_meta():

    model = """
    from django.db import models

    class Publication(models.Model):
        title = models.CharField(max_length=30)

        class Meta:
            ordering = ['title']

        def __str__(self):
            return self.title

    class Article(models.Model):
        headline = models.CharField(max_length=100)
        publications = models.ManyToManyField(Publication)

        class Meta:
            ordering = ['headline']

        def __str__(self):
            return self.headline
    """

    result = parse(model)
    expected = [
        {
            "attrs": [
                {
                    "default": None,
                    "name": "title",
                    "properties": {"max_length": "30"},
                    "type": "Char",
                }
            ],
            "name": "Publication",
            "parents": ["models.Model"],
            "properties": {"ordering": "['title']"},
        },
        {
            "attrs": [
                {
                    "default": None,
                    "name": "headline",
                    "properties": {"max_length": "100"},
                    "type": "Char",
                },
                {
                    "default": None,
                    "name": "publications",
                    "properties": {"foreign_key": "Publication"},
                    "type": "ManyToMany",
                },
            ],
            "name": "Article",
            "parents": ["models.Model"],
            "properties": {"ordering": "['headline']"},
        },
    ]
    assert result == expected
