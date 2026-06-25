---
layout: default
---

<div class="flex flex-col justify-center h-full">
  <div class="flex items-start gap-8">
    <div class="flex-1">
      <div class="cover-title">powering up your types<br/>with <mark>annotated</mark></div>
      <div class="cover-subtitle">typing.Annotated · python 3.9+ · PEP 593</div>
      <div class="cover-author">Vlad Fedoriuk</div>
    </div>
    <div class="flex flex-col items-center gap-3 mt-4">
      <div class="marker-circle" style="width:2.5rem;height:2.5rem;"></div>
      <div class="marker-square" style="width:2.5rem;height:2.5rem;"></div>
      <div class="marker-triangle" style="border-left-width:1.3rem;border-right-width:1.3rem;border-bottom-width:2.5rem;"></div>
    </div>
  </div>
</div>

<!--
Welcome everyone. Today we're going to explore typing.Annotated — arguably the most powerful and underappreciated feature in Python's modern type system.

Annotated landed in Python 3.9 as PEP 593, and it fundamentally changes what types can do. It breaks the boundary between static analysis — what your type checker sees — and runtime behavior — what your code actually does at execution time.

We'll start with two practical use cases, then go deep into the internals, explore how the ecosystem builds on top of it, and look at real-world patterns including dependency injection — all powered by this single typing construct.
-->
