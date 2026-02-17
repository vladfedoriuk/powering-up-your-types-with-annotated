---
theme: neversink
title: Extra Toppings - Powering Up Your Types with Annotated
info: |
  ## Extra Toppings
  Powering Up Your Types with Annotated in Python
# apply UnoCSS classes to the current slide
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
layout: intro
color: white
---

:: note ::

Python 3.9+ / PEP 593

# Extra Toppings
## Powering Up Your Types with ==typing.Annotated==

<div class="flex flex-col items-center justify-center mt-10">
  <div class="relative h-40 w-40 flex items-center justify-center">
     <div class="absolute h-32 w-32 bg-orange-100 rounded-full border-4 border-orange-200 opacity-50 shadow-inner animate-pulse" />
     <mdi-pizza class="text-7xl text-orange-500 z-10" />
  </div>
  <div class="mt-8 text-2xl font-medium">
    Vlad Fedoriuk
  </div>
</div>

---
layout: top-title
color: yellow
---

:: title ::

# Enter `Annotated` (PEP 593)

:: content ::

<div class="grid grid-cols-3 gap-10">

<div class="text-left">


- Added in `Python 3.9`
- Universal ==metadata engine==
- `Annotated[T, *Metadata]`

<div class="mt-8">

<div class="text-xs opacity-50 mb-2 font-bold tracking-widest">Two Strategies</div>

<div class="ns-c-border ns-c-tight">

- semantic types
- framework metadata

</div>

</div>

</div>

<div class="text-left">

<div class="neversink-sky-light-scheme ns-c-bind-scheme px-3 py-1 mb-4 text-center text-xs font-bold rounded-md border shadow-sm">
  1. semantic types
</div>

```python
# Naming what data IS

ReaderEngine = Annotated[
    Engine, "Reader"
]

WriterEngine = Annotated[
    Engine, "Writer"
]
```

</div>

<div class="text-left">

<div class="neversink-orange-light-scheme ns-c-bind-scheme px-3 py-1 mb-4 text-center text-xs font-bold rounded-md border shadow-sm">
  2. framework metadata
</div>

```python
# Instructions for Tools

class Result(BaseModel):
    total: Annotated[
        int, Field(ge=0)
    ]

@app.get("/search/")
def search(
    q: Annotated[
        str, Query(min_length=3)
    ]
): ...
```

</div>

</div>

<div class="absolute bottom-10 right-10 w-90">
  <AdmonitionType title="Breaking the Boundary" type="important" color="amber-light">
    <code>Annotated</code> fuses <strong>static analysis</strong> &amp; <strong>runtime behavior</strong>
  </AdmonitionType>
</div>

---
layout: top-title-two-cols
color: amber
---

:: title ::

# `annotated-types`

:: left ::

- Standard definitions for run-time constraints.
- Introduces a protocol for metadata using `BaseMetadata` and `GroupedMetadata`.
- Designed at the ==PyCon 2022 sprints== by the maintainers of ==Pydantic== and ==Hypothesis==.
- A shared standard for the Python ecosystem.

:: right ::

<div class="flex flex-wrap gap-x-3 gap-y-4 text-lg font-mono opacity-90">
  <span class="bg-amber-100 text-amber-900 px-2 rounded">Gt</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">Ge</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">Lt</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">Le</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">Interval</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">MultipleOf</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">MinLen</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">MaxLen</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">Len</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">Timezone</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">Predicate</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">LowerCase</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">UpperCase</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">IsDigits</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">IsFinite</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">IsNotFinite</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">IsNan</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">IsNotNan</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">IsInfinite</span>
  <span class="bg-amber-100 text-amber-900 px-2 rounded">IsNotInfinite</span>
</div>

---
layout: section
color: orange
---

# Building the Pizza
## The Dough: Pure Domain Model

<img src="/assets/dough-nobg.png" class="mx-auto h-80" />

---
layout: default
title: Domain Model - Pizza
color: orange-light
---

