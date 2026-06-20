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

- [SQLAlchemy 2.0 ORM Annotated Declarative Guide](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-annotated-declarative-complete-guide)
  - Comprehensive guide on using `Annotated` with SQLAlchemy's ORM for declarative table definitions.

## API & Validation — Pydantic / FastAPI

- [Pydantic Functional Validators API](https://docs.pydantic.dev/latest/api/functional_validators/)
  - API documentation for Pydantic's functional validators, allowing custom validation logic for models.
- [Pydantic Functional Serializers API](https://docs.pydantic.dev/latest/api/functional_serializers/)
  - API documentation for Pydantic's functional serializers, for customizing how model data is serialized.
- [Pydantic v2.8 Validators Concepts](https://docs.pydantic.dev/2.8/concepts/validators/#before-after-wrap-and-plain-validators)
  - Pydantic v2.8 concepts explaining different types of validators (before, after, wrap, plain) for data processing.
- [FastAPI Type Hints with Metadata Annotations](https://fastapi.tiangolo.com/python-types/#type-hints-with-metadata-annotations)
  - FastAPI documentation explaining how to use `Annotated` to add metadata to type hints for request validation and dependency injection.

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
