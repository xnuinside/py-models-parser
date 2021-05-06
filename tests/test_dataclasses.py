from py_models_parser import parse

def test_dataclasses():
    expected = [{'attrs': [{'default': "'article'",
             'name': 'article',
             'properties': {},
             'type': None},
            {'default': "'video'",
             'name': 'video',
             'properties': {},
             'type': None}],
  'name': 'MaterialType',
  'parents': ['str, Enum'],
  'properties': {}},
 {'attrs': [{'default': None, 'name': 'id', 'type': 'int'},
            {'default': 'None',
             'name': 'description',
             'properties': {},
             'type': 'str'},
            {'default': 'None',
             'name': 'additional_properties',
             'properties': {},
             'type': 'Union[dict, list, tuple, anything]'},
            {'default': 'datetime.datetime.now()',
             'name': 'created_at',
             'properties': {},
             'type': 'datetime.datetime'},
            {'default': 'None',
             'name': 'updated_at',
             'properties': {},
             'type': 'datetime.datetime'}],
  'name': 'Material',
  'parents': [],
  'properties': {}},
 {'attrs': [{'default': None, 'name': 'id', 'type': 'int'},
            {'default': 'None',
             'name': 'description',
             'properties': {},
             'type': 'str'},
            {'default': 'None',
             'name': 'additional_properties',
             'properties': {},
             'type': 'Union[dict, list]'},
            {'default': 'datetime.datetime.now()',
             'name': 'created_at',
             'properties': {},
             'type': 'datetime.datetime'},
            {'default': 'None',
             'name': 'updated_at',
             'properties': {},
             'type': 'datetime.datetime'}],
  'name': 'Material2',
  'parents': [],
  'properties': {}}]
    model = """

    class MaterialType(str, Enum):

        article = 'article'
        video = 'video'


    @dataclass
    class Material:

        id: int
        description: str = None
        additional_properties: Union[dict, list, tuple, anything] = None
        created_at: datetime.datetime = datetime.datetime.now()
        updated_at: datetime.datetime = None

    @dataclass
    class Material2:

        id: int
        description: str = None
        additional_properties: Union[dict, list] = None
        created_at: datetime.datetime = datetime.datetime.now()
        updated_at: datetime.datetime = None

    """
    result = parse(model)
    assert result == expected