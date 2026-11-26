# BigQuery で dbt incremental モデルのパフォーマンス改善をしてみた
uma-chan
2025-09-28

## 1. はじめに

ログ同士を突き合わせる dbt モデルの dbt run
実行時間が1時間を超えていたため、BigQuery
の特性を活かしつつ実行時間を40分短縮した流れを紹介します。対象はイミューターなログを扱うモデルで、過去データの更新を考慮しない前提を置ける構造でした。

## 2. 当初の課題

- incremental_strategy が merge で、ターゲットテーブル全体を走査していた
- unique_key が15列と多く、結合条件が複雑であった
- 参照元テーブルが期間条件なしで FULL OUTER JOIN
  され、中間結果が肥大化していた

## 3. 実施した改善策

### 3.1. incremental_strategy の切り替え

- merge から insert_overwrite
  へ変更し、対象パーティションのみを差し替えた

### 3.2. パーティションプルーニングの徹底

- vars で渡した日付範囲を JOIN
  前のフィルタで適用し、読み取り対象を日次で限定した
- パーティション指定を日単位で明示化し、BigQuery
  のスキャン範囲を事前に制限した

### 3.3. 重複除去ロジックの簡素化

- 15列のunique_key指定を ROW_NUMBER() による決定的な重複除去に変更した
- 複雑なMERGE処理からシンプルな重複除去ロジックへ簡素化した

## 4. 効果と検証

- dbt run 実行時間は1時間超えから40分短縮できた
- 同期間の surrogate key 単位で件数と代表値を比較し整合性を確認できた
- 修正前後で更新内容に差異がないことを確認できた
  (ログデータの特性上そうなる)

## 5. おわりに

BigQuery の挙動と dbt の incremental
モデルへの習熟度がまだまだなので引き続き学びを深めます。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-09-28-bigquery-dbt-incremental-intro.html&text=BigQuery%20%E3%81%A7%20dbt%20incremental%20%E3%83%A2%E3%83%87%E3%83%AB%E3%81%AE%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9%E6%94%B9%E5%96%84%E3%82%92%E3%81%97%E3%81%A6%E3%81%BF%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=BigQuery%20%E3%81%A7%20dbt%20incremental%20%E3%83%A2%E3%83%87%E3%83%AB%E3%81%AE%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9%E6%94%B9%E5%96%84%E3%82%92%E3%81%97%E3%81%A6%E3%81%BF%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-09-28-bigquery-dbt-incremental-intro.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-09-28-bigquery-dbt-incremental-intro.html&title=BigQuery%20%E3%81%A7%20dbt%20incremental%20%E3%83%A2%E3%83%87%E3%83%AB%E3%81%AE%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9%E6%94%B9%E5%96%84%E3%82%92%E3%81%97%E3%81%A6%E3%81%BF%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
