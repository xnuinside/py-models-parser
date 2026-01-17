"""Tests for OpenAPI 3.0 parser."""
import pytest
from py_models_parser import parse_openapi


def test_simple_openapi_yaml():
    """Test parsing simple OpenAPI schema in YAML format."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
"""
    result = parse_openapi(openapi_spec)

    assert len(result) == 1
    assert result[0]["name"] == "User"
    assert len(result[0]["attrs"]) == 3

    id_attr = next(a for a in result[0]["attrs"] if a["name"] == "id")
    assert id_attr["type"] == "int"
    assert id_attr["properties"]["required"] is True

    name_attr = next(a for a in result[0]["attrs"] if a["name"] == "name")
    assert name_attr["type"] == "str"
    assert name_attr["properties"]["required"] is True

    email_attr = next(a for a in result[0]["attrs"] if a["name"] == "email")
    assert email_attr["type"] == "str"
    assert email_attr["properties"].get("format") == "email"


def test_openapi_json():
    """Test parsing OpenAPI schema in JSON format."""
    openapi_spec = """
{
    "openapi": "3.0.0",
    "info": {"title": "Test API", "version": "1.0"},
    "components": {
        "schemas": {
            "Product": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "price": {"type": "number"}
                }
            }
        }
    }
}
"""
    result = parse_openapi(openapi_spec)

    assert len(result) == 1
    assert result[0]["name"] == "Product"

    price_attr = next(a for a in result[0]["attrs"] if a["name"] == "price")
    assert price_attr["type"] == "float"


def test_openapi_with_refs():
    """Test parsing OpenAPI schema with $ref references."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    Address:
      type: object
      properties:
        street:
          type: string
        city:
          type: string
    Person:
      type: object
      properties:
        name:
          type: string
        address:
          $ref: '#/components/schemas/Address'
"""
    result = parse_openapi(openapi_spec)

    assert len(result) == 2

    person = next(m for m in result if m["name"] == "Person")
    address_attr = next(a for a in person["attrs"] if a["name"] == "address")
    assert address_attr["type"] == "Address"


def test_openapi_array_type():
    """Test parsing OpenAPI schema with array types."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    Order:
      type: object
      properties:
        items:
          type: array
          items:
            type: string
        quantities:
          type: array
          items:
            type: integer
"""
    result = parse_openapi(openapi_spec)

    order = result[0]
    items_attr = next(a for a in order["attrs"] if a["name"] == "items")
    assert items_attr["type"] == "List[str]"

    quantities_attr = next(a for a in order["attrs"] if a["name"] == "quantities")
    assert quantities_attr["type"] == "List[int]"


def test_openapi_with_enum():
    """Test parsing OpenAPI schema with enum."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    Status:
      type: object
      properties:
        status:
          type: string
          enum:
            - pending
            - active
            - completed
"""
    result = parse_openapi(openapi_spec)

    status = result[0]
    status_attr = next(a for a in status["attrs"] if a["name"] == "status")
    assert status_attr["properties"]["enum"] == ["pending", "active", "completed"]


def test_openapi_with_allof():
    """Test parsing OpenAPI schema with allOf (inheritance)."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    BaseModel:
      type: object
      properties:
        id:
          type: integer
    ExtendedModel:
      allOf:
        - $ref: '#/components/schemas/BaseModel'
        - type: object
          properties:
            name:
              type: string
"""
    result = parse_openapi(openapi_spec)

    extended = next(m for m in result if m["name"] == "ExtendedModel")
    assert "BaseModel" in extended["parents"]
    assert any(a["name"] == "name" for a in extended["attrs"])


def test_openapi_with_formats():
    """Test parsing OpenAPI schema with various formats."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    Document:
      type: object
      properties:
        created_at:
          type: string
          format: date-time
        date:
          type: string
          format: date
        uuid:
          type: string
          format: uuid
        data:
          type: string
          format: binary
"""
    result = parse_openapi(openapi_spec)

    doc = result[0]

    created_attr = next(a for a in doc["attrs"] if a["name"] == "created_at")
    assert created_attr["type"] == "datetime.datetime"

    date_attr = next(a for a in doc["attrs"] if a["name"] == "date")
    assert date_attr["type"] == "datetime.date"

    uuid_attr = next(a for a in doc["attrs"] if a["name"] == "uuid")
    assert uuid_attr["type"] == "uuid.UUID"

    data_attr = next(a for a in doc["attrs"] if a["name"] == "data")
    assert data_attr["type"] == "bytes"


