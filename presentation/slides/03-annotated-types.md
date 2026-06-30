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
To get the most out of Annotated, the community built annotated-types — a shared standard library for runtime constraint metadata.

It was designed at the PyCon 2022 sprints by Samuel Colvin, the maintainer of Pydantic, and the Hypothesis maintainers. The idea is simple: instead of every library inventing its own way to say "greater than zero" or "minimum length of 1", we have one set of frozen dataclass objects that everyone agrees on.

You can see the full set here: numeric constraints like Gt, Ge, Lt, Le, and Interval; length constraints like MinLen, MaxLen, and Len; string predicates like IsDigits, LowerCase, UpperCase; numeric predicates like IsFinite and IsNotNan; and general-purpose tools like Predicate and Timezone.

These are all plain frozen dataclasses — lightweight, inspectable, hashable. Libraries like Pydantic do isinstance checks against BaseMetadata to find the constraints they understand. This is the shared vocabulary that makes the whole Annotated ecosystem work.
-->
