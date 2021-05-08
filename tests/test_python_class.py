from py_models_parser import parse


def test_parse_attrs_from_init():
    model = """
class ComplexNumber:

    a = 100
    b = 'b'
    c: str = 'default'

    def __init__(self, r=0, i=0, j:int=0):
        self.real = r
        self.imag = i

    def get_data(self, k):
        print(f'{self.real}+{self.imag}j')

"""

    result = parse(model)
    expected = [
        {
            "attrs": [
                {"default": "100", "name": "a", "properties": {}, "type": None},
                {"default": "'b'", "name": "b", "properties": {}, "type": None},
                {"default": "'default'", "name": "c", "properties": {}, "type": "str"},
            ],
            "name": "ComplexNumber",
            "parents": [],
            "properties": {
                "init": [
                    {"default": "0", "name": "r", "properties": {}, "type": None},
                    {"default": "0", "name": "i", "properties": {}, "type": None},
                    {"default": "0", "name": "j", "properties": {}, "type": "int"},
                ]
            },
        }
    ]
    assert result == expected
