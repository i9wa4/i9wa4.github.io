# Markdown ライクな Quarto でブログやスライドを作って GitHub Pages
で公開する
uma-chan
2024-08-25

> [!WARNING]
>
> ### Deprecated
>
> この記事の内容は古くなっています。最新の情報は以下の記事を参照してください。
>
> [uv + Quarto でブログやスライドを作成して GitHub Pages で公開する
> (HTML エクスポートにも対応)](https://i9wa4.github.io/2025-12-15-uv-quarto-intro.md)

GitHub でブログやスライドを管理したい方にオススメな Quarto による GitHub
Pages 公開手順を紹介していきます。

スライド管理に興味がない方は適宜スライドに関する記述を無視しながら読み進めてください。

ここでは以下のドキュメントの手順をなぞりつつ、ブログ記事とスライドを管理するためのプロジェクト構成を導入します。

[Quarto – GitHub
Pages](https://quarto.org/docs/publishing/github-pages.html)

## 1. 想定する読者

- Python の環境構築ができている方
- Git/GitHub 操作の説明がなくても問題ない方

## 2. 事前準備

### 2.1. Quarto のインストール

まずは Quarto をインストールしておきましょう。

``` sh
$ pip install quarto-cli
```

なぜか公式ドキュメントではこのインストール方法は説明されていなかったのですが、これが一番簡単です。同じ疑問をもった方が以下で質問していました。

[Installing quarto-cli via pip · quarto-dev/quarto-cli · Discussion
\#8597](https://github.com/quarto-dev/quarto-cli/discussions/8597)

### 2.2. GitHub リポジトリ作成

任意の名前でリポジトリを作成しましょう。

私は GitHub リポジトリ <https://github.com/i9wa4/i9wa4.github.io>
を作成していて公開 URL は <https://i9wa4.github.io> になります。

ここではデモ用に <https://github.com/i9wa4/quarto-page>
というリポジトリを作成してみます。こちらの公開 URL は
<https://i9wa4.github.io/quarto-page> になります。

特にこだわりがなければリポジトリ名は `username.github.io`
でよいでしょう。

## 3. 基本構造を整える

作成したリポジトリをクローンして以下のファイルを作成します。

- `_quarto.yml`

  <div class="code-with-filename">

  **\_quarto.yml**
  ``` yml
  project:
    type: website
    output-dir: docs
  ```

  </div>

- `.nojelyll`

  空ファイルなので下記コマンドで作成します。

  ``` sh
  $ touch .nojekyll
  ```

- `.gitignore`

  <div class="code-with-filename">

  **.gitignore**
  ``` txt
  /.quarto/
  /docs/
  ```

  </div>

- `index.qmd`

  <div class="code-with-filename">

  **index.qmd**
  ``` md
  ---
  title: トップページ index.qmd
  ---

  本文
  ```

  </div>

作成できたら main ブランチに push しておきましょう。

## 4. 初回デプロイを行う

初回はローカル環境からデプロイを実行します。

指示に従って yes と入力すると `gh-pages`
ブランチが作成されて初回デプロイが完了します。

``` sh
$ quarto publish gh-pages
? Publish site to ssh://git@github.com/i9wa4/quarto-page using gh-pages? (Y/n) › Yes
```

## 5. 2回目以降のデプロイを自動化する

2回目以降のデプロイは以下のファイルを作成しておくことで GitHub Actions
に任せることができます。

<div class="code-with-filename">

**.github/workflows/publish.yml**

``` yml
on:
  workflow_dispatch:
  push:
    branches: main

name: Quarto Publish

jobs:
  build-deploy:
    runs-on: ubuntu-latest
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

## 6. ブログ記事とスライドのための構造を整える

以下の内容を push すると <https://i9wa4.github.io/quarto-page>
が完成します。

- `index.qmd`

  <div class="code-with-filename">

  **index.qmd**
  ``` md
  ---
  title: トップページ index.qmd
  listing:  # トップページにリスト表示させたくない場合は listing の設定は不要
    contents:
      - "blog"
      - "slides"  # トップページにスライドを表示させる場合
    exclude:
      filename: "index.qmd"
    sort:
      - "date desc"
  ---

  本文

  - [ブログ記事一覧](./blog)
  - [スライド一覧](./slides)

  ## ブログとスライドの新着一覧

  ブログやスライドなどディレクトリを分けている記事をまとめてリスト表示することができます。
  ```

  </div>

### 6.1. ブログ

- `blog/index.qmd`

  <div class="code-with-filename">

  **blog/index.qmd**
  ``` md
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

- `blog/2024-08-25-test1.qmd`

  <div class="code-with-filename">

  **blog/2024-08-25-test1.qmd**
  ``` md
  ---
  title: test1
  date: 2024-08-25
  ---

  1行目

  ファイル名の先頭に日付をつけておくと管理しやすいですが必須ではありません。
  ```

  </div>

- `blog/test2.qmd`

  <div class="code-with-filename">

  **blog/test2.qmd**
  ``` md
  ---
  title: test2
  date: 2024-08-26
  ---

  ここが1行目

  ファイル名の先頭に日付をつけておくと管理しやすいですが必須ではありません。
  ```

  </div>

### 6.2. スライド

- `slides/index.qmd`

  <div class="code-with-filename">

  **slides/index.qmd**
  ``` md
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

- `slides/test1-slide.qmd`

  <div class="code-with-filename">

  **slides/test1-slide.qmd**
  ``` md
  ---
  title: "test1-slide タイトル"
  author: i9wa4
  date: 2024-08-25
  format:
    revealjs:
      slide-level: 2
      slide-number: true
  ---

  本文

  ## サブタイトル1

  本文

  ## サブタイトル2

  本文
  ```

  </div>

- `slides/test2-slide.qmd`

  <div class="code-with-filename">

  **slides/test2-slide.qmd**
  ``` md
  ---
  title: "test2-slide タイトル"
  author: i9wa4
  date: 2024-08-25
  format:
    revealjs:
      slide-level: 2
      slide-number: true
  ---

  本文

  ## サブタイトル1

  本文

  ## サブタイトル2

  本文
  ```

  </div>

## 7. プレビューを確認しつつ編集する

プレビューを Web ブラウザで確認しながら編集が可能です。

``` sh
$ quarto preview
```

編集内容がリアルタイムに反映されるので執筆体験がとても良いです！

\[2024-08-26 追記\] プロジェクト構成によっては Firefox 以外の Web
ブラウザでうまくプレビューできない事象が発生している模様。

[Quarto preview only loading homepage in Firefox · Issue \#3045 ·
quarto-dev/quarto-cli](https://github.com/quarto-dev/quarto-cli/issues/3045)

遭遇した場合は以下のコマンドで `docs/` 配下に都度 html
ファイルを作成する、もしくは Firefox を使う、で対処しましょう。

``` sh
$ quarto render
```

## 8. おわりに

もっと色々といじっていきたい方は以下を参考にしてみるとよいでしょう。

- Quarto 公式
  - ページ <https://quarto.org>
  - リポジトリ <https://github.com/quarto-dev/quarto-web>
- i9wa4 の GitHub Pages
  - ページ <https://i9wa4.github.io>
  - リポジトリ <https://github.com/i9wa4/i9wa4.github.io>

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-08-25-publishing-github-pages-with-quarto.html&text=Markdown%20%E3%83%A9%E3%82%A4%E3%82%AF%E3%81%AA%20Quarto%20%E3%81%A7%E3%83%96%E3%83%AD%E3%82%B0%E3%82%84%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%A6%20GitHub%20Pages%20%E3%81%A7%E5%85%AC%E9%96%8B%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Markdown%20%E3%83%A9%E3%82%A4%E3%82%AF%E3%81%AA%20Quarto%20%E3%81%A7%E3%83%96%E3%83%AD%E3%82%B0%E3%82%84%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%A6%20GitHub%20Pages%20%E3%81%A7%E5%85%AC%E9%96%8B%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-08-25-publishing-github-pages-with-quarto.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-08-25-publishing-github-pages-with-quarto.html&title=Markdown%20%E3%83%A9%E3%82%A4%E3%82%AF%E3%81%AA%20Quarto%20%E3%81%A7%E3%83%96%E3%83%AD%E3%82%B0%E3%82%84%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%A6%20GitHub%20Pages%20%E3%81%A7%E5%85%AC%E9%96%8B%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
