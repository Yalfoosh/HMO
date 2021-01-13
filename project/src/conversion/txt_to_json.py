import json
import os
from pathlib import Path
from typing import Any, Dict, Union

from .constants import WHITESPACE_REGEX, COLUMN_SEPARATOR_REGEX
from .parsing.txt_to_json_parser import get_txt_to_json_parser


def parse_txt(txt: str) -> Dict[str, Any]:
    to_return = dict()

    lines = txt.splitlines()
    lines = [x.strip() for x in lines]

    vehicle_columns = WHITESPACE_REGEX.split(lines[1])
    vehicle_tuple = WHITESPACE_REGEX.split(lines[2])
    customer_columns = COLUMN_SEPARATOR_REGEX.split(lines[5])
    customer_rows = [
        WHITESPACE_REGEX.split(line)
        for line in lines[7:]
        if (line is not None and len(line) != 0)
    ]

    to_return["vehicle"] = dict()

    for column, element in zip(vehicle_columns, vehicle_tuple):
        to_return["vehicle"][column.lower()] = int(element)

    to_return["customers"] = [tuple([x.lower() for x in customer_columns])]

    for row in customer_rows:
        row_to_add = tuple([int(x) for x in row])
        to_return["customers"].append(row_to_add)

    return to_return


def txt_to_json(source_path: Union[Path, str], destination_path: Union[Path, str]):
    src = Path(source_path)
    dest = Path(destination_path)

    if not os.path.exists(src):
        raise FileNotFoundError(f"Source path {src} doesn't exist!")

    with open(src, encoding="utf8", errors="replace") as file:
        json_dict = parse_txt(file.read())

    os.makedirs(dest.parent, exist_ok=True)

    with open(dest, mode="w+", encoding="utf8", errors="replace") as file:
        json.dump(
            json_dict,
            file,
            skipkeys=False,
            ensure_ascii=False,
            sort_keys=False,
        )


def main():
    parser = get_txt_to_json_parser()
    args = parser.parse_args()

    txt_to_json(source_path=args.source_path, destination_path=args.destination_path)


if __name__ == "__main__":
    main()
