# Quarto による DataFrame の表示テスト
uma-chan
2024-09-08

Pandas の DataFrame
をウェブサイト一覧表作成に転用するための実験記事です。

以下のように使用すれば CSV
ファイルでタグを付与した形でウェブサイト一覧を管理できます。

## 1. ライブラリのインストール

``` py
#| include: true
!python3 -m pip install pandas
!python3 -m pip install --upgrade jinja2
```

## 2. 関数定義

``` py
#| include: true
import numpy as np
import pandas as pd

df_all = pd.read_csv('../assets/2024-09-08-quarto-df/quarto-df.csv')


def make_clickable(url, title):
    return f'<a href="{url}">{title}</a>'


def extract_tag(tag, df=df_all):
    _df = df[df['Tags'].str.contains(tag)].copy()

    # 欠損埋め
    _df = _df.fillna({'Date': '9999-12-31'})
    _df = _df.fillna('-')

    # HACK: __init__.py を強調させないためのワークアラウンド
    _df['Title'] = _df['Title'].replace(
            '__init__.py', '__ init __.py', regex=True
        )

    # 日付とクリック可能なページ名の表示
    _df = _df[['Date', 'Title', 'URL']].sort_values(
            ['Date', 'Title'], ascending=[False, True]
        )
    _df.index = np.arange(1, len(_df) + 1)
    _df['Website'] = _df.apply(
            lambda row: make_clickable(row['URL'], row['Title']), axis=1
        )
    _df = _df[['Date', 'Website']].to_html(escape=False, index=False)
    return _df
```

## 3. CSV 内容確認

``` py
!cat ../assets/2024-09-08-quarto-df/quarto-df.csv
```

## 4. TagA

``` py
#| code-fold: false
extract_tag('TagA')
```

## 5. TagB

``` py
#| code-fold: true
extract_tag('TagB')
```

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-09-08-quarto-dataframe-preview-test.html&text=Quarto%20%E3%81%AB%E3%82%88%E3%82%8B%20DataFrame%20%E3%81%AE%E8%A1%A8%E7%A4%BA%E3%83%86%E3%82%B9%E3%83%88%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Quarto%20%E3%81%AB%E3%82%88%E3%82%8B%20DataFrame%20%E3%81%AE%E8%A1%A8%E7%A4%BA%E3%83%86%E3%82%B9%E3%83%88%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-09-08-quarto-dataframe-preview-test.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-09-08-quarto-dataframe-preview-test.html&title=Quarto%20%E3%81%AB%E3%82%88%E3%82%8B%20DataFrame%20%E3%81%AE%E8%A1%A8%E7%A4%BA%E3%83%86%E3%82%B9%E3%83%88%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
