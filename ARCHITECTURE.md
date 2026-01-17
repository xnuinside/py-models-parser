# Архитектура py-models-parser

## О проекте

**Py-Models-Parser** — текстовый парсер Python моделей и определений таблиц, который извлекает структурную информацию из различных ORM-фреймворков без необходимости импортировать исходный код.

Парсер использует PEG (Parsing Expression Grammar) через библиотеку `parsimonious` для анализа текста кода как строк.

## Поддерживаемые модели

- SQLAlchemy ORM
- Gino ORM
- Tortoise ORM
- Encode ORM
- Django ORM Models
- Pydantic
- Python Enums
- Pony ORM
- Piccolo ORM
- Pydal Tables (Web2Py)
- Python Dataclasses
- Чистые Python классы
- OpenAPI 3.0/Swagger specifications

## Структура проекта

```
py-models-parser/
├── py_models_parser/              # Основной пакет
│   ├── __init__.py               # Публичный API
│   ├── core.py                   # Основная логика парсинга
│   ├── grammar.py                # PEG грамматика
│   ├── visitor.py                # Visitor для преобразования AST
│   ├── types.py                  # Определения типов и триггеры
│   ├── utils.py                  # Утилиты
│   ├── cli.py                    # CLI интерфейс
│   └── parsers/
│       ├── pydal.py              # Специализированный парсер для Pydal
│       └── openapi.py            # Парсер OpenAPI/Swagger спецификаций
├── tests/                        # Тесты
│   ├── test_*.py                 # Тесты для каждого типа моделей
│   └── data/                     # Тестовые данные
├── tox.ini                       # Конфигурация tox для мультиверсионного тестирования
└── pyproject.toml                # Конфигурация Poetry
```

## Основные компоненты

### 1. Public API (`__init__.py`)

Экспортирует функции:
- `parse(models: str)` — парсинг строки с Python моделями
- `parse_from_file(file_path)` — парсинг Python моделей из файла
- `dump_result(output, file_path)` — сохранение результатов в JSON
- `parse_openapi(content: str)` — парсинг OpenAPI спецификации из строки
- `parse_openapi_file(file_path)` — парсинг OpenAPI спецификации из файла

### 2. Core (`core.py`)

Главный модуль с логикой парсинга:

| Функция | Назначение |
|---------|-----------|
| `parse()` | Главная функция парсинга |
| `parse_from_file()` | Парсинг из файла |
| `pre_processing()` | Удаление импортов, комментариев, декораторов |
| `get_models_type()` | Определение типа модели |
| `sqlalchemy_type_identify()` | Различие SQLAlchemy ORM и Core |
| `format_ouput()` | Постобработка результатов |
| `process_models_attr()` | Разрешение ссылок на другие модели |
| `clear_parents()` | Удаление служебной информации |

### 3. Grammar (`grammar.py`)

PEG-грамматика для парсинга:

```
expr        → (class/if_else/call_result/...)* - корневое выражение
class       → class_def attr_def* funct_def*   - определение класса
class_def   → class_name args? ":"*            - сигнатура класса
attr_def    → id type? ("=" right_part)*       - атрибут
type        → ":" (id args_in_brackets / id)   - аннотация типа
args        → "(" (list/call_result/...)* ")"  - аргументы
```

### 4. Visitor (`visitor.py`)

Класс `Visitor(NodeVisitor)` для преобразования AST в структуры данных:

| Метод | Назначение |
|-------|-----------|
| `visit_class_name()` | Извлечение названия класса |
| `visit_class_def()` | Обработка определения класса |
| `visit_attr_def()` | Обработка атрибута |
| `visit_right_part()` | Анализ правой части присваивания |
| `visit_type()` | Парсинг аннотаций типов |
| `extract_orm_attr()` | Извлечение параметров ORM |
| `_process_attr()` | Классификация атрибутов |

### 5. Types (`types.py`)

Конфигурация для распознавания типов моделей:

```python
orm_triggers = ["Column", "Field", "relationship"]
pony_orm_fields = ["Required", "Set", "Optional", "PrimaryKey"]
ormar_and_piccollo_types = ["Integer", "String", "Text", ...]
```

### 6. CLI (`cli.py`)

Интерфейс командной строки:

```bash
pmp path_to_models.py [-d output.json]
```

## Поток данных

```
Входной Python-код
       │
       ▼
┌─────────────────────┐
│ pre_processing()    │  Удаление импортов, комментариев
│ get_models_type()   │  Определение типа модели
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ grammar.parse()     │  PEG парсинг → AST
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Visitor.visit()     │  Обход AST
│ extract_orm_attr()  │  Распознавание ORM-параметров
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ format_ouput()      │  Постобработка
│ process_models_attr │
│ clear_parents()     │
└─────────┬───────────┘
          │
          ▼
   Структурированный JSON
```

## Выходной формат

```python
{
    "name": str,              # Имя класса/модели
    "parents": [str],         # Родительские классы
    "attrs": [
        {
            "name": str,      # Имя атрибута
            "type": str,      # Тип данных
            "default": str,   # Значение по умолчанию
            "properties": {   # Метаданные
                "primary_key": bool,
                "nullable": bool,
                "foreign_key": str,
                ...
            }
        }
    ],
    "properties": {           # Свойства модели
        "table_name": str,
        "table_args": str,
        ...
    }
}
```

## Зависимости

**Runtime:**
- `parsimonious` ^0.10.0 — PEG парсер для Python моделей
- `pyyaml` ^6.0 — парсер YAML для OpenAPI спецификаций

**Development:**
- `pytest` ^7.4
- `tox` — мультиверсионное тестирование

**Python:** 3.9, 3.10, 3.11, 3.12, 3.13

## Использование

```python
# Парсинг Python моделей из строки
from py_models_parser import parse
result = parse(models_string)

# Парсинг Python моделей из файла
from py_models_parser import parse_from_file
result = parse_from_file("path/to/models.py")

# Парсинг OpenAPI спецификации
from py_models_parser import parse_openapi, parse_openapi_file
result = parse_openapi(openapi_yaml_string)
result = parse_openapi_file("path/to/openapi.yaml")
```

```bash
# CLI
pmp models.py -d output.json
```

## Расширение

Для добавления поддержки нового ORM:

1. Добавить триггеры в `types.py`
2. Расширить грамматику в `grammar.py` (при необходимости)
3. Добавить методы в `visitor.py` для специфики ORM
4. Создать специализированный парсер в `parsers/` (опционально)
