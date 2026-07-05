from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Annotated, Any, get_args, get_origin, get_type_hints

from annotated_types import BaseMetadata, GroupedMetadata


@dataclass(frozen=True)
class Depends[**Params, ReturnType](BaseMetadata):
    dependency: Callable[Params, ReturnType]


class DependencyResolutionError(RuntimeError):
    pass


def get_constraints(hint: Any) -> Iterator[BaseMetadata]:
    for meta in get_args(hint)[1:]:
        if isinstance(meta, BaseMetadata):
            yield meta
        elif isinstance(meta, GroupedMetadata):
            yield from meta  # type: ignore[misc]


def resolve_dependencies[**Params, ReturnType](
    fn: Callable[Params, ReturnType],
) -> dict[str, Any]:
    injected: dict[str, Any] = {}
    for name, hint in get_type_hints(fn, include_extras=True).items():
        if get_origin(hint) is not Annotated:
            continue
        dep = next((m for m in get_constraints(hint) if isinstance(m, Depends)), None)
        if dep is None:
            continue
        try:
            injected[name] = dep.dependency(**resolve_dependencies(dep.dependency))
        except Exception as exc:
            msg = f"Could not resolve dependency for {name!r}"
            raise DependencyResolutionError(msg) from exc
    return injected


def settings() -> str:
    return "prod"


def current_user(env: Annotated[str, Depends(settings)]) -> str:
    return f"ada@{env}"


def handle_request(
    env: Annotated[str, Depends(settings)],
    user: Annotated[str, Depends(current_user)],
) -> str:
    return f"{user} via {env}"


deps = resolve_dependencies(handle_request)
result = handle_request(**deps)
