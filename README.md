# lab-github-cicd-demo-public

GitHub Actions の CI/CD ワークフローを試すためのシンプルな Python プロジェクトです。`main.py` からメッセージを出力する CLI を実行でき、Sentry へのエラーレポート送信をオプションで有効化できます。

## プロジェクト構成
- `main.py`: CLI エントリーポイント。Sentry DSN を検出して初期化し、リポジトリ紹介メッセージを出力します。
- `pyproject.toml`: パッケージ名・依存関係などのメタデータを管理します。
- `uv.lock`: [uv](https://github.com/astral-sh/uv) 向けのロックファイルです。`uv sync --dev` で同じ依存関係（開発用を含む）を再現できます。
- `lab-github-cicd-demo-public.code-workspace`: VS Code 用のワークスペース設定です。

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
