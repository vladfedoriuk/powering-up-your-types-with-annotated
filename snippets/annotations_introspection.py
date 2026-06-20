import functools
import inspect
from collections.abc import Iterator
from decimal import Decimal
from typing import Annotated, get_args, get_origin

import annotated_types
import annotationlib
from annotated_types import Ge, Gt, Le, MaxLen, MinLen
from annotationlib import Format

Name = Annotated[str, MinLen(1), MaxLen(100)]
Price = Annotated[Decimal, Gt(0)]
Percentage = Annotated[Decimal, Gt(0), Le(100)]

Constraint = annotated_types.BaseMetadata | annotated_types.GroupedMetadata | slice

# ---------------------------------------------------------------------------
# __origin__ and __metadata__ — direct attribute access on Annotated objects
#
# Every Annotated type exposes two dunder attributes:
#   __origin__   — the unwrapped base type (str, Decimal, …)
#   __metadata__ — tuple of all metadata arguments, preserving order
#
# Do NOT confuse __origin__ with get_origin():
#   get_origin(Name)   → Annotated      ← the generic alias itself
#   Name.__origin__    → str            ← the first argument to Annotated

_name_origin = Name.__origin__  # str
_name_metadata = Name.__metadata__  # (MinLen(1), MaxLen(100))

_price_origin = Price.__origin__  # Decimal
_price_metadata = Price.__metadata__  # (Gt(0),)

# Metadata order matters — these are distinct types:
_ordered_a = Annotated[int, MinLen(1), MaxLen(100)]
_ordered_b = Annotated[int, MaxLen(100), MinLen(1)]
# _ordered_a != _ordered_b

# Duplicated metadata is preserved, never deduplicated:
_with_dup = Annotated[int, MinLen(1), MinLen(1)]
# _with_dup.__metadata__ == (MinLen(1), MinLen(1))

# ---------------------------------------------------------------------------
# Flattening — nested Annotated types are flattened, innermost metadata first
#
# Annotated[Annotated[int, MinLen(1)], MaxLen(100)]
#   == Annotated[int, MinLen(1), MaxLen(100)]
#
# EXCEPTION: flattening does NOT happen when the inner Annotated is reached
# through a TypeAliasType (PEP 695 `type` statement).  The compiler avoids
# forcing evaluation of lazy aliases, so the outer Annotated sees only one
# argument (the alias object) and cannot introspect inside it.

_inner = Annotated[int, MinLen(1)]
_flattened = Annotated[_inner, MaxLen(100)]
# _flattened == Annotated[int, MinLen(1), MaxLen(100)]
# _flattened.__metadata__ == (MinLen(1), MaxLen(100))

type _AliasedInner = Annotated[int, MinLen(1)]  # PEP 695 TypeAliasType
_not_flattened = Annotated[_AliasedInner, MaxLen(100)]
# _not_flattened != Annotated[int, MinLen(1), MaxLen(100)]
# _not_flattened.__metadata__ == (MaxLen(100),)  ← only outer metadata visible

# Generic TypeAliasType — same non-flattening rule applies regardless of
# whether the alias is parameterized.  Subscripting (_From3To10[int]) produces
# a new object that is still treated as an opaque argument by Annotated.
type _From3To10[T] = Annotated[T, Ge(3), Le(10)]
_generic_not_flattened = Annotated[_From3To10[int], MinLen(1)]
# _generic_not_flattened != Annotated[int, Ge(3), Le(10), MinLen(1)]
# _generic_not_flattened.__metadata__ == (MinLen(1),)  ← only outer metadata


class HasName:
    name: Name


class Product(HasName):
    price: Price
    discount: Percentage | None


# Annotation introspection API — evolution across Python versions
#
#  Python ≤ 3.9   getattr(o, '__annotations__', None)
#                   Raw access; class inheritance bug (parent dict returned
#                   for unannotated subclass) fixed only in 3.10.
#                   For classes, use o.__dict__.get('__annotations__', None).
#
#  Python 3.10–3.13  inspect.get_annotations(o, *, globals, locals, eval_str)
#                   First safe, cross-version API. Returns own annotations only,
#                   never inherits parent dict. No format parameter.
#
#  Python 3.14+   annotationlib.get_annotations(o, *, format, eval_str, ...)
#                   Supersedes inspect version. Adds Format enum
#                   (VALUE / FORWARDREF / STRING). inspect.get_annotations
#                   becomes a literal alias pointing to this function.
#
#  All versions   typing.get_type_hints(o, include_extras, ...)
#                   Higher-level: evaluates strings, merges MRO, strips
#                   Annotated by default.  Not a direct replacement for
#                   get_annotations — different contract.

