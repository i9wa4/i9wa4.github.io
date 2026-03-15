# ローカル dbt で BigQuery への認証を行う
uma-chan
2025-06-15

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

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-15-dbt-bigquery-auth.html&text=%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%20dbt%20%E3%81%A7%20BigQuery%20%E3%81%B8%E3%81%AE%E8%AA%8D%E8%A8%BC%E3%82%92%E8%A1%8C%E3%81%86%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%20dbt%20%E3%81%A7%20BigQuery%20%E3%81%B8%E3%81%AE%E8%AA%8D%E8%A8%BC%E3%82%92%E8%A1%8C%E3%81%86%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-15-dbt-bigquery-auth.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-15-dbt-bigquery-auth.html&title=%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%20dbt%20%E3%81%A7%20BigQuery%20%E3%81%B8%E3%81%AE%E8%AA%8D%E8%A8%BC%E3%82%92%E8%A1%8C%E3%81%86%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
