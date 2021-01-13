import copy
from typing import Dict, List, Tuple, Union


from .utils import get_players_from_rows, Player


class NoSolution(Exception):
    def __init__(self, message):
        super().__init__(message)


class PlayerScoreMaximizer:
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

    def solve(
        self,
        price_budget: float,
        position_budget: Dict[str, int],
        max_players_per_club: int = 3,
        verbosity: int = 0,
    ):
        # First attempt and construct a team consisting of the cheapest players
        cheapest_players = sorted(
            self.players,
            key=lambda x: (x.price, -x.score),
        )
        money_left = price_budget
        position_spending = {k: 0 for k in position_budget}
        club_spending = {
            club: 0 for club in {player.club for player in cheapest_players}
        }
        number_of_players = sum(position_budget.values())

        initial_solution = list()

        for player in cheapest_players:
            if len(initial_solution) >= number_of_players:
                break

            if (
                position_spending[player.position] < position_budget[player.position]
                and club_spending[player.club] < max_players_per_club
            ):
                if player.price <= money_left:
                    initial_solution.append(player)

                    position_spending[player.position] += 1
                    club_spending[player.club] += 1
                    money_left -= player.price
                else:
                    break

        # If we can't get the required number of players choosing
        # the cheapest ones, there is no solution.
        if len(initial_solution) < number_of_players:
            raise NoSolution("There is no solution for the given constraints.")

        if verbosity > 10:
            print(f"[Initial]  Score: {sum([x.score for x in initial_solution]):g}")

            if verbosity > 11:
                print(f"[Initial] Money left: {money_left}")

            print()

        # We evaluate our pools by max score, so we can copy the
        # self.pools which are already sorted.
        pools = copy.deepcopy(self.pools)

        # Remove chosen players from the pool, since we've picked
        # them already and will never pick them again.
        for player in initial_solution:
            pools[player.position].remove(player)

        current_solution = copy.deepcopy(initial_solution)

        while True:
            # Sort the solution so the lowest scores are attended
            # to first.
            current_solution = sorted(current_solution, key=lambda x: x.score)

            index_to_remove = None

            for i, player in enumerate(current_solution):
                # print(player)
                # Assume we're not going to have to play for the
                # player we've got if we're swapping.
                hypothetical_money = money_left + player.price

                for j, new_player in enumerate(pools[player.position]):
                    if new_player.score > player.score and (
                        player.club == new_player.club
                        or club_spending[new_player.club] < max_players_per_club
                    ):
                        if new_player.price <= hypothetical_money:
                            index_to_remove = j

                            club_spending[player.club] -= 1
                            club_spending[new_player.club] += 1

                            current_solution[i] = copy.deepcopy(new_player)
                            money_left = hypothetical_money - new_player.price

                            break

                # If index_to_remove is not None, we found a swap.
                # So we need to exclude the new player from the
                # pool.
                if index_to_remove is not None:
                    del pools[player.position][index_to_remove]
                    break

            if verbosity > 10:
                print(f"[New]  Score: {sum([x.score for x in current_solution]):g}")

                if verbosity > 11:
                    print(f"[New] Money left: {money_left}")

                print()

            # If no solution was found, this is the best solution
            # so return it.
            if index_to_remove is None:
                return current_solution
