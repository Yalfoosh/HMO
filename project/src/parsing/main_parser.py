import argparse


def get_main_parser():
    parser = argparse.ArgumentParser()

    file_group = parser.add_argument_group(
        "File Arguments", "Arguments relating to file paths."
    )

    constraint_group = parser.add_argument_group(
        "Constraint Arguments", "Arguments relating to constraints."
    )

    # region File Arguments
    file_group.add_argument(
        "--instance_path",
        type=str,
        required=True,
        help=(
            "A string representing the path to the instance. Can be either the .txt "
            "variant, or the JSON variant."
        ),
    )

    file_group.add_argument(
        "--dump_path",
        type=str,
        default=None,
        help=(
            "A string representing the path to the dump location. If it's a folder, "
            "the dump will be saved as dump.json. Default: None (no dumping)."
        ),
    )

    # endregion

    # region Constraint Arguments
    constraint_group.add_argument(
        "--max_runtime",
        type=int,
        nargs="+",
        default=(1, 5, 25),
        help=(
            "A list of ints representing the maximum number of minutes the algorithm "
            "will run. Duplicates will be removed. To make the algorithm run "
            "indefinitely, pass a large number. Default: (1, 5, 25)"
        ),
    )

    # endregion

    return parser
