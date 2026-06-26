---
layout: default
---


# Three ways to do the same thing

<div class="divider-red"></div>

<p class="slide-tagline">Different tradeoffs, same goal.</p>

- Django/DRF — one model rules everything
- SQLModel — one class, ORM + schema
- `Annotated` — each layer reads what it needs

<!--
Quick comparison before the code. Not "X is bad" — just different coupling strategies. Django and SQLModel trade flexibility for convenience. Annotated keeps layers independent.
-->
