# Powering Up Your Types with Annotated

Code samples and materials for the EuroPython talk **"Powering Up Your Types with Annotated"**.
View the slides at: https://powering-up-your-types-with-annotated.pages.dev/

## Overview

This talk explores `typing.Annotated` (PEP 593) as a universal metadata engine that breaks the boundary between static analysis and runtime behavior. We cover:

- **Semantic Types**: Using `Annotated` to express domain meaning without subclassing
- **Framework Metadata**: How Pydantic, FastAPI, and SQLAlchemy read `Annotated` metadata
- **Internals**: `__origin__`, `__metadata__`, flattening, and introspection APIs
- **TypeForm**: PEP 747 and the solution for accepting type-form objects
- **Dependency Injection**: Building DI systems with `Annotated` metadata
- **Domain Architecture**: Clean architecture through metadata layering

## Development

This project uses [uv](https://docs.astral.sh/uv/), [just](https://just.systems/), and [prek](https://prek.j178.dev/).

Consult the `justfile` for all development recipes:

```bash
just
```

## Structure

- `snippets/`: Python examples demonstrating `Annotated` for validation, persistence, APIs, and dependency injection
- `docs/`: Example `mkdocs` site with `mkdocstrings[python]` and `annotated-doc`
- `presentation/`: Slidev slides with Bauhaus design system

## Presentation

To view the slides:

```bash
cd presentation
pnpm install
pnpm run dev
```

Navigate to `http://localhost:3030`
