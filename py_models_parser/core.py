import json
import os
from typing import Dict, List

from py_models_parser.grammar import grammar
from py_models_parser.utils import supported_types
from py_models_parser.visitor import Visitor


def sqlalchemy_type_identify(models_source: str) -> str:
    for _import in ["declarative_base", "Table"]:
        if _import in models_source:
            if _import == "declarative_base":
                return "sqlalchemy"
            else:
                return "sqlalchemy_core"


def get_models_type(models_source: str) -> str:
    for _type in supported_types:
        if _type in models_source:
            if _type == "sqlalchemy":
                return sqlalchemy_type_identify
            else:
                return _type


def pre_processing(models: str):
    models = models.split("\n")
    start_statements = ["from", "import", "#", '"', "'", "@"]
    inline_statements = ["Gino", "declarative_base"]
    to_process = []
    comment_start = True
    for line in models:
        process = True
        check_line = line.strip()
        if check_line.startswith('"""') or check_line.startswith("'''"):
            if not comment_start:
                comment_start = True
                continue
            else:
                comment_start = False
                continue
        for state in start_statements:
            if check_line.startswith(state):
                process = False
                break
        if process:
            for state in inline_statements:
                if state in line:
                    process = False
                    break
            else:
                if line:
                    to_process.append(line)
    return "\n".join(to_process)


def output(input: str):
    v = Visitor()
    output = v.visit(input)
    return output


def process_models_attr(model: Dict, models_by_name: Dict) -> Dict:
    for attr in model["attrs"]:
        if (
            attr.get("properties")
            and attr["properties"].get("foreign_key")
            and not attr["properties"].get("through")
        ):
            split_type = attr["type"].split(".")
            target_model = models_by_name.get(split_type[0])
            if target_model:
                key = [
                    attr
                    for attr in target_model["attrs"]
                    if attr["name"] == split_type[1]
                ]
                if not key:
                    _type = "serial"
                else:
                    _type = key[0]["type"]
                attr["type"] = _type
    return model


def clear_parents(model: Dict) -> Dict:

    parents = []

    for parent in model["parents"]:
        if "tablename" in parent:
            name = parent.split("=")
            model["properties"]["table_name"] = name[1]
            continue
        parents.append(parent)

    model["parents"] = parents

    return model


def format_ouput(output: List[Dict]):
    models_by_name = {model["name"]: model for model in output}
    for model in output:
        model = process_models_attr(model, models_by_name)
        model = clear_parents(model)
    return output


def parse(models: str) -> List[Dict]:
    models = pre_processing(models)
    result = grammar.parse(models)
    result = output(result)
    result = format_ouput(result)
    return result


def parse_from_file(file_path: str) -> List[Dict]:
    if not os.path.isfile(file_path):
        print(
            f"Path {file_path} is not a file or not exists. You need to provide valid path to .py module with models"
        )
    with open(file_path, "r") as f:
        models = f.read()
        return parse(models)


def dump_result(output: str, file_path: str) -> None:
    with open(file_path, "w+") as f:
        json.dump(output, f, indent=1)
