# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-18

### Added

**Pydantic 2.x Support**
- Union types with `|` operator (PEP 604): `int | None`, `str | None`
- `Field()` with validation constraints: `max_length`, `min_length`, `gt`, `ge`, `lt`, `le`
- `model_config` with `ConfigDict` handling
- Nested generic types: `list[dict[str, str]]`, `dict[str, list[int]]`

**OpenAPI 3.0/Swagger Support**
- New `parse_openapi()` function to parse OpenAPI specs from string
- New `parse_openapi_file()` function to parse from YAML or JSON files
- Supports OpenAPI 3.0 `components/schemas` and Swagger 2.0 `definitions`
- Type mapping from OpenAPI types to Python types
- Support for `$ref`, `allOf`, `oneOf`, `anyOf` compositions

**Python Version Support**
- Added support for Python 3.12
- Added support for Python 3.13

**Documentation**
- Added ARCHITECTURE.md with project documentation

### Changed

**Breaking Changes**
- Dropped support for Python 3.7
- Dropped support for Python 3.8
- Minimum required Python version is now 3.9

**Dependencies**
- Added `pyyaml` dependency for OpenAPI parsing

### Testing
- Added 8 new tests for Pydantic 2.x features
- Added 15 tests for OpenAPI parsing
- Updated CI to test Python 3.9, 3.10, 3.11, 3.12, 3.13

## [0.7.0]

### Changed
- Updated to latest version of parsimonious
- Library now works with Python 3.11

## [0.6.0]

### Added
- Support for [Encode ORM](https://github.com/encode/orm) models
- Support for [Piccolo ORM](https://piccolo-orm.readthedocs.io/en/latest/piccolo/schema/defining.html) models

## [0.5.1]

### Fixed
- Multiple parent names in "parents" output were sometimes joined in one string

## [0.5.0]

### Added
- Base support for PyDAL tables definitions
- Support for Python list syntax like `[]`

## [0.4.0]

### Fixed
- Return tuples (multiple values) are now parsed correctly
- Symbols like `*&^%$#!±~`§<>` no longer cause errors
- Classes without any args no longer cause errors

## [0.3.0]

### Added
- CLI command `pmp` with `-d`, `--dump` arguments
- Support for simple Django ORM models
- Base support for pure Python classes

## [0.2.0]

### Added
- Support for Dataclasses
- `parse_from_file()` method
- Correct handling of types with comma inside: `Union[dict, list]`, `Union[dict, list, tuple, anything]`

## [0.1.1]

### Added
- Base parser logic for:
  - Pydantic models
  - Python Enums
  - SQLAlchemy Models
  - GinoORM models
  - TortoiseORM models
- Initial test suite
