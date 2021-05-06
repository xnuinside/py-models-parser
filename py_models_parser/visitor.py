from typing import Dict

from parsimonious.nodes import NodeVisitor


class Visitor(NodeVisitor):
    def visit_class_name(self, node, visited_children):
        """get class name"""
        class_name = node.children[1].children[0].text.strip().replace(':', '')
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
        orm_columns = ["Column", "Field", "relationship"]
        for i in orm_columns:
            if i in text:
                not_orm = False
                # in case of models
                index = text.find("(")
                base_text = text
                text = text[index + 1 : -1]  # noqa E203
                text = text.split(",")

                text = self.clean_up_cases_with_inner_pars(text)
                if i == "Field":
                    # for tortoise orm
                    split_by_field = base_text.split("Field")[0].split(".")
                    if len(split_by_field) == 2:
                        _type = split_by_field[1]
                    else:
                        _type = split_by_field[0]
                    prop_index = 0
                else:
                    prop_index = 1
                    _type = text[0]
                if i == "relationship":
                    properties["relationship"] = True
                for i in text[prop_index:]:
                    if "=" in i:
                        # can be backref=db.backref('pages', lazy=True)
                        index = i.find("=")
                        left = i[:index].strip()
                        right = i[index + 1 :].strip()  # noqa: E203
                        if left == "default":
                            default = right
                        else:
                            properties[left] = right
                    elif "foreign" in i.lower():
                        properties["foreign_key"] = i.split("(")[1].split(")")[0]
                break
        return default, _type, properties, not_orm

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
        left = node.children[1].children[0].text.strip()
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
        return attr

    def process_chld(self, child, final_child):
        if "attr" in child and child["attr"]["name"]:
            if "tablename" in child["attr"]["name"]:
                final_child["properties"]["table_name"] = child["attr"]["default"]
            elif "table_args" in child["attr"]["name"]:
                final_child["properties"][child["attr"]["name"]] = (
                    child["attr"]["type"] or child["attr"]["default"]
                )
            else:
                final_child["attrs"].append(child["attr"])
        else:
            if isinstance(child, dict):
                final_child.update(child)
            elif isinstance(child, list):
                for i in child:
                    final_child= self.process_chld(i, final_child)
        return final_child

    def visit_expr(self, node, visited_children):
        """Makes a dict of the section (as key) and the key/value pairs."""
        children_values = []
        n = -1
        for i in visited_children:
            final_child = {"name": None, "attrs": [], "parents": [], "properties": {}}
            final_child = self.process_chld(i, final_child)
            if final_child.get('name') and final_child['name'] == 'Meta' and children_values:
                for attr in final_child['attrs']:
                    children_values[n]["properties"][attr["name"]] = (
                        attr["type"] or attr["default"]
                    )
            elif final_child.get("name"):
                children_values.append(final_child)
                n += 1
            if "attr" in final_child:
                del final_child["attr"]
        return children_values

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node
