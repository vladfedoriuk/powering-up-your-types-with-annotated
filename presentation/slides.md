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
layout: center
color: orange-light
---

<img src="/assets/dough-nobg.png" class="absolute top-4 right-4 w-25" />

<div>

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
