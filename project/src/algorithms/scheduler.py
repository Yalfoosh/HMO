from typing import Iterable

from .customer import Customer, CustomerGraph


class Scheduler:
    @staticmethod
    def _check_init_args(n_vehicles: int, vehicle_capacity: int):
        if not isinstance(n_vehicles, int):
            raise TypeError(
                "Expected argument n_vehicles to be an int, instead it is "
                f"{type(n_vehicles)}."
            )

        if not isinstance(vehicle_capacity, int):
            raise TypeError(
                "Expected argument vehicle_capacity to be an int, instead it is "
                f"{type(vehicle_capacity)}."
            )

        if n_vehicles < 1:
            raise ValueError(
                "Expected argument n_vehicles to be a positive integer, instead it is "
                f"{n_vehicles}."
            )

        if vehicle_capacity < 1:
            raise ValueError(
                "Expected argument vehicle_capacity to be a positive integer, instead "
                f"it is {vehicle_capacity}."
            )

        return n_vehicles, vehicle_capacity

    def __init__(
        self, n_vehicles: int, vehicle_capacity: int, customers: Iterable[Customer]
    ):
        n_vehicles, vehicle_capacity = self._check_init_args(
            n_vehicles=n_vehicles, vehicle_capacity=vehicle_capacity
        )

        self._n_vehicles = n_vehicles
        self._vehicle_capacity = vehicle_capacity
        self._customer_graph = CustomerGraph(customers=customers)

    # region Properties
    @property
    def n_vehicles(self) -> int:
        return self._n_vehicles

    @property
    def vehicle_capacity(self) -> int:
        return self._vehicle_capacity

    @property
    def customer_graph(self) -> CustomerGraph:
        return self._customer_graph

    # endregion
