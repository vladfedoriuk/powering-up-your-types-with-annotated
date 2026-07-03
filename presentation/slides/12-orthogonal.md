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
One RoomId, three concerns stacked in the same alias — SQLAlchemy, Pydantic, and FastAPI each hook into the piece they understand and skip the rest.

[click] The type stays central — stack as many concerns as you need, and neither the database nor the API gets the final say.

[click] Types stop being just annotations for the type checker — they become central to your data model, defining what the data actually is.

[click] And when the ecosystem agrees on shared standards like annotated-types, that composition goes even further — these contracts work across libraries without anyone coordinating.
-->
