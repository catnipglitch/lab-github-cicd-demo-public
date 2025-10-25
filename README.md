# lab-github-cicd-demo-public

GitHub Actions の CI/CD ワークフローを試すためのシンプルな Python プロジェクトです。`main.py` からメッセージを出力する CLI を実行でき、Sentry へのエラーレポート送信をオプションで有効化できます。

## プロジェクト構成
- `main.py`: CLI エントリーポイント。Sentry DSN を検出して初期化し、リポジトリ紹介メッセージを出力します。
- `pyproject.toml`: パッケージ名・依存関係などのメタデータを管理します。
- `uv.lock`: [uv](https://github.com/astral-sh/uv) 向けのロックファイルです。`uv sync --dev` で同じ依存関係（開発用を含む）を再現できます。
- `lab-github-cicd-demo-public.code-workspace`: VS Code 用のワークスペース設定です。

## GitHub Actions ワークフロー

| ファイル | ワークフロー名 | トリガー | 概要 |
| --- | --- | --- | --- |
| `.github/workflows/pylint.yml` | Pylint | `push`(`main`), `pull_request`(`main`) | uv で依存を同期し、全 Python ファイルに対して Pylint を実行します。 |
| `.github/workflows/pylint-issue-report.yml` | Pylint Issue Reporter (Pylint to Issue) | `push`, `pull_request` | Pylint の JSON レポートから E/F のみを抽出し、単一の Issue に集約・更新します。 |
| `.github/workflows/push_test_print.yml` | Push and Hello world! | `push` | プッシュ時にジョブを起動し、メッセージを出力する動作確認用ワークフローです。 |
| `.github/workflows/dispatch_test_input_print.yml` | Dispatch Manual | `workflow_dispatch` | 手動入力した文字列をそのまま出力するシンプルなデモジョブです。 |
| `.github/workflows/dispatch_test_print_context.yml` | Dispatch Context Print | `workflow_dispatch` | 手動実行で `github` コンテキスト全体を JSON として出力します。 |
| `.github/workflows/dispatch_test_variables_print.yml` | Dispatch Print Variables DEMO | `workflow_dispatch` | 指定した環境・リポジトリ変数を読み取り、標準出力に表示するサンプルです。 |
| `.github/workflows/schedule_test_print.yml` | Schedule Test | `schedule`(*/15 * * * *) | 15 分間隔で日時を出力するスケジュール実行の検証ジョブです。 |

> 今後ワークフローを追加した際は、この表に行を追加して管理してください。

## セットアップ
1. Python 3.13 以降を用意します。
2. 任意で仮想環境を作成します。
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows は .venv\Scripts\activate
   ```
3. 依存関係をインストールします。
   - uv を利用する場合（推奨）：
     ```bash
     uv sync --dev
     ```
   - pip を利用する場合：
     ```bash
     pip install --upgrade pip
     pip install loadenv sentry-sdk
     ```

### Sentry 連携（任意）
Sentry への送信を有効化するには、プロジェクト直下に `.env` を作成して `SENTRY_DSN`（必要に応じて `SENTRY_TRACES_SAMPLE_RATE`）を設定するか、同じ環境変数をシェルでエクスポートしてください。

```env
SENTRY_DSN=https://examplePublicKey@o0.ingest.sentry.io/0
SENTRY_TRACES_SAMPLE_RATE=1.0
```

`main.py` 実行時に `.env` から読み込めるライブラリ `loadenv` がインストールされていれば、環境変数が自動的に設定されます。

## 実行方法

```bash
python main.py
```

`main.py` は CLI としてメッセージを表示し、Sentry が構成されていれば初期化およびトレース設定も行います。