<img src="/assets/dough-nobg.png" class="absolute top-4 right-4 w-25" />

<div style="transform: scale(0.9); transform-origin: top left;">

```python
@dataclass
class Topping:
    name: str
    price: Decimal

@dataclass
class Pizza:
    name: str
    price: Decimal
    toppings: list[Topping] = field(default_factory=list)

@dataclass
class Order:
    MAX_EXTRA_TOPPINGS = 10

    reference: str
    pizza: Pizza
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    extra_toppings: list[Topping] = field(default_factory=list)

    def add_topping(self, topping: Topping) -> None:
        if len(self.extra_toppings) >= self.MAX_EXTRA_TOPPINGS:
            raise ValueError(
                f"Cannot add more than {self.MAX_EXTRA_TOPPINGS} extra toppings",
            )
        self.extra_toppings.append(topping)
```

</div>

---
layout: default
title: Domain Function - calculate_order_total
color: orange-light
---

# `calculate_order_total`

This function illustrates a core domain logic: calculating the total price of an order.

<img src="/assets/dough-nobg.png" class="absolute top-4 right-4 w-25" />

```python
def calculate_order_total(
    order: Order,
    discount_percent: Decimal = Decimal(0),
    tax_rate: Decimal = Decimal("0.1"),
) -> Decimal:
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
```

---
layout: section
color: orange
---

# The Sauce: Semantic Enrichment
## Layering Meaning onto Our Types

<img src="/assets/with-sauce-nobg.png" class="mx-auto h-80" />

---
layout: default
title: Adding Semantics - Annotated Types
color: orange-light
---

# The Sauce: Semantic Enrichment
## Types with Extra Flavor!

<img src="/assets/with-sauce-nobg.png" class="absolute top-4 right-4 w-25" />

```python
# Semantic Types
Name = Annotated[str, MinLen(1), MaxLen(100)]
OrderReference = Annotated[str, Len(6), IsDigits]

# The Base Layer: Amount must be a finite, non-NaN decimal
Amount = Annotated[
    Decimal,
    Predicate(lambda x: x.is_finite()),
    Predicate(lambda x: not x.is_nan()),
]

# Layering: Adding domain data model constraints on top of the base Amount
Price = Annotated[Amount, Gt(0)]
Percentage = Annotated[Amount, Ge(0), Le(100)]
TaxRate = Annotated[Amount, Ge(0), Le(1)]

# Ensure timezone-aware date-times
TimestampTz = Annotated[datetime.datetime, Timezone(...)]
```
---
layout: default
title: Shiki Magic Move - Plain to Annotated
color: orange-light
---

# From Plain to Gourmet

<img src="/assets/with-sauce-nobg.png" class="absolute top-4 right-4 w-25" />


<div style="transform: scale(0.9); transform-origin: top left;">

````md magic-move {duration: 1000, stagger: 0.3}


```python
@dataclass
class Topping:
    name: str
    price: Decimal


@dataclass
class Pizza:
    name: str
    price: Decimal


@dataclass
class Order:
    MAX_EXTRA_TOPPINGS = 10

    reference: str
    pizza: Pizza
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    extra_toppings: list[Topping] = field(default_factory=list)

    def add_topping(self, topping: Topping) -> None:
        ...

```

```python {3-4,9-10,17,19}
@dataclass
class Topping:
    name: Name
    price: Price


@dataclass
class Pizza:
    name: Name
    price: Price


@dataclass
class Order:
    MAX_EXTRA_TOPPINGS = 10

    reference: OrderReference
    pizza: Pizza
    created_at: TimestampTz = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    extra_toppings: list[Topping] = field(default_factory=list)

    def add_topping(self, topping: Topping) -> None:
        ...

```

````

</div>

---
layout: default
title: Function Signatures Get Semantic Too
color: orange-light
---

# Function Signatures Get Semantic Too

