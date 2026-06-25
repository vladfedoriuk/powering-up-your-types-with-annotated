---
layout: default
---


# production implementations

<div class="divider-blue"></div>

<p class="slide-tagline">Toy works — production libs add lifecycle, dedup, async.</p>

- `uncalled-for` — standalone typed DI, async lifecycle
- `FastDepends` — FastAPI's DI extracted, sync/async, Provider overrides
- `FastMCP` — production consumer of `uncalled-for`

<!--
Our twenty-line toy works, but production dependency injection engines add layers of complexity that the toy ignores.

uncalled-for is a standalone typed DI engine built entirely on Annotated metadata. It adds async context manager lifecycle support and dependency deduplication, so the same dependency is resolved once per call rather than multiple times.

FastDepends is FastAPI's dependency injection system extracted into a pure Python library. It supports both sync and async, adds Provider-based overriding for tests, and includes custom field support. It powers FastStream and Propan.

FastMCP is a production consumer of uncalled-for. Its CurrentContext, CurrentFastMCP, and TokenClaim are all Annotated metadata objects resolved at call time via async context managers.

The arc is the same: a twenty-line toy demonstrates the pattern, libraries like uncalled-for and FastDepends add production features, and frameworks like FastMCP consume them. But the mechanism underneath is always the same Annotated pattern.
-->
