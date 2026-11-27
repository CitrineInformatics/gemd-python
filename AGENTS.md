# AGENTS.md

`gemd-python` is the Python binding for GEMD, the Citrine data model for materials, processes, and measurements. Users install it from PyPI as `gemd`. The `citrine` SDK in `citrine-python` depends on `gemd>=3,<4`, so a change here that breaks the API also breaks that SDK.

## Layout

| Path | Contents |
|------|----------|
| `gemd/entity/object/` | Specs and runs for materials, processes, ingredients, and measurements |
| `gemd/entity/template/` | Templates for objects and attributes |
| `gemd/entity/attribute/`, `bounds/`, `value/` | Attributes, their bounds, and their values |
| `gemd/entity/dict_serializable.py`, `link_by_uid.py` | Base serialization and links between objects by UID |
| `gemd/json/` | `GEMDJson` and the JSON encoder |
| `gemd/units/` | Unit parsing on top of `pint`, with Citrine unit definitions in `citrine_en.txt` and `constants_en.txt` |
| `gemd/builders/`, `gemd/util/` | Helpers that build and traverse object graphs |
| `gemd/demo/` | Example data and builders. Coverage omits this directory |
| `gemd/__version__.py` | Package version, read by setuptools |
| `tests/` | Unit tests, which mirror `gemd/` |
| `docs/source/` | Sphinx source in `.rst` |

## Commands

The repo uses uv, and `uv.lock` pins every dependency. See "Testing" in `CONTRIBUTING.md` for the full list of gates.

| Task | Command |
|------|---------|
| Install | `uv sync --dev` |
| Lint | `uv run ruff check gemd tests` |
| Format check | `uv run ruff format --check gemd tests` |
| Tests with coverage | `uv run pytest --cov=gemd --cov-report term-missing:skip-covered --cov-fail-under=100 tests/` |
| Lockfile check | `uv lock --check` |
| Docs | `uv run --group docs make -C docs/ html SPHINXOPTS='-W --keep-going'` |

## CI gates

Pull requests into `main` and `release/**` run `.github/workflows/pr-checks.yml` and `pr-tests.yml`. Both call the `@v3` shared workflows in `CitrineInformatics/common-gh-actions`. To pass, a PR needs:

1. Clean `ruff check` and `ruff format --check` runs on `gemd`, with the ruff version that `uv.lock` pins.
2. A higher version in `gemd/__version__.py` than `main` has. This check applies to PRs into `main`.
3. No deprecated code at or past its `removed_in` version.
4. A `uv.lock` in sync with `pyproject.toml`.
5. A docs build free of Sphinx warnings.
6. Passing tests at 100% line coverage on Ubuntu, with the dependency versions in `uv.lock`.

CI also runs the tests on Python 3.10 through 3.14 on Linux, macOS, and Windows. One matrix uses the lowest direct dependency versions, and another uses the latest. Publishing a GitHub release deploys to PyPI and GitHub Pages.

## Conventions

- Style is PEP 8 with a 99-character code limit and a 119-character docstring limit. `pyproject.toml` holds the ruff config, including pydocstyle and isort rules.
- Write Numpy-style docstrings. Sphinx autogenerates `docs/source/reference/`, which git ignores.
- Make arguments keyword-only. Every positional argument must be required.
- Run `uv lock` after you change dependencies in `pyproject.toml`, and commit `uv.lock`.
- Before you remove a field, module, or exported name from the public API, follow "Removing a capability from the public API" in `CONTRIBUTING.md`.
- Python 3.10 is the floor, set by `requires-python` and the ruff `target-version`.
- List new data files under `[tool.setuptools.package-data]` in `pyproject.toml`, so the wheel includes them.

## Further reading

- `CONTRIBUTING.md`: checks, style, removing a capability, branching, and the release process
- `gemd/demo/README.md`: the example builders
- GEMD data model docs: https://citrineinformatics.github.io/gemd-docs/
- Package docs: https://citrineinformatics.github.io/gemd-python/
