---
layout: default
class: code-center
---


# polyfactory: test data

<div class="divider-red"></div>

<p class="slide-tagline">Factories read constraints from types — zero config.</p>

```python
from polyfactory.factories.dataclasses import DataclassFactory

class ReservationFactory(DataclassFactory[Reservation]):
    __model__ = Reservation

mock_res = ReservationFactory.build()
```

<!--
For automated testing, polyfactory reads the Annotated constraints.

Since the constraints are part of the type signature, the ReservationFactory can automatically generate mock reservations that comply with the GuestCount limit and RoomRate constraints without requiring any manual configuration.
-->
