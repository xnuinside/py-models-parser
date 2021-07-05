from typing import Dict, List

pydal_order_field_args = {
    1: "length",
    3: "required",
    4: "requires",
    5: "ondelete",
    6: "notnull",
    7: "unique",
}


def _pydal_table_properties(table_def: Dict, value: str) -> Dict:
    table_prop = value.split(",")
    previos_prop = None
    for num, prop in enumerate(table_prop):
        if num == len(table_prop) - 1:
            prop = prop.replace(")", "")
        prop = prop.strip().split("=")
        if len(prop) > 1:
            table_def["properties"][prop[0].strip()] = prop[1].strip()
            previos_prop = prop[0].strip()
        else:
            # like lists
            table_def["properties"][previos_prop] += f", {prop[0]}"

    return table_def


def pydal_column_properties(attr: Dict, column: List) -> Dict:
    properties = {}
    default = None
    _type = None
    for num, param in enumerate(column[1:]):
        param = param.strip().split("=")
        if len(param) > 1:
            if "default" == param[0]:
                default = param[1]
            elif "type" == param[0]:
                _type = param[1]
            else:
                properties[param[0]] = param[1]
        else:
            if param[0]:
                if num == 0:
                    _type = param[0]
                elif num == 2:
                    default = param[0]
                else:
                    order_param = pydal_order_field_args.get(num)
                    if order_param:
                        properties[order_param] = param[0]

    attr.update({"properties": properties, "default": default, "type": _type})
    return attr


def process_pydal_table_definition(pydal_def: str) -> Dict:
    table_def = {
        "attrs": [],
        "name": "name",
        "properties": {},
    }
    pydal_def = pydal_def.split("Field(")

    table_def["name"] = pydal_def[0].split(",")[0].split("define_table(")[1]
    for column in pydal_def[1:]:
        _column = column.strip().replace(") ,", "),").split("),")
        if len(_column) == 2 and _column[-1] != "":
            table_def = _pydal_table_properties(table_def, _column[-1])
        column = column.replace(")", "").strip().split(",")
        column_name = column[0]
        attr = {"name": column_name}
        attr = pydal_column_properties(attr, column)
        table_def["attrs"].append(attr)
    return table_def
