import datetime

import sqlalchemy
import sqlalchemy.orm
from dirty_equals import HasLen, IsPositive, IsStr
from polyfactory import Use
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from .persistent_reservation import Reservation, Room


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


pytestmark = __import__("pytest").mark.anyio


async def test_persist_room_to_db(session: AsyncSession) -> None:
    room = RoomFactory.build()

    session.add(room)
    await session.flush()

    stmt = (
        sqlalchemy.select(Room)
        .where(Room.id == room.id)
        .options(sqlalchemy.orm.selectinload(Room.reservations))
    )
    result = await session.execute(stmt)
    persisted_room = result.scalar_one()

    assert persisted_room.id is not None
    assert persisted_room.room_id == IsStr(regex=r"^101$")
    assert persisted_room.capacity == IsPositive
    assert persisted_room.reservations == HasLen(1)


async def test_add_reservation_enforces_overlap_guard(session: AsyncSession) -> None:
    room = Room(room_id="201", capacity=2)
    room.add_reservation(
        ReservationFactory.build(
            room_id="201",
            starts_at=datetime.date(2026, 8, 1),
            ends_at=datetime.date(2026, 8, 3),
        )
    )

    session.add(room)
    await session.flush()

    assert room.reservations == HasLen(1)
