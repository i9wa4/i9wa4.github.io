# AWS Lambda でコンテナイメージを実行する with Terraform & GitHub
Actions
uma-chan
2025-05-12

## 1. はじめに

AWS Lambda で ECR
にあるコンテナイメージを実行するために必要な全てのリソースを Terraform
で構築し、GitHub Actions でデプロイできるようにします。

## 2. 背景

以下のような記事を参考にしながら MCP クライアントと MCP サーバーを全て
Lambda (& ECR) で管理させようと考えています。

- [SlackからLambda上にあるMCPクライアントとMCPサーバー動かす](https://zenn.dev/georgia1/articles/214056407379b2)
- [コンテナイメージを使用してAWS Lambda関数を作成する \#Python -
  Qiita](https://qiita.com/kyamamoto9120/items/f1cda89ffc7cb5254f17)
- [AWS Cost Analysis MCP ServerのツールをLambda関数に移植してAWS Lambda
  MCP Server経由で実行する \|
  DevelopersIO](https://dev.classmethod.jp/articles/securing-mcp-tools-with-aws-lambda-integration/)
- [爆速？！コンテナイメージからデプロイしたLambdaのコールドスタートについて検証してみた
  \#reinvent \|
  DevelopersIO](https://dev.classmethod.jp/articles/measure-container-image-lambda-coldstart/)

まずは表題の通り動く Lambda を作成し CI/CD
を整備することで以降に備えます。

## 3. 構成

とりあえず動くようになったので、ほぼ無説明で構成だけ載せます。

<https://github.com/i9wa4/terraform-mono-repo/tree/fe67b11fe6e7696325103fd997980f5cf8e94f1d>

関係する部分は以下になっています。

``` sh
$ tree -a -I ".git/|hands-on-import|hands-on-sfn|.terraform" -A
.
├── .github
│   └── workflows
│       └── hands-on-lambda-ecr-deploy.yml
└── services
    └── hands-on-lambda-ecr
        ├── app
        │   ├── app.py
        │   ├── Dockerfile
        │   └── requirements.txt
        ├── README.md
        └── terraform
            ├── .terraform.lock.hcl
            ├── main.tf
            ├── outputs.tf
            ├── variables.tf
            └── versions.tf
```

モノレポの練習で作ってみたリポジトリなのですが、整備はこれからという感じです。

## 4. 大変だった点

- ECR Image URI の取得周り
  - ECR タグを Immutable にしたせい
- GitHub Actions 内の OIDC 認証
  - 初めてやると慣れてなくて手間取った

## 5. 課題

- デプロイだけ手動でできるが CI は追加できていない
- main.tf でかすぎ
- dev/prod 環境分離考慮してない
- ローカルから Makefile でデプロイできるようにしてない

## 6. おわりに

今までで一番大変な Hello World でした。

整備は一旦後回しにして MCP 周りの実装をやっていきたいです。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-12-hands-on-lambda-ecr.html&text=AWS%20Lambda%20%E3%81%A7%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%82%92%E5%AE%9F%E8%A1%8C%E3%81%99%E3%82%8B%20with%20Terraform%20%26%20GitHub%20Actions%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=AWS%20Lambda%20%E3%81%A7%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%82%92%E5%AE%9F%E8%A1%8C%E3%81%99%E3%82%8B%20with%20Terraform%20%26%20GitHub%20Actions%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-12-hands-on-lambda-ecr.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-12-hands-on-lambda-ecr.html&title=AWS%20Lambda%20%E3%81%A7%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%82%92%E5%AE%9F%E8%A1%8C%E3%81%99%E3%82%8B%20with%20Terraform%20%26%20GitHub%20Actions%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
