# Databricks AI/BI ダッシュボードの Git 連携の運用方法
uma-chan
2025-05-21

## 1. はじめに

Databricks のダッシュボードは Git 連携できます！

[GitにおけるDatabricks AI/BIダッシュボードのソース管理
\#Databricks_AI_BI -
Qiita](https://qiita.com/taka_yayoi/items/af580c4bad7db4aebc38)

バックアップを取り安心したいので必ず導入しましょう。

Git 連携を用いた運用方法について検討したので記事として残します。

## 2. Databricks の Git 連携機能とダッシュボードの相性

Commit & Push とブランチ切り替え以外の操作は結構厳しいです。

JSON形式でウィジェット配置やSQLを管理しているのでコンフリクトが起きた場合の解消が難しいです。

なのでそもそもコンフリクトの起きない運用をしておきたいです。

## 3. Databricks の考えるベストプラクティス

> 自分の開発ブランチで作業するユーザーごとに、リモート Git
> リポジトリにマップされた個別の Databricks Git フォルダーを使用します
> 。

<https://docs.databricks.com/aws/ja/repos/git-operations-with-repos#ベスト-プラクティス-git-フォルダーでの共同作業>

そうは言うけれども実際は開発スキルを持たない方がダッシュボードを作成しますよね。

これを守るのは現実的ではないです。

## 4. 実際の運用

共有ワークスペース内に Git フォルダを作成して Git Flow
で運用しています。

ワークスペースでは常時 develop ブランチ固定で時々 Commit & Push したり
main にマージしたりします。

main への直接の Push 禁止という企業も多いと思いますので、その観点でも
Git Flow は運用しやすそうです。

これくらいのゆるさで気楽に今後も運用していきます。

``` mermaid
%%{
    init: {
        'logLevel': 'debug',
        'theme': 'base',
        'themeVariables': {
            'commitLabelFontSize': '14px',
            'tagLabelFontSize': '12px'
        }
    }
}%%
gitGraph LR:
    checkout main
    commit
    branch develop order: 4
    checkout develop
    commit
    commit

    branch release-1 order: 2
    checkout release-1
    commit

    checkout main
    merge release-1 tag: "25.02"

    checkout develop
    commit
    commit

    branch feature/new-master-data order: 5
    checkout feature/new-master-data
    commit
    commit
    checkout develop
    merge feature/new-master-data
    commit

    branch release-2 order: 3
    checkout release-2
    commit

    checkout main
    merge release-2 tag: "25.05"

    checkout develop
    commit
    commit
    commit
```

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-21-databricks-dashboard-github-operation.html&text=Databricks%20AI%2FBI%20%E3%83%80%E3%83%83%E3%82%B7%E3%83%A5%E3%83%9C%E3%83%BC%E3%83%89%E3%81%AE%20Git%20%E9%80%A3%E6%90%BA%E3%81%AE%E9%81%8B%E7%94%A8%E6%96%B9%E6%B3%95%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Databricks%20AI%2FBI%20%E3%83%80%E3%83%83%E3%82%B7%E3%83%A5%E3%83%9C%E3%83%BC%E3%83%89%E3%81%AE%20Git%20%E9%80%A3%E6%90%BA%E3%81%AE%E9%81%8B%E7%94%A8%E6%96%B9%E6%B3%95%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-21-databricks-dashboard-github-operation.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-21-databricks-dashboard-github-operation.html&title=Databricks%20AI%2FBI%20%E3%83%80%E3%83%83%E3%82%B7%E3%83%A5%E3%83%9C%E3%83%BC%E3%83%89%E3%81%AE%20Git%20%E9%80%A3%E6%90%BA%E3%81%AE%E9%81%8B%E7%94%A8%E6%96%B9%E6%B3%95%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
