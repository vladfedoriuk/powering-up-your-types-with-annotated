---
layout: default
---

# The DI ecosystem

<div class="divider-blue"></div>

<p class="slide-tagline">FastDepends powers FastStream · uncalled-for powers FastMCP</p>

<div class="flex flex-wrap gap-x-3 gap-y-3 font-mono text-sm">
  <span class="pill pill--red">FastDepends</span>
  <span class="pill pill--red">svcs</span>
  <span class="pill pill--red">di</span>
  <span class="pill pill--red">Lagom</span>
  <span class="pill pill--red">diwire</span>
  <span class="pill pill--red">anydi</span>
  <span class="pill pill--red">Picodi</span>
  <span class="pill pill--red">andi</span>
  <span class="pill pill--red">uncalled-for</span>
  <span class="pill pill--blue">python-dependency-injector</span>
  <span class="pill pill--blue">Injector</span>
  <span class="pill pill--blue">Dishka</span>
  <span class="pill pill--blue">Inject</span>
  <span class="pill pill--blue">Kink</span>
  <span class="pill pill--blue">Punq</span>
  <span class="pill pill--blue">Wireup</span>
  <span class="pill pill--blue">That Depends</span>
  <span class="pill pill--blue">Rodi</span>
  <span class="pill pill--blue">python-injection</span>
  <span class="pill pill--blue">injectable</span>
  <span class="pill pill--blue">Opyoid</span>
  <span class="pill pill--blue">myfy</span>
  <span class="pill pill--blue">Modern DI</span>
  <span class="pill pill--blue">Injex</span>
  <span class="pill pill--blue">ididi</span>
  <span class="pill pill--blue">injection</span>
  <span class="pill pill--blue">Fresh Bakery</span>
  <span class="pill pill--blue">engin</span>
  <span class="pill pill--blue">Clean IoC</span>
  <span class="pill pill--blue">Overlay</span>
</div>

<!--
The Python DI ecosystem is richer than most people realise. There are dozens of libraries, ranging from traditional IoC containers to modern Annotated-powered auto-wiring engines.

The Annotated-native ones (red) are the ones most relevant to this talk: they use typing.Annotated as their primary configuration channel — FastDepends (FastAPI's DI extracted), svcs (Hynek's service locator), di (Adrian Garcia Badarasco's pythonic DI), Lagom (type-based auto-wiring), diwire (type-safe with scopes), anydi (type-safe with framework integrations), Picodi (FastAPI-inspired), andi (annotation-based), and uncalled-for (async-native lifecycle).

The traditional ones (blue) use a different approach: explicit container registration, wiring declarations, or provider modules. python-dependency-injector is the most starred Python DI library overall. Injector is Guice-inspired. Dishka offers a clean API with request scoping. At the tail you'll find Opyoid (Kotlin Koin-inspired), ididi (single-line DI), injection (python-dependency-injector replacement), Fresh Bakery (async-first), engin (Uber Fx-inspired), Clean IoC (generics-focused), and Overlay (pytest-fixture syntax).

The full landscape is tracked at github.com/sfermigier/awesome-dependency-injection-in-python.
-->
