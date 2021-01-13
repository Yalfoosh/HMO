import csv
import json
import os
from pathlib import Path

from parsing import tabu_search_parser
from parsing.tabu_search_config import TabuSearchConfig
from searches.main_team_search import get_main_team_and_bench
from searches.player_score_maximizer import PlayerScoreMaximizer
from searches.player_tabu_search import PlayerTabooSearch


def main():
    parser = tabu_search_parser.get_parser()
    args = parser.parse_args()

    config = TabuSearchConfig(args)

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

    psm = PlayerScoreMaximizer(rows=rows)
    best_team = psm.solve(
        price_budget=config.price_budget,
        position_budget=config.position_budget,
        max_players_per_club=config.max_players_per_club,
        verbosity=config.verbosity,
    )

    main_team, bench = get_main_team_and_bench(
        team=best_team, main_team_ranges=config.main_team_ranges
    )

    for x in main_team:
        print(x)

    print("---")

    for x in bench:
        print(x)

    tabu_dict = {"tenure": dict()}

    for tabu_tenure in config.tabu_tenures:
        pts = PlayerTabooSearch(players=psm.players, team=best_team)
        tabu_team = pts.solve(
            initial_team=best_team,
            tabu_tenure=tabu_tenure,
            max_iterations_without_improvement=(
                config.max_iterations_without_improvement
            ),
            price_budget=config.price_budget,
            main_team_ranges=config.main_team_ranges,
            position_budget=config.position_budget,
            max_players_per_club=config.max_players_per_club,
            verbosity=config.verbosity,
        )

        main_team_taboo, bench_taboo = get_main_team_and_bench(
            team=tabu_team, main_team_ranges=config.main_team_ranges
        )

        print(f"\n\nBest team for Tabu tenure {tabu_tenure}:")

        for x in main_team_taboo:
            print(x)

        print("---")

        for x in bench_taboo:
            print(x)

        tabu_price = sum([x.price for x in tabu_team])
        tabu_score = sum([x.score for x in main_team_taboo])

        print(f"With a price of {tabu_price} and score {tabu_score}")

        if tabu_tenure not in tabu_dict["tenure"]:
            tabu_dict["tenure"][tabu_tenure] = dict()

        tabu_dict["tenure"][tabu_tenure]["main_team"] = [x.id for x in main_team_taboo]
        tabu_dict["tenure"][tabu_tenure]["bench"] = [x.id for x in bench_taboo]
        tabu_dict["tenure"][tabu_tenure]["price"] = tabu_price
        tabu_dict["tenure"][tabu_tenure]["score"] = tabu_score

    with open(config.dump_path, mode="w+") as file:
        json.dump(tabu_dict, file, indent=2)


if __name__ == "__main__":
    main()
