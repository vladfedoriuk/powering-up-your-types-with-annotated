# TODO: Powering Up Your Types with Annotated

## Presentation Overview

**Title:** Powering Up Your Types with Annotated
**Target:** EuroPython
**Core Message:** `Annotated` is a universal metadata engine that enables cleaner architecture through composition and
metadata layering, breaking the boundary between static analysis and runtime execution.

**Status:** Deck complete — 48 slides across `presentation/slides/`, all with finished speaker notes. Build verified
(`pnpm run build`). Remaining open items below are either deliberately cut for time or left as bonus/snippet-only
material (noted inline).

______________________________________________________________________

## Phase 0: The Hook - Breaking the Boundary

Delivered in `00-cover.md`, `00-about-me.md`, `01-section-two-patterns.md`.

- [x] Introduce `Annotated` as the most powerful typing feature in modern Python.
- [x] Explain how it breaks the boundary between "checking code" (static analysis) and "executing code" (runtime behavior).
- [x] Set the stage: Moving from simple hints to rich, self-describing types.

## Phase 1: The Two Pillars of Annotated

Delivered in `01-use-case-semantic.md`, `02-use-case-framework.md`.

- [x] **Use Case A: Semantic Types.** Defining what data *is* (e.g., `RoomRate`, `GuestCount`, `RoomId`).
- [x] **Use Case B: Framework/Library Idioms.** Leveraging metadata for tools like FastAPI (`Depends`, `Query`) and
  Pydantic (`Field`).
- [x] Provide simple, contrasting code snippets for both.

## Phase 2: Architectural Composition & Metadata Layering

