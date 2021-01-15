import copy
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import numpy as np


class Customer:
    @staticmethod
    def _check_init_args(
        number: int,
        x: int,
        y: int,
        demand: int,
        ready_time: int,
        due_time: int,
        service_time: int,
        serviced_at: Optional[int],
    ) -> Tuple[int, int, int, int, int, int, int, int]:
        if serviced_at is None:
            serviced_at = 0

        # region Type Checking
        try:
            number = int(number)
        except TypeError:
            raise TypeError(
                "Expected argument number to be an int or castable to one, "
                f"instead it is {type(number)}."
            )

        try:
            x = int(x)
        except TypeError:
            raise TypeError(
                "Expected argument x to be an int or castable to one, instead it is "
                f"{type(x)}."
            )

        try:
            y = int(y)
        except TypeError:
            raise TypeError(
                "Expected argument y to be an int or castable to one, instead it is "
                f"{type(y)}."
            )

        try:
            demand = int(demand)
        except TypeError:
            raise TypeError(
                "Expected argument demand to be an int or castable to one, instead it "
                f"is {type(demand)}."
            )

        try:
            ready_time = int(ready_time)
        except TypeError:
            raise TypeError(
                "Expected argument ready_time to be an int or castable to one, instead "
                f"it is {type(ready_time)}."
            )

        try:
            due_time = int(due_time)
        except TypeError:
            raise TypeError(
                "Expected argument due_time to be an int or castable to one, instead "
                f"it is {type(due_time)}."
            )

        try:
            service_time = int(service_time)
        except TypeError:
            raise TypeError(
                "Expected argument service_time to be an int or castable to one, "
                f"instead it is {type(service_time)}."
            )

        if not isinstance(serviced_at, int):
            raise TypeError(
                "Expected argument serviced_at to be an int, instead it is "
                f"{type(serviced_at)}."
            )

        # endregion

        return number, x, y, demand, ready_time, due_time, service_time, serviced_at

    def __init__(
        self,
        number: int,
        x: int,
        y: int,
        demand: int,
        ready_time: int,
        due_time: int,
        service_time: int,
        serviced_at: Optional[int] = None,
    ):
        (
            number,
            x,
            y,
            demand,
            ready_time,
            due_time,
            service_time,
            serviced_at,
        ) = self._check_init_args(
            number=number,
            x=x,
            y=y,
            demand=demand,
            ready_time=ready_time,
            due_time=due_time,
            service_time=service_time,
            serviced_at=serviced_at,
        )

        self._number = number
        self._x = x
        self._y = y
        self._demand = demand
        self._ready_time = ready_time
        self._due_time = due_time
        self._service_time = service_time
        self._serviced_at = serviced_at

    # region Properties
    @property
    def number(self) -> int:
        return self._number

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def coords(self) -> Tuple[int, int]:
        return (self.x, self.y)

    @property
    def np_coords(self) -> np.ndarray:
        return np.array(self.coords)

    @property
    def demand(self):
        return self._demand

    @property
    def ready_time(self):
        return self._ready_time

    @property
    def due_time(self):
        return self._due_time

    @property
    def service_time(self):
        return self._service_time

    @property
    def serviced_at(self) -> int:
        return self._serviced_at

    @serviced_at.setter
    def serviced_at(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected argument value to be an int, instead it is {type(value)}."
            )

        self._serviced_at = value

    # endregion

    def distance(self, other: "Customer") -> float:
        return float(np.linalg.norm(self.np_coords - other.np_coords))

    def as_tuple(self):
        return (
            self.number,
            self.x,
            self.y,
            self.demand,
            self.ready_time,
            self.due_time,
            self.service_time,
            self.serviced_at,
        )

    # region Dunder Methods
    def __repr__(self):
        return f'({",".join([str(x) for x in self.as_tuple()])})'

    def __str__(self):
        return (
            f"Customer {self.number} @ ({self.x}, {self.y}) worth {self.demand}: ready "
            f"at {self.ready_time}, due at {self.due_time}, requires "
            f"{self.service_time}, serviced at {self.serviced_at}"
        )

    def __eq__(self, other: "Customer"):
        if other is None or not isinstance(other, Customer):
            return False

        return self.number == other.number

    def __hash__(self):
        return hash(self.number)

    # endregion


