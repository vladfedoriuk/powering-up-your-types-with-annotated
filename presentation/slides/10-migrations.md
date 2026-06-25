---
layout: default
class: code-center
---


# generating migrations

<div class="divider-blue"></div>

<p class="slide-tagline">Alembic autogenerate from <code>Annotated</code> models.</p>

```bash
alembic revision --autogenerate -m "Initial migrations"
alembic upgrade heads
```

<!--
Once our SQLAlchemy models are declared, Alembic scans the registry metadata and autogenerates migration scripts.

The DB columns are derived directly from the Annotated types, showing that our persistence schemas adapt to our domain models instead of dictating them.
-->
