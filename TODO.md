# TODO: Powering Up Your Types with Annotated

## Presentation Overview

**Title:** Powering Up Your Types with Annotated
**Target:** EuroPython
**Core Message:** `Annotated` is a universal metadata engine that enables cleaner architecture through composition and
metadata layering, breaking the boundary between static analysis and runtime execution.

______________________________________________________________________

## Phase 0: The Hook - Breaking the Boundary

- [ ] Introduce `Annotated` as the most powerful typing feature in modern Python.
- [ ] Explain how it breaks the boundary between "checking code" (static analysis) and "executing code" (runtime behavior).
- [ ] Set the stage: Moving from simple hints to rich, self-describing types.

## Phase 1: The Two Pillars of Annotated

- [ ] **Use Case A: Semantic Types.** Defining what data *is* (e.g., `RoomRate`, `GuestCount`, `RoomId`).
- [ ] **Use Case B: Framework/Library Idioms.** Leveraging metadata for tools like FastAPI (`Depends`, `Query`) and
  Pydantic (`Field`).
- [ ] Provide simple, contrasting code snippets for both.

## Phase 2: Architectural Composition & Metadata Layering

- [ ] State the thesis: `Annotated` is most powerful when combining semantic types with framework metadata.
- [ ] Explain "Metadata Layering": Adding instructions for different layers (Validation -> Persistence -> API) without
  changing the core domain logic.
- [ ] Introduce the concept of "Cleaner Architecture" through this declarative bridge

## Phase 3: The Ecosystem & `annotated-types`

