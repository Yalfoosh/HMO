import copy
from typing import Dict, List, Tuple

from tqdm import tqdm

from .main_team_search import get_score
from .utils import Player


class TabuList:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._storage = set()
        self._storage_items = set()
        self._counter = 0

    @property
    def capacity(self):
        return self._capacity

    def peek(self):
        iterator = iter(self._storage)

        try:
            _current = next(iterator)
        except StopIteration:
            return

        for x in _current:
            if x[0] < _current[0]:
                _current = x

        return _current

    def pop(self):
        to_pop = self.peek()

        self._storage.remove(to_pop)
        self._storage_items.remove(to_pop[1])

    def add(self, item):
        while len(self._storage) >= self.capacity:
            self.pop()

        self._storage.add((self._counter, item))
        self._storage_items.add(item)
        self._counter += 1

    def __contains__(self, item):
        return item in self._storage_items


class PlayerTabooSearch:
    def __init__(self, players: List[Player], team: List[Player]):
        self._players = copy.deepcopy(players)

        self._players_per_position = dict()

        for player in self.players:
            if player.position not in self.players_per_position:
                self.players_per_position[player.position] = list()

            self.players_per_position[player.position].append(player)

    @property
    def players(self):
        return self._players

    @property
    def players_per_position(self):
        return self._players_per_position

    def solve(
        self,
        initial_team: List[Player],
        tabu_tenure: int,
        max_iterations_without_improvement: int,
        price_budget: float,
        main_team_ranges: Dict[str, Tuple[int, int]],
        position_budget: Dict[str, int],
        max_players_per_club: int = 3,
        verbosity: int = 1,
    ):
        tabu_list = TabuList(capacity=tabu_tenure)

        def get_neighbours(self, solution: List[Player]):
            team_price = sum([x.price for x in solution])
            spent_position_budget = {}

            for player in solution:
                spent_position_budget[player.position] = (
                    spent_position_budget.get(player.position, 0) + 1
                )

            neighbours = set()

            team_set = set(solution)

            for i, player in enumerate(solution):
                current_neighbours = list()
                current_spent_position_budget = copy.deepcopy(spent_position_budget)
                current_spent_position_budget[player.position] -= 1

                available_budget = price_budget - team_price + player.price
                available_positions = [
                    x
                    for x, y in current_spent_position_budget.items()
                    if y < position_budget[x]
                ]

                available_players = list()

                for available_position in available_positions:
                    available_players.extend(
                        self.players_per_position[available_position]
                    )

                available_players = [
                    x
                    for x in available_players
                    if (x.price <= available_budget and x not in team_set)
                ]

                for available_player in available_players:
                    new_solution = copy.deepcopy(solution)
                    new_solution[i] = copy.deepcopy(available_player)

                    new_solution_tuple = tuple(new_solution)

                    if new_solution_tuple not in tabu_list:
                        current_neighbours.append(
                            (
                                get_score(
                                    team=new_solution, main_team_ranges=main_team_ranges
                                ),
                                tuple(new_solution),
                            )
                        )

                neighbours.update(set(current_neighbours))

            return neighbours

        current_solution = copy.deepcopy(initial_team)
        best_solution = copy.deepcopy(current_solution)
        current_best = get_score(
            team=current_solution, main_team_ranges=main_team_ranges
        )
        counter = 0

        tabu_list.add(tuple(current_solution))
        iterator = tqdm(None)

        while True:
            new_solution = None

            neighbours = get_neighbours(self, solution=current_solution)
            neighbours = sorted(
                neighbours, key=lambda x: (-x[0], sum([xx.price for xx in x[1]]))
            )

            if len(neighbours) == 0:
                break
            else:
                new_best, new_solution = neighbours[0]

            new_solution = list(new_solution)

            if new_best > current_best:
                best_solution = copy.deepcopy(new_solution)
                current_best = new_best
                counter = 0
            else:
                counter += 1

            iterator.update()
            iterator.set_description(f"No improvement seen for {counter} iterations")

            current_solution = new_solution

            if counter >= max_iterations_without_improvement:
                print("Timed out")
                break

        return best_solution
