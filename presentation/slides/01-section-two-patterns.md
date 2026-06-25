---
layout: section
class: section-patterns
---

# Two distinct usage patterns

<div class="section-patterns-grid">
  <div class="section-pattern section-pattern--blue">
    <span class="marker-circle section-pattern-marker"></span>
    <div class="section-pattern-label">semantic types</div>
    <div class="section-pattern-detail">name what data <em>is</em></div>
  </div>
  <div class="section-pattern section-pattern--red">
    <span class="marker-square section-pattern-marker"></span>
    <div class="section-pattern-label">framework metadata</div>
    <div class="section-pattern-detail">instructions for tools</div>
  </div>
</div>

<!--
This is our narrative pivot — the bow before we launch the first arrow. Everything in this talk flows from one idea: Annotated lets you attach metadata to types. But people reach for it in two fundamentally different ways, and conflating them is how teams get confused.

The first pattern is semantic types. You have two SQLAlchemy engines, both typed as Engine. Annotated lets you create ReaderEngine and WriterEngine — same runtime type, different meaning. The metadata names what the data is in your domain. Your type checker sees Engine; your DI container or code reviewer sees the label.

The second pattern is framework metadata. Pydantic Field, FastAPI Query, SQLAlchemy mapped_column — instructions that tools read at runtime. Your type checker sees int or str; Pydantic sees ge=0 or min_length=3.

These are not competing uses. They're complementary layers on the same typing construct. The next two slides show one example of each. Keep this contrast in mind — we'll return to it when we build the full domain model later in the talk.
-->
