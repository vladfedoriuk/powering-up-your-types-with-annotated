set dotenv-load := true
set shell := ["bash", "-c"]

[doc("List available recipes")]
default:
    @just --list

[doc("Install all needed dependencies and pre-commit hooks")]
install:
    @just uv-sync
    @just prek-install

[doc("Install all needed dependencies")]
[group("setup")]
uv-sync:
    @uv sync --all-groups

[doc("Install prek hooks")]
[group("pre-commit")]
prek-install:
    @prek install --overwrite --install-hooks

[doc("Run all prek hooks on all files")]
[group("pre-commit")]
prek-run-all-files:
    @prek run --all-files

[doc("Run tests")]
test:
    @uv run pytest

[doc("Serve documentation with mkdocs")]
[group("docs")]
docs:
    @uv run mkdocs serve

[doc("Run zensical")]
[group("docs")]
zensical:
    @uv run zensical

[doc("Upgrade heads")]
[group("alembic")]
upgrade-heads:
    @uv run alembic upgrade heads
