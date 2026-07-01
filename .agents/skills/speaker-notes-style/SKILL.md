---
name: speaker-notes-style
description: >
  Style guide for writing speaker notes for this Slidev presentation.
  Use when writing or refining speaker notes in any slide under presentation/slides/.
---

# Speaker Notes Style Guide

Captured from iterative refinement with the presenter. Apply these rules to every slide.

## Timing

- **Content slides** — ~30 seconds of spoken text
- **Section / transition slides** — ~15 seconds
- **Code-heavy slides** — up to ~45 seconds if needed to walk through the code
- When in doubt: less is more. You can always pause.

## Structure (per slide)

1. **Intro phrase** — one sentence that orients the audience to this slide
2. **Key points** — 2–3 short spoken sentences covering what matters
3. **Outro / bridge** — one sentence that leads naturally into the next slide

Not every note needs all three parts — short slides may just need 1–2 sentences.

## Tone & Voice

- **Friendly, semi-informal** — talk like you're explaining to a junior dev colleague, not presenting at a board meeting
- **Direct and clear** — say the thing, then stop
- **Natural spoken rhythm** — read it out loud; if it sounds stiff, rewrite it
- Jokes are welcome when they arise naturally (self-deprecating works great); never force them
- No pretentious, snobby, or "smartass" phrasing

## Language Rules

### Do
- Simple words over fancy ones
- Short sentences with clear subjects
- "Let's get into it" as a slide transition
- Say library names when they're actually on the slide; omit them in section/intro slides
- Balance between minimalism and fluency — not so terse it's choppy, not so long it rambles

### Don't
- "domain model" — say "real code" or describe specifically what you're building
- "conflating" — say "mixing up" or restructure the sentence
- "This is our narrative pivot" or any self-aware meta commentary
- "It's worth keeping X in mind" — just make the point directly
- "Fundamentally changes" / "breaks the boundary" — too grand
- Any AI clichés: "seamless", "elevate", "unleash", "next-gen"
- Bullet dumps — write real sentences you'd actually speak
- Roadmap speeches ("We'll cover A, then B, then C, and finally D")
- Introducing libraries before their dedicated slides

## Formatting

- Write as flowing prose, not bullet points
- Separate paragraphs with blank lines (one thought per paragraph)
- Keep inside <!-- ... --> Slidev comment blocks
- No markdown formatting inside notes (no **bold**, no - lists)

## Examples

### Good
Two SQLAlchemy engines — reader and writer. Both typed as Engine. Nothing stops you from mixing them up.

Annotated fixes that. You create ReaderEngine and WriterEngine — same runtime type, different label. The type checker sees Engine; your DI container sees which one you meant.

The metadata is just a string here — but it could be anything. That's the point.

### Bad
This is our narrative pivot. Annotated fundamentally changes how we think about types by breaking the boundary between static analysis and runtime behavior. The first pattern is semantic types — you can leverage Annotated to create domain-meaningful type aliases. The second pattern is framework metadata. These are not competing uses but rather complementary layers.

## Slide-by-slide progress

Track which slides have been written and approved in this session:

- [x] 00-cover.md
- [x] 00-about-me.md
- [x] 01-section-two-patterns.md
- [ ] 01-use-case-semantic.md
- [ ] 02-use-case-framework.md
- [ ] 04-section-annotated-101.md
- [ ] 04-origin-metadata.md
- [ ] 04-flattening-direct.md
- [ ] 04-flattening-type-alias.md
- [ ] 07-annotated-not-a-type.md
- [ ] 07-svcs-problem.md
- [ ] 07-typeform-fix.md
- [ ] 05-section-consuming-metadata.md
- [ ] 05-hasname-product.md
- [ ] 05-get-annotations-overview.md
- [ ] 05-get-annotations.md
- [ ] 05-get-type-hints.md
- [ ] 08-section-contracts.md
- [ ] 03-annotated-types.md
- [ ] 08-contracts.md
- [ ] 05-introspecting-annotated.md
- [ ] 08-section-di.md
- [ ] 08-di-depends.md
- [ ] 08-di-resolve.md
- [ ] 08-di-usage.md
- [ ] 08-production-di.md
- [ ] 08-production-di-libs.md
- [ ] 09-section-lets-build.md
- [ ] 09-pure-domain.md
- [ ] 09-semantic-types.md
- [ ] 09-polyfactory-factory.md
- [ ] 09-polyfactory.md
- [ ] 09-hypothesis.md
- [ ] 10-column-blueprints.md
- [ ] 10-migrations.md
- [ ] 11-api-schemas.md
- [ ] 11-validators-metadata.md
- [ ] 11-fastapi-endpoint.md
- [ ] 12-philosophy.md
- [ ] 12-orthogonal.md
- [ ] 12-section-why.md
- [ ] 12-not-django.md
- [ ] 12-not-sqlmodel.md
- [ ] 12-structural-pressure.md
- [ ] 13-section-closing.md
- [ ] 14-annotated-doc.md
- [ ] 14-mkdocs-config.md
- [ ] 15-thank-you.md
