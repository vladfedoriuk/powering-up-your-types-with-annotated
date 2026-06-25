---
layout: default
---

# documentation: `annotated-doc`

<div class="divider-yellow"></div>

- **Self-documenting code**: inline descriptions stored directly in type signatures
- **Tooling integration**: supported by `mkdocstrings` and documentation tools

```python
from annotated_doc import Doc

FIRST_ORDER_DISCOUNT: Annotated[
    Percentage,
    Doc("Discount percentage applied to the first reservation made by a guest"),
] = Decimal(15)
```

<!--
For our final layer, we look at documentation.

annotated-doc introduces the Doc metadata object, which was proposed in the revoked PEP 727. It allows you to document constants, parameters, or fields directly inside their types. Sebastian Ramirez championed this pattern, and it powers Typer and FastAPI's internal documentation rendering.
-->

---
layout: default
class: text-center
---

# thank you!

<div class="flex flex-col items-center justify-center mt-10">
  <QRCode value="https://github.com/vladfedoriuk/powering-up-your-types-with-annotated" :size="200" render-as="svg" />
</div>

<br />

## questions?

<!--
Thank you for attending this talk on typing.Annotated!

We have covered how Annotated breaks the static/runtime barrier, acts as a composable metadata engine, and decouples our domain from SQL databases, API schemas, and documentation tools.

I am open to any questions you may have.
-->