<img src="/assets/with-sauce-nobg.png" class="absolute top-4 right-4 w-25" />


<div style="transform: scale(0.9); transform-origin: top left;">

````md magic-move {duration: 1000, stagger: 0.3}


```python
def calculate_order_total(
    order: Order,
    discount_percent: Decimal = Decimal(0),
    tax_rate: Decimal = Decimal("0.1"),
) -> Decimal:
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
```

```python {3-4,5}
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
```

````

</div>

---
layout: section
color: amber
---

# The Cheese: Automated Testing
## Binding It All Together

<img src="/assets/some-toppings-nobg.png" class="mx-auto h-80" />

---
layout: top-title-two-cols
color: amber-light
---

:: title ::

# ==polyfactory==: (Almost) Zero-Config Test Data

:: left ::

<img src="/assets/some-toppings-nobg.png" class="absolute top-4 right-4 w-25" />

<div style="transform: scale(0.85); transform-origin: top left;">

```python
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
```

</div>


:: right ::

<div style="transform: scale(0.75); transform-origin: top left" class="mt-8">

```python
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
```



<div class="mt-4">

<AdmonitionType title="Constraints Respected" type="tip" color="green-light">
  <ul class="text-xs">
    <li><code>Price</code> → Always > 0</li>
    <li><code>Name</code> → 1-100 chars</li>
  </ul>
</AdmonitionType>

</div>

<div class="mt-4">

<AdmonitionType title="Manual Config Sometimes Needed" type="warning" color="orange-light">
  <ul class="text-xs">
    <li>Datetime resolution bugs</li>
    <li>Custom string formats (e.g., <code>OrderReference</code>)</li>
  </ul>
</AdmonitionType>

</div>


</div>

---
layout: top-title-two-cols
color: amber-light
---

:: title ::

# ==hypothesis==: Property-Based Testing

:: left ::

<div class="min-w-60">

<img src="/assets/some-toppings-nobg.png" class="absolute top-4 right-4 w-25" />


**Strategy Generation:**

- `st.from_type(T)`: Infers strategy from type hints.
- `st.builds(T)`: Builds strategy for class `T` using the annotations.



<div class="mt-2">

<AdmonitionType title="Current Limitations" type="warning" color="orange-light">
  <ul class="text-xs">
    <li>Very basic support for <code>annotated-types</code> for now.</li>
    <li>Unable to unnest/flatten <code>Annotated</code> (leads to <code>ResolutionFailed</code>).</li>
    <li>Lacking proper support for <code>Timezone</code>, <code>IsNotNan</code>, and <code>IsFinite</code>.</li>
  </ul>
</AdmonitionType>

</div>

</div>



:: right ::

<div style="transform: scale(0.8); transform-origin: top left" class="mt-4">

```python {2,3,5,6,16,17,18,19,24}
@given(
    order=st.builds(
        Order,
        reference=st.text(min_size=6, max_size=6, alphabet=string.digits),
        pizza=st.builds(
            Pizza,
            name=st.text(min_size=1, max_size=100),
            price=st.decimals(min_value=Decimal("0.01"), max_value=Decimal(100)),
        ),
        extra_toppings=st.lists(
            st.builds(Topping, price=st.decimals(min_value=0.01)),
            max_size=10,
        ),
        created_at=st.datetimes(timezones=st.just(datetime.UTC)),
    ),
    discount=st.from_type(Percentage),
    tax=st.from_type(TaxRate),
)
def test_no_free_lunch_property(order: Order, discount: Percentage, tax: TaxRate) -> None:
    """Property: For any valid order and valid discount/tax,
    the total price must be non-negative.
    """
    total = calculate_order_total(order, discount_percent=discount, tax_rate=tax)
    assert total >= 0
```

</div>

---
layout: section
color: orange
---

# The Toppings: Persistence Layer
## (SQLAlchemy)

<img src="/assets/some-toppings-nobg.png" class="mx-auto h-80" />

