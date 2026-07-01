---
layout: default
---


# Shared constraint vocabulary.

<div class="flex flex-wrap gap-x-3 gap-y-3 mt-4 font-mono text-sm">
  <span class="pill pill--red">Gt</span>
  <span class="pill pill--red">Ge</span>
  <span class="pill pill--red">Lt</span>
  <span class="pill pill--red">Le</span>
  <span class="pill pill--blue">Interval</span>
  <span class="pill pill--blue">MultipleOf</span>
  <span class="pill pill--yellow">MinLen</span>
  <span class="pill pill--yellow">MaxLen</span>
  <span class="pill pill--yellow">Len</span>
  <span class="pill">Timezone</span>
  <span class="pill">Predicate</span>
  <span class="pill">IsFinite</span>
  <span class="pill">IsNotNan</span>
</div>

<!--
The library `annotated-types` was created at the PyCon 2022 sprints by Samuel Colvin, the maintainer of Pydantic, alongside the Hypothesis maintainers.

The goal was to establish a shared library of frozen dataclass constraints, so other libraries wouldn't have to reinvent definitions like "greater than" or "minimum length".

It gives the community a unified vocabulary, which we'll look at next.
-->
