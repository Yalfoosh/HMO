import copy
from typing import Callable, Iterable, List, Optional

import numpy as np

from customer import Customer


class Route:
    @staticmethod
    def _default_function(
        current: Customer, previous: Optional[Customer] = None
    ) -> Customer:
        if previous is None:
            current.serviced_at = 0
        else:
            current.serviced_at = (
                previous.serviced_at
                + previous.service_time
                + int(np.ceil(previous.distance(current)) + 0.1)
            )

        return current

    def _check_init_args(
        self,
        customers: Optional[Iterable[Customer]],
        function: Optional[Callable[[List], int]],
    ):
        if customers is None:
            customers = list()

        if function is None:
            function = self._default_function

        try:
            iter(customers)
        except TypeError:
            raise TypeError(
                "Expected argument customers to be an iterable, instead it is "
                f"{type(customers)}."
            )

        if not callable(function):
            raise TypeError(
                "Expected argument function to be callable, instead it is "
                f"{type(function)}."
            )

        customers = list(customers)

        return customers, function

    def __init__(
        self,
        customers: Optional[Iterable[Customer]] = None,
        function: Optional[Callable[[List], int]] = None,
    ):
        customers, function = self._check_init_args(
            customers=customers, function=function
        )

        self._customers = copy.deepcopy(customers)
        self._function = copy.deepcopy(function)

        for i in range(len(self._customers)):
            self._customers[i] = self.function(
                self._customers[i], self._customers[i - 1] if i > 0 else None
            )

    # region Properties
    @property
    def customers(self):
        return copy.deepcopy(self._customers)

    @property
    def function(self):
        return copy.deepcopy(self._function)

    @property
    def cost(self):
        return self._customers[-1].serviced_at + self._customers[-1].service_time

    # endregion

    def add_stop(self, customer: Customer):
        self._customers.append(self.function(customer, self._customers[-1]))

    def insert_stop(self, customer: Customer, index: int):
        if index > len(self):
            raise IndexError(
                f"Attempted to insert at index {index} but there are only {len(self)} "
                "elements in the route!"
            )
        elif index == len(self):
            return self.add_stop(customer=customer)

        self._customers = self._customers[:index] + [customer] + self._customers[index:]

        for i, customer in enumerate(self._customers[index:], index):
            self._customers[i] = self.function(customer, self._customers[i - 1])

    def pop_stop(self):
        self._customers.pop()

    def remove_stop(self, index: int):
        if index >= len(self):
            raise IndexError(
                f"Attempted to remove at index {index} but there are only {len(self)} "
                "elements in the route!"
            )
        elif index == len(self) - 1:
            return self.pop_stop()

        self._customers = self._customers[:index] + self._customers[index + 1 :]

        for i, customer in enumerate(self._customers[index:], index):
            self._customers[i] = self.function(customer, self._customers[i - 1])

    # region Dunder Methods
    def __repr__(self):
        return "->".join(
            f"{customer.number}({customer.serviced_at})" for customer in self._customers
        )

    def __str__(self):
        return repr(self)

    def __len__(self):
        return len(self._customers)

    def __getitem__(self, key):
        return self._customers[key]

    def __eq__(self, other: "Route"):
        if other is None or not isinstance(other, Route) or len(self) != len(other):
            return False

        return all(self[i] == other[i] for i in range(len(self)))

    # endregion
