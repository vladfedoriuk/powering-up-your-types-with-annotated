import inspect
import types
from decimal import Decimal
from typing import Annotated, TypeAliasType, get_args, get_origin, get_type_hints

import annotationlib
import pytest
from annotated_types import Ge, Gt, Le, MaxLen, MinLen
from annotationlib import Format, call_evaluate_function

from .annotations_introspection import (
    HasName,
    Name,
    Percentage,
    Price,
    Product,
    _AliasedInner,
    _From3To10,
    _NoOwnAnnotations,
    _annotate_string,
    _annotate_value,
    _flattened,
    _generic_not_flattened,
    _has_name_annotate,
    _has_name_raw,
    _inspect_is_annotationlib,
    _not_flattened,
    _ordered_a,
    _ordered_b,
    _partial_raw,
    _result_via_annotationlib,
    _result_via_inspect,
    _via_call_annotate,
    _with_dup,
    get_constraints,
)


@pytest.mark.parametrize(
    "tp, expected",
    [
        pytest.param(Price, Annotated, id="Price"),
        pytest.param(Name, Annotated, id="Name"),
        pytest.param(Percentage, Annotated, id="Percentage"),
        pytest.param(int, None, id="int"),
        pytest.param(list[int], list, id="list[int]"),
    ],
)
def test_get_origin(tp: type, expected: type | None) -> None:
    assert get_origin(tp) is expected


@pytest.mark.parametrize(
    "tp, expected_origin",
    [
        pytest.param(Name, str, id="Name"),
        pytest.param(Price, Decimal, id="Price"),
        pytest.param(Percentage, Decimal, id="Percentage"),
    ],
)
def test_dunder_origin_is_base_type(tp: type, expected_origin: type) -> None:
    # __origin__ is the unwrapped base type — not the same as get_origin()
    assert tp.__origin__ is expected_origin  # type: ignore[union-attr]


@pytest.mark.parametrize(
    "tp, expected_metadata",
    [
        pytest.param(Name, (MinLen(1), MaxLen(100)), id="Name"),
        pytest.param(Price, (Gt(0),), id="Price"),
        pytest.param(Percentage, (Gt(0), Le(100)), id="Percentage"),
    ],
)
def test_dunder_metadata(tp: type, expected_metadata: tuple) -> None:
    assert tp.__metadata__ == expected_metadata  # type: ignore[union-attr]


def test_metadata_order_matters_for_equality() -> None:
    assert _ordered_a != _ordered_b


def test_metadata_duplicates_preserved() -> None:
    assert _with_dup.__metadata__ == (MinLen(1), MinLen(1))  # type: ignore[union-attr]


def test_nested_annotated_is_flattened() -> None:
    assert _flattened == Annotated[int, MinLen(1), MaxLen(100)]
    assert _flattened.__metadata__ == (MinLen(1), MaxLen(100))  # type: ignore[union-attr]


def test_type_alias_annotated_not_flattened() -> None:
    # PEP 695 TypeAliasType blocks flattening — outer Annotated cannot
    # see inside the alias without evaluating it.
    assert _not_flattened != Annotated[int, MinLen(1), MaxLen(100)]
    assert _not_flattened.__metadata__ == (MaxLen(100),)  # type: ignore[union-attr]

    alias_obj = get_args(_not_flattened)[0]
    assert isinstance(alias_obj, TypeAliasType)
    assert alias_obj is _AliasedInner


def test_generic_type_alias_not_flattened() -> None:
    # Subscripting a generic TypeAliasType produces a types.GenericAlias —
    # flattening is still blocked, only outer metadata is visible.
    assert _generic_not_flattened != Annotated[int, Ge(3), Le(10), MinLen(1)]
    assert _generic_not_flattened.__metadata__ == (MinLen(1),)  # type: ignore[union-attr]

    subscripted = get_args(_generic_not_flattened)[0]
    assert isinstance(subscripted, types.GenericAlias)
    assert get_origin(subscripted) is _From3To10  # the TypeAliasType
    assert get_args(subscripted) == (int,)  # the type argument


