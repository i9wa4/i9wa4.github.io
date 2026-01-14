# uv + Quarto でブログやスライドを作成して GitHub Pages で公開する (HTML
エクスポートにも対応)
uma-chan
2025-12-15

## 1. はじめに

Markdown ライクな記法でブログやスライドを作成できる Quarto
の入門記事です。

この記事では以下のリポジトリをテンプレートとして使用します。

<https://github.com/i9wa4/quarto-intro>

公開ページ: <https://i9wa4.github.io/quarto-intro>

## 2. 想定読者

- Git/GitHub 操作の説明がなくても問題ない方

## 3. Quarto とは

<https://quarto.org/>

> An open-source scientific and technical publishing system

オープンソースの科学技術出版システムです。Pandoc
をベースにしていて手軽でありつつも拡張性があり細かいところに手が届くという印象です。

## 4. 環境構築

uv を使って Quarto をインストールします。

### 4.1. uv のインストール

uv がまだインストールされていない場合は以下を参照してください。

<https://docs.astral.sh/uv/getting-started/installation/>

### 4.2. プロジェクトの作成

GitHub で空のリポジトリを作成してからローカルに clone します。

``` sh
# リポジトリを clone
git clone git@github.com:your-username/your-repo.git
cd your-repo

# uv で初期化
uv init

# quarto-cli をインストール
uv add quarto-cli
```

### 4.3. pyproject.toml

<div class="code-with-filename">

**pyproject.toml**

``` toml
[project]
name = "your-repo"
version = "0.1.0"
description = "Quarto intro project"
requires-python = ">=3.14"
dependencies = [
  "quarto-cli",
]
```

</div>

## 5. プロジェクト構成

quarto-intro リポジトリの構成は以下の通りです。

``` sh
./
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── export-to-html.yaml
│       └── publish.yaml
├── .gitignore
├── .nojekyll
├── _quarto.yml
├── assets/
│   └── common/
│       └── title-background.jpg
├── blog/
│   ├── index.qmd
│   └── 2024-08-25-test1.qmd
├── index.qmd
├── pyproject.toml
├── slides/
│   ├── index.qmd
│   └── 2025-05-05-initial-slide.qmd
└── uv.lock
```

### 5.1. `_quarto.yml`

プロジェクトの設定を記述するファイルです。

<div class="code-with-filename">

**\_quarto.yml**

``` yaml
project:
  type: website
  output-dir: "_site"

date-format: iso

website:
  title: "quarto-intro"
```

</div>

### 5.2. `.gitignore`

<div class="code-with-filename">

**.gitignore**

``` sh
/.quarto/
/_site/
/_extensions/

**/*.quarto_ipynb
```

</div>

### 5.3. `index.qmd`

トップページを作成するためのファイルです。

<div class="code-with-filename">

**index.qmd**

``` markdown
---
title: "quarto-intro"
listing:
  contents:
    - "blog"
    - "slides"
  exclude:
    filename: "index.qmd"
  sort:
    - "date desc"
---

- [ブログ記事一覧](./blog)
- [スライド一覧](./slides)
```

</div>

## 6. ブログ記事の作成

`blog/` ディレクトリに `.qmd` ファイルを作成します。

### 6.1. `blog/index.qmd`

<div class="code-with-filename">

**blog/index.qmd**

``` markdown
---
title: ブログ記事一覧
listing:
  contents:
    - "."
  sort:
    - "date desc"
---
```

</div>

### 6.2. ブログ記事の例

<div class="code-with-filename">

**blog/2024-08-25-test1.qmd**

``` markdown
---
title: test1
date: 2024-08-25
---

ブログ記事の本文です。
```

</div>

## 7. スライドの作成

Quarto は reveal.js 形式のスライドを作成できます。

### 7.1. `slides/index.qmd`

<div class="code-with-filename">

**slides/index.qmd**

``` markdown
---
title: スライド一覧
listing:
  contents:
    - "."
  sort:
    - "date desc"
---
```

</div>

### 7.2. スライドの例

<div class="code-with-filename">

**slides/2025-05-05-initial-slide.qmd**

``` markdown
---
title: スライドタイトル
author: uma-chan
date: 2025-05-05
format:
  revealjs:
    slide-level: 3
    slide-number: true
---

## セクション1

### スライド1

本文

### スライド2

本文

## セクション2

### スライド3

本文
```

</div>

