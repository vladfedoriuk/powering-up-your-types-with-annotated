import datetime
from decimal import Decimal

import pytest
from dirty_equals import HasLen, IsPositive
from hypothesis import given
from hypothesis import strategies as st
from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.fields import Use

from .annotated_reservation import (
    GuestCount,
    Percentage,
    Reservation,
    Room,
    TaxRate,
    calculate_stay_total,
)


class ReservationFactory(DataclassFactory[Reservation]):
    __model__ = Reservation

    room_id = "101"
    guest_count = 2
    starts_at = datetime.date(2026, 7, 1)
    ends_at = datetime.date(2026, 7, 4)
    rate = Use(
        DataclassFactory.__faker__.pydecimal, min_value=50, max_value=500, positive=True
    )
    created_at = Use(
        DataclassFactory.__faker__.date_time_between,
        start_date="-30d",
        end_date="now",
        tzinfo=datetime.UTC,
    )


class RoomFactory(DataclassFactory[Room]):
    __model__ = Room

    room_id = "101"
    capacity = 4
    reservations = Use(lambda: [ReservationFactory.build()])


def test_room_properties() -> None:
    room = RoomFactory.build()

    assert room.capacity == IsPositive
    assert room.reservations == HasLen(1)
    assert room.reservations[0].night_count == 3
    assert room.reservations[0].created_at.tzinfo is not None


def test_room_rejects_capacity_overflow() -> None:
    room = Room(room_id="101", capacity=2)
    reservation = ReservationFactory.build(guest_count=3)

    with pytest.raises(ValueError, match="Reservation exceeds room capacity"):
        room.add_reservation(reservation)


def test_room_rejects_overlapping_reservations() -> None:
    room = Room(room_id="101", capacity=4)
    room.add_reservation(
        ReservationFactory.build(
            starts_at=datetime.date(2026, 7, 1),
            ends_at=datetime.date(2026, 7, 4),
        )
    )
    overlapping = ReservationFactory.build(
        starts_at=datetime.date(2026, 7, 3),
        ends_at=datetime.date(2026, 7, 5),
    )

    with pytest.raises(ValueError, match="Reservation overlaps existing reservation"):
        room.add_reservation(overlapping)


def test_room_accepts_adjacent_reservations() -> None:
    room = Room(room_id="101", capacity=4)
    room.add_reservation(
        ReservationFactory.build(
            starts_at=datetime.date(2026, 7, 1),
            ends_at=datetime.date(2026, 7, 4),
        )
    )
    room.add_reservation(
        ReservationFactory.build(
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
    guest_count=st.from_type(GuestCount),
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
