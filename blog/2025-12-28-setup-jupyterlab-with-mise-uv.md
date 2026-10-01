# mise + uv で JupyterLab 環境をセットアップする
uma-chan
2025-12-28

## 1. はじめに

最近 mise と uv が好きで、色んな切り口でこの話をしたいです。

なので JupyterLab 環境セットアップ手順も書きます。

## 2. 環境構築手順

### 2.1. 事前準備

mise をインストールしておきます。

<https://mise.jdx.dev/getting-started.html>

### 2.2. プロジェクト作成

まずディレクトリもしくは Git リポジトリを作成します。

``` bash
mkdir jupyterlab-project
```

### 2.3. mise セットアップ

mise.toml ファイルを作成します。

``` bash
cd jupyterlab-project
```

``` bash
touch mise.toml
```

mise.toml を作成するとエラーが出るので `mise trust` しておきます。

``` bash
mise trust
```

mise.toml の内容は以下にしておきます。

<div class="code-with-filename">

**mise.toml**

``` toml
[tools]
uv = "latest"

[tasks.jupyter]
description = "Start JupyterLab"
run = "mise exec -- uv run jupyter-lab"
```

</div>

mise.toml に記述したツールをインストールします。

``` bash
mise install
```

### 2.4. uv セットアップ

以下のように uv プロジェクトを初期化します。

``` bash
uv init
```

### 2.5. JupyterLab 追加

``` bash
uv add jupyterlab
```

### 2.6. JupyterLab 起動

以下のコマンドで JupyterLab を起動します。

``` bash
mise run jupyter
```

ブラウザが自動的に開いて JupyterLab が起動しているはず！

### 2.7. ライブラリを追加したい場合

``` bash
uv add numpy pandas matplotlib
```

## 3. おまけ

既存のプロジェクトを uv 移行することが多くて実際はあまり `uv init`
を使ってませんでした。

そこで `src/`
ディレクトリを伴う初期化ってどうするんだろうとふと思って調べたら以下の記事が参考になりました。

[Python プロジェクト管理したくて uv に触れてみたメモ \#初心者 -
Qiita](https://qiita.com/0xmks/items/f5a4fcac81714ac2f803)

``` bash
uv init --lib
```

これでいけますね！次からちゃんと活用していきます。

## 4. おわりに

mise も uv も便利！

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-12-28-setup-jupyterlab-with-mise-uv.html&text=mise%20%2B%20uv%20%E3%81%A7%20JupyterLab%20%E7%92%B0%E5%A2%83%E3%82%92%E3%82%BB%E3%83%83%E3%83%88%E3%82%A2%E3%83%83%E3%83%97%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=mise%20%2B%20uv%20%E3%81%A7%20JupyterLab%20%E7%92%B0%E5%A2%83%E3%82%92%E3%82%BB%E3%83%83%E3%83%88%E3%82%A2%E3%83%83%E3%83%97%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-12-28-setup-jupyterlab-with-mise-uv.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-12-28-setup-jupyterlab-with-mise-uv.html&title=mise%20%2B%20uv%20%E3%81%A7%20JupyterLab%20%E7%92%B0%E5%A2%83%E3%82%92%E3%82%BB%E3%83%83%E3%83%88%E3%82%A2%E3%83%83%E3%83%97%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
