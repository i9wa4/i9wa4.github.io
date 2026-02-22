# mise + pre-commit 設定の供養
uma-chan
2026-01-06

## 1. はじめに

dotfiles リポジトリで mise と pre-commit を活用して CI
を構築していましたが、Nix
へ移行完了したため不要になりました。削除前に知見を残しておきます。

## 2. mise.toml

<div class="code-with-filename">

**mise.toml**

``` toml
[tools]
# Tools for CI
"aqua:JohnnyMorganz/StyLua"    = "2.3.1"
"aqua:gitleaks/gitleaks"       = "8.30.0"
"aqua:rhysd/actionlint"        = "1.7.9"
"aqua:suzuki-shunsuke/ghalint" = "1.5.4"
"aqua:suzuki-shunsuke/ghatm"   = "1.0.0"
"aqua:suzuki-shunsuke/pinact"  = "3.7.3"
"aqua:zizmorcore/zizmor"       = "1.19.0"
pre-commit                     = "4.5.1"
shellcheck                     = "0.11.0"
shfmt                          = "3.12.0"
uv                             = "0.9.18"

# Custom packages (nix/packages/*.nix)
"aqua:rvben/rumdl"             = "0.0.206"
"aqua:rhysd/vim-startuptime"   = "1.3.2"
```

</div>

### 2.1. ツール解説

#### 2.1.1. CI/Linter 系

| ツール     | 用途                                    |
|------------|-----------------------------------------|
| StyLua     | Lua フォーマッター (Neovim 設定用)      |
| gitleaks   | シークレット検出                        |
| actionlint | GitHub Actions Workflow の Linter       |
| ghalint    | GitHub Actions のセキュリティ Linter    |
| ghatm      | GitHub Actions のテンプレート管理       |
| pinact     | GitHub Actions のバージョン固定         |
| zizmor     | GitHub Actions のセキュリティスキャナー |
| pre-commit | Git hooks マネージャー                  |
| shellcheck | シェルスクリプト Linter                 |
| shfmt      | シェルスクリプトフォーマッター          |
| uv         | Python パッケージマネージャー           |

#### 2.1.2. 開発ツール系

| ツール          | 用途                      |
|-----------------|---------------------------|
| rumdl           | Markdown Linter/Formatter |
| vim-startuptime | Vim の起動時間計測        |

## 3. pre-commit-mise.yaml (GitHub Actions Workflow)

GitHub Actions で mise と pre-commit を組み合わせて CI
を実行するワークフローです。

<div class="code-with-filename">

**.github/workflows/pre-commit-mise.yaml**

``` yaml
name: pre-commit (mise)
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
        uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1
        with:
          persist-credentials: false

      - name: Install mise
        uses: jdx/mise-action@146a28175021df8ca24f8ee1828cc2a60f980bd5 # v3.5.1
        with:
          cache: true

      - name: Cache
        uses: actions/cache@9255dc7a253b0ccc959486e2bca901246202afeb # v5.0.1
        with:
          path: |
            ~/.cache/pre-commit
            ~/.cache/uv
            .venv
          key: |
            cache-${{ runner.os }}-${{ runner.arch }}-${{ hashFiles('.pre-commit-config.yaml', 'uv.lock') }}
          restore-keys: |
            cache-${{ runner.os }}-${{ runner.arch }}-

      - name: Run pre-commit
        run: |
          pre-commit run --all-files --verbose
```

</div>

## 4. まとめ

mise + pre-commit の組み合わせは開発環境と CI 環境を同一にしつつ CI
実行時間を最短にできるので有用です。 趣味で dotfiles を Nix
に移行しただけで mise は悪くないですよ！

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-01-06-mise-pre-commit.html&text=mise%20%2B%20pre-commit%20%E8%A8%AD%E5%AE%9A%E3%81%AE%E4%BE%9B%E9%A4%8A%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=mise%20%2B%20pre-commit%20%E8%A8%AD%E5%AE%9A%E3%81%AE%E4%BE%9B%E9%A4%8A%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-01-06-mise-pre-commit.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-01-06-mise-pre-commit.html&title=mise%20%2B%20pre-commit%20%E8%A8%AD%E5%AE%9A%E3%81%AE%E4%BE%9B%E9%A4%8A%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