@pytest.mark.parametrize(
    "annotated_type, expected_all_metadata",
    [
        pytest.param(
            _not_flattened,
            (MinLen(1), MaxLen(100)),
            id="non-generic-alias",
        ),
        pytest.param(
            _generic_not_flattened,
            (Ge(3), Le(10), MinLen(1)),
            id="generic-alias",
        ),
    ],
)
def test_recover_all_metadata_through_alias(
    annotated_type: object, expected_all_metadata: tuple[object, ...]
) -> None:
    # evaluate_value + call_evaluate_function works identically for both
    # TypeAliasType (non-generic) and types.GenericAlias (subscripted generic).
    # For the generic case T stays unresolved, but metadata is concrete.
    alias_obj, *outer_meta = get_args(annotated_type)
    inner_annotated = call_evaluate_function(
        alias_obj.evaluate_value, Format.VALUE, owner=alias_obj
    )
    all_metadata = inner_annotated.__metadata__ + tuple(outer_meta)
    assert all_metadata == expected_all_metadata


@pytest.mark.parametrize(
    "tp, expected_args",
    [
        pytest.param(Price, (Decimal, Gt(0)), id="Price"),
        pytest.param(Name, (str, MinLen(1), MaxLen(100)), id="Name"),
        pytest.param(Percentage, (Decimal, Gt(0), Le(100)), id="Percentage"),
        pytest.param(int, (), id="int"),
    ],
)
def test_get_args(tp: type, expected_args: tuple[object, ...]) -> None:
    assert get_args(tp) == expected_args


@pytest.mark.parametrize(
    "tp, expected_constraints",
    [
        pytest.param(Price, [Gt(0)], id="Price"),
        pytest.param(Name, [MinLen(1), MaxLen(100)], id="Name"),
        pytest.param(Percentage, [Gt(0), Le(100)], id="Percentage"),
    ],
)
def test_get_constraints(tp: type, expected_constraints: list[object]) -> None:
    assert list(get_constraints(tp)) == expected_constraints


@pytest.mark.parametrize(
    "cls, include_extras, expected",
    [
        pytest.param(
            Product,
            False,
            {"name": str, "price": Decimal, "discount": Decimal | None},
            id="Product-stripped",
        ),
        pytest.param(
            Product,
            True,
            {"name": Name, "price": Price, "discount": Percentage | None},
            id="Product-extras",
        ),
        pytest.param(
            HasName,
            True,
            {"name": Name},
            id="HasName-own-only",
        ),
    ],
)
def test_get_type_hints(
    cls: type, include_extras: bool, expected: dict[str, object]
) -> None:
    assert get_type_hints(cls, include_extras=include_extras) == expected


def test_get_type_hints_merges_mro() -> None:
    # Product inherits name from HasName; get_type_hints traverses the full MRO.
    assert set(get_type_hints(Product)) == {"name", "price", "discount"}


@pytest.mark.parametrize(
    "cls, fmt, expected",
    [
        pytest.param(HasName, Format.VALUE, {"name": Name}, id="HasName-VALUE"),
        pytest.param(HasName, Format.STRING, {"name": "Name"}, id="HasName-STRING"),
        pytest.param(
            Product,
            Format.VALUE,
            {"price": Price, "discount": Percentage | None},
            id="Product-VALUE",
        ),
        pytest.param(
            Product,
            Format.STRING,
            {"price": "Price", "discount": "Percentage | None"},
            id="Product-STRING",
        ),
    ],
)
def test_get_annotations_formats(
    cls: type, fmt: Format, expected: dict[str, object]
) -> None:
    assert annotationlib.get_annotations(cls, format=fmt) == expected


def test_get_annotations_own_only() -> None:
    # get_annotations does NOT traverse MRO — own annotations only.
    assert set(annotationlib.get_annotations(Product, format=Format.VALUE)) == {
        "price",
        "discount",
    }