Delivered later than originally planned — folded into `12-philosophy.md` and `12-orthogonal.md` (the "Nest. Overlay.
Compose." section), after the full working example instead of right after Phase 1. Reads better once the audience has
seen persistence + API layering in practice.

- [x] State the thesis: `Annotated` is most powerful when combining semantic types with framework metadata.
- [x] Explain "Metadata Layering": Adding instructions for different layers (Validation -> Persistence -> API) without
  changing the core type.
- [x] Introduce the concept of "Cleaner Architecture" through this declarative bridge.

## Phase 3: The Ecosystem & `annotated-types`

Delivered in `03-annotated-types.md` (shared constraint vocabulary), `04-flattening-direct.md`,
`04-flattening-type-alias.md` (the flattening debate).

- [x] History and importance of [annotated-types](https://github.com/annotated-types/annotated-types).
- [x] Adoption by major libraries (Pydantic, etc.).
- [x] Showcase core metadata objects: `Gt`, `Lt`, `MinLen`, `MaxLen`, `Predicate`.
- [x] **Technical Deep Dive:** Discuss the "Nested Annotated" pitfall and the flattening debate (CPython issue #63041).

## Phase 3.5: Working with Annotations at Runtime

Delivered in `04-section-annotated-101.md`, `04-origin-metadata.md`, `04-flattening-direct.md`,
`04-flattening-type-alias.md`, `05-section-consuming-metadata.md`, `05-hasname-product.md`,
`05-get-annotations-overview.md`, `05-get-annotations.md`, `05-get-type-hints.md`, `05-introspecting-annotated.md`.

- [x] **Slide: `Annotated` internals — `__origin__`, `__metadata__`, and flattening.**
  - `__origin__` — the unwrapped base type (`str`, `Decimal`, …). Distinct from `get_origin()`, which returns `Annotated` itself.
  - `__metadata__` — tuple of all metadata arguments in order. Never deduplicated.
  - Metadata order matters for equality: `Annotated[int, MinLen(1), MaxLen(100)] != Annotated[int, MaxLen(100), MinLen(1)]`.
  - Nested `Annotated` types **are flattened** (innermost metadata first): `Annotated[Annotated[int, MinLen(1)], MaxLen(100)] == Annotated[int, MinLen(1), MaxLen(100)]`.
  - **Exception:** flattening does **not** occur through a PEP 695 `TypeAliasType` — the alias is preserved as an opaque argument to avoid forcing evaluation.
- [x] **Slide: Introspecting Annotated types.** Runtime tools covered: `typing.get_origin()`, `typing.get_args()`, the
  `get_constraints()` pattern (from `annotated-types`), `typing.get_type_hints(include_extras=True)`, and
  `annotationlib.get_annotations()` (Python 3.14+).
- [x] **`get_type_hints` vs `get_annotations` — key differences.** Delivered across `05-get-type-hints.md` and
  `05-get-annotations.md` as two focused slides rather than a single comparison table — reads better paced one API at
  a time.
- [x] **Caveat: `from __future__ import annotations` (PEP 563).** Covered in `05-get-annotations.md` speaker notes.
- [x] **Caveat: ForwardRef and FORWARDREF format.** Covered in `05-get-annotations.md` speaker notes.
- [x] **PEP 747 — TypeForm** mention. Landed on `07-typeform-fix.md` instead (paired with the `svcs` fix — better
  narrative fit than a standalone mention here).
- [x] **Code snippet:** `snippets/annotations_introspection.py` and `snippets/test_annotations_introspection.py` — done, referenced conceptually from the slides above.

## Phase 3.6: `Annotated` is Not a Type — Exploiting Type Checker Behavior

Delivered in `07-annotated-not-a-type.md`, `07-svcs-problem.md`, `07-typeform-fix.md`.

- [x] **Slide: `Annotated` is a special form, not a `type`.** Delivered in `07-annotated-not-a-type.md`.
- [x] **Slide: The `svcs` problem — a real-world collision.** Delivered in `07-svcs-problem.md`.
- [x] **Type checkers — who rejects what?** Folded into `07-svcs-problem.md`'s tagline and code comment
  (`# ↑ type error in mypy, pyright, ty, pyrefly`) instead of a separate conformance-table slide — the same
  information, without adding another slide to the deck.
- [x] **Slide: The proper fix — `TypeForm[T]`.** Delivered in `07-typeform-fix.md`, as a magic-move before/after.
- [x] **Snippet:** `snippets/type_checker_annotated.py` — done.

## Phase 3.7: `annotated-types` Contracts & Annotated-Powered Dependency Injection

Delivered in `08-section-contracts.md`, `08-contracts.md`, `08-section-di.md`, `08-di-depends.md`, `08-di-resolve.md`,
`08-di-usage.md`, `08-production-di.md`, `08-production-di-libs.md`.

- [x] **Slide: `BaseMetadata` and `GroupedMetadata` — the contracts.** Delivered in `08-contracts.md`.
- [x] **Slide: Build your own — dependency autowiring with `Annotated`.** Delivered across `08-di-depends.md`,
  `08-di-resolve.md`, `08-di-usage.md` (split into three focused slides instead of one dense one).
- [x] **Slide: Production implementations — what the toy leaves out.** Delivered in `08-production-di.md`
  (the four gaps as click-revealed cards) and `08-production-di-libs.md` (`uncalled-for`, `FastDepends`, FastMCP).
- [x] **Snippet:** `snippets/dependency_injection.py` and `snippets/test_dependency_injection.py` — done.

## Phase 4: Building the Domain — Resources, Reservations, and Rules

Delivered in `09-section-lets-build.md`, `09-pure-domain.md`, `09-semantic-types.md`, `09-polyfactory-factory.md`,
`09-polyfactory.md`, `09-hypothesis.md`.

- [x] **Code samples:** room-reservation domain built out in `snippets/basic_reservation.py`,
  `snippets/annotated_reservation.py`, `snippets/persistent_reservation.py`, `snippets/api_reservation.py`, and their
  tests. Core entities `Room`/`Reservation`; core semantic types `RoomId`, `GuestCount`, `RoomRate`, `NightCount`.
- [x] **4.1: Pure Domain Model.** Delivered in `09-pure-domain.md`.
- [x] **4.2: Adding Semantics.** Delivered in `09-semantic-types.md` (magic-move: primitives → `Annotated` types).
- [x] **4.3: Automated Testing with "Polyfactory".** Delivered in `09-polyfactory-factory.md` (click-highlighted
  walkthrough of the two manual overrides) and `09-polyfactory.md` (using factories in a test).
- [x] **4.4: Logic & Property-Based Testing.** Delivered in `09-hypothesis.md`, including the Hypothesis
  `annotated-types` support caveat (basic support, can't unnest, weak `Timezone`/`IsNotNan`/`IsFinite` support).

## Phase 5: Layer 1 — Persistence (SQLAlchemy)

Delivered in `10-column-blueprints.md`, `10-migrations.md`.

- [x] Enrich classes with SQLAlchemy metadata.
- [x] Show how `Annotated` types map to database columns.
- [x] Generate migrations using `Alembic`.
- [x] **Advanced SQLAlchemy: `Annotated` as reusable column blueprints.**
  `snippets/sqlalchemy_advanced.py` implements all three variants (A: `type_annotation_map` keys, B: whole
  `mapped_column()` embedded in the alias, C: generic `PrimaryKey[T]` blueprint) with both alias spellings, verified
  against `CREATE TABLE` DDL. The slide itself condenses to Variant B + C (the embedded-`mapped_column` alias and the
  generic blueprint) as a 3-step magic-move — Variant A is snippet-only, cut from the slide for time.

______________________________________________________________________

## Testing & Data Generation Notes

- **Polyfactory:** Use for generating simple objects (DTOs, Value Objects, Pydantic models, plain dataclasses/attrs).
- **Factory-boy:** Prefer for generating complex entities with relationships and database state.

## Phase 6: Layer 2 — API & Validation (Pydantic & FastAPI)

Delivered in `11-api-schemas.md`, `11-validators-metadata.md`, `11-fastapi-endpoint.md`.

- [x] Leverage Pydantic functional validators for advanced logic. Delivered in `11-validators-metadata.md`.
- [x] Create a FastAPI endpoint that uses these types for automatic request validation. Delivered in
  `11-fastapi-endpoint.md`.
- [x] Automated tests for the API layer — `snippets/test_api_reservation.py`.
- [x] **Advanced Pydantic: the full `Annotated` type toolkit.** `snippets/pydantic_advanced.py` covers every item
  below and is referenced as bonus/self-study material; only a subset made it onto slides for time:
  - Validators as `Annotated` metadata (`BeforeValidator`, `AfterValidator`, `PlainValidator`, `WrapValidator`,
    `WithJsonSchema`) and `TypeAdapter` — **on slide**, `11-validators-metadata.md`.
  - Implicit vs named type aliases (JSON Schema `$defs`/`$ref` behavior), generic type aliases, the named-alias
    field-metadata restriction, `__get_pydantic_core_schema__`, and `GetPydanticSchema` — **snippet-only**, not on a
    slide. Candidate for a future deep-dive talk or blog post.

## Phase 7: Comparison & Philosophical Takeaway

Delivered in `12-philosophy.md`, `12-orthogonal.md`, `12-section-why.md`, `12-not-django.md`, `12-not-sqlmodel.md`,
`12-structural-pressure.md`.

- [x] **Comparison:** Contrast this approach with DRF (Django Rest Framework) and SQLModel. Delivered in
  `12-not-django.md` / `12-not-sqlmodel.md`. The literal lines "No, it is not like Django" / "No, it is not like
  SQLModel" were tried during the speaker-notes pass and cut — they read as filler once spoken aloud; the contrast
  comes through via the code + notes instead.
- [x] **Design Pressure:** Delivered in `12-structural-pressure.md`, including the "I don't feel the design
  pressure\*" joke (\*now recommending Hynek's talk to everyone).
- [x] **Independence:** Showcase how DB persistence and API schemas can change independently. Delivered in
  `12-orthogonal.md`.
- [x] **Types as a first-class citizen.** Delivered in `12-orthogonal.md`'s click-revealed cards.
- [x] **Types dictate to frameworks, not the other way around.** Delivered in `12-orthogonal.md`.
- [x] **Conclusion:** Recapping `Annotated` as a tool for architectural sanity. Delivered in `15-thank-you.md`.
- [x] **Slide: The Django/DRF way.** Delivered in `12-not-django.md`. `snippets/comparison_django.py` exists as the
  extended, fully-worked version (Model/ModelSerializer/Serializer-override/`clean()`); the slide shows a condensed
  single example rather than the full side-by-side — enough to land the point in ~30 seconds.
- [x] **Slide: The SQLModel way.** Delivered in `12-not-sqlmodel.md`. `snippets/comparison_sqlmodel.py` exists as the
  extended version (read/write model divergence); the slide shows the condensed appeal + coupling example.
- [x] **Slide: Composition-based design — the synthesis.** Delivered in `12-orthogonal.md` (one `RoomId` type,
  three concerns stacked) rather than a separate slide — the payoff lands better right where the code is on screen.
  The closing key phrase ("The type is the contract...") was cut from spoken notes as too grand; the same idea is
  carried by the code + cards instead.

## Phase 7.5: Bonus — Pandera: `Annotated` for DataFrame Validation

**Cut from the final deck.** `snippets/pandera_demo.py` exists and works (valid/invalid `DataFrame` examples with
`Annotated[T, pa.Field(...)]`), but no slide was built for it — the talk runs long enough without a fourth ecosystem
example, and Pydantic + SQLAlchemy + FastAPI already make the "any metadata object, any framework" point. Keep the
snippet as a bonus link/QA answer rather than forcing a slide.

- [ ] **Slide: Pandera `DataFrameModel`.** Not planned unless time budget opens up.
- [x] **Snippet:** `snippets/pandera_demo.py` — done, unused in the deck.

## Phase 8: Layer 3 — Documentation with `annotated-doc`

Delivered in `14-annotated-doc.md`, `14-mkdocs-config.md`.

- [x] **Context:** Introduce `annotated-doc` and the revoked PEP 727.
- [x] **History:** @tiangolo's role and adoption in Typer/FastAPI.
- [x] **Implementation:** `Doc` on a reservation domain type (`Percentage`/`FIRST_ORDER_DISCOUNT`).
- [x] **Tooling:** MkDocs/Zensical + `mkdocstrings` + `griffe_typingdoc` plugin config.
- [x] **Integration + caveat:** `Doc` must be first in the annotation and used directly on constants/args (not through
  an alias) for doc tools to pick it up — captured explicitly in `14-annotated-doc.md` speaker notes. Also landed the
  docstring-drift benefit ("add/remove a field, the docs update automatically") in `14-mkdocs-config.md`.
- [x] Docstrings for code snippets shown on slides — not pursued repo-wide for every snippet file (not needed for the
  talk itself); leave as a nice-to-have for the repo as a standalone learning resource.

______________________________________________________________________

## Repository & Tooling Tasks

- [x] **README.md:** Rewritten to reflect the presentation goals and project structure.
- [x] **Pre-commit:** Set up via `prek` (`prek.toml` + `just prek-install` / `just prek-run-all-files`), not the
  Python `pre-commit` tool — same job, faster.
- [x] **Reference Links:** `docs/links.md` — done.
- [x] **Final Garnish:** QR code on `15-thank-you.md` via `slidev-addon-qrcode`.
- [x] **Presentation Framework:**
  - [x] Slidev set up as the main presentation, one file per slide under `presentation/slides/`.
  - [ ] Marimo for interactive code examples — not pursued. Shiki Magic Move + click-highlighted code covered the
    "show code evolving" need without a second tool in the stack.
- [x] **Code Samples:** Snippets already use room-reservation naming throughout; no pizza-themed files remain.
- [x] **Slide Theme:** No pizza-themed assets, puns, or branding remain — Bauhaus theme throughout.
- [x] **Environment:** `pyproject.toml` has FastAPI, Pydantic, SQLAlchemy, Polyfactory, Hypothesis, `annotated-doc`,
  and friends.

## Slide Rework — Content & Design

- [x] **Taglines earn their space.** Reviewed across the deck — taglines are one line, add information the title
  doesn't already carry, or are omitted.
- [x] **Minimise slide text.** Every slide carries a short title, a code snippet or diagram, and at most a couple of
  key points; explanatory prose lives in speaker notes.
- [x] **Speaker notes pass.** Every slide (48/48) has finished speaker notes, written as flowing spoken prose per
  `.claude/skills/speaker-notes-style/SKILL.md`, with `[click]` markers synced to on-slide reveals/highlights where
  the slide has clickable steps.
- [x] **Shiki Magic Move animations.** In use on `09-semantic-types.md`, `10-column-blueprints.md`,
  `11-api-schemas.md`, `11-validators-metadata.md`, and `07-typeform-fix.md`. Click-based line highlighting (a
  related but distinct feature — `{all|4-9|10-13|all}` style stage annotations) is also used on
  `09-polyfactory-factory.md` and `09-hypothesis.md`, synced to `[click]` markers in the notes.
- [x] **Split slides into separate files.** `slides.md` is headmatter + `src:` imports only; 48 files under
  `presentation/slides/`.
- [x] **Bauhaus theme & design tokens.** Implemented in `presentation/styles/index.css` per `DESIGN.md` tokens.
- [x] **Split cluttered slides into smaller focused slides.** Deck consistently follows one-topic-per-slide (e.g. DI
  autowiring split across three slides instead of one dense one).
