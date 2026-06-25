---
layout: default
class: code-center
---


# pandera: dataframe validation

<div class="divider-blue"></div>

<p class="slide-tagline"><code>Series[T]</code> + <code>pa.Field</code> for tabular constraints.</p>

```python
import pandera as pa
from pandera.typing import Series

class ReservationModel(pa.DataFrameModel):
    room_id: Annotated[Series[str], pa.Field(unique=True)]
    guest_count: Annotated[Series[int], pa.Field(ge=1, le=10)]
    rate: Annotated[Series[float], pa.Field(gt=0)]

ReservationModel.validate(dataframe)
```

<!--
Pandera is a fantastic example of the Python ecosystem embracing typing.Annotated for dataframe validation.

By using Series[T] wrapped in Annotated with pa.Field metadata, you define high-level constraints like column uniqueness, numeric ranges, and metadata descriptions. The dataframe is verified at runtime against this single source of truth.
-->
