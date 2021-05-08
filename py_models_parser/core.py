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


def parse(models: str) -> List[Dict]:
    models = pre_processing(models)
    result = grammar.parse(models)
    result = output(result)
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
