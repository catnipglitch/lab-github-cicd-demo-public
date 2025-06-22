# Gradio Hello World アプリケーション要件

## プロジェクト概要
このプロジェクトでは、Gradioライブラリを使用して「Hello world」を表示するシンプルなWebアプリケーションを作成します。

## 機能要件
- Gradio UIを使用したシンプルなWebインターフェース
- アプリケーション起動時に「Hello world」というテキストを表示
- 特別な入力操作は不要

## 技術要件
- プログラミング言語: Python
- 主要ライブラリ: Gradio
- 依存関係管理: pip (requirements.txt)

## 実装詳細
1. `gradio_hello.py`ファイルの作成
   - `import gradio as gr`でライブラリをインポート
   - 「Hello world」を返す関数の定義
   - Gradioインターフェースの設定（入力なし、テキスト出力）
   - アプリケーションの起動コード

2. `requirements.txt`ファイルの作成
   - 必要なライブラリとバージョンの指定
   ```
   gradio>=4.0.0
   ```

## 実行方法
1. 依存関係のインストール
   ```
   pip install -r requirements.txt
   ```

2. アプリケーションの起動
   ```
   python gradio_hello.py
   ```

## 期待される動作
- アプリケーション起動後、ブラウザが自動的に開く
- Gradio UIが表示され、「Hello world」というテキストが表示される
