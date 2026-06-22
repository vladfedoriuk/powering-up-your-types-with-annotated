import datetime
from decimal import Decimal
from pathlib import Path
from typing import Annotated, Generator

from annotated_types import Ge, Gt, Le, MaxLen, MinLen
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

_ROOT = Path(__file__).resolve().parent.parent

RoomId = Annotated[str, MinLen(1), MaxLen(20)]
GuestCount = Annotated[int, Ge(1), Le(10)]
RoomRate = Annotated[Decimal, Gt(0)]
NightCount = Annotated[int, Ge(1), Le(365)]
Percentage = Annotated[Decimal, Ge(0), Le(100)]
TaxRate = Annotated[Decimal, Ge(0), Le(1)]


class RoomBase(SQLModel):
    room_id: RoomId = Field(index=True, unique=True, max_length=20)
    capacity: GuestCount = Field(ge=1, le=10)


class Room(RoomBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    def add_reservation(self, reservation: "Reservation") -> None:
        if reservation.room_id != self.room_id:
            raise ValueError("Reservation belongs to another room")
        if reservation.guest_count > self.capacity:
            raise ValueError("Reservation exceeds room capacity")
        if reservation.night_count < 1:
            raise ValueError("Reservation must last at least one night")


class RoomCreate(RoomBase):
    pass


class RoomPublic(RoomBase):
    id: int


class ReservationBase(SQLModel):
    room_id: RoomId = Field(index=True, foreign_key="room.room_id", max_length=20)
    guest_count: GuestCount = Field(ge=1, le=10)
    rate: RoomRate = Field(max_digits=10, decimal_places=2)
    starts_at: datetime.date
    ends_at: datetime.date


class Reservation(ReservationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )

    @property
    def night_count(self) -> NightCount:
        return self.ends_at.toordinal() - self.starts_at.toordinal()

    def overlaps(self, other: "Reservation") -> bool:
        return self.starts_at < other.ends_at and other.starts_at < self.ends_at


class ReservationCreate(ReservationBase):
    pass


class ReservationPublic(ReservationBase):
    id: int
    created_at: datetime.datetime
    night_count: int


sqlite_url = f"sqlite:///{_ROOT}/reservations_sqlmodel.db"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


app = FastAPI(title="SQLModel Reservation API")


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.post("/rooms/", response_model=RoomPublic)
def create_room(*, session: Session = Depends(get_session), room: RoomCreate) -> Room:
    db_room = Room.model_validate(room)
    session.add(db_room)
    session.commit()
    session.refresh(db_room)
    return db_room


@app.get("/rooms/", response_model=list[RoomPublic])
def read_rooms(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> list[Room]:
    return list(session.exec(select(Room).offset(offset).limit(limit)).all())


@app.get("/rooms/{room_id}", response_model=RoomPublic)
def read_room(*, session: Session = Depends(get_session), room_id: str) -> Room:
    room = session.exec(select(Room).where(Room.room_id == room_id)).one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@app.post("/reservations/", response_model=ReservationPublic)
def create_reservation(
    *, session: Session = Depends(get_session), reservation: ReservationCreate
) -> Reservation:
    room = session.exec(
        select(Room).where(Room.room_id == reservation.room_id)
    ).one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if reservation.guest_count > room.capacity:
        raise HTTPException(status_code=409, detail="Reservation exceeds room capacity")

    db_reservation = Reservation.model_validate(reservation)
    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)
    return db_reservation


@app.get("/reservations/", response_model=list[ReservationPublic])
def read_reservations(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> list[Reservation]:
    return list(session.exec(select(Reservation).offset(offset).limit(limit)).all())


@app.get("/reservations/{reservation_id}", response_model=ReservationPublic)
def read_reservation(
    *, session: Session = Depends(get_session), reservation_id: int
) -> Reservation:
    reservation = session.exec(
        select(Reservation).where(Reservation.id == reservation_id)
    ).one_or_none()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


def calculate_stay_total(
    reservation: Reservation,
    discount_percent: Percentage = Decimal(0),
    tax_rate: TaxRate = Decimal("0.1"),
) -> Decimal:
    subtotal = reservation.rate * Decimal(reservation.night_count)
    discount_amount = subtotal * (discount_percent / Decimal(100))
    total = (subtotal - discount_amount) * (Decimal(1) + tax_rate)
    return total.quantize(Decimal("0.01"))


if __name__ == "__main__":
    create_db_and_tables()
