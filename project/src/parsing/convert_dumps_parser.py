import argparse


def get_convert_dumps_parser():
    parser = argparse.ArgumentParser()

    file_group = parser.add_argument_group(
        "File Arguments", "Arguments relating to file paths."
    )

    # region File Arguments
    file_group.add_argument(
        "--dump_path",
        type=str,
        required=True,
        help="A string representing the path to the JSON dump.",
    )

    file_group.add_argument(
        "--destination_path",
        type=str,
        default=None,
        help="A string representing the destination folder path.",
    )

    # endregion

    return parser