# In Python 3.14, inspect.get_annotations IS annotationlib.get_annotations
_inspect_is_annotationlib = inspect.get_annotations is annotationlib.get_annotations

# Both return identical results (same function in 3.14+)
_result_via_inspect = inspect.get_annotations(HasName)
_result_via_annotationlib = annotationlib.get_annotations(HasName, format=Format.VALUE)

# inspect.get_annotations in 3.10–3.13 had NO format parameter.
# In 3.14 it accepts format= because it is the annotationlib version.

# ---------------------------------------------------------------------------
# getattr(o, '__annotations__', None) — the safe low-level access pattern
#
# Preferred for unknown callables that may not have __annotations__ at all
# (e.g. functools.partial).  For functions / classes / modules prefer
# annotationlib.get_annotations() which handles edge-cases automatically.
#
# Without `from __future__ import annotations` (Python 3.14 default, PEP 649),
# __annotations__ is lazily evaluated and contains actual Python objects.
# With `from __future__ import annotations` (PEP 563) it contains raw strings.

# Class with own annotations → dict of actual objects (Python 3.14+)
_has_name_raw = getattr(HasName, "__annotations__", None)
# {'name': Annotated[str, MinLen(1), MaxLen(100)]}


# Class that inherits but declares nothing itself → empty dict (own-only, Python 3.10+)
class _NoOwnAnnotations(HasName):
    pass


_inherited_raw = getattr(_NoOwnAnnotations, "__annotations__", None)
# {}  — parent annotations NOT included (guaranteed since Python 3.10)

# functools.partial doesn't have __annotations__ → None
_partial = functools.partial(lambda x: x, 1)
_partial_raw = getattr(_partial, "__annotations__", None)
# None

# __annotate__ — the deferred-evaluation callable (Python 3.14+, PEP 649)
#
# The compiler attaches __annotate__ to every class / function / module that
# carries annotations when using Python 3.14's default evaluation semantics.
# It is a callable that accepts one positional argument — a Format member —
# and returns the annotations dict in the requested format.
#
# annotationlib.get_annotations() calls __annotate__ internally.
# Prefer call_annotate_function() over calling __annotate__ directly; it
# handles fallback logic when a format is not natively supported.
#
# NOT present when `from __future__ import annotations` is active (PEP 563):
# in that case the compiler stores plain strings in __annotations__ and
# never generates an __annotate__ function.

_has_name_annotate = HasName.__annotate__
# <function HasName.__annotate__ at 0x...>

# Compiler-generated __annotate__ functions only support Format.VALUE natively.
# Calling them directly with STRING or FORWARDREF raises NotImplementedError.
_annotate_value = HasName.__annotate__(Format.VALUE)
# {'name': Annotated[str, MinLen(1), MaxLen(100)]}

# For STRING / FORWARDREF use call_annotate_function — it handles the fallback:
# if the format is not natively supported, it re-runs __annotate__ in a special
# fake-globals environment that intercepts name lookups to produce strings or
# ForwardRef proxies.
_annotate_string = annotationlib.call_annotate_function(
    HasName.__annotate__, Format.STRING, owner=HasName
)
# {'name': 'Name'}

_via_call_annotate = annotationlib.call_annotate_function(
    HasName.__annotate__, Format.FORWARDREF, owner=HasName
)
# {'name': Annotated[str, MinLen(1), MaxLen(100)]}  (resolved immediately here)


def get_constraints(tp: type) -> Iterator[Constraint]:
    """Yield BaseMetadata / GroupedMetadata constraints from an Annotated type."""
    origin = get_origin(tp)
    assert origin is Annotated, (
        f"Expected Annotated type, got {tp!r} (origin: {origin!r})"
    )
    args = iter(get_args(tp))
    next(args)
    for arg in args:
        if isinstance(arg, annotated_types.BaseMetadata):
            yield arg
        elif isinstance(arg, annotated_types.GroupedMetadata):
            yield from arg  # type: ignore[misc]
        elif isinstance(arg, slice):
            yield from annotated_types.Len(arg.start or 0, arg.stop)
