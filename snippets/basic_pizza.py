import datetime
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Topping:
    name: str
    price: Decimal


@dataclass
class Pizza:
    name: str
    price: Decimal


@dataclass
class Order:
    MAX_EXTRA_TOPPINGS = 10

    reference: str
    pizza: Pizza
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    extra_toppings: list[Topping] = field(default_factory=list)

    def add_topping(self, topping: Topping) -> None:
        if len(self.extra_toppings) >= self.MAX_EXTRA_TOPPINGS:
            raise ValueError(
                f"Cannot add more than {self.MAX_EXTRA_TOPPINGS} extra toppings",
            )
        self.extra_toppings.append(topping)
