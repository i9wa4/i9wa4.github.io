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
