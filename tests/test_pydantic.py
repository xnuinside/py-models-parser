from py_models_parser.core import parse


def test_pydantic_with_defaults():
    models_str = """
    class Material(BaseModel):

        id: int
        title: str
        description: Optional[str]
        link: str = 'http://'
        type: Optional[MaterialType]
        additional_properties: Optional[Json]
        created_at: Optional[datetime.datetime] = datetime.datetime.now()
        updated_at: Optional[datetime.datetime]
    """
    result = parse(models_str)
    excepted = [
        {
            "attrs": [
                {"default": None, "name": "id", "type": "int"},
                {"default": None, "name": "title", "type": "str"},
                {"default": None, "name": "description", "type": "Optional[str]"},
                {
                    "default": "'http://'",
                    "name": "link",
                    "properties": {},
                    "type": "str",
                },
                {"default": None, "name": "type", "type": "Optional[MaterialType]"},
                {
                    "default": None,
                    "name": "additional_properties",
                    "type": "Optional[Json]",
                },
                {
                    "default": "datetime.datetime.now()",
                    "name": "created_at",
                    "properties": {},
                    "type": "Optional[datetime.datetime]",
                },
                {
                    "default": None,
                    "name": "updated_at",
                    "type": "Optional[datetime.datetime]",
                },
            ],
            "name": "Material",
            "parents": ["BaseModel"],
            "properties": {},
        }
    ]
    assert result == excepted
