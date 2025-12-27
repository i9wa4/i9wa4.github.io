# ローカル dbt で BigQuery への認証を行う
uma-chan
2025-06-15

<div class= "page-columns page-rows-contents page-layout-article"><div class="social-share"><a href="https://twitter.com/share?url=https://i9wa4.github.io/blog/2025-06-15-dbt-bigquery-auth.html&text=ローカル dbt で BigQuery への認証を行う" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=ローカル dbt で BigQuery への認証を行う https://i9wa4.github.io/blog/2025-06-15-dbt-bigquery-auth.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https://i9wa4.github.io/blog/2025-06-15-dbt-bigquery-auth.html&title=ローカル dbt で BigQuery への認証を行う" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div></div>

## 1. はじめに

dbt も BigQuery も経験それなりにあるものの dbt x BigQuery
をやったことがなかったので認証方法を知ったのが今となります。

## 2. dbt のドキュメントを参照してみる

OAuth を使った認証方法は以下のドキュメントに記載されています。

<https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup#local-oauth-gcloud-setup>

ではあるのですが、実際のログイン方法として紹介されているコマンドは少し違うようで、代表的なものは以下のような感じです。

[dbt CoreでローカルからBigQueryを操作するためのセットアップ方法 \|
DevelopersIO](https://dev.classmethod.jp/articles/dbt-core-bigquery/)

記事でよく見かけるものを実行していきます。

## 3. 認証手順

### 3.1. profiles.yml の設定

以下のような記載が含まれていれば OK

`method: oauth` を指定していることがポイントです。

<div class="code-with-filename">

**~/.dbt/profiles.yml**

``` yml
my_dbt_project:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: my-google-cloud-project
      threads: 4
      schema: my_schema
```

</div>

### 3.2. アプリケーション向けのログイン

以下のコマンドにより dbt が Google Cloud の API
を呼び出せることになります。

``` sh
$ gcloud auth application-default login
```

## 4. おわりに

いま手元では1環境にしかログインしないのであまり深く理解していなくても大丈夫ですが、複数環境にログインする際にもうちょっと深く理解しておきます。
