from typing import Annotated

_annotated_type = Annotated[int, "x"]
print(type(_annotated_type))
# <class 'typing._AnnotatedAlias'>

print(isinstance(_annotated_type, type))
# False


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
