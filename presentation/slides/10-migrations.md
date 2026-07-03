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
Once the models are defined, generating the migration is the easy part — Alembic scans them and writes it for us. String(20), Numeric(10, 2), DateTime(timezone=True), the index — all of it comes straight from the Annotated aliases.

This is trimmed from the actual generated output in this repo.
-->