def test_get_annotations_forwardref() -> None:
    # ForwardRef proxies are produced by the compiler-generated __annotate__
    # when the referenced name is not yet defined at introspection time.
    # Python 3.14 deferred evaluation means the name isn't looked up at class
    # definition — only when get_annotations actually calls __annotate__.
    class Early:
        sibling: Pending  # type: ignore[name-defined]  # noqa: F821

    # Pending is not defined yet → FORWARDREF returns a proxy, VALUE raises.
    forwardref_anns = annotationlib.get_annotations(Early, format=Format.FORWARDREF)
    assert isinstance(forwardref_anns["sibling"], annotationlib.ForwardRef)

    with pytest.raises(NameError):
        annotationlib.get_annotations(Early, format=Format.VALUE)

    class Pending:  # noqa: F811
        pass

    # Now that Pending exists in scope, VALUE resolves it.
    value_anns_local = annotationlib.get_annotations(Early, format=Format.VALUE)
    assert value_anns_local["sibling"] is Pending


def test_annotate_is_callable() -> None:
    assert callable(_has_name_annotate)


@pytest.mark.parametrize(
    "result, expected",
    [
        pytest.param(_annotate_value, {"name": Name}, id="VALUE-direct"),
        pytest.param(
            _annotate_string, {"name": "Name"}, id="STRING-via-call_annotate_function"
        ),
        pytest.param(
            _via_call_annotate,
            {"name": Name},
            id="FORWARDREF-via-call_annotate_function",
        ),
    ],
)
def test_annotate_formats(
    result: dict[str, object], expected: dict[str, object]
) -> None:
    assert result == expected


def test_annotate_non_value_raises_directly() -> None:
    # Compiler-generated __annotate__ only supports Format.VALUE natively.
    # STRING and FORWARDREF require call_annotate_function to work.
    with pytest.raises(NotImplementedError):
        HasName.__annotate__(Format.STRING)


def test_annotate_matches_get_annotations() -> None:
    assert HasName.__annotate__(Format.VALUE) == annotationlib.get_annotations(
        HasName, format=Format.VALUE
    )


@pytest.mark.parametrize(
    "obj, expected",
    [
        pytest.param(HasName, {"name": Name}, id="class-with-annotations"),
        pytest.param(_NoOwnAnnotations, {}, id="class-no-own-annotations"),
        pytest.param(_partial_raw, None, id="partial-no-dunder"),
    ],
)
def test_getattr_annotations(obj: object, expected: dict[str, object] | None) -> None:
    assert getattr(obj, "__annotations__", None) == expected


def test_getattr_returns_actual_objects_without_future() -> None:
    # Without `from __future__ import annotations` (Python 3.14 deferred eval),
    # __annotations__ contains evaluated Python objects, not strings.
    assert _has_name_raw == {"name": Name}
    assert _has_name_raw is not None
    assert get_origin(_has_name_raw["name"]) is Annotated


def test_inspect_get_annotations_is_annotationlib_in_314() -> None:
    # Python 3.14: inspect.get_annotations is a literal alias — same object.
    assert _inspect_is_annotationlib


def test_inspect_and_annotationlib_return_identical_results() -> None:
    assert _result_via_inspect == _result_via_annotationlib


def test_inspect_get_annotations_accepts_format_in_314() -> None:
    # In 3.10–3.13, inspect.get_annotations had NO format parameter.
    # In 3.14 it does because it *is* annotationlib.get_annotations.
    result = inspect.get_annotations(HasName, format=Format.STRING)
    assert result == {"name": "Name"}


def test_getattr_inherited_class_returns_empty() -> None:
    # Python 3.10+ guarantees own-only: a subclass that adds no annotations
    # returns {} rather than its parent's dict.
    assert _has_name_raw is not getattr(_NoOwnAnnotations, "__annotations__", None)
    assert getattr(_NoOwnAnnotations, "__annotations__", None) == {}
