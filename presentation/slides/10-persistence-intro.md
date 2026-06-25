---
layout: default
---


# persistence layer: sqlalchemy

<div class="divider-blue"></div>

<p class="slide-tagline">Layer ORM metadata onto types, not base classes.</p>

<!--
Now we look at the persistence layer using SQLAlchemy.

Rather than polluting our pure domain model by inheriting from a database-specific base model, we use composition. We overlay persistence metadata using typing.Annotated, allowing our models to be mapped to tables while keeping them clean.
-->
