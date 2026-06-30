---
layout: default
---


# Generating migrations

<div class="divider-blue"></div>

<p class="slide-tagline">Alembic reads the models — you write nothing.</p>

```bash
alembic revision --autogenerate -m "Initial migrations"
alembic upgrade heads
```

```python
op.create_table(
    "rooms",
    sa.Column("id", sa.Integer(), sa.Identity(), nullable=False),
    sa.Column("room_id", sa.String(20), nullable=False),
    sa.Column("capacity", sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint("id"),
)
op.create_index("ix_rooms_room_id", "rooms", ["room_id"], unique=True)
# ...
```

<!--
Alembic scans the SQLAlchemy models and writes the migration. String(20), Numeric(10, 2), DateTime(timezone=True), the index — all come from the Annotated aliases. Nothing to repeat.

This is trimmed from the actual generated output in this repo.
-->
