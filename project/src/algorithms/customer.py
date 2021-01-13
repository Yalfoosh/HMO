import copy
from typing import Any, Dict, Iterable, List, Set, Tuple

import numpy as np


class Customer:
    @staticmethod
    def _check_init_args(
        customer_number: int,
        x: int,
        y: int,
        demand: int,
        ready_time: int,
        due_time: int,
        service_time: int,
    ) -> Tuple[int, int, int, int, int, int, int]:
        # region Type Checking
        try:
            customer_number = int(customer_number)
        except TypeError:
            raise TypeError(
                "Expected argument customer_number to be an int or castable to one, "
                f"instead it is {type(customer_number)}."
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

        # endregion

        # region Logic Checking
        if ready_time + service_time > due_time:
            raise RuntimeError(
                "Expected argument due_time to be greater or equal to ready_time + "
                f"service_time ({ready_time + service_time}), instead it is "
                f"{due_time}. As a consequence, this node will make the problem not "
                "solvable."
            )

        # endregion

        return customer_number, x, y, demand, ready_time, due_time, service_time

    def __init__(
        self,
        customer_number: int,
        x: int,
        y: int,
        demand: int,
        ready_time: int,
        due_time: int,
        service_time: int,
    ):
        (
            customer_number,
            x,
            y,
            demand,
            ready_time,
            due_time,
            service_time,
        ) = self._check_init_args(
            customer_number=customer_number,
            x=x,
            y=y,
            demand=demand,
            ready_time=ready_time,
            due_time=due_time,
            service_time=service_time,
        )

        self._customer_number = customer_number
        self._x = x
        self._y = y
        self._demand = demand
        self._ready_time = ready_time
        self._due_time = due_time
        self._service_time = service_time

    # region Properties
    @property
    def customer_number(self) -> int:
        return self._customer_number

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

    # endregion

    def distance(self, other: "Customer") -> float:
        return float(np.linalg.norm(self.np_coords - other.np_coords))

    def as_tuple(self):
        return (
            self.customer_number,
            self.x,
            self.y,
            self.demand,
            self.ready_time,
            self.due_time,
            self.service_time,
        )

    def __repr__(self):
        return f'({",".join(self.as_tuple())})'

    def __str__(self):
        return (
            f"Customer {self.customer_number:04d} @ ({self.x}, {self.y}): ready at "
            f"{self.ready_time}, due at {self.due_time}, requires {self.service_time}"
        )

    def __eq__(self, other: "Customer"):
        if other is None or not isinstance(other, Customer):
            return False

        return self.customer_number == other.customer_number

    def __hash__(self):
        return hash(self.as_tuple())


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

        return min_neighbour, min_distance

    def get_closest_neighbour(
        self, customer: Customer, to_ignore: Iterable[Customer] = tuple()
    ):
        return self.get_closest_neighbour_with_distance(
            customer=customer, to_ignore=to_ignore
        )[0]

    def __str__(self):
        to_return = "A CustomerGraph containing:\n\t"
        to_return += "\n\t".join([str(x) for x in self._customers])

        return to_return
