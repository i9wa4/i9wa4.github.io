---
title: "Databricks で uv を活用して依存関係を管理する"
emoji: "🐴"
type: "tech"
topics:
  - "databricks"
  - "python"
  - "uv"
publication_name: "genda_jp"
published: true
published_at: 2025-12-11 07:00
---

## 1. はじめに

株式会社GENDA データエンジニア / MLOps エンジニアの uma-chan です。
この記事は GENDA Advent Calendar 2025 シリーズ4 Day 11 の記事です。

@[card](https://qiita.com/advent-calendar/2025/genda)

本記事では、Databricks で uv を使って依存関係を管理する方法を紹介します。

## 2. uv とは

uv は Rust 製の高速な Python パッケージマネージャです。

@[card](https://docs.astral.sh/uv/)

主な特徴

- pip の10-100倍高速
- `uv.lock` による再現可能な依存関係管理
- Python バージョン管理も可能

## 3. Databricks でのパッケージ管理方法

本記事では3つの方法を紹介します。

| 方法                      | 概要                       | おすすめ度   |
| ------                    | ------                     | ------------ |
| uv sync --active          | ローカルと同じワークフロー | ★★★       |
| requirements.txt 事前生成 | PR で差分確認可能          | ★★☆       |
| requirements.txt 動的生成 | ファイル管理不要           | ★☆☆       |

### 3.1. uv sync --active (おすすめ)

`--active` オプションを使うと、Databricks の既存環境に直接インストールできます。

```python
%pip install uv
```

```python
import subprocess

result = subprocess.run(
    ["uv", "sync", "--no-dev", "--active"],
    capture_output=True,
    text=True
)
```

`--active` オプションは、新しい `.venv` を作成せず、
現在アクティブな仮想環境 (`VIRTUAL_ENV` 環境変数で指定された環境) を使用します。

Databricks ノートブック環境では、既に `/local_disk0/` 上に
仮想環境がアクティブになっているため、
`/Workspace` 上に `.venv` を作成する際の問題を回避できます。

メリット

- ローカル開発と同じワークフロー
- `uv.lock` から直接インストールするため整合性が保証される

デメリット

- 毎回 uv のダウンロードが発生する

#### 3.1.1. 注意点

- Python バージョンの整合性
  - `requires-python` を DBR の Python バージョンに合わせる
  - 例: DBR 17.3 LTS は Python 3.12.3
- DBR プリインストールパッケージとの競合
  - `dependencies` には DBR にないパッケージのみ記載する
  - pandas, numpy 等は DBR にプリインストール済み

### 3.2. requirements.txt 事前生成

`uv.lock` から `requirements.txt` を生成し、リポジトリにコミットしておきます。

```bash
uv export --no-hashes --no-dev > requirements.txt
```

Databricks では事前生成した requirements.txt を使います。

```python
%pip install -r requirements.txt
```

pre-commit で自動化すると、生成忘れや手動編集による整合性エラーを防げます。

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: uv-export
        name: uv export
        entry: uv export --no-hashes --no-dev -o requirements.txt
        language: system
        files: ^(pyproject\.toml|uv\.lock)$
        pass_filenames: false
```

メリット

- PR で依存関係の変更が見やすい
- uv のインストールが不要

デメリット

- requirements.txt の生成忘れリスク

### 3.3. requirements.txt 動的生成

uv をインストールしておき動的生成することも可能です。

```python
%pip install uv
```

```python
import subprocess
result = subprocess.run(
    ["uv", "export", "--no-hashes", "--no-dev"],
    cwd="/Workspace/Repos/<user>/<repo>",
    capture_output=True,
    text=True
)
print(result.stdout)
```

そもそも `uv sync --active` が動くのであれば特にこの方法を選ぶ利点はありません。

## 4. pyproject.toml の構成

```toml:pyproject.toml
[project]
name = "databricks-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    # Project-specific (not included in DBR)
    "httpx",
]

[project.optional-dependencies]
dbr-17-3 = [
    # DBR 17.3 LTS preinstalled packages
    # https://docs.databricks.com/aws/en/release-notes/runtime/17.3lts
    #
    # Purpose:
    # - Used for dependency resolution in uv.lock (not installed by uv sync)
    # - Ensures compatibility with Databricks Runtime environment
    # - Excluded from Renovate updates via matchDepTypes in renovate.json
    "matplotlib==3.10.0",
    "mlflow-skinny==3.0.1",
    "numpy==2.1.3",
    "pandas==2.2.3",
    "pyarrow==19.0.1",
    "pyspark==4.0.0",
    "scikit-learn==1.6.1",
    "scipy==1.15.1",
]

[dependency-groups]
dev = [
    "jupyter-databricks-kernel",
    "jupyterlab",
    "pytest",
    "ruff",
]
```

ポイント

- `dependencies`: Databricks にインストールするパッケージ (Databricks Runtime にないもの)
- `[project.optional-dependencies]`: Databricks Runtime プリインストール済みパッケージ
  - `uv sync` ではインストールされない (依存解決のみに使用)
  - Databricks Runtime との互換性を確保するためにバージョンを固定
  - Databricks 側から requirements.txt が提供されてなさそうなのでリリースノートから情報を取得しました
- `dev`: ローカル開発ツール

## 5. Renovate で Databricks Runtime パッケージを更新対象から除外

Databricks Runtime プリインストールパッケージは Databricks Runtime のバージョンに合わせて固定する必要があるため、Renovate の自動更新から除外します。

```json:renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "matchDepTypes": ["optional-dependencies"],
      "enabled": false
    }
  ]
}
```

`matchDepTypes` で `optional-dependencies` を指定することで、`[project.optional-dependencies]` に定義したパッケージが Renovate の更新対象から除外されます。
これにより、Databricks Runtime のバージョンアップに合わせて手動で更新するワークフローが実現できます。

## 6. まとめ

uv を使うことでパッケージ依存関係を効率的に管理できます。

まだ uv を使ったことがない場合はぜひ試してみてください。

## 7. 関連記事

@[card](https://zenn.dev/genda_jp/articles/2025-12-19-databricks-notebook-ai-ready)

@[card](https://zenn.dev/genda_jp/articles/2025-12-10-organize-databricks-notebook-management)

@[card](https://zenn.dev/genda_jp/articles/2025-12-06-ai-guardrails-local-cloud)

## 8. 参考

- <https://docs.astral.sh/uv/>
- <https://docs.astral.sh/uv/reference/cli/#uv-export>
