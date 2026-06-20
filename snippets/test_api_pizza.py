import datetime
import string
from typing import Callable, Awaitable

import httpx
import pytest
from dirty_equals import IsPartialDict, IsPositive
from polyfactory import Use
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .api_pizza import (
    Order,
    Pizza,
    Topping,
)

pytestmark = pytest.mark.usefixtures("_override_registry")


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


@pytest.fixture()
async def add_order(session: AsyncSession) -> Callable[[Order], Awaitable[None]]:

    async def _add_order(order: Order) -> None:
        session.add(order)
        await session.flush()

    return _add_order


@pytest.mark.anyio
async def test_get_order_api(
    client: httpx.AsyncClient, add_order: Callable[[Order], Awaitable[None]]
) -> None:
    order = OrderFactory.build(reference="123456")
    await add_order(order)

    response = await client.get("/orders/", params={"ref": order.reference})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data == IsPartialDict(
        order=IsPartialDict(
            ref="#12-34-56",
        ),
        total=IsPositive,
    )
