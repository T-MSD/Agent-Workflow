# AGENTS.md – Agent Workflow Guidelines

This file provides guidance for agentic coding assistants working in this repository. The project is a multi-agent Enterprise Architecture workflow system with a Python/FastAPI backend (LangChain/LangGraph) and a React/TypeScript frontend.

## Project Structure

```
src/
  backend/           # Python FastAPI + LangGraph agents
    agents/          # Agent classes (Analyst, Architect, Supervisor)
    helpers/         # State, graph builder utilities
    main.py          # FastAPI entrypoint
    cli_main.py      # CLI entrypoint for local testing
  frontend/          # React + TypeScript + Vite
    src/components/  # React components (Chat UI)
    src/hooks/       # Custom React hooks
    src/services/    # API service layer
```

## Quick Start

**Backend:**
```bash
cd src/backend
python -m venv .venv && source .venv/bin/activate  # Unix
pip install -r ../../requirements.txt
cp .env.example .env  # Configure GROQ_API_KEY, Oracle DB credentials
python main.py        # FastAPI server
python cli_main.py    # CLI testing mode
```

**Frontend:**
```bash
cd src/frontend
npm install
npm run dev           # Vite dev server
```

## Build / Lint / Test Commands

### Backend (Python)
| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Run API server | `python src/backend/main.py` |
| Run CLI mode | `python src/backend/cli_main.py` |
| Run all tests | `pytest -q` |
| Run single test file | `pytest -q tests/test_file.py` |
| Run single test | `pytest -q tests/test_file.py::TestClass::test_name` |
| Run tests by pattern | `pytest -q -k "pattern"` |
| Debug a test | `pytest -q tests/test_x.py -k test_name -s --pdb` |
| Lint | `flake8 .` |
| Format | `black .` |
| Sort imports | `isort .` |
| Type check | `mypy .` |
| Full check | `black . && isort . && flake8 . && mypy .` |

### Frontend (TypeScript/React)
| Task | Command |
|------|---------|
| Install deps | `npm install` (in `src/frontend/`) |
| Dev server | `npm run dev` |
| Build | `npm run build` |
| Lint | `npm run lint` |
| Type check | `tsc -b` |

## Code Style Guidelines

### Python

**Imports:**
- Group: stdlib, third-party, local application (use `isort` to enforce)
- Prefer absolute imports: `from helpers.state import AgentState`
- Use relative imports only within the same package: `from .agent import BaseAgent`

**Formatting:**
- Use `black` with default 88-char line length
- Run `black . && isort .` before commits

**Typing:**
- Add type hints to all public functions and methods
- Use modern syntax: `list[int]`, `dict[str, Any]`, `Optional[...]`
- Use `TypedDict` for structured dicts (see `AgentState` in `helpers/state.py`)
- Use `Literal` for constrained string types (see `Router` in `supervisor.py`)

**Naming:**
- Files/modules: `snake_case.py`
- Functions/variables: `snake_case`
- Classes: `PascalCase` (e.g., `BaseAgent`, `Supervisor`)
- Constants: `UPPER_CASE` (e.g., `_SYSTEM_PROMPT`, `_DB_DATA`)
- Private members: prefix with underscore (`_get_connection`)

**Docstrings:**
- Use Google-style docstrings for public functions and classes
- Include description, parameters, returns, and raises sections

**Error Handling:**
- Catch specific exceptions: `except oracledb.Error as exc:`
- Preserve context when re-raising: `raise RuntimeError(...) from exc`
- Validate inputs early and raise `ValueError`/`TypeError`
- Use context managers for resources: `with _get_connection() as conn:`

**Logging:**
- Use `logging` module, not `print()` in library code
- CLI scripts may use `print()` for user output

### TypeScript/React

**Imports:**
- Group: React, third-party, local components, types, styles

**Naming:**
- Components: `PascalCase.tsx` (e.g., `ChatMessage.tsx`)
- Hooks: `camelCase` with `use` prefix (e.g., `useAgent.tsx`)
- Types: `PascalCase` in `types/types.ts`
- Utilities: `camelCase.ts`

**Typing:**
- Define interfaces/types in `src/types/types.ts`
- Use explicit return types on exported functions

## LangGraph Agent Patterns

This codebase uses LangGraph for multi-agent orchestration:

**Agent Classes:**
- Inherit from `BaseAgent` (see `agents/agent.py`)
- Override `run(state: AgentState)` for custom logic
- Bind tools in constructor: `model.bind_tools(tools)`

**State Management:**
- Use `AgentState` TypedDict from `helpers/state.py`
- Messages use `Annotated[Sequence[BaseMessage], operator.add]` for append semantics

**Supervisor Pattern:**
- Use `with_structured_output(Router)` for routing decisions
- Return `{"next": "AgentName"}` to control flow

**Adding New Agents:**
1. Create class in `agents/` inheriting `BaseAgent`
2. Export from `agents/__init__.py`
3. Register node in `helpers/graph_builder.py`
4. Add routing in `Supervisor` and conditional edges

## Configuration & Secrets

- Use `.env` files for local configuration (never commit)
- Required env vars: `GROQ_API_KEY`, `HOST`, `PORT`, `ORIGIN`
- Oracle DB: `ORACLE_DB_USER`, `ORACLE_DB_PASSWORD`, `ORACLE_DB_DSN`, `TABLE_NAME`

## Testing Guidance

- Use `pytest` with fixtures
- Use `monkeypatch` for env vars and dependencies
- Mock external services (LLM calls, database)
- Structure tests as Arrange/Act/Assert

## Agent Behavior Expectations

- Read files before editing (enforced by runner)
- Make minimal, focused changes
- Preserve existing code style
- Fix root causes, not symptoms
- Run tests when making behavioral changes
- Do not create new files unless explicitly requested
- Do not commit unless the user explicitly asks
- Never apply changes unless the user says "You may implement the changes"

## Cursor / Copilot Rules

This repository contains no `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md` files.

## Useful Paths

- Backend entrypoint: `src/backend/main.py`
- CLI entrypoint: `src/backend/cli_main.py`
- Agents: `src/backend/agents/`
- Graph builder: `src/backend/helpers/graph_builder.py`
- State definition: `src/backend/helpers/state.py`
- Frontend app: `src/frontend/src/App.tsx`
- API service: `src/frontend/src/services/api.ts`
- Requirements: `requirements.txt`

## Scope

Rules in this AGENTS.md apply repository-wide unless a more specific AGENTS.md exists in a subdirectory. Local instructions take precedence.
