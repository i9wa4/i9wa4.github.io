# 職務経歴書 ― 馬渡 大樹


馬渡 大樹

データエンジニアリングチームマネージャー・MLOpsエンジニア

[Website](https://i9wa4.github.io) \|
[LinkedIn](https://www.linkedin.com/in/daikm) \|
[GitHub](https://github.com/i9wa4)

職務経歴書 ([Website](https://i9wa4.github.io/resume/index.html),
[PDF](https://i9wa4.github.io/resume/index.pdf)) \| Resume
([Website](https://i9wa4.github.io/en/resume/index.html),
[PDF](https://i9wa4.github.io/en/resume/index.pdf))

## 1. 職務要約

データ基盤とMLOpsの領域で、チームマネジメントと実務の両面に取り組んでいます。ソフトウェアエンジニアリング10年以上、データエンジニアリングと機械学習運用4年以上の経験を持ち、現職GENDAではデータエンジニアチームのマネージャーとして、グループ横断のデータ利活用、データマート・ダッシュボード提供、MLOps、関係者調整、チーム運営をリードしています。事業部、営業、データサイエンス、エンジニアリングの要件を、信頼できるデータ基盤、分析ワークフロー、開発者体験へ落とし込み、継続的に運用できる形で届けることを得意としています。Databricks、dbt、Snowflake、BigQuery、AWS
/ Google
Cloud、AI活用、Notebookツール開発、権限・ガバナンス、開発ワークフローを組み合わせ、データ活用と機械学習運用を支える基盤づくりに取り組んでいます。

## 2. コアスキル

- データ基盤・分析基盤 - Databricks、Snowflake、BigQuery、dbt Core /
  Cloud、Airflow / MWAA、データマート、ダッシュボード
- クラウド・インフラ - AWS、Google Cloud、Terraform、GitHub
  Actions、Docker
- MLOps・AI活用 - CI/CD、DataRobot、Snowpark ML、Databricks
  notebooks、Notebook tooling、MCP tooling、AI coding agent workflow
- 開発生産性・ガバナンス - Nix /
  mise、Ruff、レビュー前提のデプロイ、権限設計、データガバナンス、ドキュメンテーション
- 組織運営 -
  チームマネジメント、コードレビュー、採用、1on1、技術移譲、データチーム運営
- エンジニアリング基盤 - Python、SQL、Shell Script、C、C++

## 3. 職務経歴

### 3.1. 株式会社GENDA \| データエンジニア / MLOpsエンジニア / データエンジニアチームマネージャー

2024/11 - 現在 \| 正社員

- グループ会社のデータ利活用を担当し、M&Aで拡大する事業の管理・営業・現場要件をデータ基盤、データマート、ダッシュボード、分析ワークフローへ接続しています。
- 2026/04よりデータエンジニアチームのマネージャーに就任し、進捗管理、コードレビュー、1on1、採用活動、技術移譲の仕組み化を担当しています。
- カラオケ事業会社のデータ利活用では、経営・営業向け帳票9件、データ取込DAG
  13件、既存ダッシュボード37件を依存関係と移行優先度を含むロードマップに整理しました。
- 店舗分析資料の生成プロセスを改善し、所要時間を約1-2日から約20分へ短縮しました。
- CI/CD、Ruff、mise、レビュー前提のデプロイ、Databricksへのスコアリング移行によりMLOpsを改善しました。
- AI-readyなNotebook・開発ワークフローを改善し、データサイエンティストとデータエンジニアが安全に速く価値検証できる開発者体験の整備に貢献しました。

### 3.2. PIVOT株式会社 \| 業務委託データエンジニア

2025/06 - 現在 \| 業務委託

- KPIレポート、リファラル分析、GA4 /
  ULIZAトラッキング、パフォーマンス改善向けのBigQuery /
  dbtモデルを構築・改善しています。
- OOMを起こしていたウィンドウ関数中心のロジックをJOIN中心の設計へ変更し、主要モデルの実行時間を51-90分から数分へ短縮しました。
- GA4のユーザー同定・トラッキング継続性を整備し、匿名訪問からログイン後までを追跡する全期間ユーザー分析のincrementalモデルを実装しました。
- 安定したマージキー、パーティション、クラスタリング設定によりBigQuery
  MERGEの効率を改善しました。

### 3.3. 株式会社hacomono \| データエンジニア

2024/04 - 2024/10 \| 正社員

- 一人データエンジニアとして、BigQuery、Embulk、AWS、Google
  Cloud、Terraform、Terragruntを用いた顧客向け・社内向けDWH転送運用、インフラ
  / IaC変更、提供支援を担当しました。
- RDSメトリクス、転送ログ、Embulkチューニングによりバッチ転送の安定性を改善しました。
- BigQuery権限を手動付与からTerraform管理のdatasetレベル権限へ移行しました。
- Google Cloud DatastreamによるRDS
  MySQLからBigQueryへのリアルタイム転送を検証し、障害・復旧時の挙動を文書化しました。

### 3.4. 株式会社シイエヌエス北海道 \| データエンジニア / MLOpsエンジニア

2022/04 - 2024/03 \| 正社員

- 顧客行動予測ワークフロー50本をオンプレミス環境からAWS、Snowflake、DataRobotへ移行しました。
- Snowflake Python APIとJupyter Notebook中心のワークフローからdbt
  Coreへ移行し、依存関係の可視性、可読性、保守性を改善しました。
- DataRobotからSnowpark
  MLへの移行をコスト、性能、セキュリティの観点で調査し、小規模な検証チームをリードしました。
- 約200店舗を対象としたベイズ統計ベースの来店客数予測処理を並列実行改善により約2日で完了させ、4日以内という要件を満たしました。

### 3.5. 株式会社新光商事LSIデザインセンター \| 組込ソフトウェアエンジニア

2018/08 - 2022/03 \| 正社員

- 車載・産業機器向け組込ファームウェアとして、トラクション制御更新機能、噴霧器インバータ制御、操作コントローラーを要件整理から設計、実装、テストまで担当しました。
- C / アセンブラ、Renesas / GHS系ツールチェーン、RH850 /
  RL78、QAC、winAMSを用いた開発に従事しました。
- 5名が扱う30件以上のテスト仕様書整形を自動化し、Pythonで顧客向け分析資料を作成し、CAN通信講座も担当しました。

### 3.6. オークマ株式会社 \| Windowsアプリケーションエンジニア

2016/04 - 2018/07 \| 正社員

- CNC工作機械向けWindows CAD /
  CAMアプリケーションについて、UI要件、テスト、ユーザー問い合わせ、不具合対応、性能改善を担当しました。
- 品質保証、業務ドメイン理解、ユーザー向けソフトウェア保守の基礎を身につけました。

## 4. 学歴

- 北海道大学 理学部 数学科 卒業

## 5. 資格

- 2023/04: 統計検定2級
- 2015/03: TOEIC スコア 805 <!-- - 2012/11: 普通自動車第一種運転免許 -->

## 6. 登壇・執筆

### 6.1. 登壇

- 2026/03/06:
  [Databricksで堅牢なコードを書く上での課題とその解決](https://i9wa4.github.io/slides/2026-03-06-kenro-py.html)
- 2026/01/26: [Mosaic AI
  Gatewayでコーディングエージェントを配るための運用Tips](https://speakerdeck.com/genda/jedai-2026-meetup-ai-coding-mawatari)
- 2025/12/23:
  [M&Aで拡大し続けるGENDAのデータ活用を促すためのDatabricks権限管理](https://speakerdeck.com/genda/aeon-tech-hub-22-mawatari)
- 2025/12/12: [Databricks向けJupyter
  Kernelでデータサイエンティストの開発環境をAI-Readyにする](https://speakerdeck.com/genda/data-ai-world-tour-tokyo-after-party-mawatari)
- 2025/11/07: [GENDA の機械学習環境を AWS から Databricks
  に移行してみた](https://i9wa4.github.io/slides/2025-11-07-tamesare-data-sapporo-uma-chan.html)
- 2025/05/22: [Cursorのおすすめ設定 &
  Cursorにデータ分析を任せる方法](https://i9wa4.github.io/slides/2025-05-22-midas-cursor-tips.html)

### 6.2. 執筆

- 2026/03/24:
  [GENDAデータ基盤へのDatabricks導入時の状況と現在](https://findy-tools.io/products/databricks/11/164)
- 2025/10/31: [データ分析を促進する dbt incremental モデル設計 ―
  全期間追跡の低コスト化](https://zenn.dev/pivotmedia/articles/pivot-incremental-friendly-dbt-model)
- 2025/09/01:
  [GENDAのデータサイエンティスト開発体験向上の取り組み紹介―AWS
  ECSからDatabricksへの移行](https://zenn.dev/genda_jp/articles/724a597e8f18ff)
- 2025/06/25:
  [成長を支えるハブとなりたい。データドリブンな組織を加速させるデータ基盤とMLOps｜GENDA](https://note.com/genda_jp/n/n94def6811d47)
- 2024/10/08: [39社のデータ基盤アーキテクチャ特集 -
  ツールの技術選定のポイントと活用術 - Findy
  Tools](https://findy-tools.io/articles/data-review/28)
- 2024/08/21:
  [株式会社hacomonoのBigQuery導入事例](https://findy-tools.io/products/bigquery/49/231)
- 2024/07/02: [hacomonoデータ基盤におけるデータ転送の課題と今後の対応 -
  hacomono TECH
  BLOG](https://techblog.hacomono.jp/entry/2024/07/02/1100)

### 6.3. 受賞

- 2026/03/24: JEDAI Order 2026 Knight
  - [JEDAI Order 2026 受賞者一覧 \| Databricks User
    Groups](https://usergroups.databricks.com/v0/forum/databricks-japan-user-group-27/topic/jedai-order-2026-受賞者一覧-118/)
  - [データマネジメント部 マネージャーの馬渡がJEDAI Order
    2026に選出](https://zenn.dev/genda_jp/articles/e3f6da7d2224c1)
