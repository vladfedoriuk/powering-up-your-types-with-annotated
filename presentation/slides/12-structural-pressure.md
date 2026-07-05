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
This is design pressure — when your database structure and your API contract keep pulling on each other. Hynek's got a whole talk on it, linked right there.

[click] Change a column, and it ripples straight through your endpoint — one side always ends up in charge.

[click] None of this is bad. For CRUD apps, stable schemas, internal tools, Django and SQLModel shine exactly because of this coupling.

[click] And sometimes it's fine to repeat yourself — duplicate first, refactor once you actually understand the shape you need.
-->
