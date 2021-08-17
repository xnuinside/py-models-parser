orm_triggers = ["Column", "Field", "relationship"]

pony_orm_fields = ["Required", "Set", "Optional", "PrimaryKey"]

ormar_and_piccollo_types = [
    "Integer",
    "String",
    "Text",
    "Boolean",
    "BigInteger",
    "SmallInteger",
    "Float",
    "Decimal",
    "Date",
    "Time",
    "JSON",
    "DateTime",
    "LargeBinary",
    "ForeignKey",
    "Varchar",
    "UUID",
    "JSONB",
    "Time",
    "ARRAY",
    "Interval",
    "Timestamp",
]
orm_triggers.extend(pony_orm_fields)
orm_triggers.extend(ormar_and_piccollo_types)
