---
layout: section
class: section-patterns
---

# What the toy leaves out

<div class="section-patterns-grid">
  <div v-click class="section-pattern section-pattern--blue">
    <span class="marker-circle section-pattern-marker"></span>
    <div class="section-pattern-label">Deduplication & Caching</div>
    <div class="section-pattern-detail">same dep resolved once per scope; parsed signatures &amp; type hints cached across calls</div>
  </div>
  <div v-click class="section-pattern section-pattern--red">
    <span class="marker-square section-pattern-marker"></span>
    <div class="section-pattern-label">Async &amp; generators</div>
    <div class="section-pattern-detail"><code>async def</code> deps, <code>yield</code>-based teardown</div>
  </div>
  <div v-click class="section-pattern section-pattern--yellow">
    <span class="marker-triangle section-pattern-marker"></span>
    <div class="section-pattern-label">Scoping</div>
    <div class="section-pattern-detail">per-call isolated state — no leaks across concurrent requests</div>
  </div>
  <div v-click class="section-pattern section-pattern--blue">
    <span class="marker-circle section-pattern-marker"></span>
    <div class="section-pattern-label">Overriding</div>
    <div class="section-pattern-detail">swap deps in tests without touching call sites</div>
  </div>
</div>

<!--
While our twenty-line tool works, production-grade engines solve a few more engineering problems.

[click] First: Deduplication and Caching. We don't want to re-resolve the same dependency multiple times within a single request.

[click] Second: Async and Generators. We need to handle async functions and yield-based setup and teardown.

[click] Third: Scoping. We must isolate state per call so concurrent requests don't leak into each other.

[click] And fourth: Overriding. We need to easily swap dependencies in our tests.

Now, let's look at the libraries in the ecosystem that handle this.
-->