class CustomerGraph:
    @staticmethod
    def _check_init_args(customers: Iterable[Customer]):
        try:
            iter(customers)
        except TypeError:
            raise TypeError(
                "Expected argument customers to be an iterable, instead it is "
                f"{type(customers)}."
            )

        customers = set(customers)

        if len(customers) < 2:
            raise RuntimeError(
                "Expected argument customers to have at least a length of 2, instead "
                f"it has length {len(customers)}."
            )

        for customer in customers:
            if not isinstance(customer, Customer):
                raise TypeError(
                    "Expected all elements of argument customers to be of type "
                    f"Customer, but found an element of type {type(customer)}."
                )

        return sorted(customers, key=lambda x: x.coords)

    @staticmethod
    def initialize_graph(customers: List[Customer]):
        graph = dict()

        for i, customer in enumerate(customers[:-1]):
            key = customer.coords
            graph[key] = dict()

            for other in customers[i + 1 :]:
                graph[key][other.coords] = customer.distance(other)

        return graph

    def __init__(self, customers: Iterable[Customer]):
        customers = self._check_init_args(customers=customers)

        self._customers = copy.deepcopy(customers)
        self._graph = self.initialize_graph(customers=customers)

    # region Properties
    @property
    def customers(self):
        return copy.deepcopy(self._customers)

    @property
    def graph(self):
        return copy.deepcopy(self._graph)

    # endregion

    def get_distance(self, x: Customer, y: Customer) -> float:
        if x.coords == y.coords:
            return 0.0

        x, y = sorted([x, y], key=lambda x: x.coords)

        if x.coords not in self._graph:
            raise KeyError(f"Customer with coordinates {x.coords} isn't in the graph!")

        x = self._graph[x.coords]

        if y.coords not in x:
            raise KeyError(f"Customer with coordinates {y.coords} isn't in the graph!")

        return x[y.coords]

    def get_closest_neighbour_with_distance(
        self, customer: Customer, to_ignore: Iterable[Customer] = tuple()
    ):
        key = customer.coords

        if key == self._customers[0].coords:
            starting_index = 2
        else:
            starting_index = 1

        min_neighbour = copy.deepcopy(self._customers[starting_index - 1])
        min_distance = self.get_distance(customer, min_neighbour)

        for other in self._customers[starting_index:]:
            if key != other.coords and other not in to_ignore:
                distance = self.get_distance(customer, other)

                if distance < min_distance:
                    min_neighbour = copy.deepcopy(other)
                    min_distance = distance

        if min_neighbour in to_ignore:
            return None, None

        return min_neighbour, min_distance

    def get_closest_neighbour(
        self, customer: Customer, to_ignore: Iterable[Customer] = tuple()
    ):
        return self.get_closest_neighbour_with_distance(
            customer=customer, to_ignore=to_ignore
        )[0]

    def get_soonest_neighbour_with_time(
        self, customer: Customer, to_ignore: Iterable[Customer] = tuple()
    ):
        key = customer.coords

        if key == self._customers[0].coords:
            starting_index = 2
        else:
            starting_index = 1

        min_neighbour = copy.deepcopy(self._customers[starting_index - 1])
        min_time = max(
            min_neighbour.ready_time,
            customer.serviced_at + self.get_distance(customer, min_neighbour),
        )

        for other in self._customers[starting_index:]:
            if key != other.coords and other not in to_ignore:
                time = max(
                    min_neighbour.ready_time,
                    customer.serviced_at + self.get_distance(customer, min_neighbour),
                )

                if time < min_time:
                    min_neighbour = copy.deepcopy(other)
                    min_time = time

        if min_neighbour in to_ignore:
            return None, None

        return min_neighbour, min_time

    def get_soonest_neighbour(
        self, customer: Customer, to_ignore: Iterable[Customer] = tuple()
    ):
        return self.get_soonest_neighbour_with_time(
            customer=customer, to_ignore=to_ignore
        )[0]

    # region Dunder Methods
    def __str__(self):
        to_return = "A CustomerGraph containing:\n\t"
        to_return += "\n\t".join([str(x) for x in self._customers])

        return to_return

    # endregion
