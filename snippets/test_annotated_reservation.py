import datetime
import random
from decimal import Decimal

import pytest
from dirty_equals import HasLen, IsPositive
from hypothesis import given
from hypothesis import strategies as st
from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.fields import PostGenerated, Use

from .annotated_reservation import (
    Percentage,
    Reservation,
    Room,
    TaxRate,
    calculate_stay_total,
)


class ReservationFactory(DataclassFactory[Reservation]):
    __model__ = Reservation

    # ends_at must follow starts_at — cross-field constraint polyfactory can't infer
    ends_at = PostGenerated(
        lambda name, values, *args, **kwargs: (
            values["starts_at"] + datetime.timedelta(days=random.randint(1, 14))
        )
    )
    # Timezone(...) means "any tz" — polyfactory passes ellipsis as tzinfo, which fails
    created_at = Use(
        DataclassFactory.__faker__.date_time_between,
        start_date="-30d",
        end_date="now",
        tzinfo=datetime.UTC,
    )
    # room_id → RoomId  = Annotated[str, MinLen(1), MaxLen(20)]  ← auto
    # guest_count → GuestCount = Annotated[int, Ge(1), Le(10)]   ← auto
    # rate → RoomRate = Annotated[Decimal, Gt(0)]                 ← auto


class RoomFactory(DataclassFactory[Room]):
    __model__ = Room

    # room_id → RoomId   ← auto
    # capacity → GuestCount ← auto
    reservations = Use(lambda: [])


def test_room_properties() -> None:
    room = RoomFactory.build()

    assert 1 <= room.capacity <= 10  # GuestCount = Annotated[int, Ge(1), Le(10)]
    assert room.reservations == HasLen(0)


def test_reservation_constraints_satisfied() -> None:
    res = ReservationFactory.build()

    assert 1 <= res.guest_count <= 10  # GuestCount
    assert 1 <= len(res.room_id) <= 20  # RoomId
    assert res.rate > 0  # RoomRate = Annotated[Decimal, Gt(0)]
    assert res.night_count >= 1
    assert res.created_at.tzinfo is not None


def test_room_rejects_capacity_overflow() -> None:
    room = Room(room_id="101", capacity=2)
    reservation = ReservationFactory.build(room_id="101", guest_count=3)

    with pytest.raises(ValueError, match="Reservation exceeds room capacity"):
        room.add_reservation(reservation)


def test_room_rejects_overlapping_reservations() -> None:
    room = Room(room_id="101", capacity=10)
    room.add_reservation(
        ReservationFactory.build(
            room_id="101",
            starts_at=datetime.date(2026, 7, 1),
            ends_at=datetime.date(2026, 7, 4),
        )
    )
    overlapping = ReservationFactory.build(
        room_id="101",
        starts_at=datetime.date(2026, 7, 3),
        ends_at=datetime.date(2026, 7, 5),
    )

    with pytest.raises(ValueError, match="Reservation overlaps existing reservation"):
        room.add_reservation(overlapping)


def test_room_accepts_adjacent_reservations() -> None:
    room = Room(room_id="101", capacity=10)
    room.add_reservation(
        ReservationFactory.build(
            room_id="101",
            starts_at=datetime.date(2026, 7, 1),
            ends_at=datetime.date(2026, 7, 4),
        )
    )
    room.add_reservation(
        ReservationFactory.build(
            room_id="101",
            starts_at=datetime.date(2026, 7, 4),
            ends_at=datetime.date(2026, 7, 6),
        )
    )

    assert room.reservations == HasLen(2)


valid_rates = st.decimals(
    min_value=Decimal("0.01"),
    max_value=Decimal("1000.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)

valid_dates = st.dates(
    min_value=datetime.date(2026, 1, 1),
    max_value=datetime.date(2026, 12, 1),
)


@given(
    starts_at=valid_dates,
    nights=st.integers(min_value=1, max_value=30),
    rate=valid_rates,
    discount=st.from_type(Percentage),
    tax=st.from_type(TaxRate),
)
def test_stay_total_is_never_negative(
    starts_at: datetime.date,
    nights: int,
    guest_count: int,
    rate: Decimal,
    discount: Decimal,
    tax: Decimal,
) -> None:
    reservation = Reservation(
        room_id="101",
        guest_count=guest_count,
        starts_at=starts_at,
        ends_at=starts_at + datetime.timedelta(days=nights),
        rate=rate,
    )

    total = calculate_stay_total(reservation, discount_percent=discount, tax_rate=tax)

    assert total >= 0


@given(rate=valid_rates, starts_at=valid_dates)
def test_hypothesis_from_type_limitation_for_nested_annotated(
    rate: Decimal,
    starts_at: datetime.date,
) -> None:
    # Hypothesis has basic annotated-types support. Nested/flattened Annotated
    # aliases like RoomRate may still fail to resolve in some releases,
    # especially with metadata such as IsNotNan, IsFinite, or Timezone.
    reservation = Reservation(
        room_id="101",
        guest_count=2,
        starts_at=starts_at,
        ends_at=starts_at + datetime.timedelta(days=1),
        rate=rate,
    )

    assert calculate_stay_total(reservation) == IsPositive
