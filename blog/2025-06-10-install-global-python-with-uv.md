# uv で Python のグローバルインストールを行う
uma-chan
2025-06-10

<div class= "page-columns page-rows-contents page-layout-article"><div class="social-share"><a href="https://twitter.com/share?url=https://i9wa4.github.io/blog/2025-06-10-install-global-python-with-uv.html&text=uv で Python のグローバルインストールを行う" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=uv で Python のグローバルインストールを行う https://i9wa4.github.io/blog/2025-06-10-install-global-python-with-uv.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https://i9wa4.github.io/blog/2025-06-10-install-global-python-with-uv.html&title=uv で Python のグローバルインストールを行う" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div></div>

## 1. はじめに

Python 環境管理に uv を使い始めて以来 pyenv
が不要になりアンインストールしたのですが、スポット的に Python
のグローバルインストールが必要になったので uv
での手順をメモしておきます。

## 2. 手順

[Python versions \|
uv](https://docs.astral.sh/uv/concepts/python-versions/#installing-python-executables)

``` sh
$ uv python install 3.12 --default --preview
```
