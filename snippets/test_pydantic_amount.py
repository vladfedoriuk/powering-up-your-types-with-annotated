from decimal import Decimal
from typing import Annotated

from annotated_types import Gt
from pydantic import PlainSerializer, TypeAdapter, WrapValidator

Amount = Annotated[
    Decimal,
    Gt(0),
    WrapValidator(lambda v, handler: handler(v).quantize(Decimal("0.01"))),
    PlainSerializer(lambda v: float(v), return_type=float, when_used="always"),
]

ta = TypeAdapter(Amount)


def test_validate_rounding() -> None:
    assert ta.validate_python(Decimal("10.123")) == Decimal("10.12")


def test_validate_string_input() -> None:
    assert ta.validate_python("10.456") == Decimal("10.46")


def test_validate_negative_rejected() -> None:
    from pydantic import ValidationError

    import pytest

    with pytest.raises(ValidationError):
        ta.validate_python(Decimal("-1"))


def test_serialize_to_float() -> None:
    assert ta.dump_python(Decimal("10.12")) == 10.12


def test_json_serialization() -> None:
    assert ta.dump_json(Decimal("10.12")) == b"10.12"