def test_openapi_with_defaults():
    """Test parsing OpenAPI schema with default values."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    Config:
      type: object
      properties:
        enabled:
          type: boolean
          default: true
        count:
          type: integer
          default: 10
        name:
          type: string
          default: "default_name"
"""
    result = parse_openapi(openapi_spec)

    config = result[0]

    enabled_attr = next(a for a in config["attrs"] if a["name"] == "enabled")
    assert enabled_attr["default"] is True

    count_attr = next(a for a in config["attrs"] if a["name"] == "count")
    assert count_attr["default"] == 10

    name_attr = next(a for a in config["attrs"] if a["name"] == "name")
    assert name_attr["default"] == "default_name"


def test_openapi_with_constraints():
    """Test parsing OpenAPI schema with validation constraints."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    Validated:
      type: object
      properties:
        age:
          type: integer
          minimum: 0
          maximum: 150
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          pattern: "^[a-z]+@[a-z]+[.][a-z]+$"
"""
    result = parse_openapi(openapi_spec)

    validated = result[0]

    age_attr = next(a for a in validated["attrs"] if a["name"] == "age")
    assert age_attr["properties"]["minimum"] == 0
    assert age_attr["properties"]["maximum"] == 150

    name_attr = next(a for a in validated["attrs"] if a["name"] == "name")
    assert name_attr["properties"]["min_length"] == 1
    assert name_attr["properties"]["max_length"] == 100

    email_attr = next(a for a in validated["attrs"] if a["name"] == "email")
    assert "pattern" in email_attr["properties"]


def test_openapi_with_nullable():
    """Test parsing OpenAPI schema with nullable fields."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    NullableModel:
      type: object
      properties:
        optional_field:
          type: string
          nullable: true
        required_field:
          type: string
"""
    result = parse_openapi(openapi_spec)

    model = result[0]

    optional_attr = next(
        a for a in model["attrs"] if a["name"] == "optional_field"
    )
    assert optional_attr["properties"]["nullable"] is True


def test_openapi_swagger_v2_definitions():
    """Test parsing Swagger 2.0 style definitions."""
    swagger_spec = """
swagger: "2.0"
info:
  title: Test API
  version: "1.0"
definitions:
  LegacyModel:
    type: object
    properties:
      id:
        type: integer
      name:
        type: string
"""
    result = parse_openapi(swagger_spec)

    assert len(result) == 1
    assert result[0]["name"] == "LegacyModel"


def test_openapi_multiple_schemas():
    """Test parsing OpenAPI with multiple schemas."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
    Post:
      type: object
      properties:
        id:
          type: integer
        title:
          type: string
        author:
          $ref: '#/components/schemas/User'
    Comment:
      type: object
      properties:
        id:
          type: integer
        text:
          type: string
        post:
          $ref: '#/components/schemas/Post'
"""
    result = parse_openapi(openapi_spec)

    assert len(result) == 3
    names = [m["name"] for m in result]
    assert "User" in names
    assert "Post" in names
    assert "Comment" in names


def test_openapi_with_description():
    """Test parsing OpenAPI schema with descriptions."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    Documented:
      type: object
      description: A well-documented model
      title: Documented Model
      properties:
        field:
          type: string
          description: A field with description
"""
    result = parse_openapi(openapi_spec)

    model = result[0]
    assert model["properties"]["description"] == "A well-documented model"
    assert model["properties"]["title"] == "Documented Model"

    field_attr = next(a for a in model["attrs"] if a["name"] == "field")
    assert field_attr["properties"]["description"] == "A field with description"


def test_openapi_array_with_ref():
    """Test parsing OpenAPI schema with array of references."""
    openapi_spec = """
openapi: "3.0.0"
info:
  title: Test API
  version: "1.0"
components:
  schemas:
    Item:
      type: object
      properties:
        name:
          type: string
    Container:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/Item'
"""
    result = parse_openapi(openapi_spec)

    container = next(m for m in result if m["name"] == "Container")
    items_attr = next(a for a in container["attrs"] if a["name"] == "items")
    assert items_attr["type"] == "List[Item]"


def test_invalid_openapi_spec():
    """Test error handling for invalid OpenAPI specification."""
    with pytest.raises(ValueError, match="Invalid OpenAPI specification"):
        parse_openapi("not valid yaml or json {{{")
