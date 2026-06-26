---
layout: default
---

# Production implementations

<div class="divider-blue"></div>

- **`uncalled-for`** — standalone engine, async lifecycle, generator teardown, framework-agnostic
- **`FastDepends`** — FastAPI DI extracted, sync/async, dependency overrides, powers FastStream
- **`FastMCP`** — production consumer of `uncalled-for`

<!--
Three libraries that ship the production version of the pattern from the toy.

uncalled-for is a standalone DI engine designed to be embedded inside larger frameworks. It handles async dependency functions, generator-based teardown (yield-style), and scoped resolution.

FastDepends is FastAPI's dependency injection system extracted into a standalone library. It supports both sync and async callables, a Provider object for per-test dependency overrides, and powers FastStream (async message brokers) and Propan.

FastMCP is the production Python SDK for the Model Context Protocol. CurrentContext, CurrentFastMCP, and TokenClaim are Annotated markers resolved from the active async context manager at call time — exactly the pattern the toy showed.

The mechanism underneath all three: inspect the parameter annotations, find the metadata, resolve it. Annotated all the way down.
-->
