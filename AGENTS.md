# Repository Guidelines

## Project Structure & Module Organization
- `main.py` is the CLI entry point; it configures Sentry (when `SENTRY_DSN` is present) and emits the demo log messages.
- `pyproject.toml` defines the Python 3.13+ package metadata and runtime dependencies; `uv.lock` pins resolved versions for `uv sync --dev`.
- `.github/workflows/*.yml` hosts GitHub Actions pipelines (linting via Pylint plus manual dispatch demos). Adjust or add jobs there when automating checks.
- Place local secrets in `.env` (ignored by Git) so `main.py` and the CI secrets layout stay aligned.

## Build, Test, and Development Commands
- `uv sync --dev` installs runtime + tooling dependencies from the lockfile; prefer this before running any commands.
- `uv run python main.py` (or `python main.py`) executes the CLI locally and validates Sentry initialization.
- `uv run pylint main.py` mirrors the CI lint workflow; keep the score clean before opening a PR.
- `uv run pytest` runs the test suite once you add modules under `tests/`; pass `-q` for faster feedback.

## Coding Style & Naming Conventions
- Follow standard Python style: 4-space indentation, type hints for public functions, and `lower_snake_case` for functions/variables with `UPPER_SNAKE_CASE` constants.
- Keep modules small and prefer pure functions; log side effects via `logging.getLogger(__name__)` as in `main.py`.
- Maintain lightweight module docstrings summarizing intent, and use f-strings for interpolated output.

## Testing Guidelines
- Use `pytest` with files named `tests/test_<module>.py`; mirror the source directory so fixtures stay discoverable.
- Cover both successful CLI runs and Sentry-disabled paths (e.g., patch `os.environ` for DSN scenarios).
- Record reproduction commands in the PR description and re-run `uv run pytest -q` before requesting review.

## Commit & Pull Request Guidelines
- Write concise, imperative commit subjects (`Add Pylint Issue Reporter workflow`, `demo:test`) and keep bodies brief but informative.
- Group related changes per commit; include references to issues or Actions runs when relevant.
- PRs should summarize user impact, list validation commands, and call out Sentry or workflow changes so reviewers can verify secrets and CI updates.

## Security & Configuration Notes
- Never commit real DSNs or API keys; rely on `.env` locally and repository secrets in GitHub Actions.
- When introducing new workflows, double-check required secrets exist and document any new environment variables in `README.md`.

## Agent Task Logging Guidelines

Create a folder named `.agents/` at the repository root.  
Each task must have its own log file in `.agents/`, named:  
`agent_task_YYYYMMDDHHMMSS_<slug>.md`  
Example: `agent_task_20251010_153210_fix-login.md`

Each log file should include:

- User instruction (summary of what was requested)  
- TODO list (steps to complete the task)  
- Execution log (commands, timestamps, results)  
- Outcome (final result, links to PRs or artifacts)

If clarification from the user is needed, record the open question in the log before pausing work.  
Resume the same task by appending updates to the same log file.  
Always link the related `.agents/` log in the Pull Request description.  
Never include secrets, DSNs, or API keys in `.agents/` logs.
