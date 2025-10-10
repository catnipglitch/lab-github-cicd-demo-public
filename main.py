"""ローカルの .env または Codespaces のシークレットから Sentry を初期化するエントリポイント。"""

import logging
import os
from pathlib import Path
from dotenv import load_dotenv
import sentry_sdk


def _get_sentry_dsn() -> str | None:
    """実行環境に応じて Sentry DSN を決定する。"""
    in_codespaces = bool(
        os.getenv("CODESPACES") or os.getenv("CODESPACE_NAME")
    )
    if not in_codespaces:
        env_file = Path(__file__).resolve().parent / ".env"
        load_dotenv(env_file, override=False)

    return os.getenv("SENTRY_DSN")


dsn = _get_sentry_dsn()
if dsn:
    sentry_sdk.init(
        dsn=dsn,
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
    )


logging.basicConfig(level=logging.INFO)


def main():
    """CLI としてリポジトリ紹介メッセージをログ出力する。"""
    logger = logging.getLogger(__name__)
    logger.info("Hello from github-cicd-demo!")
    logger.info("This is a demo repository for GitHub Actions CI/CD workflows.")
    logger.info("You can trigger workflows on push or via manual dispatch with inputs.")


if __name__ == "__main__":
    main()
