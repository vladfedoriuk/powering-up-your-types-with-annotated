---
layout: default
---

# Structural pressure

<div class="divider-red"></div>

<div class="flex flex-col gap-4 mt-6">
  <div v-click class="flex items-start gap-3">
    <span class="marker-circle flex-shrink-0 mt-1"></span>
    <div>
      <strong>DB and API pull on each other</strong>
      <p class="text-sm opacity-80">Change a column, ripple through the endpoint. One has the upper hand.</p>
    </div>
  </div>
  <div v-click class="flex items-start gap-3">
    <span class="marker-triangle flex-shrink-0 mt-1"></span>
    <div>
      <strong>Great when stable</strong>
      <p class="text-sm opacity-80">CRUD, low volatility, no backward-compatibility dance — these tools shine.</p>
    </div>
  </div>
  <div v-click class="flex items-start gap-3">
    <span class="marker-square flex-shrink-0 mt-1"></span>
    <div>
      <strong>Do repeat yourself</strong>
      <p class="text-sm opacity-80">Duplicate first — refactor once understanding emerges.</p>
    </div>
  </div>
</div>

<p class="text-xs opacity-60 mt-8"><em>Design pressure</em> — <a href="https://hynek.me/talks/design-pressure/">https://hynek.me/talks/design-pressure/</a></p>

<!--
The core insight: when your DB table structure directly dictates your API contract — or vice versa — you have design pressure. Hynek's talk on Design Pressure names this beautifully. Neither direction is bad per se, but you should know when it's happening.

Django and SQLModel are fantastic tools when the pressure is irrelevant — CRUD apps, stable domains, internal tools. The point is not that they're wrong, but that the coupling is baked in.

With Annotated, the domain type is independent. SQLAlchemy reads mapped_column. Pydantic reads BeforeValidator. Neither imposes on the other.

And sometimes, breaking DRY on purpose — writing a separate read model and write model — teaches you more about your domain than forcing a single abstraction. DRY is a means, not a goal.
-->
