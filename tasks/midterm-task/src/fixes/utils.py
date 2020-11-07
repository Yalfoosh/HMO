import csv
import os
from pathlib import Path
from typing import List, Tuple, Union


def load_csv(csv_path: Union[Path, str]) -> List:
    with open(
        csv_path, newline="", encoding="unicode-escape", errors="replace"
    ) as file:
        return list(csv.reader(file))


def save_rows(
    rows: Union[List, Tuple],
    destination_path: Union[Path, str],
    delimiter: str = "\t",
    quotechar: str = '"',
):
    with open(destination_path, mode="w+", encoding="utf8", errors="replace") as file:
        csv.writer(file, delimiter=delimiter, quotechar=quotechar).writerows(rows)


def get_filename_without_extension(file_path: Union[Path, str]) -> str:
    file_basename = os.path.basename(file_path)
    filename_without_extension = file_basename.split(".")[0]

    return filename_without_extension
