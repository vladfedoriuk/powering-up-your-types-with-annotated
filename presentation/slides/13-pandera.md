---
layout: default
class: code-center
---


# <span class="slide-title-code">Pandera</span>: DataFrame validation

<div class="divider-blue"></div>

<p class="slide-tagline"><code>Annotated[str, pa.Field(...)]</code> — column dtype + checks in one annotation.</p>

```python
import pandera.pandas as pa
from typing import Annotated

class ReservationModel(pa.DataFrameModel):
    room_id: Annotated[str, pa.Field(unique=True)]
    guest_count: Annotated[int, pa.Field(ge=1, le=10)]
    rate: Annotated[float, pa.Field(gt=0)]

ReservationModel.validate(dataframe)
```

<!--
Pandera is a fantastic example of the Python ecosystem embracing typing.Annotated for dataframe validation.

By using Annotated[str, pa.Field(...)] on DataFrameModel columns, you embed dtype and checks — uniqueness, numeric ranges — directly in the type annotation. The dataframe is verified at runtime against this single source of truth.
-->
