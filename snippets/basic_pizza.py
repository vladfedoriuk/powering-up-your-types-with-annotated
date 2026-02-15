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
    reference: str
    pizza: Pizza
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    extra_toppings: list[Topping] = field(default_factory=list)
