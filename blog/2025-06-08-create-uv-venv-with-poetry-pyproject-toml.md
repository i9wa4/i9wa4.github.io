# Poetry の pyproject.toml を使って uv で .venv を作成する
uma-chan
2025-06-08

## 1. はじめに

最近 Python の仮想環境構築に uv を利用し始めて以来 pyenv
を削除してしまったりとすっかり uv が気に入っています。

とはいえ全てのプロジェクトを直ちに uv
へ移行するのも全員の学習コストがかかるため難しいと思います。

過渡期の対応としてローカルで Poetry の pyproject.toml を使用して uv
で仮想環境構築する方法をメモしておきます。

## 2. 仮想環境構築手順

``` sh
# .venv を作成する
# このとき .python-version に記載された Python で構築される
$ uv venv
Using CPython 3.12.1
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate

# 仮想環境にパッケージをインストールする
$ uv pip install --requirement pyproject.toml
```

## 3. おわりに

`$ uv pip install --requirement pyproject.toml` ここ爆速すぎて uv
が好きになると思うのでちょっとやってみてほしいです。

ちなみにこの方法だと poetry.lock
に従うわけではないので完全に同じ環境を再現するわけではありません。

とはいえほとんど齟齬のない環境を構築できます。

しばらくすると忘れそうなのでメモ代わりの記事でした。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-08-create-uv-venv-with-poetry-pyproject-toml.html&text=Poetry%20%E3%81%AE%20pyproject.toml%20%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%20uv%20%E3%81%A7%20.venv%20%E3%82%92%E4%BD%9C%E6%88%90%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Poetry%20%E3%81%AE%20pyproject.toml%20%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%20uv%20%E3%81%A7%20.venv%20%E3%82%92%E4%BD%9C%E6%88%90%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-08-create-uv-venv-with-poetry-pyproject-toml.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-08-create-uv-venv-with-poetry-pyproject-toml.html&title=Poetry%20%E3%81%AE%20pyproject.toml%20%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%20uv%20%E3%81%A7%20.venv%20%E3%82%92%E4%BD%9C%E6%88%90%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
