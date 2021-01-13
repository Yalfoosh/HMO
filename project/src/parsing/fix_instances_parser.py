import argparse


def get_fix_instances_parser():
    parser = argparse.ArgumentParser()

    file_group = parser.add_argument_group(
        "File Arguments", "Arguments related to file paths."
    )

    file_group.add_argument(
        "--source_folder_path",
        type=str,
        required=True,
        help=(
            "A string representing the path to the folder where the .txt files you "
            "wish to convert to JSON are."
        ),
    )

    file_group.add_argument(
        "--destination_folder_path",
        type=str,
        required=True,
        help="A string representing the destination folder path of the converted JSON.",
    )

    return parser
