from typing import Dict, Tuple

from parsimonious.nodes import NodeVisitor


class Visitor(NodeVisitor):
    def visit_class_name(self, node, visited_children):
        """get class name"""
        class_name = node.children[1].children[0].text.strip().replace(":", "")
        return {"name": class_name}

    def visit_class_def(self, node, visited_children):
        """get class def"""
        parents = []
        try:
            for chld_node in node.children[2].children[0].children[1:-1]:
                parent = chld_node.text.strip()
                if parent:
                    parents.append(parent)
        except IndexError:
            pass

        parents = {"parents": parents}

        for children in visited_children:
            if "name" in children:
                parents.update(children)

        return parents

    @staticmethod
    def clean_up_cases_with_inner_pars(text: str) -> str:
        del_ = []
        for num, item in enumerate(text):
            if item.endswith(")") and "(" not in item:
                text[num - 1] = f"{text[num-1]},{text[num]}"
                del_.append(item)
        for d in del_:
            try:
                text.remove(d)
            except ValueError:
                pass
        return text

    def extract_orm_attr(self, text: str):
        _type = None
        default = None
        not_orm = True
        properties = {}
        orm_columns = ["Column", "Field", "relationship", "ForeignKey"]
        pony_orm_fields = ["Required", "Set", "Optional", "PrimaryKey"]
        orm_columns.extend(pony_orm_fields)
        for i in orm_columns:
            if i in text:
                not_orm = False
                # in case of models
                index = text.find("(")
                base_text = text
                text = text[index + 1 : -1]  # noqa E203
                text = text.split(",")
                text = self.clean_up_cases_with_inner_pars(text)
                prop_index = 1
                if i == "Field":
                    _type, properties = get_django_info(text, base_text, properties)
                    prop_index = 0
                elif i == "ForeignKey":
                    # mean it is a Django model.ForeignKey
                    _type = "serial"
                    properties["foreign_key"] = text[0]
                elif i in pony_orm_fields:
                    # mean it is a Pony ORM
                    _type, properties = get_pony_orm_info(
                        text, i, base_text, properties
                    )
                else:
                    _type = text[0]
                if i == "relationship":
                    properties["relationship"] = True
                for item in text[prop_index:]:
                    properties, default = self.add_property(item, properties)
                break
        return default, _type, properties, not_orm

    @staticmethod
    def add_property(item: str, properties: Dict) -> Tuple[Dict, str]:
        default = None
        if "=" in item:
            # can be backref=db.backref('pages', lazy=True)
            index = item.find("=")
            left = item[:index].strip()
            right = item[index + 1 :].strip()  # noqa: E203
            if left == "default":
                default = right
            else:
                properties[left] = right
        elif "foreign" in item.lower():
            properties["foreign_key"] = item.split("(")[1].split(")")[0]
        return properties, default

    def extractor(self, text: str) -> Dict:
        _type = None
        default = None
        not_orm = True
        properties = {}
        if "(" in text:
            default, _type, properties, not_orm = self.extract_orm_attr(text)
        if not_orm:
            # in case of enums or pydantic
            default = text
        return {"default": default, "type": _type, "properties": properties}

    def visit_right_part(self, node, visited_children):
        return self.extractor(node.text.strip())

    def visit_attr_def(self, node, visited_children):
        """Makes a dict of the section (as key) and the key/value pairs."""
        left = node.children[1].children[0].children[0].text.strip()
        default = None
        _type = None
        if "def " in left:
            attr = {"attr": {"name": None, "type": _type, "default": default}}
            return attr
        if ":" in left:
            _type = left.split(":")[-1].strip()
            left = left.split(":")[0].strip()
        attr = {"attr": {"name": left, "type": _type, "default": default}}
        for children in visited_children:

            if isinstance(children, list):
                if isinstance(children[-1], list):
                    if "default" in children[-1][-1]:
                        attr["attr"]["default"] = children[-1][-1]["default"]
                        attr["attr"]["properties"] = children[-1][-1]["properties"]
                        if children[-1][-1]["type"] is not None:
                            attr["attr"]["type"] = children[-1][-1]["type"]
                elif isinstance(children[-1], dict) and "type" in children[-1]:
                    attr["attr"]["type"] = children[-1]["type"]
        return attr

    def process_chld(self, child, final_child):
        if "attr" in child and child["attr"]["name"]:
            # todo: this is a hack, need refactor it
            if child["attr"]["name"] == "self" and not final_child["properties"].get(
                "init"
            ):
                final_child["properties"]["init"] = []
            elif "tablename" in child["attr"]["name"]:
                final_child["properties"]["table_name"] = child["attr"]["default"]
            elif "table_args" in child["attr"]["name"]:
                final_child["properties"][child["attr"]["name"]] = (
                    child["attr"]["type"] or child["attr"]["default"]
                )
            else:
                if final_child["properties"].get("init") is not None:
                    final_child["properties"]["init"].append(child["attr"])
                else:
                    final_child["attrs"].append(child["attr"])
        else:

            if "attr" in child:
                final_child = process_no_name_attrs(final_child, child)
            elif isinstance(child, dict):
                final_child.update(child)
            elif isinstance(child, list):
                for i in child:
                    final_child = self.process_chld(i, final_child)
        return final_child

    def visit_expr(self, node, visited_children):
        """Makes a dict of the section (as key) and the key/value pairs."""
        children_values = []
        n = -1
        for i in visited_children:
            final_child = {"name": None, "attrs": [], "parents": [], "properties": {}}
            final_child = self.process_chld(i, final_child)
            if (
                final_child.get("name")
                and final_child["name"] == "Meta"
                and children_values
            ):
                for attr in final_child["attrs"]:
                    children_values[n]["properties"][attr["name"]] = (
                        attr["type"] or attr["default"]
                    )
            elif final_child.get("name"):
                children_values.append(final_child)
                n += 1
            if "attr" in final_child:
                del final_child["attr"]
            if final_child["properties"].get("init") == []:
                del final_child["properties"]["init"]
            elif final_child["properties"].get("init"):
                if not children_values[n]["properties"].get("init"):
                    children_values[n]["properties"]["init"] = final_child[
                        "properties"
                    ]["init"]
        return children_values

    def visit_type(self, node, visited_children):
        _index = node.text.find(":")
        _type = node.text[_index + 1 :]  # noqa: E203
        return {"type": _type.strip()}

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node


