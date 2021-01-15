import copy
import sys
from typing import Iterable, List, Set

import numpy as np

from .customer import Customer, CustomerGraph
from .route import Route
from .scheduler import Scheduler


def first_time_when_done(customer: Customer):
    return customer.ready_time + customer.service_time


def rounded_distance(x: Customer, y: Customer):
    return int(np.ceil(x.distance(y)) + 0.1)


def is_eligible(x: Customer, depot: Customer):
    return (first_time_when_done(x) + rounded_distance(x, depot)) <= depot.due_time


def get_earliest_service_time(customer: Customer, depot: Customer):
    return max(
        depot.ready_time,
        customer.ready_time - (rounded_distance(customer, depot) + depot.service_time),
    )


class GreedyScheduler(Scheduler):
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

    def construct_solution(self, customers: Iterable[Customer]):
        depot = [x for x in customers if x.number == 0][0]

        # Remove customers that can't be serviced before depot
        # closes
        eligible_customers = {x for x in customers if is_eligible(x=x, depot=depot)}

        # Build a CustomerGraph from the eligible customers
        graph = CustomerGraph(customers=eligible_customers)

        customers_to_ignore = {x for x in customers if x.number == 0}

        # Sort customers so priority is given to those that have
        # earlier due times, earlier ready times and smaller
        # service times.
        customer_pick_order = list(
            sorted(
                set(eligible_customers),
                key=lambda x: (x.due_time, x.ready_time - x.service_time, -x.demand),
            )
        )
        index = 0

        routes = list()

        while index < len(customer_pick_order):
            if customer_pick_order[index] in customers_to_ignore:
                index += 1
                continue

            current_route = Route()
            current_route.add_stop(customer=copy.deepcopy(depot))

            while index < len(customer_pick_order):
                if customer_pick_order[index] in customers_to_ignore:
                    index += 1
                    continue

                max_cost = self.vehicle_capacity - current_route.cost
                first = customer_pick_order[index]
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
                            # Only nearest is viable
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
                routes.append(current_route)

        return routes
