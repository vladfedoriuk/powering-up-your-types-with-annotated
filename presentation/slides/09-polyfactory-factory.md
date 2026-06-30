---
layout: default
class: code-center
---


# Polyfactory: almost zero config

<div class="divider-red"></div>

<p class="slide-tagline"><code>Ge</code>, <code>Le</code>, <code>Gt</code>, <code>MinLen</code>, <code>MaxLen</code> — resolved automatically.</p>

```python
class ReservationFactory(DataclassFactory[Reservation]):
    __model__ = Reservation

    # PostGenerated: ends_at must follow starts_at
    ends_at = PostGenerated(
        lambda name, values, **kw: values["starts_at"]
        + datetime.timedelta(days=random.randint(1, 14))
    )
    # Timezone(...) bug: polyfactory passes ... as tzinfo
    created_at = Use(
        faker.date_time_between, start_date="-30d", end_date="now", tzinfo=UTC
    )
```

<!--
Polyfactory reads Ge, Le, Gt, MinLen, MaxLen from Annotated automatically. No overrides needed for those fields.

Two manual overrides remain:
1. ends_at — cross-field dependency (must follow starts_at). PostGenerated computes it after starts_at is resolved.
2. created_at — Timezone(...) means "any timezone". Polyfactory bug: passes ellipsis as tzinfo → ParameterException. Workaround: Use() with explicit tzinfo=UTC.

Predicate constraints (lambda-based) are silently skipped — polyfactory can't satisfy arbitrary callables.
-->
