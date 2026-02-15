# Talk Description: Extra Toppings

## Title: Extra Toppings: Powering Up Your Types with Annotated

### The Core Premise

Modern Python typing has evolved far beyond static analysis. `Annotated` (introduced in PEP 593) serves as a
**universal metadata engine**, allowing us to attach arbitrary objects to type hints. This talk argues that `Annotated`
is the most significant evolution in the Python type system because it effectively breaks the boundary between
"checking code" (static analysis) and "executing code" (runtime behavior).

### What We Are Building

To demonstrate these concepts, we will build a **Pizza Ordering Domain**. Instead of the traditional "Database-First"
or "Framework-First" approach, we will build from the inside out:

1. **The Pure Domain:** We start with the core business logic (pizzas, toppings, prices) using pure Python structures
   (`attrs`/`dataclasses`).
2. **Semantic Enrichment:** We replace primitive types with "Semantic Types" using `Annotated` and `annotated-types`
   (e.g., `Price`, `Quantity`, `DiscountPercentage`).
3. **Automated Testing Layer:** We show how these enriched types allow tools like `Polyfactory` and `Hypothesis` to
   automatically understand our domain constraints, enabling zero-config test data generation and property-based
   testing.
4. **The Persistence Layer:** We layer SQLAlchemy metadata onto our *existing* domain types. This demonstrates how to achieve persistence without letting the database schema "infect" our business logic.
5. **The API Layer:** We layer Pydantic and FastAPI metadata to handle serialization, complex functional validation, and automatic OpenAPI documentation.

### The Final Garnish: Fresh Basil & Documentation

To top off our pizza, we explore how `Annotated` serves as the primary source of truth for documentation. We will dive
into `annotated-doc`, the `Doc` annotation, and the history of PEP 727. Although the PEP was revoked, the concept lives
on through @tiangolo's `annotated-doc` library, now used internally by Typer and FastAPI. We will showcase how to
leverage these annotations to automatically generate beautiful project documentation using MkDocs.

### Key Objectives & Achievements

- **Demonstrate Metadata Layering:** Show how a single type (e.g., `Price`) can carry validation logic, database column
  definitions, and API documentation simultaneously, yet keep these concerns decoupled.
- **Promote Cleaner Architecture:** Argue for a "Domain-First" design. By using `Annotated`, we can defer decisions
  about our database or web framework without sacrificing type safety or functionality.
- **Reduce "Design Pressure":** Referencing Hynek Schlawack’s concept of design pressure, we show how `Annotated`
  allows the domain to remain stable while the infrastructure (DB/API) evolves independently.
- **Ecosystem Mastery:** Provide a whirlwind tour of how the modern async Python stack (Pydantic v2, SQLAlchemy 2.0,
  FastAPI) has converged on `Annotated` as their primary configuration interface.

### The "Zero" Phase: The Great Boundary Break

We begin by acknowledging that `Annotated` is likely the most powerful typing feature in modern Python. Its true
strength lies in **breaking the boundary** between "checking code" (static analysis) and "executing code" (runtime).
This shift allows us to move away from "magic" (like `Field` or `Column` as default values) and towards a declarative,
**composition-based architecture**. By **layering metadata** onto our types, we create a single source of truth that
informs our domain, our database, and our API without these layers ever bleeding into one another.
