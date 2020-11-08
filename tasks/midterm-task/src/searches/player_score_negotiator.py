import copy
from typing import Dict, List, Tuple, Union


from .main_team_search import get_main_team_and_bench
from .utils import get_players_from_rows, Player


class PlayerScoreNegotiator:
    def __init__(
        self,
        rows: List[List],
    ):
        # We just separate players into position pools and sort
        # them in a descending order by price.
        players: List[Player] = get_players_from_rows(rows=rows)
        positions = {player.position for player in players}

        self.pools = {
            position: [player for player in players if player.position == position]
            for position in positions
        }

        for position, pool in self.pools.items():
            self.pools[position] = sorted(pool, key=lambda x: -x.score)

    @property
    def players(self) -> List[Player]:
        to_return = list()

        for pool in self.pools.values():
            to_return.extend(pool)

        return to_return

    def find_cheaper_bench(
        self,
        bench: List[Player],
        pools: Dict[str, List[Player]],
        club_spending: Dict[str, int],
        max_players_per_club: int = 3,
    ):
        new_bench = list()
        new_bench_target_length = len(bench)
        new_bench_candidates = list()
        new_position_budget = {k: 0 for k in {player.position for player in bench}}
        new_position_spending = copy.deepcopy(new_position_budget)

        for player in bench:
            # First ignore the clubs of the bench, as they might
            # all get swapped around
            club_spending[player.club] -= 1
            new_position_budget[player.position] += 1

            new_bench_candidates.append(copy.deepcopy(player))
            new_bench_candidates.extend(
                [x for x in pools[player.position] if x.price <= player.price]
            )

        # Sort the new candidates by price in an ascending order
        # so we check the cheapest ones first.
        new_bench_candidates.sort(key=lambda x: x.price)

        # Greedily get the cheapest bench
        for player in new_bench_candidates:
            if len(new_bench) >= new_bench_target_length:
                break

            if (
                new_position_spending[player.position]
                < new_position_budget[player.position]
                and club_spending[player.club] < max_players_per_club
            ):
                if player in pools[player.position]:
                    pools[player.position].remove(player)

                new_bench.append(copy.deepcopy(player))
                new_position_spending[player.position] += 1
                club_spending[player.club] += 1

        players_to_add_to_pool = set(new_bench) - set(bench)
        pools[player.position].extend(list(players_to_add_to_pool))

        return new_bench

    def solve(
        self,
        current_solution: List[Player],
        price_budget: float,
        position_budget: Dict[str, int],
        main_team_ranges: Dict[str, Tuple[int, int]],
        max_players_in_main_team: int = 11,
        max_players_per_club: int = 3,
        verbosity: int = 0,
    ):
        # Adjust the pool so they don't include the current
        # solution.
        pools = copy.deepcopy(self.pools)

        for player in current_solution:
            pools[player.position].remove(player)

        # Calculate the search state
        position_spending = {k: 0 for k in position_budget}
        club_spending = {k: 0 for k in {player.club for player in self.players}}

        for player in current_solution:
            position_spending[player.position] += 1
            club_spending[player.club] += 1

        # Get the main team and the bench
        main_team, bench = get_main_team_and_bench(
            team=current_solution,
            main_team_ranges=main_team_ranges,
            max_players_in_main_team=max_players_in_main_team,
        )

        # Make the bench as cheap as you can
        bench = self.find_cheaper_bench(
            bench,
            pools=pools,
            club_spending=club_spending,
            max_players_per_club=max_players_per_club,
        )
        current_solution = main_team + bench

        # Recalulate the money we have left
        money_left = price_budget - sum([x.price for x in current_solution])

        # Second phase: try upgrading main team members with low
        # price efficiencies
        while True:
            main_team = sorted(main_team, key=lambda x: x.score + x.price_efficiency)
            swapped = False

            for i, player in enumerate(main_team):
                hypothetical_money = money_left + player.price

                better_players = [
                    x for x in pools[player.position] if x.score > player.score
                ]

                for better_player in sorted(
                    better_players, key=lambda x: (-x.score, x.price)
                ):
                    if better_player.price <= hypothetical_money and (
                        player.club == better_player.club
                        or club_spending[better_player.club] < max_players_per_club
                    ):
                        club_spending[player.club] -= 1
                        club_spending[better_player.club] += 1

                        main_team[i] = copy.deepcopy(better_player)
                        money_left = hypothetical_money - better_player.price

                        swapped = True
                        break

                # If a swap occured, break so that player swap
                # priorities get recalculated.
                if swapped:
                    break

            # If no swaps occured, our current solution is the
            # optimal one.
            if not swapped:
                break

        return main_team + bench
