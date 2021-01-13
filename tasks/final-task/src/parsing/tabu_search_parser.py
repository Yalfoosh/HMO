import argparse


def get_parser():
    parser = argparse.ArgumentParser()

    path_group = parser.add_argument_group(
        "Path Arguments", "Arguments relating to paths"
    )

    algorithm_group = parser.add_argument_group(
        "Algorithm Arguments", "Arguments relating to Tabu Search"
    )

    constraint_group = parser.add_argument_group(
        "Constraint Arguments", "Arguments relating to constraints"
    )

    output_group = parser.add_argument_group(
        "Output Arguments", "Arguments relating to output"
    )

    # region Path Arguments
    path_group.add_argument(
        "--instance_path",
        type=str,
        metavar="PATH",
        required=True,
        help="A path to the player population.",
    )

    path_group.add_argument(
        "--dump_path",
        type=str,
        metavar="PATH",
        default="data/greedy-search/dump.json",
        help=(
            "A path to the dump file with the results. Defaults to "
            "data/greedy-search/dump.json."
        ),
    )

    # endregion

    # region Algorithm Arguments
    algorithm_group.add_argument(
        "--tabu_tenures",
        type=int,
        nargs="+",
        default=[15],
        help=(
            "A list of floats representing the capacity of the tabu list. Defaults to "
            "15.",
        ),
    )

    algorithm_group.add_argument(
        "--max_iterations_without_improvement",
        type=int,
        default=10,
        help=(
            "An int representing the number of iterations without improvement after "
            "which the search stops. Defaults to 10."
        ),
    )

    # endregion

    # region Constraint Arguments
    constraint_group.add_argument(
        "--price_budget",
        type=float,
        default=100.0,
        help=(
            "A float representing the price budget for the whole team in millions. "
            "Defaults to 100.0."
        ),
    )

    constraint_group.add_argument(
        "--max_players_in_main_team",
        type=int,
        default=11,
        help=(
            "An int representing the maximum number of players in the main team. "
            "Defaults to 11"
        ),
    )

    constraint_group.add_argument(
        "--max_players_per_club",
        type=int,
        default=3,
        help=(
            "An int representing the maximum number of players from the same club. "
            "Defaults to 3."
        ),
    )

    constraint_group.add_argument(
        "--gk_count",
        type=int,
        default=2,
        help="An int representing the number of goalkeepers to choose. Defaults to 2.",
    )

    constraint_group.add_argument(
        "--def_count",
        type=int,
        default=5,
        help="An int representing the number of defenders to choose. Defaults to 5.",
    )

    constraint_group.add_argument(
        "--mid_count",
        type=int,
        default=5,
        help="An int representing the number of midfielders to choose. Defaults to 5.",
    )

    constraint_group.add_argument(
        "--fw_count",
        type=int,
        default=3,
        help="An int representing the number of forwards to choose. Defaults to 3.",
    )

    constraint_group.add_argument(
        "--gk_range",
        type=int,
        nargs="+",
        default=(1, 1),
        help=(
            "A pair of ints representing the minimum and the maximum number of "
            "goalkeepers in the main team. Defaults to exactly 1."
        ),
    )

    constraint_group.add_argument(
        "--def_range",
        type=int,
        nargs="+",
        default=(3,),
        help=(
            "A pair of ints representing the minimum and the maximum number of "
            "defenders in the main team. Defaults to at least 3."
        ),
    )

    constraint_group.add_argument(
        "--mid_range",
        type=int,
        nargs="+",
        default=(0,),
        help=(
            "A pair of ints representing the minimum and the maximum number of "
            "midfielders in the main team. Defaults to any number."
        ),
    )

    constraint_group.add_argument(
        "--fw_range",
        type=int,
        nargs="+",
        default=(1,),
        help=(
            "A pair of ints representing the minimum and the maximum number of "
            "goalkeepers in the main team. Defaults to at least 1."
        ),
    )
    # endregion

    # region Output Arguments
    output_group.add_argument(
        "--verbosity",
        type=int,
        default=0,
        help=(
            "An int representing the level of verbosity for console output. Defaults "
            "to 0 (no output)."
        ),
    )

    # endregion

    return parser
