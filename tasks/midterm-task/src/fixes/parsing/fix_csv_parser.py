import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    path_group = parser.add_argument_group(
        "Path Arguments", "Arguments relating to paths"
    )

    format_group = parser.add_argument_group(
        "Format Arguments", "Arguments relating to the output format"
    )
    format_mutex = format_group.add_mutually_exclusive_group()

    # region Path Arguments
    path_group.add_argument(
        "--csv_paths",
        type=str,
        metavar="PATH",
        nargs="+",
        required=True,
        help="A list of paths to the CSV files you wish to fix.",
    )

    path_group.add_argument(
        "--destination_folder",
        type=str,
        metavar="DIR",
        default=None,
        help=(
            "A path to the folder where corrected files will be saved. Defaults to "
            "None (same folder as source)."
        ),
    )

    # endregion

    # region Processing Arguments
    format_mutex.add_argument(
        "--csv",
        action="store_true",
        help=(
            "A flag; if set the output will be a CSV file. Mutually exclusive with "
            "--tsv."
        ),
    )

    format_mutex.add_argument(
        "--tsv",
        action="store_true",
        help=(
            "A flag; if set the output will be a TSV file. Mutually exclusive with "
            "--csv."
        ),
    )

    # endregion

    return parser
