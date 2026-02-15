# TODO: Extra Toppings: Powering Up Your Types with Annotated

## Presentation Overview

**Title:** Extra Toppings: Powering Up Your Types with Annotated
**Target:** Python Pizza
**Core Message:** `Annotated` is a universal metadata engine that enables cleaner architecture through composition and
metadata layering, breaking the boundary between static analysis and runtime execution.

______________________________________________________________________

## Phase 0: The Hook - Breaking the Boundary

- [x] Introduce `Annotated` as the most powerful typing feature in modern Python.
- [x] Explain how it breaks the boundary between "checking code" (static analysis) and "executing code" (runtime behavior).
- [x] Set the stage: Moving from simple hints to rich, self-describing types.

## Phase 1: The Two Pillars of Annotated

- [x] **Use Case A: Semantic Types.** Defining what data *is* (e.g., `Price`, `Email`, `Percentage`).
- [x] **Use Case B: Framework/Library Idioms.** Leveraging metadata for tools like FastAPI (`Depends`, `Query`) and
  Pydantic (`Field`).
- [x] Provide simple, contrasting code snippets for both.

## Phase 2: Architectural Composition & Metadata Layering

- [x] State the thesis: `Annotated` is most powerful when combining semantic types with framework metadata.
- [x] Explain "Metadata Layering": Adding instructions for different layers (Validation -> Persistence -> API) without
  changing the core domain logic.
- [x] Introduce the concept of "Cleaner Architecture" through this declarative bridge

## Phase 3: The Ecosystem & `annotated-types`

- [x] History and importance of [annotated-types](https://github.com/annotated-types/annotated-types).
- [x] Adoption by major libraries (Pydantic, etc.).
- [x] Showcase core metadata objects: `Gt`, `Lt`, `MinLen`, `MaxLen`, `Predicate`.
- [x] **Technical Deep Dive:** Discuss the "Nested Annotated" pitfall and the flattening debate (CPython issue #63041).

## Phase 4: Building the Pizza: The Dough, The Sauce, and The Cheese

- [x] **4.1: Pure Domain Model.** Create base `attrs` or `dataclasses` for a Pizza ordering app (e.g., `Pizza`,
  `Topping`, `Order`).
- [ ] **4.2: Adding Semantics.** Refactor primitive types to `Annotated` types (e.g., `Price = Annotated[Decimal, Gt(0)]`).
- [ ] **4.3: Automated Testing with "Polyfactory".** Generate fake pizza data for unit tests using `polyfactory`.
- [ ] **4.4: Logic & Property-Based Testing.**
  - Implement a formula (e.g., `calculate_discount`).
  - Use `Hypothesis` to test the logic using the `Annotated` constraints as input strategies.
  - **Note:** Mention Hypothesis' current limitations:
    - Very basic support for `annotated-types` for now.
    - Unable to unnest/flatten `Annotated` (leads to `ResolutionFailed`).
    - Lacking proper support for `Timezone`, `IsNotNan`, and `IsFinite`.

## Phase 5: First Topping - The Persistence Layer (SQLAlchemy)

- [ ] Enrich domain classes with SQLAlchemy metadata.
- [ ] Show how `Annotated` types map to database columns.
- [ ] Generate migrations using `Alembic`.

______________________________________________________________________

## Testing & Data Generation Notes

- **Polyfactory:** Use for generating simple objects (DTOs, Value Objects, Pydantic models, plain dataclasses/attrs).
- **Factory-boy:** Prefer for generating complex entities with relationships and database state.

## Phase 6: Second Topping - The API Layer (Pydantic & FastAPI)

- [ ] Leverage Pydantic functional validators for advanced logic (e.g., cross-field validation).
- [ ] Create a FastAPI endpoint that uses these types for automatic request validation and documentation.
- [ ] Show how `annotated-doc` translates metadata into Swagger/OpenAPI documentation.
- [ ] Implement automated tests for the API layer.

## Phase 7: Comparison & Philosophical Takeaway

- [ ] **Comparison:** Contrast this approach with DRF (Django Rest Framework) or SQLModel.
- [ ] **Design Pressure:** Explain why we don't start with the database model (Reference: Hynek's talk on
  "Design Pressure").
- [ ] **Independence:** Showcase how DB persistence and API schemas can change independently while the domain stays stable.
- [ ] **Conclusion:** Recapping `Annotated` as a tool for architectural sanity.

## Phase 8: The Final Garnish - Documentation with `annotated-doc`

- [ ] **The Analogy:** "A drizzle of hot honey" or "a sprinkle of parmesan" to finish — elevating the types with documentation.
- [ ] **Context:** Introduce `annotated-doc` and the revoked PEP 727.
- [ ] **History:** Mention @tiangolo's role and adoption in Typer/FastAPI.
- [ ] **Implementation:** Use `Doc` to add human-readable descriptions to our pizza types.
- [ ] **Tooling:** Showcase the MkDocs plugin and how it automatically renders these descriptions.
- [ ] **Integration:** Show how `annotated-doc` integrates with MkDocs to produce beautiful, type-driven documentation.
  - **Note:** Use `Doc` directly for constants/args instead of through Aliases. It must be the first member of a top-level annotation to ensure documentation tools pick it up correctly.
- [ ] Provide docstrings for all code snippets.

______________________________________________________________________

## Repository & Tooling Tasks

- [x] **README.md:** Rewrite to reflect the presentation goals and project structure.
- [x] **Pre-commit:** Set up hooks (Ruff, Mypy, etc.) to ensure code snippet quality.
- [x] **Reference Links:** Create an MD file with all reference links and resources.
- [ ] **Final Garnish:** Add a QR code to the repository at the end of the presentation.
- [ ] **Presentation Framework:**
  - [x] Set up [Slidev](https://sli.dev/) for the main presentation.
  - [ ] Explore [Marimo](https://marimo.io/) for interactive code examples/notebooks.
- [ ] **Code Samples:** Ensure all snippets are concise, "Pizza-themed", and fit on a slide.
- [x] **Environment:** Finalize `pyproject.toml` with all dependencies (FastAPI, Pydantic, SQLAlchemy, Polyfactory,
  Hypothesis, etc.).
