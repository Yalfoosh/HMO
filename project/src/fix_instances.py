import os
from pathlib import Path
from typing import Union

from conversion.txt_to_json import txt_to_json
from parsing.fix_instances_parser import get_fix_instances_parser


def fix_instances(
    source_folder_path: Union[Path, str], destination_folder_path: Union[Path, str]
):
    src_folder = Path(source_folder_path)
    dest_folder = Path(destination_folder_path)

    if not os.path.exists(src_folder):
        raise FileNotFoundError(f"Folder {src_folder} doesn't exist!")

    if not os.path.isdir(src_folder):
        raise NotADirectoryError(f"Path {src_folder} doesn't point to a directory!")

    if os.path.exists(dest_folder):
        if not os.path.isdir(dest_folder):
            raise NotADirectoryError(f"Path {src_folder} doesn't point to a directory!")
    else:
        os.makedirs(dest_folder)

    for file_name in os.listdir(src_folder):
        source_path = os.path.join(src_folder, file_name)
        destination_path = os.path.join(dest_folder, f"{Path(file_name).stem}.json")

        txt_to_json(source_path=source_path, destination_path=destination_path)


def main():
    parser = get_fix_instances_parser()
    args = parser.parse_args()

    fix_instances(
        source_folder_path=args.source_folder_path,
        destination_folder_path=args.destination_folder_path,
    )


if __name__ == "__main__":
    main()
