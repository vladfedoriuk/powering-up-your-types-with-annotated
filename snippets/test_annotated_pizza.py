import datetime
import string
from decimal import Decimal

import pytest
from dirty_equals import HasLen, IsPositive
from hypothesis import given
from hypothesis import strategies as st
from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.fields import Use

from .annotated_pizza import (
    Order,
    Percentage,
    Pizza,
    TaxRate,
    Topping,
    calculate_order_total,
)


class ToppingFactory(DataclassFactory[Topping]):
    __model__ = Topping


class PizzaFactory(DataclassFactory[Pizza]):
    __model__ = Pizza


class OrderFactory(DataclassFactory[Order]):
    __model__ = Order
    __min_collection_length__ = 1

    created_at = Use(
        DataclassFactory.__faker__.date_time_between,
        start_date="-30d",
        end_date="now",
        tzinfo=datetime.UTC,
    )
    reference = Use(
        DataclassFactory.__faker__.pystr_format,
        string_format="######",
        letters=string.digits,
    )


def test_order_properties() -> None:
    order = OrderFactory.build(extra_toppings=ToppingFactory.batch(10))

    assert order.pizza.price == IsPositive
    assert order.extra_toppings == HasLen(10)
    assert order.created_at.tzinfo is not None


def test_order_cannot_add_more_than_10_toppings() -> None:
    order = OrderFactory.build(extra_toppings=ToppingFactory.batch(10))
    new_topping = ToppingFactory.build()

    with pytest.raises(ValueError, match="Cannot add more than 10 extra toppings"):
        order.add_topping(new_topping)


@given(
    order=st.builds(
        Order,
        reference=st.text(min_size=6, max_size=6, alphabet=string.digits),
        pizza=st.builds(
            Pizza,
            name=st.text(min_size=1, max_size=100),
            price=(
                price_strategy := st.decimals(
                    min_value=Decimal("0.01"),
                    max_value=Decimal(100),
                )
            ),
        ),
        extra_toppings=st.lists(
            st.builds(
                Topping,
                name=st.text(min_size=1, max_size=100),
                price=price_strategy,
            ),
            max_size=10,
        ),
        created_at=st.datetimes(timezones=st.just(datetime.UTC)),
    ),
    discount=st.from_type(Percentage),
    tax=st.from_type(TaxRate),
)
def test_no_free_lunch_property(order: Order, discount: Decimal, tax: Decimal) -> None:
    """Property: For any valid order and valid discount/tax, the total price
    must be non-negative.
    """
    total = calculate_order_total(order, discount_percent=discount, tax_rate=tax)
    assert total >= 0
