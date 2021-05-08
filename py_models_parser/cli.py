import argparse
import os
import pprint
import sys

from py_models_parser import dump_result, parse_from_file


def version(**kwargs):
    return "0.2.0"


def cli():
    pmp_cli = argparse.ArgumentParser(description="Python Models Parser")

    pmp_cli.add_argument(
        "file_path", type=str, help="The path to .py file with models to parse"
    )

    pmp_cli.add_argument(
        "-d",
        "--dump",
        nargs="?",
        type=str,
        const="output_models.json",
        help="Target path to save parse results in .json files",
    )

    return pmp_cli


def run_for_file(args):
    print(f"Start parsing file {args.file_path} \n")
    result = parse_from_file(args.file_path)
    if args.dump:
        dump_result(result, args.dump)
    print(f"File with result was saved to >> {args.dump} file")
    if not args.dump:
        pprint.pprint(result)


def correct_extension(file_name: str) -> bool:
    ext = ["ddl", "sql", "hql", ""]
    split_name = file_name.split(".")
    if len(split_name) >= 2:
        ext_file = split_name[1]
        if ext_file in ext:
            return True
    return False


def main():
    sdb_cli = cli()
    args = sdb_cli.parse_args()
    if not os.path.exists(args.file_path):
        print("The file path specified does not exist")
        sys.exit()
    if os.path.isfile(args.file_path):
        run_for_file(args)
    else:
        files = [
            os.path.join(args.ddl_file_path, file_name)
            for file_name in os.listdir(args.ddl_file_path)
            if correct_extension(file_name)
        ]
        for file_path in files:
            args.ddl_file_path = file_path
            run_for_file(args)
