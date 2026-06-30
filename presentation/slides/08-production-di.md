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
The toy resolves synchronously, re-resolves the same callable every time, shares no state, and has no teardown. Production engines address all four gaps:

Deduplication — the same dependency callable is resolved exactly once per resolution scope and the result is cached. Calling the same endpoint twice in one request should not create two database connections.

Async & generators — dependencies can be async functions or generators with setup + teardown (yield-based). The engine calls __aenter__/__aexit__ or drains async generators after the call completes.

Scoping — each resolution scope gets its own isolated state dict. Concurrent requests cannot see each other's resolved values. The toy shares nothing because it resolves fresh every call; production engines share within a scope and isolate across scopes.

Overriding — in tests you want to swap the real database engine for a fixture. Production DI engines provide a Provider or override API so you never have to patch globals.

The next slide shows the full ecosystem — Annotated-native libraries (FastDepends, svcs, di, Lagom, diwire, anydi, uncalled-for, Picodi, andi) and traditional DI containers (python-dependency-injector, returns, Injector, Dishka, and more).

The mechanism underneath every one of the Annotated-native ones is the same pattern from the twenty-line toy.
-->
