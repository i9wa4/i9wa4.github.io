---
title: "データ分析を促進する dbt incremental モデル設計 ― 全期間追跡の低コスト化"
emoji: "📊"
type: "tech"
topics:
  - "bigquery"
  - "dbt"
published: true
published_at: 2025-10-31 07:00
publication_name: "pivotmedia"
---

## 1. はじめに

[ビジネス映像メディア「PIVOT」](https://pivotmedia.co.jp/app) データエンジニアの uma-chan です。

私はデータエンジニアとして、データ利用を促進できるような基盤を作ることを重要視しています。

今回はそれを念頭に置きつつ全期間のユーザー行動を低コストで追跡できる dbt モデル [^1] を設計した話を紹介します。このモデルを足がかりに、様々な時間軸での分析を促進できればと考えています。

## 2. 対象読者

- dbt の incremental モデルの実践的な設計パターンを知りたい方
- BigQuery などの DWH でコスト最適化に取り組んでいる方
- GA4 のユーザーID統一（`user_pseudo_id` と `user_id` の紐付け）をしつつ長期間追跡を実現したい方

dbt に詳しくない方にも理解できるよう、仕組みの説明を交えながら紹介します。

## 3. 課題

ユーザーの流入元分析を実施する中で、以下のようなモデルを新規作成しようとしていました。

- 流入元別の継続率分析（初回訪問から N 週間後に再訪問したかなど）
- ユーザーの初回訪問から現状までの変化の追跡
- 長期的な視点でのユーザー獲得品質の評価

初期実装ではあまり深く考えずに以下のように実装したことで Out Of Memory (OOM) エラーとなりました。

- FIRST_VALUE/LAST_VALUE ウィンドウ関数で全期間データを走査
- 全ユーザーの全期間データをメモリに展開

## 4. 設計のポイント

必要以上に集計コストが増大することを避けるため、まず手始めに全期間を低コストで追跡する方法として「incremental（増分更新）に向いているモデル設計」を考えました。

### 4.1. dbt の設定

まず、dbt の設定で incremental モデルとして定義します。

```sql
{{
    config(
        materialized="incremental",    -- 増分更新モード
        unique_key="user_id",
        incremental_strategy="merge",  -- 既存ユーザーで差分があると UPDATE、新規ユーザーは INSERT
    )
}}
```

### 4.2. 集計期間の制御

`is_incremental()` を使って、full-refresh 時と incremental 時で処理するデータ期間を切り替えます。

```sql
base_events as (
    select user_id, date(event_datetime_jst) as event_date, event_datetime_jst
    from {{ ref("whs_action__ga") }}
    {% if is_incremental() %}
        where
            -- incremental 時は直近 N 日分のみ処理 (デフォルト3日)
            -- NOTE: date() 利用時のタイムゾーンの扱いに注意
            date(event_datetime_jst) >= date_sub(
                current_date("Asia/Tokyo"),
                interval {{ var("touch_lookback_days", 3) }} day
            )
    {% endif %}
)
```

平常時は incremental で直近3日分のデータを参照するだけなので、処理データ量が大幅に削減されます。

### 4.3. 初回訪問と最終訪問の管理

incremental 実行時は、直近3日間にアクティブなユーザーのみが処理対象となります。MERGE により unique_key が一致するレコードが UPDATE され、初回訪問は既存と比較して古い方を保持し、最終訪問は新しい値で上書きされます。

```sql
-- 集計期間内 (base_events) から初回訪問と最終訪問を集約
first_touch as (
    select
        user_id,
        array_agg(event_datetime_jst order by event_datetime_jst asc limit 1)[
            offset(0)
        ] as first_touch_time
    from base_events
    group by user_id
),

last_touch as (
    select
        user_id,
        array_agg(event_datetime_jst order by event_datetime_jst desc limit 1)[
            offset(0)
        ] as last_touch_time
    from base_events
    group by user_id
),

merged_touches as (
    select ft.user_id, ft.first_touch_time, lt.last_touch_time
    from first_touch ft
    left join last_touch lt on ft.user_id = lt.user_id
),

{% if is_incremental() %}
    -- 既存データを読み込み
    existing_data as (
        select user_id, first_touch_time
        from {{ this }}
        where user_id in (select distinct user_id from base_events)
    ),
{% endif %}

-- 最終的なマージ
select
    mt.user_id,
    {% if is_incremental() %}
        -- 初回訪問は既存と新規で古い方を保持
        case
            when
                ex.first_touch_time is not null
                and ex.first_touch_time <= mt.first_touch_time
            then ex.first_touch_time
            else mt.first_touch_time
        end as first_touch_time,
    {% else %} mt.first_touch_time,
    {% endif %}
    -- 最終訪問は常に新規データ (base_events 内の最新) を使用
    mt.last_touch_time
from merged_touches mt
{% if is_incremental() %}
    left join existing_data ex on mt.user_id = ex.user_id
{% endif %}
```

直近3日間にアクティブだったユーザーのレコードのみが最終的な SELECT 文でクエリされることとなります。
そして `incremental_strategy="merge"` の仕様により既存のデータとの差分があれば UPDATE されます。

:::message
この設計が incremental と相性が良いのは「初回訪問」「最終訪問」が冪等性を持つ（何度実行しても結果が同じ）ためです。既存データと新規データの比較だけで正しい結果が得られます。

逆に「累積の訪問回数」のような指標は incremental で単純実装すると再実行時に二重カウントされるなどの集計ズレの恐れがあります。この場合は過去データを都度参照する、あるいは集計済みの中間テーブルを用意するなどの対応が必要です。
:::

### 4.4. ユーザーIDの統一

本モデルでは、匿名訪問期間を含めた全期間のユーザー行動を追跡するため、GA4 の複数のIDを統一しています。

#### 4.4.1. GA4 のID体系

- ログイン前: `user_pseudo_id`（匿名ID、Cookie/デバイスベース）
- ログイン後: `user_id`（認証ID、アカウントベース）
- 同じユーザーでも時間軸やデバイスで異なるIDが付与される

#### 4.4.2. 統一の仕組み

マッピングテーブルで `user_pseudo_id` と `user_id` を紐付け、`COALESCE` で優先順位をつけて統一することで、匿名訪問からログイン後まで同一ユーザーとして追跡できます。

#### 4.4.3. incremental における制約

匿名訪問から `touch_lookback_days` を超える期間経過後にログインすると、古い匿名IDのレコードが残り重複データとなります。
ただし、本モデルはログイン済みユーザーの動向追跡が主目的のため、低頻度の full-refresh で対応すれば十分です。

#### 4.4.4. 既存データマートとの違い

既存のユーザー関連モデル（`whs_user__user_master` など）は登録ユーザー (`user_id`) のみを対象としており、匿名訪問期間を含めた全期間追跡はこのモデルが初めての実装となります。このユーザーID統一の仕組みは隠れた成果と言えます。

### 4.5. その他の設計ポイント

同じ要領で以下もカラムとして追加できます。

- 初回訪問・最終訪問イベントに紐づく情報
  - 訪問時刻、流入元、プラットフォーム、流入経路など

## 5. 成果

### 5.1. 技術的な成果

- データスキャン量は約 1/50 に削減
  - full-refresh: 24.6 GiB
  - incremental: 約 500 MiB (3日分の差分)
  - 利用する DWH が BigQuery のためスキャン量削減は重要
- OOM 発生なし
- 更新コストが低い（1日に複数回の更新処理実行でも問題ないし、失敗しても次の更新でリカバリ可能）

### 5.2. データ分析への貢献

- 本来は膨大なデータを集計しないと得られないクエリ結果を低コストで得られる
- 分析者が気軽に長期間のユーザー行動を追跡できるようになった
  - 様々な時間軸での分析の需要を促進し、モデルを更に充実させる好循環を目指す

## 6. おわりに

初回訪問と最終訪問という特定の指標を中心に据えて全期間追跡を実現するために、「incremental に向いているモデル設計」という基本を押さえることにしました。

OOM 解消だけでなく、低コストでの運用や擬似的なユーザーのユニークリストという副次的な成果も得られました。

今回のモデルは、長期間の分析に目を向けるための第一歩として導入しました。このモデルを基礎として、様々な時間軸でのユーザー行動分析を円滑に進められる一助になれればと思います。

[^1]: dbt では SELECT 文で定義された変換ロジックのことをモデルと呼び、実行すると BigQuery などの DWH 上のテーブルやビューが生成されます。
