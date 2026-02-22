# Python 開発環境最適化編 ― uv + pre-commit + GitHub Actions
uma-chan
2025-07-28

本記事は3部構成の2本目です。

1.  [Claude Code 対応 Dev Container 環境構築編 - VS Code
    でもそれ以外でも](https://i9wa4.github.io/2025-07-28-article1-devcontainer.md)
2.  [Python 開発環境最適化編 - uv + pre-commit + GitHub
    Actions](https://i9wa4.github.io/2025-07-28-article2-python-env.md)
3.  [Databricks Connect 実践編 - ローカルから Databricks
    コンピュートを利用](https://i9wa4.github.io/2025-07-28-article3-databricks-connect.md)

## 1. はじめに

前回の Dev Container 環境に Python 開発環境を追加します。

uv によるパッケージ管理と pre-commit
による品質管理で、チーム開発でも個人開発でも快適な Python
環境を構築できます。

## 2. 対象読者

- Python開発環境を効率化したい方
- チーム開発でコード品質を統一したい方
- VS Code以外のエディタでも同じ環境を使いたい方

## 3. uv とは

今回利用している Python 環境管理ツールです。

<https://github.com/astral-sh/uv>

最低限理解しておくべき要点は以下です。

- uv 自体は Python エコシステムの外にあるツール
- インストールしたい Python パッケージを `pyproject.toml` で管理する
- `pyproject.toml` のパッケージの依存関係解決結果を `uv.lock`
  に保存し環境の再現性を担保している

## 4. Python 環境設定

Python コーディング向け環境設定について説明していきます。

基本的なライブラリと pre-commit で Black isort, flake8
を利用していきます。

### 4.1. pyproject.toml

<div class="code-with-filename">

**pyproject.toml**

``` toml
[project]
name = "your-project-name"
version = "0.1.0"
description = "Add your description here"
requires-python = "~=3.13.0"
dependencies = [
  "ipykernel",
  "jupyterlab",
  "matplotlib",
  "numpy",
  "pandas",
  "python-dotenv",
  "requests",
  "seaborn",
]

[dependency-groups]
dev = [
  "pre-commit~=4.2.0",
  "black==25.1.0",
  "isort==6.0.0",
  "flake8==7.3.0",
  "flake8-pyproject",
]

[tool.black]
line-length = 88
target-version = ['py313']

[tool.isort]
profile = "black"
line_length = 88

[tool.flake8]
max-line-length = 88
extend-exclude = [".venv"]
extend-ignore = [
    "E203",  # Whitespace before ':'
    "E701",  # Multiple statements on one line (colon)
]
```

</div>

### 4.2. pre-commit 設定

Formatter設定をVS Codeから切り離すことでVS Code以外のエディタやGitHub
Actionsでも利用できるようになります。

<div class="code-with-filename">

**.pre-commit-config.yaml**

``` yaml
default_stages: [pre-commit]
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-added-large-files
      - id: check-json
      - id: check-yaml
      - id: detect-private-key
      - id: end-of-file-fixer
      - id: mixed-line-ending
        args: [--fix=no]
      - id: trailing-whitespace
        args: [--markdown-linebreak-ext=md]

  - repo: local
    hooks:
      - id: black
        name: black
        entry: uv run --no-sync black
        language: system
        types: [python]

  - repo: local
    hooks:
      - id: isort
        name: isort (python)
        entry: uv run --no-sync isort
        language: system
        types: [python]

  - repo: local
    hooks:
      - id: flake8
        name: flake8
        entry: uv run --no-sync flake8
        language: system
        types: [python]

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.28.0
    hooks:
      - id: gitleaks
```

</div>

### 4.3. GitHub Actions での pre-commit

GitHub Actionsでpre-commitを実行するための設定です。

<div class="code-with-filename">

**.github/workflows/pre-commit.yaml**

``` yaml
name: pre-commit
run-name: ${{ github.event_name }} on ${{ github.ref_name }} by @${{ github.actor }}

on:
  workflow_dispatch:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
    types:
      - opened
      - synchronize
      - reopened

permissions: {}

defaults:
  run:
    shell: bash

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    permissions:
      contents: read

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          # プルリクエスト時はソースブランチ(github.head_ref)を、
          # 手動実行時は実行対象ブランチ(github.ref_name)をチェックアウト
          ref: ${{ github.event_name == 'pull_request' && github.head_ref || github.ref_name }}
          persist-credentials: false

      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          version: "0.8.3"

      - name: Set up Python
        run: |
          uv sync --only-group dev

      - name: Cache pre-commit
        uses: actions/cache@v4
        with:
          path: ~/.cache/pre-commit
          key: |
            pre-commit-${{ runner.os }}-${{ hashFiles('.pre-commit-config.yaml') }}-${{ hashFiles('uv.lock') }}

      - name: Install pre-commit
        run: |
          uv run --no-sync pre-commit install

      - name: Run pre-commit
        run: |
          uv run --no-sync pre-commit run --all-files
```

</div>

## 5. Dev Container への統合

### 5.1. devcontainer.json の更新

前回の devcontainer.json に以下の設定を追加します。

``` json
{
    "customizations": {
        "vscode": {
            "extensions": [
                "editorconfig.editorconfig",
                "elagil.pre-commit-helper",
                "ms-python.python",
                "ms-toolsai.jupyter"
            ]
        }
    },
    "remoteEnv": {
        "UV_LINK_MODE": "copy"
    },
    "postStartCommand": "uv sync --frozen --group dev && uv run pre-commit install"
}
```

### 5.2. JupyterLab 起動スクリプト

VS Code ユーザーは不要ですが一応 JupyterLab
を起動するスクリプトも用意しました。

ポートは自動割り当てにしています。

> [!NOTE]
>
> ### 5.2.1. `.devcontainer/start-jupyter.sh`
>
> <div class="code-with-filename">
>
> **.devcontainer/start-jupyter.sh**
>
> ``` sh
> #!/usr/bin/env bash
> set -o errexit
>
> # JupyterLab起動スクリプト
> # 快適な開発用
>
> echo "🔥 JupyterLab 環境を起動中..."
>
> # ポート設定（環境変数または自動割り当て）
> # JUPYTER_PORT=8888 # NOTE: この行をコメントアウトすると自動ポート検索が有効になります
> JUPYTER_PORT=${JUPYTER_PORT:-0}
>
> if [ "$JUPYTER_PORT" = "0" ]; then
>   echo "📡 利用可能なポートを自動検索中..."
> else
>   echo "📡 指定ポート ${JUPYTER_PORT} で起動します"
> fi
>
> # Python環境の確認
> if [ -f "uv.lock" ]; then
>   echo "📦 uv環境を使用してJupyterLabを起動します"
>   uv sync --frozen
>   nohup uv run jupyter lab --ip=0.0.0.0 --port=${JUPYTER_PORT} --no-browser --allow-root \
>     --NotebookApp.token='' --NotebookApp.password='' \
>     --ServerApp.allow_origin='*' --ServerApp.disable_check_xsrf=True >/dev/null 2>&1 &
> elif [ -d ".venv" ]; then
>   echo "📦 venv環境を使用してJupyterLabを起動します"
>   source .venv/bin/activate
>   nohup jupyter lab --ip=0.0.0.0 --port=${JUPYTER_PORT} --no-browser --allow-root \
>     --NotebookApp.token='' --NotebookApp.password='' \
>     --ServerApp.allow_origin='*' --ServerApp.disable_check_xsrf=True >/dev/null 2>&1 &
> else
>   echo "❌ Python仮想環境が見つかりません"
>   echo "uvまたはvenvで環境をセットアップしてください"
>   exit 1
> fi
>
> # 実際に割り当てられたポートを取得（リトライ機能付き）
> for i in {1..10}; do
>   sleep 1
>   ACTUAL_PORT=$(ss -tlnp 2>/dev/null | grep jupyter-lab | awk '{print $4}' | cut -d: -f2 | head -1)
>   if [ -n "$ACTUAL_PORT" ]; then
>     break
>   fi
> done
>
> if [ "$JUPYTER_PORT" = "0" ] && [ -n "$ACTUAL_PORT" ]; then
>   echo "🌐 JupyterLabは http://localhost:${ACTUAL_PORT}/lab でアクセス可能です"
> else
>   echo "🌐 JupyterLabは http://localhost:${JUPYTER_PORT}/lab でアクセス可能です"
> fi
> ```
>
> </div>

## 6. Python 仮想環境更新手順

1.  必要に応じて `.python-version` や `pyproject.toml` を更新します。

2.  `uv.lock` を更新します。

    ``` sh
    uv lock --upgrade
    ```

3.  .venv を更新します。

    ``` sh
    uv sync --frozen --group dev
    ```

### 6.1. パッケージ追加手順

``` sh
# 新しいパッケージを追加
uv add pandas matplotlib

# 開発用パッケージを追加
uv add --group dev pytest
```

## 7. おわりに

これで Python 開発環境が完成しました。

次回はこの環境に Databricks Connect
を追加してクラウドデータウェアハウスと連携する方法を紹介します。

[Databricks Connect 実践編 - ローカルから Databricks
コンピュートを利用](https://i9wa4.github.io/2025-07-28-article3-databricks-connect.md)

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-07-28-article2-python-env.html&text=Python%20%E9%96%8B%E7%99%BA%E7%92%B0%E5%A2%83%E6%9C%80%E9%81%A9%E5%8C%96%E7%B7%A8%20%E2%80%95%20uv%20%2B%20pre-commit%20%2B%20GitHub%20Actions%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Python%20%E9%96%8B%E7%99%BA%E7%92%B0%E5%A2%83%E6%9C%80%E9%81%A9%E5%8C%96%E7%B7%A8%20%E2%80%95%20uv%20%2B%20pre-commit%20%2B%20GitHub%20Actions%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-07-28-article2-python-env.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-07-28-article2-python-env.html&title=Python%20%E9%96%8B%E7%99%BA%E7%92%B0%E5%A2%83%E6%9C%80%E9%81%A9%E5%8C%96%E7%B7%A8%20%E2%80%95%20uv%20%2B%20pre-commit%20%2B%20GitHub%20Actions%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
