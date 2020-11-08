import copy
from typing import Dict, List, Tuple


from .utils import Player


def get_main_team_and_bench(
    team: List[Player],
    main_team_ranges: Dict[str, Tuple[int, int]],
    max_players_in_main_team: int = 11,
) -> Tuple[List[Player], List[Player]]:
    team = copy.deepcopy(team)
    main_team = list()
    bench = list()

    position_spending = {k: 0 for k in main_team_ranges}

    for position, p_range in main_team_ranges.items():
        minimum = p_range[0]

        if minimum > 0:
            choices = [
                copy.deepcopy(player) for player in team if player.position == position
            ]
            taken_choices = sorted(choices, key=lambda x: -x.score)[:minimum]

            for taken_choice in taken_choices:
                team.remove(taken_choice)
                main_team.append(taken_choice)
                position_spending[taken_choice.position] += 1

    the_rest = copy.deepcopy(team)
    the_rest.sort(key=lambda x: -x.score)

    for player in the_rest:
        if len(main_team) >= max_players_in_main_team:
            bench.append(player)
            continue

        if position_spending[player.position] < main_team_ranges[player.position][1]:
            main_team.append(player)
            position_spending[player.position] += 1
        else:
            bench.append(player)

    return main_team, bench
