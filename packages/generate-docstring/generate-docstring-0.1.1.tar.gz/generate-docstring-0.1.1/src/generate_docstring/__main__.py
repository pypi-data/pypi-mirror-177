"""

Doc string generator
"""
import argparse
import difflib
import os
from typing import Iterator

from generate_docstring import parse


def generator_source(src: list) -> Iterator[str]:
    """

    generator_source function

    Args:
        src (list): list of file to iter

    """
    for item in src:
        if os.path.isfile(item):
            yield item
        elif os.path.isdir(item):
            for root, _dirs, files in os.walk(item):
                for filepath in files:
                    yield os.path.join(root, filepath)


def main():
    """

    main function

    """
    _parser = argparse.ArgumentParser("docstring")
    _parser.add_argument("src", action="append")
    _parser.add_argument("--diff", action="store_true")
    _args = _parser.parse_args()

    for _path in generator_source(_args.src):
        with open(_path, "r", encoding="utf-8") as _file:
            try:
                _original_node, _updated_node = parse(
                    _file.read(), os.path.basename(_path)
                )
                if _args.diff:
                    print(
                        "".join(
                            difflib.unified_diff(
                                _original_node.code.splitlines(1),
                                _updated_node.code.splitlines(1),
                            )
                        )
                    )
                else:
                    print(_updated_node.code)
            except Exception as err:
                print(f"fail to parse {_path} {type(err)} {err}")


if __name__ == "__main__":
    main()
