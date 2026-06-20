# Talk Description: Powering Up Your Types with Annotated

## Title: Powering Up Your Types with Annotated

### The Core Premise

Modern Python typing has evolved far beyond static analysis. `Annotated` (introduced in PEP 593) serves as a
**universal metadata engine**, allowing us to attach arbitrary objects to type hints. This talk argues that `Annotated`
is the most significant evolution in the Python type system because it effectively breaks the boundary between
"checking code" (static analysis) and "executing code" (runtime behavior).

### What We Are Building

To demonstrate these concepts, we will build a **domain model** from the inside out. We start with the fundamentals
and progressively add layers of metadata to build a rich, functional application.

1. **The Pure Domain.** We start with the simple, structural base: the core business logic using pure Python
   structures (`attrs`/`dataclasses`). This is our foundation.
2. **Semantic Enrichment.** We replace primitive types with "Semantic Types" using `Annotated` and `annotated-types`
   (e.g., `Price`, `Quantity`, `DiscountPercentage`) to give our domain meaning.
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

### The Final Garnish: Documentation

We explore how `Annotated` serves as the primary source of truth for documentation. We will dive into `annotated-doc`,
the `Doc` annotation, and the history of PEP 727. Although the PEP was revoked, the concept lives on through
@tiangolo's `annotated-doc` library, now used internally by Typer and FastAPI. We will showcase how to leverage these
annotations to automatically generate beautiful project documentation using MkDocs.

### Key Objectives & Achievements

- **Demonstrate Metadata Layering:** Show how a single type (e.g., `Price`) can carry validation logic, database column
  definitions, and API documentation simultaneously, yet keep these concerns decoupled.
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
