import datetime
from decimal import Decimal
from typing import Annotated

import sqlalchemy.orm
from annotated_types import (
    Ge,
    Gt,
    IsDigits,
    IsFinite,
    IsNotNan,
    Le,
    Len,
    MaxLen,
    MinLen,
    Timezone,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

DATABASE_URL = "sqlite+aiosqlite:///pizza.db"

metadata = sqlalchemy.MetaData()
registry = sqlalchemy.orm.registry(metadata=metadata)

Identity = Annotated[
    int,
    Gt(0),
    mapped_column(
        sqlalchemy.Integer(),
        sqlalchemy.Identity(always=False),
        primary_key=True,
    ),
]

Name = Annotated[
    str,
    MinLen(1),
    MaxLen(100),
    mapped_column(sqlalchemy.String(100), nullable=False, index=True),
]

OrderReference = Annotated[
    str,
    Len(6),
    IsDigits,
    mapped_column(sqlalchemy.String(6), nullable=False, index=True, unique=True),
]

# The Base Layer
Amount = Annotated[Decimal, IsFinite, IsNotNan]

# Layering: Adding domain constraints and SQL mapping
Price = Annotated[
    Amount,
    Gt(0),
    mapped_column(sqlalchemy.Numeric(precision=10, scale=2), nullable=False),
]

Percentage = Annotated[
    Amount,
    Ge(0),
    Le(100),
]

TaxRate = Annotated[
    Amount,
    Ge(0),
    Le(1),
]

TimestampTz = Annotated[
    datetime.datetime,
    Timezone(...),
    mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.current_timestamp(),
    ),
]


@registry.mapped_as_dataclass
class Topping:
    """Topping entity."""

    __tablename__ = "toppings"
    __table_kwargs__ = {"sqlite_autoincrement": True}

    id: Mapped[Identity] = mapped_column(init=False)
    name: Mapped[Name]
    price: Mapped[Price]


@registry.mapped_as_dataclass
class Pizza:
    """Pizza entity."""

    __tablename__ = "pizzas"
    __table_kwargs__ = {"sqlite_autoincrement": True}

    id: Mapped[Identity] = mapped_column(init=False)
    name: Mapped[Name]
    price: Mapped[Price]


# Association table for Order and Toppings
order_toppings = sqlalchemy.Table(
    "order_toppings",
    metadata,
    sqlalchemy.Column("order_id", sqlalchemy.ForeignKey("orders.id"), primary_key=True),
    sqlalchemy.Column(
        "topping_id",
        sqlalchemy.ForeignKey("toppings.id"),
        primary_key=True,
    ),
)


@registry.mapped_as_dataclass
class Order:
    """Order entity."""

    MAX_EXTRA_TOPPINGS = 10

    __tablename__ = "orders"
    __table_kwargs__ = {"sqlite_autoincrement": True}

    id: Mapped[Identity] = mapped_column(init=False)
    reference: Mapped[OrderReference]

    pizza_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("pizzas.id"),
        init=False,
    )
    pizza: Mapped[Pizza] = relationship()

    created_at: Mapped[TimestampTz] = mapped_column(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )

    extra_toppings: Mapped[list[Topping]] = relationship(
        secondary=order_toppings,
        default_factory=list,
    )

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
