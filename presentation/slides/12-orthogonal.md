---
layout: default
class: code-center
---

# Orthogonal metadata

<div class="divider-red"></div>

```python
RoomId = Annotated[
    str,
    MinLen(1), MaxLen(20),              # domain constraint
    BeforeValidator(trim_str),          # validation at edges
    mapped_column(sa.String(20)),       # persistence
]
```

<div class="grid grid-cols-2 gap-4 mt-6">
  <div v-click class="flex items-start gap-3">
    <span class="marker-circle flex-shrink-0 mt-1"></span>
    <div>
      <strong>Domain stays central</strong>
      <p class="text-sm opacity-80">Stack orthogonal concerns — neither DB nor API has the last word.</p>
    </div>
  </div>
  <div v-click class="flex items-start gap-3">
    <span class="marker-triangle flex-shrink-0 mt-1"></span>
    <div>
      <strong>Types as first-class citizens</strong>
      <p class="text-sm opacity-80">Types define what data <em>is</em> — not just what the type checker accepts.</p>
    </div>
  </div>
  <div v-click class="flex items-start gap-3">
    <span class="marker-square flex-shrink-0 mt-1"></span>
    <div>
      <strong>Ecosystem converges</strong>
      <p class="text-sm opacity-80"><code>annotated-types</code> contracts — shared vocabulary, free composition.</p>
    </div>
  </div>
</div>

<!--
This is the payoff: one RoomId type carries everything. Each tool — SQLAlchemy, Pydantic, FastAPI — hooks into the metadata it knows and skips the rest.

Your domain model lives in type aliases, not in model classes. That's the fundamental shift: types as first-class citizens of your architecture.

And because the ecosystem is converging around annotated-types, these metadata contracts work across libraries without coordination.
-->