`##` でセクションタイトルのスライド、`###`
で通常のスライドを区切ります。

## 8. ローカルでプレビュー

``` sh
uv run quarto preview
```

ブラウザでリアルタイムにプレビューしながら編集できます。

## 9. GitHub Pages への公開

GitHub Actions を使って GitHub Pages に自動デプロイします。

### 9.1. 初回デプロイ

初回はローカルから以下のコマンドを実行して `gh-pages`
ブランチを作成します。

``` sh
uv run quarto publish gh-pages
```

### 9.2. `publish.yaml`

2回目以降は GitHub Actions で自動デプロイされます。

<div class="code-with-filename">

**.github/workflows/publish.yaml**

``` yaml
name: Quarto Publish
run-name: ${{ github.event_name }} on ${{ github.ref_name }} by @${{ github.actor }}

on:
  workflow_dispatch:
  push:
    branches: main

permissions: {}

defaults:
  run:
    shell: bash

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    permissions:
      contents: write

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Quarto
        uses: quarto-dev/quarto-actions/setup@v2

      - name: Render and Publish
        uses: quarto-dev/quarto-actions/publish@v2
        with:
          target: gh-pages
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

</div>

## 10. HTML ファイルのエクスポート

GitHub Pages を作成しない場合も、HTML ファイルを `html`
ブランチ生成するようなデプロイも可能です。

### 10.1. `export-to-html.yaml`

<div class="code-with-filename">

**.github/workflows/export-to-html.yaml**

``` yaml
name: Export to HTML
run-name: ${{ github.event_name }} on ${{ github.ref_name }} by @${{ github.actor }}

on:
  workflow_dispatch:
  push:
    branches: main

permissions: {}

defaults:
  run:
    shell: bash

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  export-html:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    permissions:
      contents: write

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Quarto
        uses: quarto-dev/quarto-actions/setup@v2

      - name: Render Quarto Website
        run: |
          quarto render

      - name: Deploy to HTML branch
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: _site
          branch: html
          clean: true
```

</div>

### 10.2. HTML ファイルの取得方法

1.  GitHub で `html` ブランチに切り替え
2.  Code \> Download ZIP でダウンロード
3.  または `git checkout html && git pull`

## 11. Dependabot の設定

GitHub Actions と uv のパッケージを自動で更新するために Dependabot
を設定します。

<div class="code-with-filename">

**.github/dependabot.yml**

``` yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "uv"
    directory: "/"
    schedule:
      interval: "weekly"
```

</div>

これにより依存パッケージを適切に管理できます。

## 12. おわりに

uv と Quarto を使えば、Markdown
ライクな記法でブログやスライドを簡単に作成できます。

テンプレートリポジトリを参考にして自分だけのサイトを作ってみてください。

<https://github.com/i9wa4/quarto-intro>

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-12-15-uv-quarto-intro.html&text=uv%20%2B%20Quarto%20%E3%81%A7%E3%83%96%E3%83%AD%E3%82%B0%E3%82%84%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89%E3%82%92%E4%BD%9C%E6%88%90%E3%81%97%E3%81%A6%20GitHub%20Pages%20%E3%81%A7%E5%85%AC%E9%96%8B%E3%81%99%E3%82%8B%20%28HTML%20%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%88%E3%81%AB%E3%82%82%E5%AF%BE%E5%BF%9C%29%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=uv%20%2B%20Quarto%20%E3%81%A7%E3%83%96%E3%83%AD%E3%82%B0%E3%82%84%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89%E3%82%92%E4%BD%9C%E6%88%90%E3%81%97%E3%81%A6%20GitHub%20Pages%20%E3%81%A7%E5%85%AC%E9%96%8B%E3%81%99%E3%82%8B%20%28HTML%20%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%88%E3%81%AB%E3%82%82%E5%AF%BE%E5%BF%9C%29%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-12-15-uv-quarto-intro.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-12-15-uv-quarto-intro.html&title=uv%20%2B%20Quarto%20%E3%81%A7%E3%83%96%E3%83%AD%E3%82%B0%E3%82%84%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89%E3%82%92%E4%BD%9C%E6%88%90%E3%81%97%E3%81%A6%20GitHub%20Pages%20%E3%81%A7%E5%85%AC%E9%96%8B%E3%81%99%E3%82%8B%20%28HTML%20%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%88%E3%81%AB%E3%82%82%E5%AF%BE%E5%BF%9C%29%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
