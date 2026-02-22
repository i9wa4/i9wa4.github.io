# 技術系 Tips まとめ
uma-chan
2024-07-15

たまに使うけど忘れてしまうような技術系の小ネタ (コマンド・設定)
まとめ記事です。

分量が増えてきた分野は別記事に切り出すかもしれません。

## 1. Git

``` sh
# よく使うコマンド
git add -n .
git log --graph
git diff --name-only HEAD HEAD~2
git diff ID1 ID2 filename
git difftool ID1 ID2
git show ID

git reflog
git rebase

# リモートリポジトリ作成
git init --bare --shared
git remote add origin url
git clone url
```

## 2. PostgreSQL

``` sh
# 起動～データベースへのアクセス
pg_ctl restart
psql -U postgres -d db_name

pg_ctl restart
psql -U postgres
CREATE DATABASE db_name;
\c db_name
CREATE SCHEMA sc_name;
```

## 3. Google Cloud CLI (gcloud CLI)

``` sh
# keyfile 登録からテーブル確認まで
gcloud auth activate-service-account --key-file ***.json
gcloud auth list
gcloud set account ***
bq --project_id=aaaaa ls
bq --project_id=aaaaa ls dataset_name
bq --project_id=aaaaa show dataset_name.table_name
bq --project_id=aaaaa head --max_rows 5 dataset_name.table_name
```

``` sh
# ログイン
gcloud auth login
```

## 4. Excel

### 4.1. Excel VBA

- アドイン追加先
  - `%USERPROFILE%\AppData\Roaming\Microsoft\AddIns`

### 4.2. Excel 関数

- シート名を記載したセルB2を利用したハイパーリンク作成
  - `=HYPERLINK("#'"&B2&"'!$A$1",B2)`

## 5. Word

### 5.1. Normal.dotm 作成

1.  `%APPDATA%\Microsoft\Templates\Normal.dotm` 削除
2.  デザインを作成し既定に設定する
    - テーマ設定
      - 見出し: 游ゴシック Arial
      - 本文: 游ゴシック Medium Arial
    - アウトライン –\> 新しいアウトラインの定義 –\> オプション –\>
      レベルと対応付ける見出しスタイル

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-07-15-technical-tips.html&text=%E6%8A%80%E8%A1%93%E7%B3%BB%20Tips%20%E3%81%BE%E3%81%A8%E3%82%81%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=%E6%8A%80%E8%A1%93%E7%B3%BB%20Tips%20%E3%81%BE%E3%81%A8%E3%82%81%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-07-15-technical-tips.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-07-15-technical-tips.html&title=%E6%8A%80%E8%A1%93%E7%B3%BB%20Tips%20%E3%81%BE%E3%81%A8%E3%82%81%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
