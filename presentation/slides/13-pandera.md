---
layout: default
---

# pandera: dataframe validation

<div class="divider-blue"></div>

## tabular data metadata

- **Tabular type safety**: validate DataFrame columns and types at runtime
- **Single source of truth**: embed column ranges, unique checks, and descriptions

```python
import pandera as pa
from pandera.typing import Series

class ReservationModel(pa.DataFrameModel):
    room_id: Annotated[Series[str], pa.Field(unique=True)]
    guest_count: Annotated[Series[int], pa.Field(ge=1, le=10)]
    rate: Annotated[Series[float], pa.Field(gt=0)]

# Validates column types, unique constraints, and min/max ranges
ReservationModel.validate(dataframe)
```

<!--
Pandera is a fantastic example of the Python ecosystem embracing typing.Annotated for dataframe validation.

By using Series[T] wrapped in Annotated with pa.Field metadata, you define high-level constraints like column uniqueness, numeric ranges, and metadata descriptions. The dataframe is verified at runtime against this single source of truth.
-->
