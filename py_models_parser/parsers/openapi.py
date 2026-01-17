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


def _get_type_from_schema(
    schema: Dict,
    spec: Dict,
    visited: Optional[set] = None
) -> str:
    """Convert OpenAPI schema to Python type string."""
    if visited is None:
        visited = set()

    if "$ref" in schema:
        ref = schema["$ref"]
        if ref in visited:
            return "Any"
        visited.add(ref)

        ref_schema = _resolve_ref(ref, spec)
        if ref_schema:
            ref_name = ref.split("/")[-1]
            return ref_name
        return "Any"

    schema_type = schema.get("type", "object")

    if "allOf" in schema:
        types = []
        for sub_schema in schema["allOf"]:
            types.append(_get_type_from_schema(sub_schema, spec, visited))
        return types[0] if len(types) == 1 else f"Union[{', '.join(types)}]"

    if "oneOf" in schema or "anyOf" in schema:
        sub_schemas = schema.get("oneOf") or schema.get("anyOf")
        types = []
        for sub_schema in sub_schemas:
            types.append(_get_type_from_schema(sub_schema, spec, visited))
        return f"Union[{', '.join(types)}]"

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
            "properties": {},
        }

        if prop_name in required_fields:
            attr["properties"]["required"] = True

        if "description" in prop_schema:
            attr["properties"]["description"] = prop_schema["description"]

        if "enum" in prop_schema:
            attr["properties"]["enum"] = prop_schema["enum"]

        if "minimum" in prop_schema:
            attr["properties"]["minimum"] = prop_schema["minimum"]

        if "maximum" in prop_schema:
            attr["properties"]["maximum"] = prop_schema["maximum"]

        if "minLength" in prop_schema:
            attr["properties"]["min_length"] = prop_schema["minLength"]

        if "maxLength" in prop_schema:
            attr["properties"]["max_length"] = prop_schema["maxLength"]

        if "pattern" in prop_schema:
            attr["properties"]["pattern"] = prop_schema["pattern"]

        if "nullable" in prop_schema:
            attr["properties"]["nullable"] = prop_schema["nullable"]

        if "format" in prop_schema:
            attr["properties"]["format"] = prop_schema["format"]

        if not attr["properties"]:
            attr["properties"] = {}

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
