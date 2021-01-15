import copy
import sys
from typing import List, Optional, Set

import numpy as np

from .customer import Customer, CustomerGraph
from .route import Route
from .scheduler import Scheduler


def rounded_distance(x: Customer, y: Customer):
    return int(np.ceil(x.distance(y)) + 0.1)


def route_loss(routes: List[Route]):
    return len(routes) * 1000000 - sum(
        abs(route.cost - routes[i - 1].cost) for i, route in enumerate(routes[1:])
    )


class MergerScheduler(Scheduler):
    def __init__(self, n_vehicles: int, vehicle_capacity: int):
        super().__init__(n_vehicles=n_vehicles, vehicle_capacity=vehicle_capacity)

    def get_nearest_viable_customer(
        self,
        max_cost: int,
        last_customer: Customer,
        graph: CustomerGraph,
        to_ignore: Set[Customer],
    ):
        to_ignore = copy.deepcopy(to_ignore)

        base_time = last_customer.serviced_at + last_customer.service_time

        while True:
            nearest_customer = graph.get_closest_neighbour(
                customer=last_customer, to_ignore=to_ignore
            )

            if nearest_customer is None:
                return None

            nearest_time = base_time + rounded_distance(last_customer, nearest_customer)

            if (
                nearest_time > nearest_customer.due_time
                or nearest_customer.demand > max_cost
            ):
                to_ignore.add(nearest_customer)
            else:
                return nearest_customer

        return None

    def merge_routes(self, routes: List[Route]):
        original_value = route_loss(routes=routes)

        depot = [x for x in routes[0] if x.number == 0][0]
        customer_pool = set()

        for route in routes:
            customer_pool.update({x for x in route.customers})

        graph = CustomerGraph(customers=customer_pool)

        customer_pool = list(
            sorted(
                [x for x in customer_pool if x.number != 0],
                key=lambda x: (x.ready_time, x.due_time, x.demand),
            )
        )
        customers_to_ignore = {depot}

        new_routes = list()
        index = 0

        while index < len(customer_pool):
            if customer_pool[index] in customers_to_ignore:
                index += 1
                continue

            current_route = Route()
            current_route.add_stop(copy.deepcopy(depot))

            while index < len(customer_pool):
                if customer_pool[index] in customers_to_ignore:
                    index += 1
                    continue

                max_cost = self.vehicle_capacity - current_route.cost

                first = customer_pool[index]
                nearest = self.get_nearest_viable_customer(
                    max_cost=max_cost,
                    last_customer=current_route[-1],
                    graph=graph,
                    to_ignore=customers_to_ignore,
                )

                route_start = (
                    current_route[-1].serviced_at + current_route[-1].service_time
                )
                first_time = route_start + rounded_distance(current_route[-1], first)
                first_end = (
                    first_time + first.service_time + rounded_distance(first, depot)
                )

                if nearest is None:
                    # No viable nearest found
                    if (
                        first_time > first.due_time
                        or first.demand > max_cost
                        or first_end > depot.due_time
                    ):
                        # None are viable
                        break
                    else:
                        # Only first is viable
                        current_customer = first
                else:
                    nearest_time = route_start + rounded_distance(
                        current_route[-1], nearest
                    )
                    nearest_end = (
                        nearest_time
                        + nearest.service_time
                        + rounded_distance(nearest, depot)
                    )

                    if (
                        first_time > first.due_time
                        or first.demand > max_cost
                        or first_end > depot.due_time
                    ):
                        # First definitely isn't viable

                        if nearest_end > depot.due_time:
                            # Nearest isn't viable either, other
                            # constraints were checked in the
                            # nearest search method.
                            break
                        else:
                            # Only soonest is viable
                            current_customer = nearest
                    else:
                        # First is viable

                        if nearest_end > depot.due_time:
                            # Only first is viable
                            current_customer = first
                        else:
                            # Both are viable
                            if nearest.demand > first.demand:
                                # We'd like to take the highest
                                # demand one first, but only if
                                # we can do the first one
                                # afterwards

                                if nearest_end > first.due_time:
                                    # Prefer first one
                                    current_customer = first
                                else:
                                    # Both are viable, prefer nearest
                                    current_customer = nearest
                            else:
                                # Prefer first one
                                current_customer = first

                current_route.add_stop(customer=current_customer)
                customers_to_ignore.add(current_customer)

            # If the last customer is a depot, we failed to find
            # a solution.
            if current_route[-1] == depot:
                print(
                    "WARNING - Greedy Algorithm stopped early because it failed to "
                    "find a new Route.",
                    file=sys.stderr,
                )
                break
            else:
                current_route.add_stop(customer=copy.deepcopy(depot))
                new_routes.append(current_route)

        new_value = route_loss(new_routes)

        if new_value < original_value:
            return new_routes
        else:
            return None

    def optimize_solution(
        self, routes: List[Route], max_selected_routes: Optional[int] = None
    ):
        if len(routes) < 2:
            return None

        if not isinstance(max_selected_routes, int):
            max_selected_routes = None
        else:
            max_selected_routes = max(2, min(len(routes), max_selected_routes))

        if max_selected_routes is None:
            max_selected_routes = len(routes)

        routes_to_select = np.random.randint(2, max_selected_routes + 1)
        route_indices = np.random.choice(
            range(len(routes)), routes_to_select, replace=False
        )
        selected_routes = list()
        other_routes = list()

        for i in range(len(routes)):
            if i in route_indices:
                selected_routes.append(routes[i])
            else:
                other_routes.append(routes[i])

        new_routes = self.merge_routes(selected_routes)

        if new_routes is None:
            return None
        else:
            return new_routes + other_routes
