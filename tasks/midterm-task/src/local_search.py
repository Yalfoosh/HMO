import csv
import os
from pathlib import Path

from parsing import local_search_parser
from parsing.local_search_config import LocalSearchConfig
from searches.main_team_search import get_main_team_and_bench
from searches.player_score_negotiator import PlayerScoreNegotiator
from searches.utils import get_players_from_rows


def main():
    parser = local_search_parser.get_parser()
    args = parser.parse_args()

    config = LocalSearchConfig(args)

    with open(
        config.instance_path, newline="", encoding="utf8", errors="replace"
    ) as file:
        delimiter = (
            ","
            if config.instance_path.endswith("csv")
            else "\t"
            if config.instance_path.endswith("tsv")
            else None
        )
        rows = list(csv.reader(file, delimiter=delimiter))

    with open(
        config.solution_path, newline="", encoding="utf8", errors="replace"
    ) as file:
        delimiter = (
            ","
            if config.instance_path.endswith("csv")
            else "\t"
            if config.instance_path.endswith("tsv")
            else None
        )
        best_team_rows = list(csv.reader(file, delimiter=delimiter))

    current_solution = get_players_from_rows(best_team_rows)

    psn = PlayerScoreNegotiator(rows=rows)
    best_team = psn.solve(
        current_solution=current_solution,
        price_budget=config.price_budget,
        position_budget=config.position_budget,
        main_team_ranges=config.main_team_ranges,
        max_players_in_main_team=config.max_players_in_main_team,
        max_players_per_club=config.max_players_per_club,
        verbosity=config.verbosity,
    )

    main_team, bench = get_main_team_and_bench(
        team=best_team, main_team_ranges=config.main_team_ranges
    )

    if config.verbosity > 0:
        print(f"\nScore: {sum([x.score for x in main_team])}")
        print(f"Price: {sum([x.price for x in current_solution])}")

        if config.verbosity > 1:
            print("Main team:")

            for x in main_team:
                print(f"\t{x}")

            print("\nBench:")

            for x in bench:
                print(f"\t{x}")

    dump_rows = list()

    for player in best_team:
        dump_rows.append(
            (
                player.id,
                player.position,
                player.name,
                player.club,
                player.score,
                player.price,
            )
        )

    dump_path = Path(config.dump_path)
    solution_dump_path = Path(config.solution_dump_path)
    os.makedirs(dump_path.parent, exist_ok=True)
    os.makedirs(solution_dump_path.parent, exist_ok=True)

    with open(
        config.dump_path, newline="", mode="w+", encoding="utf8", errors="replace"
    ) as file:

        csv.writer(file, delimiter=delimiter).writerows(dump_rows)

    with open(
        config.solution_dump_path,
        newline="",
        mode="w+",
        encoding="utf8",
        errors="replace",
    ) as file:
        main_ids = [f"{player.id}" for player in main_team]
        bench_ids = [f"{player.id}" for player in bench]

        main_ids = ",".join(sorted(main_ids))
        bench_ids = ",".join(sorted(bench_ids))

        to_write = f"{main_ids}\n{bench_ids}"
        file.write(to_write)


if __name__ == "__main__":
    main()