- [ ] History and importance of [annotated-types](https://github.com/annotated-types/annotated-types).
- [ ] Adoption by major libraries (Pydantic, etc.).
- [ ] Showcase core metadata objects: `Gt`, `Lt`, `MinLen`, `MaxLen`, `Predicate`.
- [ ] **Technical Deep Dive:** Discuss the "Nested Annotated" pitfall and the flattening debate (CPython issue #63041).

## Phase 3.5: Working with Annotations at Runtime (NEW — EuroPython addition)

- [ ] **Slide: `Annotated` internals — `__origin__`, `__metadata__`, and flattening.**
  - `__origin__` — the unwrapped base type (`str`, `Decimal`, …). Distinct from `get_origin()`, which returns `Annotated` itself.
  - `__metadata__` — tuple of all metadata arguments in order. Never deduplicated.
  - Metadata order matters for equality: `Annotated[int, MinLen(1), MaxLen(100)] != Annotated[int, MaxLen(100), MinLen(1)]`.
  - Nested `Annotated` types **are flattened** (innermost metadata first): `Annotated[Annotated[int, MinLen(1)], MaxLen(100)] == Annotated[int, MinLen(1), MaxLen(100)]`.
  - **Exception:** flattening does **not** occur through a PEP 695 `TypeAliasType` — the alias is preserved as an opaque argument to avoid forcing evaluation.
- [ ] **Slide: Introspecting Annotated types.** Show how to work with annotations programmatically, covering the key
  runtime tools:
  - `typing.get_origin()` — detect whether a type is `Annotated`
  - `typing.get_args()` — unpack `(base_type, *metadata)` from an `Annotated` type
  - `get_constraints()` pattern (from `annotated-types`) — iterate over `BaseMetadata` / `GroupedMetadata`
  - `typing.get_type_hints(include_extras=True)` — resolve annotations across the MRO, optionally preserving metadata
  - `annotationlib.get_annotations()` (Python 3.14+) — the new preferred API with `Format.VALUE / FORWARDREF / STRING`
- [ ] **Slide: get_type_hints vs get_annotations — key differences.**
  Contrast the two APIs on a single slide:
  | Feature | `get_type_hints` | `get_annotations` |
  |---|---|---|
  | Strips `Annotated` metadata | YES (default) | NO (always preserved) |
  | Keep metadata toggle | `include_extras=True` | n/a |
  | Merges base-class annotations | YES (full MRO) | NO (own only) |
  | Evaluates string annotations | YES (always) | only with `eval_str=True` |
  | Format support | — | VALUE / FORWARDREF / STRING |
  | Available since | Python 3.5 | Python 3.14 |
- [ ] **Caveat: `from __future__ import annotations` (PEP 563).** Explain that string-stored annotations are returned
  as-is by `get_annotations(Format.VALUE)` — `eval_str=True` or `get_type_hints` is needed to resolve them.
- [ ] **Caveat: ForwardRef and FORWARDREF format.** Show that `Format.FORWARDREF` returns proxy objects instead of
  raising `NameError` when names are undefined, useful for metaclass/framework machinery.
- [ ] **PEP 747 — TypeForm** (accepted, Python 3.15). Mention briefly that annotating functions that *accept* type form
  objects now has a proper spelling: `TypeForm[T]`.
- [ ] **Code snippet:** `snippets/annotations_introspection.py` and `snippets/test_annotations_introspection.py` already
  cover all runtime introspection APIs with passing tests. Reference from slide.

## Phase 3.6: `Annotated` is Not a Type — Exploiting Type Checker Behavior (NEW)

- [ ] **Slide: `Annotated` is a special form, not a `type`.**

  - Recap the distinction between a *type* (`int`, `str`, a class) and a *special form* (`Annotated`, `Union`, `ClassVar`).
  - The glossary definition: a [special form](https://typing.python.org/en/latest/spec/glossary.html#term-special-form) is an object
    with special meaning in the type system — comparable to a keyword. It is **not** a concrete class.
  - Consequence: `Annotated[int, "x"]` is **not** assignable to `type[T]` or `type[int]` — type checkers should and do reject it.
    The typing spec is explicit: *"An attempt to call `Annotated` (whether parameterized or not) should be treated as a type error
    by type checkers."* ([Type qualifiers — Annotated](https://typing.python.org/en/latest/spec/qualifiers.html#annotated))
  - Runtime evidence: `type(Annotated[int, "x"])` returns `typing._AnnotatedAlias`, not a subclass of `type`.

- [ ] **Slide: The `svcs` problem — a real-world collision.**

  - [svcs](https://svcs.hynek.me/) is a service locator library. Its docs recommended using `Annotated[SomeType, "tag"]` as
    a registry key, enabling multiple registrations for the same base type:
    ```python
    with svcs.Registry() as reg:
        reg.register_value(
            Annotated[int, "my_int"], 42
        )  # ← type error in Pyright ≥ 1.1.350
    ```
  - The root cause ([svcs #74](https://github.com/hynek/svcs/discussions/74),
    [typing-council #18](https://github.com/python/typing-council/issues/18)): `register_value` takes `svc_type: type[T]`.
    Pyright 1.1.350+ (along with mypy and pyre) now correctly reject `Annotated[int, "my_int"]` because it is not a `type`.
  - The "fix" ([svcs #92](https://github.com/hynek/svcs/pull/92)): hynek chose to warn users away from `Annotated` as registry
    keys rather than weaken `svc_type` to `Any`. The pattern is now documented as unsupported under strict type checking.
  - Broader lesson: **any library that passes `Annotated[…]` as a `type[T]` argument will hit this wall.**

- [ ] **Slide: Type checkers — who rejects what?**

  - Plan to demonstrate the svcs snippet against the major conforming type checkers:
    - [mypy](http://mypy-lang.org/) — rejects (has done so for some time)
    - [pyright](https://github.com/microsoft/pyright) — rejects since 1.1.350
    - [pyrefly](https://pyrefly.org/) — Meta's new type checker, conformance TBD
    - [ty](https://docs.astral.sh/ty/) — Astral's new type checker, conformance TBD
  - Reference: [conformance test suite results](https://htmlpreview.github.io/?https://github.com/python/typing/blob/main/conformance/results/results.html)
    track which tools pass which spec tests.

- [ ] **Slide: The proper fix — `TypeForm[T]`.**

  - PEP 747 (accepted, landing in **Python 3.15**) introduces `typing.TypeForm` — a special form that describes the set of all
    *type form objects* (anything that can appear as a type expression at runtime).
  - With `TypeForm`, the correct signature for a function that should accept *any* type form — including `Annotated[…]` — is:
    ```python
    from typing import TypeForm  # Python 3.15+, or typing_extensions backport


    def register_value[T](svc_type: TypeForm[T], value: T) -> None: ...
    ```
  - `TypeForm[T]` is a supertype of `type[T]`: a `type[int]` is still accepted wherever `TypeForm[int]` is expected.
  - `Annotated[int, "x"]` is now a valid `TypeForm[int]` — the type checker is satisfied.
  - Until Python 3.15 ships widely, `typing_extensions.TypeForm` provides the backport.
  - Docs: [`typing.TypeForm` (Python 3.15)](https://docs.python.org/3.15/library/typing.html#typing.TypeForm),
    [TypeForm spec](https://typing.python.org/en/latest/spec/type-forms.html)

- [ ] **Snippet plan:** `snippets/type_checker_annotated.py` — a minimal module with the failing pattern
  (`def register_value(svc_type: type[T], value: T) -> None`) and a call passing `Annotated[int, "tag"]`, so the type
  error is reproducible by running mypy / pyright / ty against the file. Add inline comments explaining why each tool
  rejects it and show the corrected `TypeForm[T]` variant below.

## Phase 3.7: `annotated-types` Contracts & Annotated-Powered Dependency Injection (NEW)

- [ ] **Slide: `BaseMetadata` and `GroupedMetadata` — the contracts.**

  - `BaseMetadata` — the base class all simple `annotated-types` constraints (`Gt`, `Le`, `MinLen`, …) inherit from.
    Libraries do `isinstance(meta, BaseMetadata)` to identify constraints they understand.
  - `GroupedMetadata` — a `@runtime_checkable` `Protocol` whose `__iter__` yields `BaseMetadata` objects.
    Lets libraries unpack composite constraints (e.g. `Interval` → `Gt + Lt`, `Len` → `MinLen + MaxLen`) uniformly.
  - The `get_constraints()` pattern from Phase 3.5 relies entirely on these two contracts.
  - Show source: [`annotated_types/__init__.py#L89`](https://github.com/annotated-types/annotated-types/blob/main/annotated_types/__init__.py#L89)
  - Key design decision: metadata classes are plain frozen dataclasses — lightweight, inspectable, hashable.

- [ ] **Slide: Build your own — dependency autowiring with `Annotated`.**

  - Demonstrate that `Annotated` metadata does not have to be a constraint — it can be *any* Python object, including
    a marker that carries injection instructions.
  - Follow the API shape of `uncalled-for`: a `Depends` metadata class (subclassing `BaseMetadata`) and a
    `resolve_dependencies` context manager that resolves and injects sync callables.
  - The mechanics are trivial: `Depends(callable)` as a `BaseMetadata` frozen dataclass, scan annotations,
    dispatch on `isinstance`, call the callable — done in ~20 lines.
  - Stress that this toy is intentionally minimal. The point is that the *pattern* emerges directly from
    `Annotated` — not from any framework magic.
  - Emphasise that the type checker sees only the base type (`T` in `Annotated[T, Depends(...)]`) and is
    never confused by the metadata.

- [ ] **Slide: Production implementations — what the toy leaves out.**

  - The toy works, but production DI engines add layers the toy ignores: dependency deduplication (same callable
    resolved once per call), async support, context-manager lifecycle (setup + teardown), per-call isolated state
    (resolved values must not leak across concurrent requests — each resolution scope owns its own state), dependency
    overriding for tests, nested / transitive dependencies, and error propagation. These are engineering problems — the
    *mechanism* is still the same `Annotated` pattern underneath.
  - [`uncalled-for`](https://github.com/chrisguidry/uncalled-for) — standalone typed DI engine built entirely on
    `Annotated` metadata, with async context manager lifecycle and dependency deduplication. Designed to be embedded
    in frameworks.
  - [`FastDepends`](https://github.com/lancetnik/FastDepends) — FastAPI's DI extracted to pure Python. Adds sync/async,
    `Provider`-based overriding, and custom fields. Powers **FastStream** and **Propan**.
  - [FastMCP `server/dependencies.py`](https://github.com/PrefectHQ/fastmcp/blob/main/fastmcp_slim/fastmcp/server/dependencies.py) —
    production consumer of `uncalled-for`: `CurrentContext()`, `CurrentFastMCP()`, `TokenClaim()` are all
    `Annotated` metadata objects resolved at call time via async context managers.
  - The arc: 20-line toy → `FastDepends` / `uncalled-for` → FastMCP — same `Annotated` mechanism, growing complexity.

- [ ] **Snippet plan:** `snippets/dependency_injection.py` — a self-contained, runnable demo:

  - `Depends(callable)` — frozen dataclass subclassing `BaseMetadata`.
  - `resolve_dependencies(fn)` — a context manager that scans `get_type_hints(include_extras=True)`, resolves each
    `Annotated[T, Depends(...)]` parameter by calling the dependency callable, stores resolved values in a dict for
    the duration of the `with` block, and yields that dict as the injected kwargs.
  - A small usage example: a function with two `Annotated` parameters, called inside `with resolve_dependencies(fn) as deps`.
  - Sync callables only. Keep it under ~50 lines.
  - Add `snippets/test_dependency_injection.py` with a few `pytest` cases asserting correct resolution and a clear
    error when a dependency callable raises.

## Phase 4: Building the Domain — Resources, Reservations, and Rules

- [ ] **Code samples:** Rewrite all snippets to use a **room-reservation domain** inspired by
  [aggregates-by-example](https://github.com/mariuszgil/aggregates-by-example/tree/master/examples/php/src/Availability).
  Core entities: `Room`, `Reservation`. Core semantic types: `RoomId`, `GuestCount`, `RoomRate`, `NightCount`.
  Business rules are enforced inside entity methods (e.g., `add_reservation`).
  Business logic: `calculate_stay_total`.
- [ ] **4.1: Pure Domain Model.** Create base `attrs` or `dataclasses` for `Room` and `Reservation`.
  `Room` carries a `capacity: GuestCount` instance attribute. Overlap and capacity guards live in `add_reservation`
  — not in separate policy objects.
- [ ] **4.2: Adding Semantics.** Refactor primitive types to `Annotated` types
  (e.g., `RoomRate = Annotated[Decimal, Gt(0)]`, `GuestCount = Annotated[int, Ge(1), Le(10)]`).
- [ ] **4.3: Automated Testing with "Polyfactory".** Generate fake reservation data for unit tests using `polyfactory`.
- [ ] **4.4: Logic & Property-Based Testing.**
  - Implement `calculate_stay_total` (rate × nights, discount, tax) and an overlap guard in `add_reservation`.
  - Use `Hypothesis` to test using the `Annotated` constraints as input strategies.
  - **Note:** Mention Hypothesis' current limitations:
    - Very basic support for `annotated-types` for now.
    - Unable to unnest/flatten `Annotated` (leads to `ResolutionFailed`).
    - Lacking proper support for `Timezone`, `IsNotNan`, and `IsFinite`.

## Phase 5: Layer 1 — Persistence (SQLAlchemy)

- [ ] Enrich domain classes with SQLAlchemy metadata.

- [ ] Show how `Annotated` types map to database columns.

- [ ] Generate migrations using `Alembic`.

- [ ] **Advanced SQLAlchemy: `Annotated` as reusable column blueprints (snippet planned).**

  - **`registry.type_annotation_map`** — how SQLAlchemy resolves `Mapped[T]` annotations to SQL column types.
    `Annotated` variants serve as keys, enabling different SQL types for the same base Python type.
  - **Variant A — `Annotated` as a `type_annotation_map` key:** map the same Python type (e.g. `str`, `Decimal`)
    to different SQL column types by using distinguishing `Annotated` aliases as dictionary keys.
  - **Variant B — whole `mapped_column()` embedded in `Annotated`:** bundle the full column declaration (SQL type,
    nullability, server defaults, constraints) into a reusable `Annotated` alias used via `Mapped[alias]` — the
    canonical way to avoid repeating `mapped_column(...)` boilerplate across dozens of models.
  - **Variant C — generic `Annotated` column blueprint:** a `TypeVar`-parameterised `Annotated` alias
    (`PrimaryKey[T]`) that applies the same column options to *any* Python type subscripted into it — e.g.
    `Mapped[PrimaryKey[int]]` vs `Mapped[PrimaryKey[uuid.UUID]]`. The PEP 695 `type PrimaryKey[T] = ...`
    spelling removes the need for an explicit `TypeVar`. Added in SQLAlchemy 2.0.44.
  - **Type alias spellings** — cover implicit assignment alias, PEP 695 `type` alias, and generic PEP 695
    alias (`type X[T] = ...`) for all variants, and note the `type_annotation_map` resolution rules:
    direct aliases resolve; chained `TypeAliasType` chains do not.
  - **Snippet plan:** `snippets/sqlalchemy_advanced.py` — all three variants with both alias spellings; verify
    by printing `CREATE TABLE` DDL.

______________________________________________________________________

## Testing & Data Generation Notes

- **Polyfactory:** Use for generating simple objects (DTOs, Value Objects, Pydantic models, plain dataclasses/attrs).
- **Factory-boy:** Prefer for generating complex entities with relationships and database state.

## Phase 6: Layer 2 — API & Validation (Pydantic & FastAPI)

- [ ] Leverage Pydantic functional validators for advanced logic (e.g., cross-field validation).

- [ ] Create a FastAPI endpoint that uses these types for automatic request validation.

- [ ] Implement automated tests for the API layer.

- [ ] **Advanced Pydantic: the full `Annotated` type toolkit (snippet planned).**

  - **Implicit vs named type aliases — and why it matters for JSON Schema.** Implicit assignment aliases
    (`PositiveInt = Annotated[int, Gt(0)]`) are invisible to Pydantic — the alias name is lost and its schema
    is inlined at every usage site. Named aliases (`TypeAliasType` / PEP 695 `type`, new in Pydantic v2.11)
    preserve the name and produce a single `$defs` entry referenced via `$ref` — critical for large schemas
    and for recursive types.
  - **Generic type aliases** — `TypeVar` inside `Annotated` works for both implicit and named aliases
    (`ShortList = Annotated[list[T], Len(max_length=4)]`). The PEP 695 `type X[T] = ...` spelling removes
    the need for an explicit `TypeVar`. Also cover the per-element form: placing the constraint on the element
    type inside the container rather than on the container itself.
  - **Named alias restriction** — only type-level metadata (constraints, JSON schema overrides) is allowed
    inside a named alias; field-specific metadata (`default`, `alias`, `deprecated`) is forbidden because
    Pydantic avoids eagerly evaluating `__value__`. This connects directly to the Phase 3.5 note that PEP 695
    `type` aliases suppress `Annotated` flattening.
  - **Validators as `Annotated` metadata** — `BeforeValidator`, `AfterValidator`, `PlainValidator`,
    `WrapValidator`, and `WithJsonSchema` can all live inside `Annotated`, making transforms reusable and
    composable across any number of types and models.
  - **`__get_pydantic_core_schema__` on a metadata class** — the extensibility hook that powers the built-in
    validators. Implementing it on a frozen dataclass placed in `Annotated` is the canonical way to integrate
    third-party types or build custom validation logic without subclassing.
  - **`GetPydanticSchema`** — lighter-weight shorthand for the above when the schema can be expressed as a
    simple callable.
  - **`TypeAdapter`** — validate, serialize, or generate JSON schema for any `Annotated` type standalone,
    outside a `BaseModel`.
  - **Snippet plan:** `snippets/pydantic_advanced.py` — one runnable file covering each concept above.
    Self-contained, no FastAPI server required.

## Phase 7: Comparison & Philosophical Takeaway

- [ ] **Comparison:** Contrast this approach with DRF (Django Rest Framework) or SQLModel.

  - Add sentences: "No, it is not like Django", "No, it is not like SQLModel"

- [ ] **Design Pressure:** Explain why we don't start with the database model (Reference: Hynek's talk on
  "Design Pressure"). Add a sentence: "We start with the domain model, not with the database model". "I don't feel the design pressure\*" (add * with "I am now recommending Hynek's talk on Design Pressure to everyone")

- [ ] **Independence:** Showcase how DB persistence and API schemas can change independently while the domain stays stable.

- [ ] **Types as a first-class citizen:** Types are no longer just for static analysis or to make your type checker happy. They are now a first-class citizen in the application, carrying metadata that informs your domain, your database, and your API.

- [ ] **Domain in the center:** Your domain is centric. Frameworks and tools are trying to hook into it via types metadata. Types and domain model dictates how the frameworks and tools should adapt to it, not the other way around.

- [ ] **Conclusion:** Recapping `Annotated` as a tool for architectural sanity.

- [ ] **Slide: The Django/DRF way — "No, it is not like Django" (extended snippets planned).**

  - The central argument: **the model is also the data infrastructure, so when the model changes, everything downstream
    changes with it.** The `Model` definition dictates the `ModelSerializer` shape, which dictates the API contract. The
    chain of dependency flows top-down from the database layer, not from the domain.
  - In Django/DRF there is no independent domain layer — the ORM model *is* the domain. Swapping the DB, or even changing
    a column name, requires touching the model, the serializer, the views, and any hand-written validation. Hynek's concept
    of [design pressure](https://hynek.me/talks/same-pattern/) applies directly: the shape of the database table exerts
    continuous pressure on every other layer of the application.
  - The serializer is structurally subordinate to the model. Even `ModelSerializer` — which auto-generates fields — breaks
    silently when the model evolves, because the generated field set is not declared explicitly and mismatches appear only
    at runtime.
  - With `Annotated`, the domain type is defined independently, and **neither the persistence layer nor the API schema
    needs to know about the other** — they both hook into the domain type via metadata, with zero coupling between them.
  - **Snippet plan (to be developed):** `snippets/comparison_django.py` — same entity modelled in Django:
    `Model` class, `ModelSerializer`, a `Serializer` override when the API shape diverges, and a `clean()` / `validate_`
    method. Annotate each duplication point and coupling. The goal is a side-by-side that makes the design pressure
    viscerally visible.

- [ ] **Slide: The SQLModel way — "No, it is not like SQLModel" (extended snippets planned).**

  - The central argument: **the table class structure dictates the schema structure.** SQLModel's appeal is real — one
    class unifies ORM and Pydantic model — but it is a different form of the same coupling. When the API needs to diverge
    from the table (hide internal fields, expose computed values, accept a different shape on write vs. read), a second
    class appears and the "single source of truth" promise fractures.
  - The design pressure is subtler than in Django but just as real: the base table class exerts pressure on all schemas
    derived from it. Hynek's [design pressure talk](https://hynek.me/talks/same-pattern/) is directly relevant here too —
    the pressure is just deferred, not eliminated.
  - Additional friction points worth mentioning (to be explored with snippets):
    - `annotated-types` constraints (`Gt`, `MinLen`) don't integrate cleanly with SQLModel's field system.
    - Fine-grained column control (`mapped_column(Numeric(10,2))`) requires reaching outside SQLModel's API.
    - Domain-only invariants have no natural home that isn't also an ORM concern.
  - With `Annotated`, the domain type is central and unchanged. SQLAlchemy hooks in via one metadata argument, Pydantic
    via another — neither imposes structure on the other.
  - **Snippet plan (to be developed):** `snippets/comparison_sqlmodel.py` — same entity in SQLModel showing the initial
    appeal, then a realistic divergence scenario (read model vs. write model, a hidden field) where a second class is
    needed. Annotate where the design pressure surfaces.

- [ ] **Slide: Composition-based design — the synthesis.**

  - The closing argument of Phase 7: after the comparisons land, recap the full example as a single `RoomRate` type
    accumulating metadata one layer at a time — domain constraint, persistence, API schema, documentation.
  - Each layer is orthogonal: every tool reads only what it understands and silently ignores the rest. The type
    itself never changes — only the instruction set grows.
  - Contrast directly with Django/DRF and SQLModel: adding a new concern there means a new class; here it means
    one more metadata argument.
  - Visualise as stackable, transparent "lenses" applied to a base type.
  - Key phrase: *"The type is the contract. The metadata is the instruction manual — and each reader only reads
    the pages written for them."*

## Phase 7.5: Bonus — Pandera: `Annotated` for DataFrame Validation (EuroPython Addition)

- [ ] **Slide: Pandera `DataFrameModel` — `Annotated` all the way down.**
  - [Pandera](https://pypi.org/project/pandera/) as another ecosystem proof point: its `DataFrameModel` API
    uses `Annotated` to embed column-level metadata (dtype, validation checks, description, title, uniqueness)
    directly in the annotation — no separate `= pa.Field(...)` assignment needed.
  - The annotation is the single source of truth. Works alongside dtype-parameterised types. If both an embedded
    `Field` and an explicit assignment exist, the assignment wins — a deliberate escape hatch.
  - Key point: Pandera demonstrates that *any* metadata object can live inside `Annotated` — the pattern is not
    limited to `annotated-types` constraints or ORM column declarations.
  - Docs: [Embedding Field metadata in Annotated](https://pandera.readthedocs.io/en/latest/dataframe_models.html#embedding-field-metadata-in-annotated)
- [ ] **Snippet plan:** `snippets/pandera_demo.py` — a `DataFrameModel` subclass with a few columns using
  `Annotated[T, pa.Field(…)]`, covering description, range checks, and uniqueness. Show a valid and an invalid
  DataFrame. Self-contained with `pd.DataFrame`, no external fixtures.

## Phase 8: Layer 3 — Documentation with `annotated-doc`

- [ ] **Context:** Introduce `annotated-doc` and the revoked PEP 727.
- [ ] **History:** Mention @tiangolo's role and adoption in Typer/FastAPI.
- [ ] **Implementation:** Use `Doc` to add human-readable descriptions to our domain types (e.g., `RoomRate`, `GuestCount`).
- [ ] **Tooling:** Showcase the MkDocs plugin and how it automatically renders these descriptions.
- [ ] **Integration:** Show how `annotated-doc` integrates with MkDocs to produce beautiful, type-driven documentation.
  - **Note:** Use `Doc` directly for constants/args instead of through Aliases. It must be the first member of a top-level annotation to ensure documentation tools pick it up correctly.
- [ ] Provide docstrings for all code snippets.

______________________________________________________________________

## Repository & Tooling Tasks

- [ ] **README.md:** Rewrite to reflect the presentation goals and project structure.
- [ ] **Pre-commit:** Set up hooks (Ruff, Mypy, etc.) to ensure code snippet quality.
- [ ] **Reference Links:** Create an MD file with all reference links and resources.
- [ ] **Final Garnish:** Add a QR code to the repository at the end of the presentation.
- [ ] **Presentation Framework:**
  - [ ] Set up [Slidev](https://sli.dev/) for the main presentation.
  - [ ] Explore [Marimo](https://marimo.io/) for interactive code examples/notebooks.
- [ ] **Code Samples:** Rename pizza-themed snippet files (`persistent_pizza.py`, `test_api_pizza.py`, etc.) to
  match the new room-reservation domain; update all entity names and variable references inside them.
- [ ] **Slide Theme:** Remove any remaining pizza-themed assets, puns, and branding from the Slidev presentation.
- [ ] **Environment:** Finalize `pyproject.toml` with all dependencies (FastAPI, Pydantic, SQLAlchemy, Polyfactory,
  Hypothesis, etc.).

## Slide Rework — Content & Design

- [ ] **Minimise slide text.** Each slide should carry only: a short title, a code snippet or diagram, and at most
  one or two key bullet points. All explanatory prose moves to **speaker notes** (`<!-- ... -->`).
- [ ] **Speaker notes pass.** Go through every slide and write complete speaker notes — enough to present from
  without needing the slide text. Notes should read as spoken sentences, not bullet dumps.
- [ ] **Shiki Magic Move animations.** Replace static code blocks with
  [`shiki-magic-move`](https://sli.dev/features/shiki-magic-move) where a concept evolves across steps (e.g.,
  adding metadata layers to a type, refactoring from primitive to `Annotated`). Use `magicmove` fences.
- [ ] **Split slides into separate files.** Break the monolithic `slides.md` into one file per phase / major
  section, imported via Slidev's `src:` directive in the root `slides.md`. Keeps individual files focused
  and diff-friendly.
- [ ] **Bauhaus theme & design tokens.** Switch to a standard Slidev base theme and apply a custom Bauhaus
  design layer via `style.css` / `theme/` overrides:
  - **Colors:** primary triad (`#C8302A` red, `#E8C018` yellow, `#1E3878` blue) + typographic black `#1A1A18`
    - studio white `#F5F2E8`. No gradients — hard colour-field boundaries only.
  - **Typography:** geometric sans-serif (e.g., DM Sans or Inter as a practical substitute). Lean toward
    lowercase, generous spacing, strong hierarchy between title and body.
  - **Layout:** strict asymmetric grid; primary color blocks as structural dividers, not decoration.
    Circle / square / triangle motifs as section markers where appropriate.
  - **Code blocks:** dark background (`#1A1A18`), syntax tokens mapped to the primary palette where legible.
  - Reference: [Bauhaus color palette](https://hueatlas.com/color-palettes/bauhaus-color-palette/),
    [DESIGN.md Bauhaus tokens](https://designmd.app/library/bauhaus),
    [Bauhaus grid guide](https://laboostudio.com/blogs/news/bauhaus-grid).
- [ ] **Split cluttered slides into smaller focused slides.** Prefer many readable slides over dense ones: short title, one code snippet or visual, and maybe one tiny note. Move extra context into speaker notes instead of crowding the slide.
