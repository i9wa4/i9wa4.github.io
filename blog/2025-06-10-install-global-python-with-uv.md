# uv で Python のグローバルインストールを行う
uma-chan
2025-06-10

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

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-10-install-global-python-with-uv.html&text=uv%20%E3%81%A7%20Python%20%E3%81%AE%E3%82%B0%E3%83%AD%E3%83%BC%E3%83%90%E3%83%AB%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%82%92%E8%A1%8C%E3%81%86%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=uv%20%E3%81%A7%20Python%20%E3%81%AE%E3%82%B0%E3%83%AD%E3%83%BC%E3%83%90%E3%83%AB%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%82%92%E8%A1%8C%E3%81%86%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-10-install-global-python-with-uv.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-10-install-global-python-with-uv.html&title=uv%20%E3%81%A7%20Python%20%E3%81%AE%E3%82%B0%E3%83%AD%E3%83%BC%E3%83%90%E3%83%AB%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%82%92%E8%A1%8C%E3%81%86%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
