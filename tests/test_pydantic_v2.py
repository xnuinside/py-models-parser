"""Tests for Pydantic v2 models parsing."""
from py_models_parser import parse


def test_pydantic_v2_basic():
    """Test basic Pydantic v2 model."""
    models_str = """
    class User(BaseModel):
        id: int
        name: str
        email: str = "test@example.com"
    """
    result = parse(models_str)

    assert len(result) == 1
    assert result[0]["name"] == "User"
    assert result[0]["parents"] == ["BaseModel"]
    assert len(result[0]["attrs"]) == 3

    id_attr = result[0]["attrs"][0]
    assert id_attr["name"] == "id"
    assert id_attr["type"] == "int"

    email_attr = result[0]["attrs"][2]
    assert email_attr["name"] == "email"
    assert email_attr["default"] == '"test@example.com"'


def test_pydantic_v2_union_types():
    """Test Python 3.10+ union type syntax (PEP 604)."""
    models_str = """
    class Config(BaseModel):
        name: str
        value: int | None = None
        tags: list[str] | None = None
        data: dict[str, int] | list[int] | None = None
    """
    result = parse(models_str)

    assert len(result) == 1
    assert result[0]["name"] == "Config"

    value_attr = next(a for a in result[0]["attrs"] if a["name"] == "value")
    assert value_attr["type"] == "int | None"
    assert value_attr["default"] == "None"

    tags_attr = next(a for a in result[0]["attrs"] if a["name"] == "tags")
    assert tags_attr["type"] == "list[str] | None"


def test_pydantic_v2_field_with_constraints():
    """Test Pydantic v2 Field() with validation constraints."""
    models_str = """
    class Product(BaseModel):
        name: str = Field(max_length=100, description="Product name")
        price: float = Field(gt=0, le=10000)
        quantity: int = Field(default=0, ge=0)
    """
    result = parse(models_str)

    assert len(result) == 1

    name_attr = next(a for a in result[0]["attrs"] if a["name"] == "name")
    assert name_attr["type"] == "str"
    assert name_attr["properties"]["max_length"] == "100"
    assert name_attr["properties"]["description"] == '"Product name"'

    price_attr = next(a for a in result[0]["attrs"] if a["name"] == "price")
    assert price_attr["type"] == "float"
    assert price_attr["properties"]["gt"] == "0"
    assert price_attr["properties"]["le"] == "10000"

    quantity_attr = next(a for a in result[0]["attrs"] if a["name"] == "quantity")
    assert quantity_attr["type"] == "int"
    assert quantity_attr["properties"]["ge"] == "0"


def test_pydantic_v2_model_config():
    """Test Pydantic v2 model_config with ConfigDict."""
    models_str = """
    class Settings(BaseModel):
        model_config = ConfigDict(str_max_length=100, frozen=True)

        name: str
        debug: bool = False
    """
    result = parse(models_str)

    assert len(result) == 1
    assert result[0]["name"] == "Settings"
    assert "model_config" in result[0]["properties"]
    assert "ConfigDict" in result[0]["properties"]["model_config"]
    assert "frozen=True" in result[0]["properties"]["model_config"]

    # Ensure model_config is not in attrs
    attr_names = [a["name"] for a in result[0]["attrs"]]
    assert "model_config" not in attr_names


def test_pydantic_v2_field_with_default():
    """Test Pydantic v2 Field() with default value."""
    models_str = """
    class Order(BaseModel):
        status: str = Field(default="pending")
        items: list[str] = Field(default_factory=list)
    """
    result = parse(models_str)

    status_attr = next(a for a in result[0]["attrs"] if a["name"] == "status")
    assert status_attr["type"] == "str"
    assert status_attr["default"] == '"pending"'


def test_pydantic_v2_optional_fields():
    """Test various optional field syntaxes."""
    models_str = """
    class Profile(BaseModel):
        username: str
        bio: str | None = None
        age: int | None = None
        avatar_url: str | None = Field(default=None, max_length=500)
    """
    result = parse(models_str)

    bio_attr = next(a for a in result[0]["attrs"] if a["name"] == "bio")
    assert bio_attr["type"] == "str | None"
    assert bio_attr["default"] == "None"

    avatar_attr = next(a for a in result[0]["attrs"] if a["name"] == "avatar_url")
    assert avatar_attr["type"] == "str | None"
    assert avatar_attr["properties"]["max_length"] == "500"


def test_pydantic_v2_generic_types():
    """Test generic types like list[str], dict[str, int]."""
    models_str = """
    class Container(BaseModel):
        items: list[str]
        mapping: dict[str, int]
        nested: list[dict[str, str]]
    """
    result = parse(models_str)

    items_attr = next(a for a in result[0]["attrs"] if a["name"] == "items")
    assert items_attr["type"] == "list[str]"

    mapping_attr = next(a for a in result[0]["attrs"] if a["name"] == "mapping")
    assert mapping_attr["type"] == "dict[str, int]"


def test_pydantic_v2_complex_model():
    """Test complex Pydantic v2 model with multiple features."""
    models_str = """
    class ComplexModel(BaseModel):
        model_config = ConfigDict(
            str_strip_whitespace=True,
            validate_default=True
        )

        id: int
        name: str = Field(min_length=1, max_length=100)
        email: str | None = None
        tags: list[str] = []
        metadata: dict[str, str] | None = Field(default=None)
    """
    result = parse(models_str)

    assert len(result) == 1
    assert result[0]["name"] == "ComplexModel"
    assert "model_config" in result[0]["properties"]

    # Check attrs count (should not include model_config)
    assert len(result[0]["attrs"]) == 5
