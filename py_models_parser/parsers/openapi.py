"""OpenAPI 3.0 Specification Parser.

Parses OpenAPI/Swagger schemas and converts them to py-models-parser format.
"""
import json
from typing import Any, Dict, List, Optional

import yaml


# OpenAPI type to Python type mapping
OPENAPI_TYPE_MAP = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "array": "list",
    "object": "dict",
}

# OpenAPI format to Python type mapping
OPENAPI_FORMAT_MAP = {
    "int32": "int",
    "int64": "int",
    "float": "float",
    "double": "float",
    "date": "datetime.date",
    "date-time": "datetime.datetime",
    "time": "datetime.time",
    "email": "str",
    "uri": "str",
    "uuid": "uuid.UUID",
    "binary": "bytes",
    "byte": "bytes",
}

# Property mappings from OpenAPI to internal format
PROPERTY_MAPPINGS = {
    "description": "description",
    "enum": "enum",
    "minimum": "minimum",
    "maximum": "maximum",
    "minLength": "min_length",
    "maxLength": "max_length",
    "pattern": "pattern",
    "nullable": "nullable",
    "format": "format",
}


def _resolve_ref(ref: str, spec: Dict) -> Optional[Dict]:
    """Resolve a $ref pointer to its definition."""
    if not ref.startswith("#/"):
        return None

    parts = ref[2:].split("/")
    current = spec
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def _get_ref_type(schema: Dict, spec: Dict, visited: set) -> str:
    """Handle $ref type resolution."""
    ref = schema["$ref"]
    if ref in visited:
        return "Any"
    visited.add(ref)

    ref_schema = _resolve_ref(ref, spec)
    if ref_schema:
        return ref.split("/")[-1]
    return "Any"


def _get_composite_type(
    sub_schemas: List[Dict],
    spec: Dict,
    visited: set
) -> str:
    """Handle allOf/oneOf/anyOf composite types."""
    types = [
        _get_type_from_schema(sub_schema, spec, visited)
        for sub_schema in sub_schemas
    ]
    if len(types) == 1:
        return types[0]
    return f"Union[{', '.join(types)}]"


def _get_type_from_schema(
    schema: Dict,
    spec: Dict,
    visited: Optional[set] = None
) -> str:
    """Convert OpenAPI schema to Python type string."""
    if visited is None:
        visited = set()

    if "$ref" in schema:
        return _get_ref_type(schema, spec, visited)

    if "allOf" in schema:
        return _get_composite_type(schema["allOf"], spec, visited)

    if "oneOf" in schema or "anyOf" in schema:
        sub_schemas = schema.get("oneOf") or schema.get("anyOf")
        return _get_composite_type(sub_schemas, spec, visited)

    schema_type = schema.get("type", "object")

    if schema_type == "array":
        items = schema.get("items", {})
        item_type = _get_type_from_schema(items, spec, visited)
        return f"List[{item_type}]"

    if "format" in schema:
        format_type = OPENAPI_FORMAT_MAP.get(schema["format"])
        if format_type:
            return format_type

    if "enum" in schema:
        return "str"

    return OPENAPI_TYPE_MAP.get(schema_type, "Any")


def _extract_attr_properties(
    prop_schema: Dict,
    prop_name: str,
    required_fields: List[str]
) -> Dict:
    """Extract properties from a single attribute schema."""
    properties = {}

    if prop_name in required_fields:
        properties["required"] = True

    for openapi_key, internal_key in PROPERTY_MAPPINGS.items():
        if openapi_key in prop_schema:
            properties[internal_key] = prop_schema[openapi_key]

    return properties


def _extract_properties(
    schema: Dict,
    spec: Dict,
    required_fields: List[str]
) -> List[Dict]:
    """Extract properties from schema and convert to attrs format."""
    attrs = []
    properties = schema.get("properties", {})

    for prop_name, prop_schema in properties.items():
        attr = {
            "name": prop_name,
            "type": _get_type_from_schema(prop_schema, spec),
            "default": prop_schema.get("default"),
            "properties": _extract_attr_properties(
                prop_schema, prop_name, required_fields
            ),
        }
        attrs.append(attr)

    return attrs


def _parse_schema(
    name: str,
    schema: Dict,
    spec: Dict
) -> Dict[str, Any]:
    """Parse a single OpenAPI schema into py-models-parser format."""
    required_fields = schema.get("required", [])

    model = {
        "name": name,
        "parents": [],
        "attrs": [],
        "properties": {},
    }

    if "allOf" in schema:
        for sub_schema in schema["allOf"]:
            if "$ref" in sub_schema:
                ref_name = sub_schema["$ref"].split("/")[-1]
                model["parents"].append(ref_name)
            elif "properties" in sub_schema:
                required_fields.extend(sub_schema.get("required", []))
                model["attrs"].extend(
                    _extract_properties(sub_schema, spec, required_fields)
                )
    else:
        model["attrs"] = _extract_properties(schema, spec, required_fields)

    if "description" in schema:
        model["properties"]["description"] = schema["description"]

    if "title" in schema:
        model["properties"]["title"] = schema["title"]

    return model


def parse_openapi(content: str) -> List[Dict]:
    """Parse OpenAPI specification and return list of models.

    Args:
        content: OpenAPI specification as YAML or JSON string

    Returns:
        List of models in py-models-parser format
    """
    try:
        spec = yaml.safe_load(content)
    except yaml.YAMLError:
        try:
            spec = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid OpenAPI specification: {e}")

    if not isinstance(spec, dict):
        raise ValueError("Invalid OpenAPI specification: root must be object")

    schemas = {}

    if "components" in spec and "schemas" in spec["components"]:
        schemas = spec["components"]["schemas"]
    elif "definitions" in spec:
        schemas = spec["definitions"]

    models = []
    for name, schema in schemas.items():
        model = _parse_schema(name, schema, spec)
        models.append(model)

    return models


def parse_openapi_file(file_path: str) -> List[Dict]:
    """Parse OpenAPI specification from file.

    Args:
        file_path: Path to OpenAPI specification file (YAML or JSON)

    Returns:
        List of models in py-models-parser format
    """
    with open(file_path, "r") as f:
        content = f.read()
    return parse_openapi(content)
