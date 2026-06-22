import datetime
from collections.abc import Awaitable, Callable

import httpx
import pytest
from dirty_equals import IsPartialDict, IsPositive
from polyfactory import Use
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .api_reservation import Reservation, Room

pytestmark = pytest.mark.usefixtures("_override_registry")


class ReservationFactory(SQLAlchemyFactory[Reservation]):
    __model__ = Reservation

    room_id = "101"
    guest_count = 2
    starts_at = datetime.date(2026, 7, 1)
    ends_at = datetime.date(2026, 7, 4)
    rate = Use(
        SQLAlchemyFactory.__faker__.pydecimal,
        min_value=50,
        max_value=500,
        positive=True,
    )
    created_at = Use(
        SQLAlchemyFactory.__faker__.date_time_between,
        start_date="-30d",
        end_date="now",
        tzinfo=datetime.UTC,
    )


class RoomFactory(SQLAlchemyFactory[Room]):
    __model__ = Room

    room_id = "101"
    capacity = 4
    reservations = Use(lambda: [ReservationFactory.build()])


@pytest.fixture()
async def add_room(session: AsyncSession) -> Callable[[Room], Awaitable[None]]:
    async def _add_room(room: Room) -> None:
        session.add(room)
        await session.flush()

    return _add_room


@pytest.mark.anyio
async def test_get_room_api(
    client: httpx.AsyncClient, add_room: Callable[[Room], Awaitable[None]]
) -> None:
    room = RoomFactory.build(room_id="A-101")
    for reservation in room.reservations:
        reservation.room_id = room.room_id
    await add_room(room)

    response = await client.get(f"/rooms/{room.room_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data == IsPartialDict(
        room=IsPartialDict(
            room_id="A-101",
            capacity=IsPositive,
        ),
        totals=[IsPositive],
    )
