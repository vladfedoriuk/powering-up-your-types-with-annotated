import datetime
import string

import pytest
import sqlalchemy
import sqlalchemy.orm
from dirty_equals import IsPositive, IsStr
from polyfactory import Use
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from .persistent_pizza import (
    Order,
    Pizza,
    Topping,
)


class ToppingFactory(SQLAlchemyFactory[Topping]):
    __model__ = Topping

    price = Use(
        SQLAlchemyFactory.__faker__.pydecimal,
        min_value=1,
        max_value=5,
        positive=True,
    )


class PizzaFactory(SQLAlchemyFactory[Pizza]):
    __model__ = Pizza

    price = Use(
        SQLAlchemyFactory.__faker__.pydecimal,
        min_value=10,
        max_value=100,
        positive=True,
    )


class OrderFactory(SQLAlchemyFactory[Order]):
    __model__ = Order
    __min_collection_length__ = 1

    pizza = Use(PizzaFactory.build)
    extra_toppings = Use(ToppingFactory.batch, size=2)

    created_at = Use(
        SQLAlchemyFactory.__faker__.date_time_between,
        start_date="-30d",
        end_date="now",
        tzinfo=datetime.UTC,
    )
    reference = Use(
        SQLAlchemyFactory.__faker__.pystr_format,
        string_format="######",
        letters=string.digits,
    )


pytestmark = pytest.mark.anyio


async def test_persist_order_to_db(session: AsyncSession) -> None:
    """Test that we can persist an order to the database using SQLAlchemy async."""
    order = OrderFactory.build()

    session.add(order)
    await session.flush()

    stmt = (
        sqlalchemy.select(Order)
        .where(Order.id == order.id)
        .options(
            sqlalchemy.orm.selectinload(Order.pizza),
            sqlalchemy.orm.selectinload(Order.extra_toppings),
        )
    )
    result = await session.execute(stmt)
    persisted_order = result.scalar_one()

    assert persisted_order.id is not None
    assert persisted_order.reference == IsStr(regex=r"^\d{6}$")
    assert persisted_order.pizza.price == IsPositive
