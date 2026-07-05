from typing import Annotated

import pytest

from .dependency_injection import (
    Depends,
    DependencyResolutionError,
    resolve_dependencies,
)


def test_resolves_annotated_dependencies() -> None:
    def token() -> str:
        return "abc"

    def user_id() -> int:
        return 42

    def endpoint(
        token_: Annotated[str, Depends(token)],
        user_id_: Annotated[int, Depends(user_id)],
    ) -> tuple[str, int]:
        return token_, user_id_

    deps = resolve_dependencies(endpoint)
    assert deps == {"token_": "abc", "user_id_": 42}
    assert endpoint(**deps) == ("abc", 42)


def test_resolves_nested_dependencies() -> None:
    def config_path() -> str:
        return "db.config"

    def db_url(path: Annotated[str, Depends(config_path)]) -> str:
        return f"sqlite:///{path}"

    def endpoint(url: Annotated[str, Depends(db_url)]) -> str:
        return url

    deps = resolve_dependencies(endpoint)
    assert deps == {"url": "sqlite:///db.config"}
    assert endpoint(**deps) == "sqlite:///db.config"


def test_ignores_plain_annotations() -> None:
    def token() -> str:
        return "abc"

    def endpoint(
        query: str,
        token_: Annotated[str, Depends(token)],
    ) -> tuple[str, str]:
        return query, token_

    deps = resolve_dependencies(endpoint)
    assert deps == {"token_": "abc"}


def test_wraps_dependency_errors_with_parameter_name() -> None:
    def broken() -> str:
        raise ValueError("boom")

    def endpoint(token_: Annotated[str, Depends(broken)]) -> str:
        return token_

    with pytest.raises(DependencyResolutionError, match="'token_'") as exc_info:
        resolve_dependencies(endpoint)

    assert isinstance(exc_info.value.__cause__, ValueError)
