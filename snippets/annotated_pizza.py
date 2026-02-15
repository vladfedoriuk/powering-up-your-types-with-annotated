import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Annotated

from annotated_types import (
    Ge,
    Gt,
    IsDigits,
    Le,
    Len,
    MaxLen,
    MinLen,
    Predicate,
    Timezone,
)

# Semantic Types
Name = Annotated[str, MinLen(1), MaxLen(100)]
OrderReference = Annotated[str, Len(6), IsDigits]

# The Base Layer: Amount must be a finite, non-NaN decimal
Amount = Annotated[
    Decimal,
    Predicate(lambda x: x.is_finite()),
    Predicate(lambda x: not x.is_nan()),
]

# Layering: Adding domain data model constraints on top of the base Amount
Price = Annotated[Amount, Gt(0)]
Percentage = Annotated[Amount, Ge(0), Le(100)]
TaxRate = Annotated[Amount, Ge(0), Le(1)]

# Ensure timezone-aware date-times
TimestampTz = Annotated[datetime.datetime, Timezone(...)]


@dataclass
class Topping:
    name: Name
    price: Price


@dataclass
class Pizza:
    name: Name
    price: Price


@dataclass
class Order:
    MAX_EXTRA_TOPPINGS = 10

    reference: OrderReference
    pizza: Pizza
    created_at: TimestampTz = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    extra_toppings: list[Topping] = field(default_factory=list)

    def add_topping(self, topping: Topping) -> None:
        if len(self.extra_toppings) >= self.MAX_EXTRA_TOPPINGS:
            raise ValueError(
                f"Cannot add more than {self.MAX_EXTRA_TOPPINGS} extra toppings",
            )
        self.extra_toppings.append(topping)


def calculate_order_total(
    order: Order,
    discount_percent: Percentage = Decimal(0),
    tax_rate: TaxRate = Decimal("0.1"),
) -> Price:
    """Calculates the total price applying:
    1. Sum of Pizza + Extra Toppings
    2. Discount percentage (0-100)
    3. Tax rate (0-1 factor)
    """
    subtotal = order.pizza.price + sum(t.price for t in order.extra_toppings)

    # Apply discount
    discount_amount = subtotal * (discount_percent / Decimal(100))
    discounted_subtotal = subtotal - discount_amount

    # Apply tax
    total = discounted_subtotal * (Decimal(1) + tax_rate)

    return total.quantize(Decimal("0.01"))
