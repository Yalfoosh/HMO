import argparse


def get_txt_to_json_parser():
    parser = argparse.ArgumentParser()

    file_group = parser.add_argument_group(
        "File Arguments", "Arguments relating to file paths."
    )

    file_group.add_argument(
        "--source_path",
        type=str,
        required=True,
        help=(
            "A string representing the path to the .txt file you want to convert to "
            "JSON."
        ),
    )

    file_group.add_argument(
        "--destination_path",
        type=str,
        required=True,
        help="A string representing the destination path of the converted JSON.",
    )

    return parser
