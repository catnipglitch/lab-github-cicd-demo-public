import importlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import logging

import pytest


class SentryStub(ModuleType):
    """A minimal stub to capture sentry_sdk.init calls without network side effects."""

    def __init__(self, name: str = "sentry_sdk"):
        super().__init__(name)
        self.inits: list[tuple[tuple, dict]] = []

    def init(self, *args, **kwargs):  # type: ignore[override]
        self.inits.append((args, kwargs))


def _load_main_from_path():
    """Load the repository's main.py as a module regardless of sys.path state."""
    repo_root = Path(__file__).resolve().parents[1]
    main_path = repo_root / "main.py"
    spec = importlib.util.spec_from_file_location("main", main_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["main"] = mod
    spec.loader.exec_module(mod)  # type: ignore[arg-type]
    return mod


def import_main_fresh(
    monkeypatch: pytest.MonkeyPatch,
    env: dict[str, str] | None = None,
    with_sentry_stub: bool = True,
):
    """Import the main module fresh with controlled environment and optional sentry stub.

    Returns the tuple (module, sentry_stub).
    """
    # Prepare environment variables
    # Start clean: remove envs we care about
    for key in (
        "SENTRY_DSN",
        "SENTRY_TRACES_SAMPLE_RATE",
        "CODESPACES",
        "CODESPACE_NAME",
    ):
        monkeypatch.delenv(key, raising=False)

    if env:
        for k, v in env.items():
            monkeypatch.setenv(k, v)

    # Prevent reading local .env during tests unless explicitly requested
    if not env or ("CODESPACES" not in env and "CODESPACE_NAME" not in env):
        monkeypatch.setenv("CODESPACES", "1")

    # Ensure a fresh import
    monkeypatch.delitem(sys.modules, "main", raising=False)

    # Optionally install sentry stub before import so top-level init is captured
    stub = None
    if with_sentry_stub:
        stub = SentryStub()
        monkeypatch.setitem(sys.modules, "sentry_sdk", stub)

    mod = _load_main_from_path()
    return mod, stub


def test_import_without_dsn_does_not_init_sentry(monkeypatch: pytest.MonkeyPatch):
    mod, stub = import_main_fresh(monkeypatch, env={}, with_sentry_stub=True)
    assert stub is not None
    assert stub.inits == [], (
        "sentry_sdk.init should not be called at import without DSN"
    )
    # Also ensure computed dsn is None
    assert getattr(mod, "dsn", None) in (None, ""), "dsn should be falsy without env"


def test_main_logs_expected_messages(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
):
    mod, _ = import_main_fresh(monkeypatch, env={})

    caplog.set_level(logging.INFO)
    mod.main()

    messages = [
        rec.getMessage() for rec in caplog.records if rec.levelno == logging.INFO
    ]
    assert any("Hello from github-cicd-demo!" in m for m in messages)
    assert any(
        "demo repository for GitHub Actions CI/CD workflows" in m for m in messages
    )
    assert any(
        "trigger workflows on push or via manual dispatch" in m for m in messages
    )


def test_import_with_dsn_calls_sentry_init(monkeypatch: pytest.MonkeyPatch):
    env = {"SENTRY_DSN": "https://example_dsn", "SENTRY_TRACES_SAMPLE_RATE": "0.5"}
    _, stub = import_main_fresh(monkeypatch, env=env, with_sentry_stub=True)

    assert stub is not None
    assert len(stub.inits) == 1, (
        "Top-level import should initialize Sentry once when DSN present"
    )
    args, kwargs = stub.inits[0]
    assert args == ()
    assert kwargs.get("dsn") == env["SENTRY_DSN"]
    # traces_sample_rate should be float-converted
    assert kwargs.get("traces_sample_rate") == 0.5


def test_main_calls_sentry_init_again_when_dsn_present(monkeypatch: pytest.MonkeyPatch):
    env = {"SENTRY_DSN": "https://example_dsn"}
    mod, stub = import_main_fresh(monkeypatch, env=env, with_sentry_stub=True)
    assert stub is not None

    # Call main(), which should initialize Sentry again using only dsn kwarg
    mod.main()

    assert len(stub.inits) == 2, "Expected a second Sentry init call from main()"
    _, first_kwargs = stub.inits[0]
    _, second_kwargs = stub.inits[1]

    assert first_kwargs.get("dsn") == env["SENTRY_DSN"]
    # First call may also include traces_sample_rate (from import-time init)

    assert second_kwargs == {"dsn": env["SENTRY_DSN"]}, (
        "main() should call sentry_sdk.init(dsn=dsn)"
    )
