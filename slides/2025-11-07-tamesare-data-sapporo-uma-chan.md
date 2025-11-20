# GENDA の機械学習環境を AWS から Databricks に移行してみた
uma-chan
2025-11-07

<meta name="Hatena::Bookmark" content="nocomment" />

<script>
// Quartoが読み込むAnchorJSのデフォルトオプションを上書き
// window.quartoConfig が存在する場合はそこから設定を変更
window.addEventListener('load', function() {
  if (window.anchors) {
    // すでに初期化されている場合は設定を変更して再適用
    window.anchors.options.icon = '#';
    window.anchors.remove('.anchored');
    window.anchors.add('.anchored');
  }
});
</script>

## 1. はじめに

### 1.1. 自己紹介

<div style="display: flex; flex-direction: column; align-items: center; gap: 2em;">

<div style="text-align: left;">

uma-chan (馬渡 大樹 / Mawatari Daiki)

</div>

<div style="text-align: left;">

|                              |                                    |
|------------------------------|------------------------------------|
| Data Engineer/MLOps Engineer | [株式会社GENDA](https://genda.jp/) |

<!-- | Data Engineer | [PIVOT株式会社](https://pivot.inc/) | -->

</div>

<div style="text-align: center;">

好きなものたち

[<img
src="https://img.shields.io/badge/Vim-019733.svg?logo=vim&amp;logoColor=white"
style="vertical-align: middle;;height:1.5em" alt="Vim" />](https://www.vim.org/)
[<img
src="https://img.shields.io/badge/Neovim-57A143.svg?logo=neovim&amp;logoColor=white"
style="vertical-align: middle;;height:1.5em" alt="Neovim" />](https://neovim.io/)
[<img
src="https://img.shields.io/badge/tmux-1BB91F.svg?logo=tmux&amp;logoColor=white"
style="vertical-align: middle;;height:1.5em" alt="tmux" />](https://github.com/tmux/tmux)
[<img
src="https://img.shields.io/badge/Alacritty-F46D01.svg?logo=alacritty&amp;logoColor=white"
style="vertical-align: middle;;height:1.5em" alt="Alacritty" />](https://alacritty.org/)

</div>

<div style="text-align: center;">

[<img
src="https://img.shields.io/badge/@i9wa4-181717.svg?logo=github&amp;logoColor=white"
style="vertical-align: middle;;height:1.5em" alt="GitHub" />](https://github.com/i9wa4)
[<img
src="https://img.shields.io/badge/@i9wa4__-000000.svg?logo=x&amp;logoColor=white"
style="vertical-align: middle;;height:1.5em" alt="X" />](https://x.com/i9wa4_)
[<img
src="https://img.shields.io/badge/🔗_i9wa4.github.io-4285F4.svg?logoColor=white"
style="vertical-align: middle;;height:1.5em" alt="Website" />](https://i9wa4.github.io)

</div>

</div>

## 2. 入社時のAWS機械学習環境

### 2.1. 入社時のAWS機械学習環境: ECS中心の構成

<!-- 図の構成案:
- 左側: データサイエンティスト (開発者)
- 右側: AWS構成
  - GitHub Actions: Dockerイメージビルド (5分)
  - Amazon ECR: コンテナレジストリ
  - Amazon ECS: 機械学習コンテナ実行 (30-60分)
  - Amazon RDS: 推論結果保存
  - Amazon S3: データ保存
  - Snowflake: 共通データソース
  - CloudWatch Logs: ログ監視
- フロー: コード作成 → GitHub push → GitHub Actions → ECR → ECS → RDS
- 課題を赤文字で表示 (.pyファイル実行でREPLなし、ビルド5分、CloudWatch確認が大変)
-->

![](https://i9wa4.github.io/assets/2025-11-07-tamesare-data-sapporo-uma-chan/aws-ml-architecture.drawio.png)

### 2.2. 開発で感じた課題

<!-- 図の構成案:
- 3つの課題を吹き出しで表現
  1. .pyファイル実行でREPL環境なし (変数確認が困難)
  2. ビルド5分 + ECS実行30-60分 = 構文エラーでも15分以上待機
  3. CloudWatch Logsでログ確認が面倒
  4. インターン生がDocker/ECR/ECS/CloudWatch Logs理解に時間を費やす
- 中央に困っている開発者のアイコン
- 「1日10回の試行錯誤で2.5時間が無駄」を強調
-->

![](https://i9wa4.github.io/assets/2025-11-07-tamesare-data-sapporo-uma-chan/aws-ml-challenges.drawio.png)

## 3. Databricksへの移行

### 3.1. 移行後: Databricks 環境の構成

<!-- 図の構成案:
- 左側: データサイエンティスト (開発者)
- 右側: Databricks on AWS構成
  - Databricks Workspace: Notebook環境 (セル単位で即座実行)
  - Databricks Compute: 計算リソース (自動起動/停止)
  - Databricks Repos: GitHub連携
  - Amazon S3: データ保存 (そのまま)
  - Amazon ECS: 本番デプロイ (S3ファイル出力後)
  - Snowflake: 共通データソース (そのまま)
- フロー: Notebook作成 → セル実行 → キリの良いところでGitHub push → リリース前にECS統合テスト
- 改善点を青文字で表示 (セル単位実行、変数状態保持、結果可視化、気軽にジョブ化)
-->

![](https://i9wa4.github.io/assets/2025-11-07-tamesare-data-sapporo-uma-chan/databricks-architecture.drawio.png)

### 3.2. AWSサービスとの対応

<!-- 図の構成案:
- 2列の対応表形式
  左列: 移行前 → 移行後
  - .pyファイル実行 → Databricks Notebook (セル単位実行)
  - Amazon ECS → Databricks Compute (開発) + Amazon ECS (本番)
  - CloudWatch Logs → Notebook内リアルタイムログ
  - IAM Role → Instance Profile
  - Amazon S3 → Amazon S3 (そのまま)
  - Snowflake → Snowflake (そのまま)
  右列: 改善ポイント
  - REPL環境で変数確認・結果可視化
  - 自動起動/停止でコスト削減
  - セル実行結果が即座に表示
  - 既存データソースそのまま利用可能
-->

![](https://i9wa4.github.io/assets/2025-11-07-tamesare-data-sapporo-uma-chan/aws-databricks-mapping.drawio.png)

## 4. 導入効果

### 4.1. 開発サイクルの変化

<!-- 図の構成案:
- Before/After比較
- Before (ECS):
  - コード作成 → GitHub push → GitHub Actionsビルド(5分) → ECSタスク手動実行(30-60分) → CloudWatch Logs確認
  - 構文エラー程度の修正でも15分以上待機
- After (Databricks):
  - Notebook作成 → セル実行(数秒) → 結果即座表示
  - キリの良いところでGitHub push、リリース前にECS統合テスト
- タイムラインで時間の差を視覚化 (15分+ vs 数秒)
-->

![](https://i9wa4.github.io/assets/2025-11-07-tamesare-data-sapporo-uma-chan/development-cycle-comparison.drawio.png)

### 4.2. インターン生でもすぐ活躍

<!-- 図の構成案:
- インターン生のアイコン
- 移行前: 学習が必要だった知識
  - Docker、Amazon ECR、Amazon ECS、CloudWatch Logs理解に時間を費やす
  - 「統計モデリング」に着手する前の準備が長い
- 移行後: 学習コスト実質ゼロ
  - コンテナ・IAM・CloudWatch Logs理解が不要に
  - 早期に本質的業務 (統計モデリング、機械学習アルゴリズム設計) に着手可能
- 左→右の矢印で「AWSの学習コストが実質ゼロに」を強調
-->

![](https://i9wa4.github.io/assets/2025-11-07-tamesare-data-sapporo-uma-chan/intern-productivity.drawio.png)

### 4.3. 定量的な改善効果

<!-- 図の構成案:
- 3つの改善ポイントをカード形式で表示
  1. 開発体験の大幅向上
     - セル単位実行、変数状態保持、結果可視化
  2. AWSの学習コスト実質ゼロ
     - コンテナ・IAM・CloudWatch Logs理解が不要
  3. 気軽にジョブ化
     - 本番運用への移行がスムーズ
- 中央に下向き矢印で「学習コストが実質ゼロに」を強調
- 矢印は「移行前 (Docker/ECR/ECS/CloudWatch Logs)」から「移行後 (不要)」に向ける
-->

![](https://i9wa4.github.io/assets/2025-11-07-tamesare-data-sapporo-uma-chan/quantitative-improvement.drawio.png)

### 4.4. ほぼゼロコストで本番運用

<!-- 図の構成案:
- 左側: 開発フロー
  - Notebook でセル実行
  - デバッグ・調整
  - 完成
- 中央: ワンクリック変換の矢印
  - 「ワンクリックでジョブ化!」を強調
- 右側: 本番運用フロー
  - Databricks Jobs として自動実行
  - スケジュール実行
  - エラー通知
- ポイント:
  - 開発と運用が全く同じコード
  - デプロイ作業不要
  - 運用コストほぼゼロ
-->

![](https://i9wa4.github.io/assets/2025-11-07-tamesare-data-sapporo-uma-chan/job-migration.drawio.png)

## 5. まとめ

### 5.1. Databricks on AWS では AWS の知見がそのまま活きる

- S3 / EC2 / IAM Role など、既存の AWS 知識が活用できる
- AWS 構成からの移行がスムーズ
- インフラは AWS のまま、開発体験が劇的に向上
  - AWS 分かる人が1人でもいれば大体何とかなる

### 5.2. 併せてこちらもご確認ください

<div style="display: flex; align-items: center; gap: 3em; margin-top: 2em;">

<div style="flex: 1;">

[<img
src="https://i9wa4.github.io/assets/2025-11-07-tamesare-data-sapporo-uma-chan/zenn-twitter-card.jpeg"
style="width:100.0%" />](https://zenn.dev/genda_jp/articles/724a597e8f18ff)

</div>

<div style="flex: 1; text-align: left;">

**GENDAのデータサイエンティスト開発体験向上の取り組み紹介**

AWS ECSからDatabricksへの移行

<https://zenn.dev/genda_jp/articles/724a597e8f18ff>

</div>

</div>
