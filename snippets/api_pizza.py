import datetime
from collections.abc import AsyncGenerator
from decimal import Decimal
from typing import Annotated, Any, TypeAlias

import attr
import sqlalchemy
import sqlalchemy.orm
import svcs
import svcs.fastapi
from annotated_doc import Doc
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
from attrs import frozen
from fastapi import FastAPI, Query, status
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request
from starlette.responses import JSONResponse

DATABASE_URL = "sqlite+aiosqlite:///pizza.db"
engine = create_async_engine(DATABASE_URL)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as session:
        yield session


def validate_reference(v: Any) -> str:
    if not isinstance(v, str):
        raise ValueError("Reference must be a string")
    return v.replace("#", "").replace("-", "")


def serialize_reference(v: str) -> str:
    return f"#{v[:2]}-{v[2:4]}-{v[4:]}"


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
    BeforeValidator(validate_reference),
    PlainSerializer(serialize_reference, return_type=str),
    mapped_column(sqlalchemy.String(6), nullable=False, index=True, unique=True),
]


def serialize_amount(v: Decimal) -> float:
    return float(v.quantize(Decimal("0.01")))


Amount = Annotated[
    Decimal,
    IsFinite,
    IsNotNan,
    PlainSerializer(serialize_amount, return_type=float, when_used="json"),
]

Price = Annotated[
    Amount,
    Gt(0),
    mapped_column(sqlalchemy.Numeric(precision=10, scale=2), nullable=False),
]

Percentage: TypeAlias = Annotated[Amount, Ge(0), Le(100)]
TaxRate: TypeAlias = Annotated[Amount, Ge(0), Le(1)]

TimestampTz = Annotated[
    datetime.datetime,
    Timezone(...),
    mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.current_timestamp(),
    ),
]


metadata = sqlalchemy.MetaData()
registry = sqlalchemy.orm.registry(metadata=metadata)


@registry.mapped_as_dataclass
class Topping:
    __tablename__ = "toppings"
    __table_kwargs__ = {"sqlite_autoincrement": True}

    id: Mapped[Identity] = mapped_column(init=False)
    name: Mapped[Name]
    price: Mapped[Price]


@registry.mapped_as_dataclass
class Pizza:
    __tablename__ = "pizzas"
    __table_kwargs__ = {"sqlite_autoincrement": True}

    id: Mapped[Identity] = mapped_column(init=False)
    name: Mapped[Name]
    price: Mapped[Price]


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


def calculate_order_total(
    order: Order,
    discount_percent: Percentage = Decimal(0),
    tax_rate: TaxRate = Decimal("0.1"),
) -> Price:
    subtotal = order.pizza.price + sum(t.price for t in order.extra_toppings)
    discount_amount = subtotal * (discount_percent / Decimal(100))
    total = (subtotal - discount_amount) * (Decimal(1) + tax_rate)
    return total.quantize(Decimal("0.01"))


class ToppingSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
        extra="forbid",
        title="Topping",
    )
    name: Name
    price: Price


class PizzaSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
        extra="forbid",
        title="Pizza",
    )
    name: Name
    price: Price


class OrderSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
        extra="forbid",
        title="Order",
    )
    reference: Annotated[
        OrderReference,
        Field(
            serialization_alias="ref",
            title="The order reference",
            description="The order reference in format #XX-XX-XX",
        ),
    ]
    pizza: PizzaSchema
    extra_toppings: list[ToppingSchema]
    created_at: TimestampTz


class OrderResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", title="Order Detail")

    order: OrderSchema
    total: Price


@svcs.fastapi.lifespan
async def lifespan(_app_: FastAPI, _registry_: svcs.Registry) -> AsyncGenerator[None]:
    _registry_.register_factory(AsyncSession, get_session)

    async def order_repo_factory(container: svcs.Container) -> OrderRepository:
        session = await container.aget(AsyncSession)
        return OrderRepository(session)

    _registry_.register_factory(OrderRepository, order_repo_factory)
    yield


app = FastAPI(
    title="Pizza Power API",
    lifespan=lifespan,
)


@attr.frozen
class OrderRepository:
    """Repository for Order entities."""

    #: The database session
    _session: AsyncSession

    async def get_by_reference(self, reference: OrderReference) -> Order | None:
        """Fetch an order from the database by its reference string."""
        stmt = (
            sqlalchemy.select(Order)
            .where(Order.reference == reference)
            .options(
                sqlalchemy.orm.selectinload(Order.pizza),
                sqlalchemy.orm.selectinload(Order.extra_toppings),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()


@frozen
class NotFoundError(Exception):
    """Exception raised when an entity is not found."""

    message: Annotated[str, Doc("The human-readable error message")]


@app.exception_handler(NotFoundError)
def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )


FIRST_ORDER_DISCOUNT: Annotated[
    Percentage,
    Doc("Discount for the first order made by a customer"),
] = Decimal(10)


@app.get("/orders/", response_model=OrderResponse)
async def get_order(
    reference: Annotated[OrderReference, Query(alias="ref")],
    services: svcs.fastapi.DepContainer,
) -> dict[str, Any]:
    repo = await services.aget(OrderRepository)
    if (order := await repo.get_by_reference(reference)) is None:
        raise NotFoundError("Order not found")

    return {"order": order, "total": calculate_order_total(order)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