---
layout: top-title-two-cols
title: SQLAlchemy Integration
color: orange-light
align: l-lt-lt
columns: is-two-thirds
margin: tight
---

:: title ::

# Persistence Layer: SQLAlchemy

:: left ::

<img src="/assets/some-toppings-nobg.png" class="absolute top-4 right-4 w-25" />


<div style="transform: scale(0.75); transform-origin: top left;">

````md magic-move{duration: 1000}

```python
Identity = Annotated[
    int,
    Gt(0),
]

Name = Annotated[
    str,
    MinLen(1),
    MaxLen(100),
]

OrderReference = Annotated[
    str,
    Len(6),
    IsDigits,
]

TimestampTz = Annotated[
    datetime.datetime,
    Timezone(...),
]
```

```python{1,3-7,11,15,18,22,25,28-32}
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

TimestampTz = Annotated[
    datetime.datetime,
    Timezone(...),
    mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.current_timestamp()
    ),
]
```

````

</div>

:: right ::

<div class="mt-10">

<AdmonitionType title="Composition" type="tip" color="orange-light">
  <div class="text-sm">
    The core domain types remain the same, we just "overlay" database metadata using <code>Annotated</code>.
  </div>
</AdmonitionType>

</div>


---
layout: default
color: orange-light
---

# Declarative Mapping: Pizza & Topping

<img src="/assets/some-toppings-nobg.png" class="absolute top-4 right-4 w-25" />

<div class="grid grid-cols-2 gap-4 mt-4">

<div style="transform: scale(0.9); transform-origin: top left;" class="grid-item grid-span-1">

````md magic-move {duration: 1000}

```python
@dataclass
class Topping:
    name: Name
    price: Price


@dataclass
class Pizza:
    name: Name
    price: Price

```

```python
@registry.mapped_as_dataclass
class Topping:
    __tablename__ = "toppings"

    id: Mapped[Identity] = mapped_column(init=False)
    name: Mapped[Name]
    price: Mapped[Price]


@registry.mapped_as_dataclass
class Pizza:
    __tablename__ = "pizzas"

    id: Mapped[Identity] = mapped_column(init=False)
    name: Mapped[Name]
    price: Mapped[Price]
```

````

</div>

<div class="mt-10 grid-item grid-span-1">
<AdmonitionType title="Declarative & Typed" type="important" color="amber-light">
  <div class="text-sm">
    With <code>Mapped[T]</code> and <code>mapped_as_dataclass</code>, we get fully typed SQLAlchemy models that behave like standard Python dataclasses.
  </div>
</AdmonitionType>
</div>

</div>

---
layout: default
title: Database Migrations
color: orange-light
---

# Generating Migrations (Alembic)

<img src="/assets/some-toppings-nobg.png" class="absolute top-4 right-4 w-25" />

Alembic detects the metadata from our models and generates migrations automatically.

<Transform scale="0.9" origin="top left">
```bash
# Generate a new migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade heads
```

```python
op.create_table(
    "pizzas",
    sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column("name", sa.String(length=100), nullable=False),
    sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint("id"),
)
op.create_index(op.f("ix_pizzas_name"), "pizzas", ["name"], unique=False)
op.create_table(
    "toppings",
    sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column("name", sa.String(length=100), nullable=False),
    sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint("id"),
)
op.create_index(op.f("ix_toppings_name"), "toppings", ["name"], unique=False)
...
```
</Transform>

---
layout: section
color: orange
---

# Second Topping: The API Layer
## Pydantic & FastAPI

<img src="/assets/some-toppings-nobg.png" class="mx-auto h-80" />

---
layout: two-cols-title
title: "API Layer: OrderReference & Amount"
color: orange-light
align: l-lt-lt
margin: tight
columns: is-6
---

:: title ::

# API Layer: `OrderReference` & `Amount`

:: left ::

<img src="/assets/some-toppings-nobg.png" class="absolute top-4 right-4 w-25" />