def process_no_name_attrs(final_child: Dict, child: Dict) -> None:
    if final_child["attrs"]:
        if child["attr"]["default"]:
            final_child["attrs"][-1]["default"] = child["attr"]["default"]
            if not final_child["attrs"][-1].get("properties"):
                final_child["attrs"][-1]["properties"] = {}
        elif child["attr"]["type"] and final_child["attrs"][-1]["default"]:
            final_child["attrs"][-1]["default"] += f':{child["attr"]["type"]}'
    return final_child


def get_pony_orm_info(
    text: list, field: str, base_text: str, properties: Dict
) -> Tuple:
    if field == "Required":
        properties["nullable"] = False
    elif field == "PrimaryKey":
        properties["primary_key"] = True
    elif field == "Optional":
        properties["nullable"] = True
    elif field == "Set":
        # relationship
        properties["relationship"] = True
        properties["foreign_key"] = text[0]
    _type = text[0]

    return _type, properties


def get_django_info(text: list, base_text: str, properties: Dict) -> Tuple:
    # for tortoise orm & django orm
    split_by_field = base_text.split("Field")[0].split(".")
    if len(split_by_field) == 2:
        _type = split_by_field[1]
    else:
        _type = split_by_field[0]
    if _type == "ManyToMany":
        properties["foreign_key"] = text[0]
    return _type, properties
