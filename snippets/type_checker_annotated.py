from typing import Annotated, NewType

# ---------------------------------------------------------------------------
# Runtime evidence — Annotated is not a concrete class
#
# `Annotated` is a typing special form: an object with special meaning to the
# type system, comparable to syntax rather than a normal runtime class.
#
# References:
# - Typing glossary: https://typing.python.org/en/latest/spec/glossary.html#term-special-form
# - Annotated spec: https://typing.python.org/en/latest/spec/qualifiers.html#annotated
#
# The important consequence for libraries:
#
#     Annotated[int, "x"] is a valid type expression,
#     but it is not a `type[int]`.
#
# At runtime Python represents it as a private typing alias object, not as a
# subclass of `type`.

_annotated_type = Annotated[int, "x"]
print(type(_annotated_type))
# <class 'typing._AnnotatedAlias'>

print(isinstance(_annotated_type, type))
# False


# ---------------------------------------------------------------------------
# The failing library signature — `type[T]`
#
# This models APIs such as `svcs.Registry.register_value`, which originally
# accepted service keys as `svc_type: type[T]`.
#
# That works for real classes (`int`, `str`, user classes), but it rejects
# `Annotated[...]` because type checkers are required to treat `Annotated` as
# a special form, not as an instance of `type`.
#
# Real-world discussion:
# - svcs #74: https://github.com/hynek/svcs/discussions/74
# - typing-council #18: https://github.com/python/typing-council/issues/18
# - Pyright #7238: https://github.com/microsoft/pyright/issues/7238


def test_type_match[T](tp: type[T], value: T) -> None: ...


test_type_match(int, 42)
test_type_match(Annotated[int, "x"], 42)  # type: ignore[arg-type]
# > zuban check
# error: Argument 1 to "test_type_match" has incompatible type "_SpecialForm"; expected "type[Never]"  [arg-type]
# > ty check
# error: Expected `<class 'int'>`, found `<special-form 'typing.Annotated[int, <metadata>]'>`
# > pyrefly check
# Argument `Annotated[int]` is not assignable to parameter `tp` with type `type[@_]` in function `test_type_match` [bad-argument-type]
# > pyright check
# [tool.pyright]
# enableExperimentalFeatures = true
# Argument of type "Annotated" cannot be assigned to parameter "tp" of type "type[T@test_type_match]" in function "test_type_match"
# > mypy --enable-incomplete-feature=TypeForm
# Argument 1 to "test_type_match" has incompatible type "<typing special form>"; expected "type[int]"  [arg-type]

# ---------------------------------------------------------------------------
# The correct signature — `TypeForm[T]`
#
# PEP 747 introduces `TypeForm[T]` for APIs that accept type-form objects:
# classes, unions, parameterized generics, `Annotated[...]`, and other objects
# that can appear in type expressions at runtime.
#
# In other words:
#
#     type[T]      → concrete classes only
#     TypeForm[T]  → any valid type form whose value type is T
#
# References:
# - PEP 747: https://peps.python.org/pep-0747/
# - TypeForm spec: https://typing.python.org/en/latest/spec/type-forms.html
# - Python 3.15 docs: https://docs.python.org/3.15/library/typing.html#typing.TypeForm

from typing_extensions import TypeForm  # noqa: E402


def test_type_form[T](tp: TypeForm[T], value: T) -> None: ...


test_type_form(int, 42)
test_type_form(Annotated[int, "x"], 42)
# > zuban check
# OK
# > ty check
# OK
# > pyrefly check
# OK
# > pyright check
# [tool.pyright]
# enableExperimentalFeatures = true
# OK
# mypy --enable-incomplete-feature=TypeForm
# OK

# ---------------------------------------------------------------------------
# NewType also passes TypeForm
#
# `NewType` creates a distinct type at the type-checker level, but at runtime
# it is still a callable that returns its argument — not a `type` subclass.
# `TypeForm` accepts it because `NewType(...)` is a valid type expression.

UserId = NewType("UserId", int)

test_type_form(UserId, 42)
test_type_form(Annotated[UserId, "x"], 42)
# > mypy --enable-incomplete-feature=TypeForm
# OK
# > pyright
# [tool.pyright]
# enableExperimentalFeatures = true
# OK
