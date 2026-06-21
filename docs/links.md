# Links Gallery

## Type Aliases

- [Type aliases — typing spec](https://typing.python.org/en/latest/spec/aliases.html)
  - Specification covering implicit aliases, `TypeAlias` (PEP 613), and the `type` statement (PEP 695), including `NewType`.
- [PEP 613 – Explicit Type Aliases](https://peps.python.org/pep-0613/)
  - Introduced `TypeAlias` annotation (Python 3.10) to remove ambiguity between plain variable assignments and type alias declarations.
- [PEP 695 – Type Parameter Syntax](https://peps.python.org/pep-0695/)
  - Introduced the `type` statement (Python 3.12) for explicit, lazy `TypeAliasType` declarations, and the `[T]` syntax for generic classes and functions. The `type` statement is what blocks `Annotated` flattening through an alias.
- [typing.TypeAliasType](https://docs.python.org/3/library/typing.html#typing.TypeAliasType)
  - Runtime type of aliases created with the `type` statement. Exposes `__value__` (the aliased type) and `__type_params__` (generic parameters), useful for resolving `Annotated` metadata blocked from flattening.

## Core — `Annotated` and the Type System

- [PEP 593 – Flexible function and variable annotations](https://peps.python.org/pep-0593/)
  - PEP introducing `Annotated` for attaching arbitrary metadata to type annotations, enabling both static analysis and runtime metadata processing.
- [Static Typing with Python](https://typing.python.org/en/latest/index.html)
  - The official documentation hub for static typing in Python, providing tutorials, guides, and technical specifications for the type system.
- [typing.Annotated](https://docs.python.org/3/library/typing.html#typing.Annotated)
  - Official documentation for the `Annotated` type, explaining how to use it to add context-specific metadata to your Python type hints.
- [Type qualifiers — Annotated](https://typing.python.org/en/latest/spec/qualifiers.html#annotated)
  - The canonical typing specification for `Annotated`: syntax rules, flattening behaviour, nested aliases, and how tools should consume metadata.
- [Special forms — type-forms spec](https://typing.python.org/en/latest/spec/type-forms.html)
  - Specification for `TypeForm` (PEP 747, Python 3.15): a new special form for annotating functions that accept type form objects at runtime.
- [Typing spec glossary — special form](https://typing.python.org/en/latest/spec/glossary.html#term-special-form)
  - Definition of key terms used in the typing specification, including "special form", "type expression", and "annotation expression".

## Runtime Annotation Introspection

- [Annotations Best Practices (Python docs)](https://docs.python.org/3/howto/annotations.html)
  - Official Python HOWTO covering best practices for accessing `__annotations__` safely across Python versions, including `get_annotations()` and `get_type_hints()`.
- [inspect.get_annotations (Python 3.10+)](https://docs.python.org/3/library/inspect.html#inspect.get_annotations)
  - The first safe cross-version API for annotation access, added in Python 3.10. No `format` parameter. In Python 3.14 it became a literal alias for `annotationlib.get_annotations()`.
- [typing.get_type_hints](https://docs.python.org/3/library/typing.html#typing.get_type_hints)
  - Documentation for `get_type_hints()`: resolves forward references, merges base-class annotations, strips `Annotated` metadata by default (use `include_extras=True` to preserve it).
- [annotationlib.get_annotations (Python 3.14+)](https://docs.python.org/3/library/annotationlib.html#annotationlib.get_annotations)
  - The modern replacement for annotation introspection in Python 3.14+. Supports `Format.VALUE`, `Format.FORWARDREF`, and `Format.STRING`; always preserves `Annotated` metadata; returns only own annotations (no MRO merging).
- [annotated-types test_main.py — get_constraints pattern](https://github.com/annotated-types/annotated-types/blob/main/tests/test_main.py#L112)
  - Real-world example of the `get_constraints()` pattern: using `get_origin`, `get_args`, and `isinstance` to iterate over `BaseMetadata` and `GroupedMetadata` from `Annotated` types.
- [PEP 747 – Annotating Type Forms](https://peps.python.org/pep-0747/)
  - Accepted PEP (Python 3.15) introducing `TypeForm[T]`, a special form for annotating callables that accept type form objects — solving the "overly-wide `object`" problem for runtime type introspection tools.
- [PEP 649 – Deferred Evaluation of Annotations](https://peps.python.org/pep-0649/)
  - The PEP behind Python 3.14's new default annotation evaluation model (lazy via `__annotate__`), which `annotationlib.get_annotations()` is built on.

## annotated-types

- [annotated-types on PyPI](https://pypi.org/project/annotated-types/)
  - PyPI page for `annotated-types`: install instructions, release history, and package metadata.
- [annotated-types on GitHub](https://github.com/annotated-types/annotated-types)
  - Reusable constraint types (like `Gt`, `Lt`, `Len`) for `typing.Annotated`, designed to be used by runtime libraries for validation and other metadata-driven behaviors.
- [annotated_types/__init__.py — BaseMetadata & GroupedMetadata](https://github.com/annotated-types/annotated-types/blob/main/annotated_types/__init__.py#L89)
  - Source of the two key contracts: `BaseMetadata` (base class for all simple constraints) and `GroupedMetadata` (protocol whose `__iter__` yields `BaseMetadata` objects, enabling uniform unpacking of composite constraints like `Interval` and `Len`).

## `Annotated` as a Special Form — Type Checker Behavior

- [`typing.TypeForm` (Python 3.15 docs)](https://docs.python.org/3.15/library/typing.html#typing.TypeForm)
  - Official Python 3.15 documentation for `TypeForm`, the new special form introduced by PEP 747. Describes how to annotate
    functions that accept type form objects (including `Annotated[…]`, unions, generics) as arguments, replacing the overly-wide
    `object` or incorrect `type[T]` signatures.
- [python/typing-council #18 — Typing spec change for `Annotated` special form](https://github.com/python/typing-council/issues/18)
  - The typing council issue that accepted the spec clarification: `Annotated` (and aliases thereof) is **not** assignable to
    `type` or `type[T]`, and an attempt to call `Annotated` should be a type error. Mypy and pyre already enforced this; Pyright
    1.1.350 aligned. The council also noted that `TypeForm` should be the long-term solution.
- [hynek/svcs discussion #74 — Type errors using `Annotated[some_type, …]` as type argument](https://github.com/hynek/svcs/discussions/74)
  - Real-world report of the issue: passing `Annotated[int, "my_int"]` to a `type[T]` parameter in `svcs.Registry.register_value`
    now raises a Pyright error. Led directly to the typing-council discussion and the `svcs` documentation change.
- [hynek/svcs pull #92 — Warn against `Annotated` & PEP 695 as registry keys](https://github.com/hynek/svcs/pull/92)
  - The resolution: `svcs` adds a warning in its docs that `Annotated[…]` and PEP 695 `type` aliases should not be used as
    registry keys under strict type checking, because neither is a `type`. The proper fix requires `TypeForm` (Python 3.15+).

## Dependency Injection via Annotated

- [Использование Annotated в Python (Habr)](https://habr.com/ru/amp/publications/822827/)
  - Russian-language article demonstrating how to build a primitive dependency injection system and a validation decorator using `Annotated`, `get_type_hints(include_extras=True)`, and `isinstance` on metadata objects. Good minimal worked example of the pattern.
- [uncalled-for (GitHub)](https://github.com/chrisguidry/uncalled-for)
  - Standalone `Annotated`-powered dependency injection engine with async context manager lifecycle. Provides `Dependency` base class, `Depends()`, and `get_dependency_parameters()`. Designed to be embedded in other frameworks.
- [FastDepends (GitHub)](https://github.com/lancetnik/FastDepends)
  - FastAPI's DI system extracted and cleared of all HTTP logic. Uses `Annotated[T, Depends(...)]` and a `@inject` decorator; supports sync and async, dependency overriding via `Provider`, and custom fields. Powers FastStream and Propan. The cleanest standalone port of the FastAPI DI pattern to pure Python.
- [FastMCP server/dependencies.py](https://github.com/PrefectHQ/fastmcp/blob/main/fastmcp_slim/fastmcp/server/dependencies.py)
  - Production use of `uncalled-for` inside FastMCP: `CurrentContext()`, `CurrentFastMCP()`, `TokenClaim()` and friends are all `Annotated` metadata objects resolved at call time. Shows the full arc from toy pattern to framework-grade DI.

## DataFrame Validation — Pandera

- [pandera on PyPI](https://pypi.org/project/pandera/)
  - PyPI page for `pandera` (v0.32.0+): a light-weight, flexible data validation library for pandas, Polars, Dask, PySpark,
    and more. Supports `Annotated` for embedding field metadata directly in type annotations.
- [Pandera DataFrameModel — Embedding Field metadata in Annotated](https://pandera.readthedocs.io/en/latest/dataframe_models.html#embedding-field-metadata-in-annotated)
  - Documentation showing how to embed `pa.Field(...)` directly inside `Annotated` on a `DataFrameModel` column annotation,
    making the annotation the single source of truth for dtype, validation checks, description, and title — without a separate
    `= pa.Field(...)` assignment. Demonstrates that `Annotated` metadata is not limited to `annotated-types` constraints.

## Domain Design Inspiration

- [aggregates-by-example — Availability (PHP)](https://github.com/mariuszgil/aggregates-by-example/tree/master/examples/php/src/Availability)
  - The room-reservation domain used throughout this talk (Resource, Reservation, Policy, Period) is adapted from
    this DDD reference implementation by Mariusz Gil. Demonstrates `Resource`, `Reservation`, and policy-based
    availability checking — translated to Python with `Annotated`-driven type semantics.

## Testing & Data Generation

- [Polyfactory Issue #347 - Support for Annotated Types](https://github.com/litestar-org/polyfactory/issues/347)
  - A GitHub issue discussing the support for `Annotated` types within the Polyfactory library for data generation.
- [Polyfactory usage with fields](https://polyfactory.litestar.dev/latest/usage/fields.html)
  - Documentation on how to use fields in Polyfactory for generating test data, often relevant for `Annotated` types.
- [Hypothesis Issues with annotated_types](https://github.com/HypothesisWorks/hypothesis/issues?q=annotated_types)
  - GitHub issues related to `annotated_types` integration and challenges within the Hypothesis property-based testing library.
- [Hypothesis strategies.from_type](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html#hypothesis.strategies.from_type)
  - Documentation for `hypothesis.strategies.from_type`, which infers strategies from type hints for property-based testing.

## Persistence — SQLAlchemy

- [SQLAlchemy 2.1 ORM Annotated Declarative — Complete Guide](https://docs.sqlalchemy.org/en/21/orm/declarative_tables.html#orm-annotated-declarative-complete-guide)
  - Full reference for the ORM Annotated Declarative system: `registry.type_annotation_map` (mapping Python
    types and `Annotated` variants to SQL column types), embedding `mapped_column()` directly in `Annotated`
    for reusable column blueprints, nullability inference from `Optional`, and PEP 695 `TypeAliasType` /
    `NewType` interaction with the type map.
- [SQLAlchemy 2.1 — Mapping Whole Column Declarations to Generic Python Types](https://docs.sqlalchemy.org/en/21/orm/declarative_tables.html#mapping-whole-column-declarations-to-generic-python-types)
  - Subsection on generic `Annotated` column blueprints using `TypeVar` and PEP 695 `type X[T] = ...` — the
    most flexible form, applying the same `mapped_column` options to any subscripted Python type. Added in 2.0.44.
- [SQLAlchemy 2.0 ORM Annotated Declarative Guide](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-annotated-declarative-complete-guide)
  - The stable 2.0 version, for reference against currently production-deployed SQLAlchemy.

## API & Validation — Pydantic / FastAPI

- [Pydantic — Types: custom types & the Annotated pattern](https://pydantic.dev/docs/validation/latest/concepts/types/)
  - Definitive reference for `Annotated`-based type customisation in Pydantic: reusable constraint aliases,
    implicit vs named type aliases and their JSON Schema `$defs` implications (new in v2.11), generic aliases
    with `TypeVar` / PEP 695 `type X[T] = ...`, the named alias restriction (type-level metadata only),
    validator metadata (`BeforeValidator`, `AfterValidator`, `WithJsonSchema`, etc.), `__get_pydantic_core_schema__`
    on metadata classes, `GetPydanticSchema`, and `TypeAdapter` for standalone validation.
- [Pydantic — Types: generics & named type aliases](https://pydantic.dev/docs/validation/latest/concepts/types/#generics)
  - Direct anchor to the generics and named alias section: implicit generic aliases with `TypeVar`, named
    generic aliases via `TypeAliasType(..., type_params=(T,))` and PEP 695, and the per-element constraint form.
- [Pydantic Functional Validators API](https://docs.pydantic.dev/latest/api/functional_validators/)
  - API documentation for Pydantic's functional validators, allowing custom validation logic for models.
- [Pydantic Functional Serializers API](https://docs.pydantic.dev/latest/api/functional_serializers/)
  - API documentation for Pydantic's functional serializers, for customizing how model data is serialized.
- [Pydantic v2.8 Validators Concepts](https://docs.pydantic.dev/2.8/concepts/validators/#before-after-wrap-and-plain-validators)
  - Pydantic v2.8 concepts explaining different types of validators (before, after, wrap, plain) for data processing.
- [FastAPI Type Hints with Metadata Annotations](https://fastapi.tiangolo.com/python-types/#type-hints-with-metadata-annotations)
  - FastAPI documentation explaining how to use `Annotated` to add metadata to type hints for request validation and dependency injection.

## Presentation Design — Bauhaus Theme

- [Bauhaus Grid Design (Laboo Studio)](https://laboostudio.com/blogs/news/bauhaus-grid)
  - Practical guide to applying the Bauhaus grid system in modern design: strict geometry, asymmetric balance,
    primary color blocks, and the underlying logic of why the grid works structurally.
- [Bauhaus Graphic Design Style Guide (Mew Design)](https://docs.mew.design/blog/bauhaus-graphic-design-style/)
  - Comprehensive overview of Bauhaus visual language: typography (geometric sans-serif, lowercase-only),
    primary color palette (red / yellow / blue / black / white), geometric motifs (circle, square, triangle),
    and "form follows function" as the governing principle — directly applicable to slide design.
- [Bauhaus Design Tokens & Template (DESIGN.md)](https://designmd.app/library/bauhaus)
  - Ready-to-use Bauhaus design file with exact color hex codes, CSS-ready geometric effects, strict grid
    specs, and light/dark mode definitions. A practical reference for implementing Bauhaus tokens in Slidev.
- [Bauhaus Color Palette — Hex Codes & Usage Guide (Hue Atlas)](https://hueatlas.com/color-palettes/bauhaus-color-palette/)
  - Precise, archival-grounded hex values for the full Bauhaus palette: primary triad (red `#C8302A`,
    yellow `#E8C018`, blue `#1E3878`), structural neutrals (studio white `#F5F2E8`, concrete `#8A8680`),
    typographic black `#1A1A18`, and workshop gold `#C89620`. Includes application rules (proportion,
    hierarchy, hard edges — no gradients) and colors to avoid.

## Documentation Generation

- [PEP 727 – Marking function parameters as 'required' or 'optional'](https://peps.python.org/pep-0727/)
  - A (withdrawn) PEP proposing syntax to explicitly mark function parameters as required or optional, relevant to type hinting.
- [annotated-doc PyPI](https://pypi.org/project/annotated-doc/)
  - PyPI page for `annotated-doc`, a library to add human-readable descriptions to `Annotated` types for documentation generation.
- [mkdocstrings-python docstrings configuration](https://mkdocstrings.github.io/python/usage/configuration/docstrings/)
  - Guide to configuring docstrings within `mkdocstrings-python` for generating API documentation from Python code.
- [mkdocstrings GitHub Repository](https://github.com/mkdocstrings/mkdocstrings)
  - The official GitHub repository for `mkdocstrings`, a tool for generating documentation from Python docstrings.
- [mkdocstrings-griffe-typingdoc API Reference](https://mkdocstrings.github.io/griffe-typingdoc/reference/api/)
  - API reference for `griffe-typingdoc`, an extension for `mkdocstrings` that improves handling of type annotations in documentation.
- [MkDocs-Material](https://squidfunk.github.io/mkdocs-material/)
  - A popular Material Design theme for MkDocs, enhancing the aesthetics and functionality of technical documentation.
- [zensical.org mkdocstrings configuration](https://zensical.org/docs/setup/extensions/mkdocstrings/#configuration-mkdocsyml)
  - Example configuration for `mkdocstrings` within `mkdocs.yml` on the Zensical documentation site.
