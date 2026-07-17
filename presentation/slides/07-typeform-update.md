---
layout: default
class: code-center
---

# <span class="slide-title-code">svcs</span> 26.1.0

<div class="divider-red"></div>

<p class="slide-tagline">Released July 13, 2026. Ships <code>TypeForm</code> support out of the box.</p>

```python
@overload
async def aget(self, svc_type: TypeForm[T1], /) -> T1: ...
```

<!--
On the evening of the second conference day, a friend of mine pointed out that Hynek had released svcs 26.1.0 the day before.

TypeForm now powers both registration and retrieval of services.

Thank you Hynek — for the work on svcs and for making me adjust my slides last minute.
-->
