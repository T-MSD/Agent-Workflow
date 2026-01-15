# AGENTS.md – Agent Workflow Guidelines

This file documents how agentic coding assistants should work in this repository. It complements any local CONTRIBUTING/README files and applies repo‑wide unless a more specific AGENTS.md is present in a subdirectory.

**Quick Start**
- Use `python3.11+` and create an isolated environment: `python -m venv .venv` then `source .venv/bin/activate` (Unix) or `.\.venv\Scripts\activate` (Windows).
- Install runtime dependencies: `pip install -r requirements.txt`.
- Install development dependencies (if present): `pip install -r dev-requirements.txt` or `pip install -U black isort flake8 mypy pytest`.
- Run the app (local dev): `python main.py` (agents in `agents/`, utilities in `src/`).

**Build / Lint / Test Commands**
- Install deps: `pip install -r requirements.txt`.
- Run all tests: `pytest -q` or `pytest -q tests/`.
- Run a single test file: `pytest -q path/to/test_file.py`.
- Run a single test case or method: `pytest -q path/to/test_file.py::TestClass::test_name`.
- Run tests with verbose output and capture: `pytest -v --maxfail=1`.
- Run tests with coverage: `coverage run -m pytest && coverage report -m`.
- Run only tests marked with a marker: `pytest -q -m marker_name` (use `@pytest.mark.marker_name`).
- Lint (style): `flake8 .`.
- Format code: `black .` (project uses 88 char line length by default).
- Sort/normalize imports: `isort .`.
- Type checking: `mypy .` (adjust strictness per-module via `mypy.ini` or `pyproject.toml`).
- Optional static checks: `pylint src/` (if configured).

**Running a Single Test (cheat sheet)**
- Test function: `pytest -q tests/test_utils.py::test_helper`.
- Test method inside class: `pytest -q tests/test_models.py::TestModel::test_save`.
- Test pattern: `pytest -q -k "substring_of_test_name"`.
- Debug a test: `pytest -q tests/test_x.py -k test_name -s` or use `pytest --pdb`.

**Formatting & Imports**
- Use `black` for formatting; run `black .` before commits.
- Keep imports grouped and ordered: standard library, third‑party, local application imports. Use `isort .` to enforce this.
- Prefer absolute imports over relative imports for application modules (easier to refactor and search).
- Avoid wildcard imports (`from module import *`).
- Use `from typing import TYPE_CHECKING` when needed to avoid runtime import cycles in type hints.

**Typing**
- Add type hints to public functions and methods. Use `typing` types (`list[int]`, `dict[str, Any]`, `Optional[...]`).
- Use `mypy` to check types. Configure `mypy.ini` or `pyproject.toml` for per-module strictness.
- For complex return types, prefer `TypedDict`, `Protocol`, `NamedTuple`, or small dataclasses over generic `dict`/`tuple` where helpful.
- Avoid `Any` in new code unless necessary; document why `Any` is used with a comment.

