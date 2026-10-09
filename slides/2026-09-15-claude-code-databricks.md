# アナリストのClaude Code x Databricks活用について
uma-chan
2026-09-15

## 1. はじめに

### 1.1. 自己紹介

<div class="columns">

<div class="column" width="50%">

- 名前：
  - uma-chan / Mawatari Daiki
- 職種：
  - データエンジニア
  - MLOpsエンジニア
- 受賞：
  - JEDAI Order 2026
  - Databricks MVP 2026
- 趣味：
  - コーヒー☕
    - ネスカフェ ゴールドブレンド (こだわりなし)
  - ターミナルにすべてを集約してAIに仕事をさせる
    - 趣味というより本業

</div>

<div class="column" width="50%">

[![](https://i9wa4.github.io/assets/2026-09-15-claude-code-databricks/terminal-night-3.png)](https://kichijojipm.connpass.com/event/404746/)

</div>

</div>

### 1.2. 本日話すこと

- Databricksへの接続方法
- 分析ノウハウ集積方法

## 2. Databricksへの接続方法

### 2.1. アナリストのPC環境の特徴

あくまでも一例です

- CLIもしくはアプリでAIエージェントを活用している
  - Claude Code / Claude Desktop
  - Codex CLI / Codex App
- Windowsユーザーが多い

普段の業務に順応するDatabricks活用環境があるととてもよい！

### 2.2. Claudeコネクタ・MCPサーバー不採用理由

前述のPC環境でデータ分析をするにはClaudeコネクタ・MCPサーバーを用意すればよさそうだが……

- Claudeコネクタ (Claudeと外部サービスを繋ぐもの)
  - 仕様上Databricksワークスペースと非人間IDを固定して全社利用するしかない
    - 複数プロダクトを抱える企業は困る
    - 全社員同一権限でデータにアクセスできてしまう
- Databricks MCPサーバー
  - ユーザー権限でログインするための実装が難しい
  - MCPサーバーのインストールが難しい
  - 結局ワークスペース切り替え問題も残る

### 2.3. 救世主Databricks CLI

元々DevContainer (Docker) で対応していましたがDatabricks CLIに乗り換え

- Databricks CLIの特徴
  - OS問わずインストールできる
  - ユーザーとしてDatabricksにログインできる (OAuth U2M)
  - CLIなので難しいことはPC上のAIエージェントが全部やってくれる
- 注意
  - Databricks CLI利用は封鎖できません！
  - 開発作業もできてしまうので要権限整理
- 公式リンク
  - <https://docs.databricks.com/aws/en/dev-tools/cli>
  - <https://github.com/databricks/cli>

## 3. 分析ノウハウ集積方法

### 3.1. Agent Skills

AIエージェントとの相性の良い **Agent Skills** を利用する

GitHub管理でアナリストが積極的にPull Requestを出せるようになるまで見守る

認証情報等のPushを阻止するガードレールは設定してあげましょう！

### 3.2. Unity Gateway Skills (ベータ版)

データ格納先と同じ場所にAgent Skillsを置くことができる

しかもGitHub同期ができる！

現状の構成と相性が良いので活用していきたい

参考:
<https://docs.databricks.com/aws/en/agents/uc-skills/create-share-uc-skills>

## 4. まとめ

### 4.1. まとめ

インストールさえできれば他の手法より楽ができます

権限整理をしてDatabricks CLIを使ってみましょう！
