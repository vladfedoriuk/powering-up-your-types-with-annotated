---
layout: default
---


# composition-based design

<div class="divider-red"></div>

<p class="slide-tagline">Type is contract — metadata is instruction manual.</p>

<!--
With typing.Annotated, the type is the contract, and metadata is the instruction manual.

The domain type is defined independently in the center. SQLAlchemy reads the persistence metadata, Pydantic reads validation rules, and other tools read only what they understand. Each layer is completely decoupled, removing design pressure and keeping your architecture clean and maintainable.
-->
