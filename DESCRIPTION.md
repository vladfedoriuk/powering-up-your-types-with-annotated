# Talk Description: Powering Up Your Types with Annotated

## Title: Powering Up Your Types with Annotated

### The Core Premise

Modern Python typing has evolved far beyond static analysis. `Annotated` (introduced in PEP 593) serves as a
**universal metadata engine**, allowing us to attach arbitrary objects to type hints. This talk argues that `Annotated`
is the most significant evolution in the Python type system because it effectively breaks the boundary between
"checking code" (static analysis) and "executing code" (runtime behavior).

### What We Are Building

To demonstrate these concepts, we will build a **room-reservation domain model** from the inside out, inspired by
the [aggregates-by-example](https://github.com/mariuszgil/aggregates-by-example/tree/master/examples/php/src/Availability)
DDD reference (originally in PHP — we bring it to Python and make every layer type-driven). We start with the
fundamentals and progressively add layers of metadata.

1. **The Pure Domain.** We start with the core business logic using pure Python structures (`attrs`/`dataclasses`):
   `Room` and `Reservation`. `Room` carries a `capacity: GuestCount` instance attribute; overlap and capacity
   guards live in `add_reservation` — no separate policy objects. This is our foundation — no ORM, no web framework.
2. **Semantic Enrichment.** We replace primitive types with "Semantic Types" using `Annotated` and `annotated-types`
   (e.g., `RoomRate = Annotated[Decimal, Gt(0)]`, `GuestCount = Annotated[int, Ge(1), Le(10)]`, `RoomId`) to give
   our domain meaning that tools can read and enforce.
3. **Automated Testing.** We show how these enriched types allow tools like `Polyfactory` and `Hypothesis` to
   automatically understand our domain constraints, enabling zero-config test data generation and property-based testing.
4. **The Persistence & API Layers.** We layer on SQLAlchemy metadata for persistence and Pydantic/FastAPI metadata for
   serialization and validation — without ever changing the domain model underneath.

### Runtime Introspection — How Libraries Actually Use Annotated (EuroPython Addition)

A dedicated section covers how to work with `Annotated` types programmatically — the foundation any library author or
framework integrator needs. This includes:

- **`__origin__` and `__metadata__`** — direct attribute access on `Annotated` objects. `__origin__` exposes the
  unwrapped base type (`str`, `Decimal`, …), while `__metadata__` is the tuple of all metadata arguments in order.
  Contrasted with `get_origin()`, which returns `Annotated` itself (not the base type).
- **Flattening and equality rules** — nested `Annotated` types are flattened (innermost metadata first); metadata
  order matters for equality; duplicates are preserved. The one exception: flattening is suppressed when the inner
  `Annotated` is referenced via a PEP 695 `TypeAliasType`, because the compiler avoids evaluating lazy aliases eagerly.
- **`get_origin()` and `get_args()`** — detect and unpack `Annotated` wrappers at runtime.
- **The `get_constraints()` pattern** — iterate over `BaseMetadata` and `GroupedMetadata` from `annotated-types`, the
  same approach used by Pydantic, SQLAlchemy, and Hypothesis internally.
- **`typing.get_type_hints(include_extras=True)`** — the classic approach; resolves the full MRO but strips metadata
  by default.
- **`annotationlib.get_annotations()` (Python 3.14+, PEP 649/749)** — the modern replacement; supports three output
  formats (`VALUE`, `FORWARDREF`, `STRING`), preserves `Annotated` metadata always, and returns only a class's own
  annotations (no MRO merging).
- **Caveats:** `from __future__ import annotations` (PEP 563) and how it changes what `get_annotations` returns;
  using `eval_str=True` or `get_type_hints` as workarounds.
- **`ForwardRef`** — how `Format.FORWARDREF` returns proxy objects instead of raising `NameError`, useful for
  metaclass and framework machinery that runs before all names are defined.
- **PEP 747 — `TypeForm`** — accepted for Python 3.15; properly annotating functions that *accept* type form objects.

### `Annotated` is Not a Type — Type Checker Behavior (EuroPython Addition)

A focused segment on a subtle but important boundary in the Python type system: `Annotated` is a *special form*, not a
concrete `type`, and modern type checkers enforce this strictly.

- **Special form vs. type** — the typing spec [glossary](https://typing.python.org/en/latest/spec/glossary.html#term-special-form)
  defines a special form as an object with special meaning in the type system, comparable to a keyword. `Annotated`, `Union`,
  `ClassVar` are all special forms. They are **not** classes and are **not** assignable to `type[T]`. The spec is explicit:
  *"An attempt to call `Annotated` (whether parameterized or not) should be treated as a type error by type checkers."*
- **The `svcs` real-world case** — [svcs](https://svcs.hynek.me/) recommended `Annotated[SomeType, "tag"]` as registry keys
  for multiple same-type registrations. Pyright ≥ 1.1.350, mypy, and pyre now correctly reject this because
  `Annotated[int, "x"]` is not a `type[int]`. The
  [typing council confirmed](https://github.com/python/typing-council/issues/18) that stricter enforcement is correct.
  hynek's resolution ([svcs #92](https://github.com/hynek/svcs/pull/92)): document the pattern as unsupported rather than
  weaken the type signature.
- **Cross-checker demonstration** — showing the same failing snippet against mypy, pyright, pyrefly (Meta), and ty (Astral)
  to illustrate that the rejection is now an ecosystem-wide consensus, not a single-tool quirk.
- **The right fix: `TypeForm[T]`** — PEP 747 (accepted, Python 3.15) introduces `typing.TypeForm`, a new special form that
  describes the full set of type form objects — including `Annotated[…]`. Changing `svc_type: type[T]` to
  `svc_type: TypeForm[T]` makes the signature accept any valid type expression while keeping it fully type-safe.
  A `typing_extensions` backport is available for earlier Python versions.

### Annotated as a Framework Primitive — Dependency Injection (EuroPython Addition)

A dedicated segment bridges the gap between "runtime constraint scanning" and "full framework machinery", showing how
the same `Annotated` pattern powers dependency injection:

- **`BaseMetadata` and `GroupedMetadata`** — the contracts from `annotated-types` that let libraries safely scan
  metadata without knowing anything about types they don't own. `GroupedMetadata.__iter__` enables uniform unpacking
  of composite constraints.
- **Build-your-own DI in 20 lines** — a toy `Injectable` metadata class plus an `@inject` decorator that resolves
  dependencies from type annotations using `get_type_hints(include_extras=True)`. Demonstrates the three-step recipe
  any library author follows: define a marker class, scan with `get_type_hints`, dispatch on `isinstance`.
- **Production implementations** — [`FastDepends`](https://github.com/lancetnik/FastDepends) (FastAPI's DI extracted
  to pure Python, powering FastStream), [`uncalled-for`](https://github.com/chrisguidry/uncalled-for) (a standalone
  `Annotated`-powered DI engine with async context manager lifecycle), and
  [FastMCP `dependencies.py`](https://github.com/PrefectHQ/fastmcp/blob/main/fastmcp_slim/fastmcp/server/dependencies.py)
  as a real-world consumer: `CurrentContext()`, `CurrentFastMCP()`, `TokenClaim()` are all `Annotated` metadata
  objects resolved at call time.
- The arc from toy to production drives home the core thesis: `Annotated` is not a type-system nicety — it is a
  universal, inspectable channel for framework metadata.

### Comparison Slides — Django/DRF and SQLModel (EuroPython Addition)

After completing the full working example, two dedicated slides make the architectural argument concrete by contrasting
the `Annotated`-based approach with two common alternatives.

- **The Django/DRF approach** — the central argument is that the ORM `Model` *is* the domain. When the model changes,
  the `ModelSerializer`, the views, and any hand-written validation change with it. There is no independent domain layer:
  the database table exerts continuous [design pressure](https://hynek.me/talks/design-pressure/) on every other layer of
  the application. Neither the persistence model nor the API schema can evolve independently — they are structurally
  subordinate to the same class. With `Annotated`, the domain type is defined first and is independent; both SQLAlchemy
  and Pydantic hook into it via metadata with zero coupling between them. Extended snippet planned:
  `snippets/comparison_django.py`.
- **The SQLModel approach** — SQLModel's appeal (one class = ORM + Pydantic model) is real but creates a subtler form
  of the same coupling: the table class structure dictates the schema structure. The moment the API shape needs to diverge
  from the table (hide internal fields, expose computed values, different read/write shapes), a second class appears and
  the "single source of truth" breaks. Hynek's design pressure concept applies here too — it is just deferred, not
  eliminated. Extended snippet planned: `snippets/comparison_sqlmodel.py`.

### Composition-Based Design — The Synthesis (EuroPython Addition)

The closing argument of the comparison section: after showing what Django/DRF and SQLModel look like, a synthesis
slide recaps the full `RoomRate` type accumulating metadata one layer at a time — domain constraint, persistence, API
schema, documentation. Each layer is orthogonal; every tool reads only what it understands and ignores the rest.
The type itself never changes.

In Django/DRF that same progression requires separate classes at every layer. In SQLModel it fractures the moment
API and DB shapes diverge. Here it is one type, one source of truth.

Key phrase: *"The type is the contract. The metadata is the instruction manual — and each reader only reads the
pages written for them."*

### Pandera — `Annotated` for DataFrame Validation (EuroPython Bonus)

[Pandera](https://pypi.org/project/pandera/) demonstrates yet another ecosystem use of the same pattern: its
`DataFrameModel` API embeds column-level metadata — dtype, validation checks, description, uniqueness — directly
into the type annotation via `Annotated`, with no default-value assignment needed. The annotation is the single
source of truth for both the schema and the documentation.

This reinforces the talk's central thesis: `Annotated` is not tied to any one framework or constraint vocabulary.
The same pattern spans domain validation, ORM columns, API schemas, DI resolution, DataFrame schemas, and
documentation generation.

### The Final Garnish: Documentation

We explore how `Annotated` serves as the primary source of truth for documentation. We will dive into `annotated-doc`,
the `Doc` annotation, and the history of PEP 727. Although the PEP was revoked, the concept lives on through
@tiangolo's `annotated-doc` library, now used internally by Typer and FastAPI. We will showcase how to leverage these
annotations to automatically generate beautiful project documentation using MkDocs.

### Key Objectives & Achievements

- **Demonstrate Metadata Layering:** Show how a single type (e.g., `RoomRate`) can carry validation logic, database
  column definitions, and API documentation simultaneously, yet keep these concerns decoupled.
- **Promote Cleaner Architecture:** Argue for a "Domain-First" design. By using `Annotated`, we can defer decisions
  about our database or web framework without sacrificing type safety or functionality.
- **Reduce "Design Pressure":** Referencing Hynek Schlawack's concept of design pressure, we show how `Annotated`
  allows the domain to remain stable while the infrastructure (DB/API) evolves independently.
- **Ecosystem Mastery:** Provide a whirlwind tour of how the modern async Python stack (Pydantic v2, SQLAlchemy 2.0,
  FastAPI) has converged on `Annotated` as their primary configuration interface.
- **Runtime Introspection:** Equip attendees to write their own `Annotated`-aware libraries and frameworks by mastering
  the full annotation introspection API.

### The "Zero" Phase: The Great Boundary Break

We begin by acknowledging that `Annotated` is likely the most powerful typing feature in modern Python. Its true
strength lies in **breaking the boundary** between "checking code" (static analysis) and "executing code" (runtime).
This shift allows us to move away from "magic" (like `Field` or `Column` as default values) and towards a declarative,
**composition-based architecture**. By **layering metadata** onto our types, we create a single source of truth that
informs our domain, our database, and our API without these layers ever bleeding into one another.
