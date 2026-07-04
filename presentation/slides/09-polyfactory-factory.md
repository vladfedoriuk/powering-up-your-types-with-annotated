---
layout: default
class: code-center
---


# Polyfactory: almost zero config

<div class="divider-red"></div>

<p class="slide-tagline"><code>Ge</code>, <code>Le</code>, <code>Gt</code>, <code>MinLen</code>, <code>MaxLen</code> — resolved automatically.</p>

```python {all|4-9|10-13|all}
class ReservationFactory(DataclassFactory[Reservation]):
    __model__ = Reservation

    # PostGenerated: ends_at must follow starts_at
    ends_at = PostGenerated(
        lambda name, values, *args, **kwargs: (
            values["starts_at"] + datetime.timedelta(days=random.randint(1, 14))
        )
    )
    # Timezone(...) bug: polyfactory passes ... as tzinfo
    created_at = Use(
        faker.date_time_between, start_date="-30d", end_date="now", tzinfo=UTC
    )
```

<!--
Now let's generate test data. Polyfactory reads `Ge`, `Le`, `Gt`, `MinLen`, and `MaxLen` straight from the Annotated metadata — no overrides needed for those fields.

[click] Two fields still need help. `ends_at` has a cross-field dependency — it has to land after `starts_at` — so we use `PostGenerated` to compute it once `starts_at` is already resolved.

[click] `created_at` hits an actual polyfactory bug: our `Timezone(...)` constraint means "any timezone is fine," but polyfactory tries to pass that ellipsis straight in as the `tzinfo` argument, which blows up. The workaround is a plain `Use()` with an explicit `UTC`.

[click] Predicate constraints get silently skipped. Polyfactory has no way to guess how to satisfy an arbitrary callable.
-->