<div style="transform: scale(0.75); transform-origin: top left;">
````md magic-move {duration: 1000, stagger: 0.3}

```python
OrderReference = Annotated[
    str,
    Len(6),
    IsDigits,
    mapped_column(sqlalchemy.String(6), nullable=False, index=True, unique=True),
]

# The Base Layer
Amount = Annotated[Decimal, IsFinite, IsNotNan]
```

```python
def validate_reference(v: Any) -> str:
    if not isinstance(v, str):
        raise ValueError("Reference must be a string")
    return v.replace("#", "").replace("-", "")


def serialize_reference(v: str) -> str:
    return f"#{v[:2]}-{v[2:4]}-{v[4:]}"


OrderReference = Annotated[
    str,
    Len(6),
    IsDigits,
    BeforeValidator(validate_reference),
    PlainSerializer(serialize_reference, return_type=str, when_used="json"),
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
```

````

</div>

:: right ::

<div class="mt-10">
<AdmonitionType title="API Data Flow" type="tip" color="amber-light">
  <ul class="text-xs">
    <li><strong>External vs. Internal:</strong> Data presented to users or consumed often differs from internal domain representation.</li>
    <li><strong>Bridging the Gap:</strong> <code>Pydantic</code>'s functional validators and serializers extend our types as another metadata layer.</li>
  </ul>
</AdmonitionType>
</div>

---
layout: two-cols-title
title: FastAPI Endpoint & Pydantic Schemas
color: orange-light
align: l-lt-lt
margin: tight
columns: is-4
---

:: title ::

# FastAPI Endpoint & Pydantic Schemas
## Types Inform the API

<img src="/assets/some-toppings-nobg.png" class="absolute top-4 right-4 w-25" />

:: left ::

<div style="transform: scale(0.8); transform-origin: top left;">
```python
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
        ),
    ]
    pizza: PizzaSchema
    extra_toppings: list[ToppingSchema]
    created_at: TimestampTz


class OrderResponse(BaseModel):
    order: OrderSchema
    total: Price
```

</div>

:: right ::

```python
# FastAPI Endpoint
@app.get("/orders/", response_model=OrderResponse)
async def get_order(
    reference: Annotated[OrderReference, Query(alias="ref")],
    services: svcs.fastapi.DepContainer,
) -> dict[str, Any]:
    repo = await services.aget(OrderRepository)
    if (order := await repo.get_by_reference(reference)) is None:
        raise NotFoundError("Order not found")

    return {"order": order, "total": calculate_order_total(order)}
```

<ArrowDraw color="red" v-drag="[700,168,82,64,194]" />
<ArrowDraw color="red" v-drag="[172,216,58,40,153]" />


<div class="mt-4">
<AdmonitionType title="Customizing Metadata" type="tip" color="orange-light">
  <ul class="text-xs">
    <li><strong>"Topping Level" Overrides:</strong> Specific metadata (e.g., `alias`, `title`, `description`) can be customized directly on the field level.</li>
    <li><strong>Framework Integration:</strong> This allows frameworks like `FastAPI` to integrate with our types and provide additional functionality.</li>
  </ul>
</AdmonitionType>
</div>
---
layout: default
title: "Comparison & Takeaway"
transition: slide-left
color: orange
---

# Comparison &  Takeaway

- No, it **is not** like ==Django==.
- No, it **is not** like ==SQLModel==.
- I don't feel the design pressure*
  <div class="text-xs italic">*I am now recommending Hynek's talk on Design Pressure to everyone.</div>
- DB and API schemas can change independently while the domain stays stable.
- Types are no longer just to make your type checker happy.
- They are now a first-class citizen in the application, carrying metadata that informs your domain and your infrastructure.
- Your domain is centric.
- Frameworks and tools are trying to hook into it via types metadata.
- Types and domain model dictate how the frameworks and tools should adapt to it, not the other way around.
