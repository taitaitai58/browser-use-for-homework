# 課題自動化アプリケーション集（browser_use 活用）

このリポジトリは、`browser_use` を活用して大学や学習サービスの課題提出を支援するスクリプト群を管理するためのものです。`browser_use` ライブラリそのものの開発を目的としたリポジトリではありません。各エージェントのコードは `HOMEWORK_AGENTS/` 以下に配置していきます。

## 主な特徴

- `browser_use` のエージェント機能とカスタムアクションを組み合わせ、課題収集・ファイル生成・アップロードを自動化
- スクリプトごとに必要な環境変数やワークフローを柔軟に設定可能
- 新しい課題サービスに対応するスクリプトを順次追加予定

### 現在実装済みの機能

- **立命館大学プロジェクト演習（プロ演）課題支援**  
  スクリプト: `HOMEWORK_AGENTS/proen/ritsumei_puroen_assignment.py`
  Rainbow へのログイン、課題内容の確認、提出ファイルの生成・保存・アップロードを自動化します。

## 共通の前提条件

- macOS / Linux / Windows（Chromium が利用できる環境）
- Python 3.11 以上
- [`uv`](https://github.com/astral-sh/uv) のインストール

## 共通セットアップ手順

1. 仮想環境の作成と依存パッケージのインストール
   ```bash
   uv venv --python 3.11
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   uv sync
   ```

2. `.env` に共通の API キーを設定
   ```
   OPENAI_API_KEY=あなたのOpenAIキー
   ```
   各スクリプト固有の認証情報が必要な場合は、同じ `.env` に追記してください（例: プロ演向け `RITSUMEI_RAINBOW_ID`, `RITSUMEI_RAINBOW_PASSWORD`）。

3. Chromium のインストール（未導入の場合）
   ```bash
   uvx browser-use install
   ```

## スクリプトの実行方法

1. 仮想環境を有効化し、必要な環境変数が設定されていることを確認します。
2. 実行したいスクリプトを指定して `uv run` で起動します。
   ```bash
   uv run examples/ritsumei_puroen_assignment.py
   ```
3. コンソールの指示に従い、課題識別情報などを入力します。
4. エージェントがブラウザ自動操作を行い、課題の要件に沿ってファイル保存や提出補助を実施します。

## カスタムアクション（プロ演スクリプト例）

- `Save assignment file`  
  課題プログラムを指定パスに保存し、再アップロード用のファイルを準備します。

- `Provide assignment file path`  
  保存済みファイルの絶対パスを返却し、`browser_use` の `upload_file` アクションで利用できる形にします。

他のスクリプトでも必要に応じてカスタムアクションを追加し、特定サービスのワークフローに合わせて拡張する予定です。

## 注意事項

- 各サービスの利用規約に従い、自動化の可否を確認したうえでご利用ください。
- `.env` に保存した認証情報はバージョン管理に含めないよう注意してください。
- 課題仕様や画面構成が変わった場合は、該当スクリプトのプロンプトやアクション定義を更新する必要があります。


