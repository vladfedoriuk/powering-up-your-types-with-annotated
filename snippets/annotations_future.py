from __future__ import annotations

import annotationlib
import functools
from annotationlib import Format
from decimal import Decimal
from typing import Annotated, get_type_hints

from annotated_types import Gt, MaxLen, MinLen

Name = Annotated[str, MinLen(1), MaxLen(100)]
Price = Annotated[Decimal, Gt(0)]


class Product:
    name: Name
    price: Price


# With `from __future__ import annotations` (PEP 563) all annotations are
# stored as strings in __annotations__ — the expressions are never evaluated.
raw = Product.__annotations__
# {'name': 'Name', 'price': 'Price'}

# Safe access via getattr — identical to raw here, but handles objects that
# may not have __annotations__ (e.g. functools.partial) by returning None.
safe_raw = getattr(Product, "__annotations__", None)
# {'name': 'Name', 'price': 'Price'}  — same result, strings

partial_raw = getattr(functools.partial(lambda x: x, 1), "__annotations__", None)
# None  — functools.partial has no __annotations__ attribute

# get_annotations(Format.VALUE) returns whatever lives in __annotations__
# as-is when it finds plain strings — it does NOT evaluate them.
value_anns = annotationlib.get_annotations(Product, format=Format.VALUE)
# {'name': 'Name', 'price': 'Price'}  ← still strings

# Pass eval_str=True to make get_annotations evaluate the strings.
evaled_anns = annotationlib.get_annotations(Product, format=Format.VALUE, eval_str=True)
# {'name': Annotated[str, MinLen(1), MaxLen(100)], 'price': Annotated[Decimal, Gt(0)]}

# Format.STRING always returns source text — same result here.
string_anns = annotationlib.get_annotations(Product, format=Format.STRING)
# {'name': 'Name', 'price': 'Price'}

# get_type_hints() always evaluates strings via the module globals.
# By default it strips Annotated wrappers.
hints = get_type_hints(Product)
# {'name': str, 'price': Decimal}

# include_extras=True preserves Annotated.
hints_extras = get_type_hints(Product, include_extras=True)
# {'name': Annotated[str, MinLen(1), MaxLen(100)], 'price': Annotated[Decimal, Gt(0)]}

# With `from __future__ import annotations` (PEP 563), Python 3.14 sets
# __annotate__ to None rather than a callable.  This signals that annotations
# are stored as plain strings in __annotations__ and no deferred evaluator
# (PEP 649) was generated.  hasattr() returns True, but the value is None.
annotate_is_none = Product.__annotate__ is None
# True — PEP 563 sets __annotate__ = None; no lazy evaluator exists