**Naming Conventions**
- Files and modules: `snake_case.py`.
- Functions and variables: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_CASE_WITH_UNDERSCORES`.
- Private module members: prefix with single underscore (e.g., `_helper`).
- Test functions: `test_<behavior>` and test classes named `Test<ClassOrModule>`.

**Docstrings & Comments**
- Use Google‑style or reST docstrings. Include a short description, parameters, returns, and raises.
- For public API functions and classes, always provide a docstring.
- Keep comments meaningful; avoid noisy comments that restate the code. Document intent and non-obvious decisions.

**Error Handling & Exceptions**
- Prefer explicit exceptions: define custom exception classes in `src/exceptions.py` (or appropriate module) when the error is part of domain logic.
- Avoid bare `except:`. Catch specific exceptions (e.g., `except ValueError:`) or `except Exception as exc:` when re-raising or wrapping.
- When catching and re-raising, preserve the original exception context using `raise NewError(...) from exc`.
- Fail fast for invalid inputs: validate arguments and raise `ValueError` / `TypeError` as appropriate.
- Use context managers (`with`) for resource management to ensure deterministic cleanup.

**Logging**
- Use the `logging` module for all runtime logs. Avoid `print()` in library code.
- Configure logging in application entrypoint (e.g., `main.py`) and keep libraries quiet by using `logger = logging.getLogger(__name__)`.
- Use structured, informative messages. Avoid logging sensitive information (secrets, tokens).
- Log at the appropriate level: `DEBUG` for development traces, `INFO` for routine events, `WARNING` for recoverable issues, `ERROR` for failures, `CRITICAL` for unrecoverable problems.

**I/O, Paths & Filesystem**
- Use `pathlib.Path` for path manipulation and avoid hardcoding OS path separators.
- For file reads/writes, open files using `with` to ensure proper closure.
- Keep test fixtures that create files in temporary directories (use `tmp_path`/`tmp_path_factory` from pytest).
- Avoid writing to absolute system paths; prefer configurable directories via environment variables or CLI flags.

**Configuration & Secrets**
- Prefer environment variables (`os.environ`) for configuration. Use a `.env` loader (e.g., python-dotenv) only in local dev; do not commit `.env` files with secrets.
- Follow 12‑factor app principles for config: keep config out of code.
- Secrets must never be checked into git. If a secret is accidentally committed, rotate it and follow org incident process.

**Testing Guidance**
- Prefer `pytest` and fixture‑based tests. Keep tests deterministic and fast.
- Use `monkeypatch` for environment and dependency injection in tests.
- Write unit tests for logic and small integration tests for external interactions.
- When adding tests, aim for clear Arrange/Act/Assert structure.
- If necessary, tag slow/integration tests with markers (`@pytest.mark.integration`) and run them separately.

**Dependency Management**
- List runtime deps in `requirements.txt`. Keep it up to date when adding libraries.
- For dev dependencies, create `dev-requirements.txt` or use `requirements-dev` in tooling.
- Avoid unnecessary dependencies; prefer stdlib when possible.

**Git, Commits & PRs**
- Commit only logical units of work. Keep messages short and descriptive (1-line summary + optional body).
- Do not commit secrets or large binary files.
- Follow the repository's branching/PR conventions; ensure tests pass before requesting review.
- If asked to create commits or PRs, the agent should prepare diffs and suggest commit messages for human approval.

**Continuous Integration & Non‑interactive Commands**
- CI jobs should run `pip install -r requirements.txt`, `black --check .`, `isort --check .`, `flake8 .`, `mypy .`, and `pytest -q`.
- Ensure all CLI commands are non‑interactive and exit non‑zero on failures.

**Local Development Helper Commands**
- Create and activate venv (Unix): `python -m venv .venv && source .venv/bin/activate`.
- Run formatting + lint as a single pipeline: `black . && isort . && flake8 .`.
- Run tests and open coverage: `coverage run -m pytest && coverage html`.

**Agent Behavior Expectations**
- Preserve existing code style and minimal surface changes.
- Fix root causes rather than temporary patches when practical.
- Do not create new files unless requested; prefer editing existing files.
- When editing files, read them first (the agent runner enforces this) and make minimal, well‑explained changes.
- If changes touch multiple modules, explain rationale in the PR/commit message.
- Run tests locally when making behavioral changes and report failing tests to the user.

**Cursor / Copilot Rules**
- This repository contains no `.cursor/rules/` or `.cursorrules` files.
- This repository contains no `.github/copilot-instructions.md` file.

**Where To Look / Useful Paths**
- Entrypoint: `main.py`.
- Agents: `agents/`.
- Application code: `src/`.
- Tests: `tests/` or `test_*.py` files at the repository root.
- Requirements: `requirements.txt` (dev: `dev-requirements.txt` if present).

**Troubleshooting & Notes**
- If a linter or test fails, run the failing command locally and capture output, then create a focused fix.
- If `mypy` is noisy, annotate `# type: ignore` with a short explanation and prefer to add precise types instead.
- If making large refactors, break work into small commits and keep tests green after each commit.

Scope
- Rules in this AGENTS.md apply repository‑wide unless a more specific AGENTS.md exists in a subdirectory. Local instructions in a subdirectory take precedence.

(End of agent guidance)