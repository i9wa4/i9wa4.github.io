# Devin 週報作成用プロンプト
uma-chan
2025-04-05

親記事は以下です。

[Devin に週報を書いてもらった](https://i9wa4.github.io/2025-04-05-weekly-report-by-devin.md)

## 1. 人間への補足

Devin
にこのプロンプトを見せて、集計開始日と集計終了日を教えてあげてください。

指示例は以下のようになります。

``` markdown
以下の Markdown の指示に従って情報収集を行った上で GitHub issue を作成してください。
<プロンプトとなるMarkdownのURL>

集計開始日：2025/03/12
集計終了日：2025/03/18
```

## 2. GitHub の情報収集方法

- テンプレートに記載した対象リポジトリの issue, pull request,
  そしてそれらの comment を取得してください。
- issue や pull request を GitHub CLI で取得する場合は `--state all`
  オプションを使用して Closed や Merged
  になっているものも忘れずに取得してください。
- 対象リポジトリにアクセスできない場合は、そのリポジトリは集計対象外としてください。
- 対象メンバー毎に活動をまとめる際は対象者が assignee でない issue や
  pull request は含めないでください。

## 3. issue テンプレート

- 補足コメントは `<!-- -->` で与えているので参照してください。
- ただし issue 作成時には補足コメントは記載しないでください。

### 3.1. Title

集計開始日と集計終了日を YYYY/MM/DD 形式で記載してください。

``` markdown
[Devin] チーム週報 (YYYY/MM/DD-YYYY/MM/DD)
```

### 3.2. Assignee

- `@i9wa4`

### 3.3. Description

``` markdown
## 1. 期間

<!-- 集計開始日と集計終了日を記載してください。 -->
<!-- (aaa) は曜日です。(月) や (火) のように記載してください。 -->

YYYY/MM/DD(aaa)～YYYY/MM/DD(aaa)

## 2. 対象リポジトリ

- GitHub リポジトリの URL

## 3. 対象メンバー (GitHub ユーザー名)

- `@i9wa4`

## 4. 概要

### 4.1. `@i9wa4`

<!-- 当該メンバーの大きめの活動をしたプロジェクトから順にやったことの概要を4文程度に要約して紹介してください。 -->

### 4.2. 他メンバーはこのような記述にする

<!-- 集計期間に活動があれば上記と同様の形式で記入してください。 -->
```

### 3.4. Comment (1)

``` markdown
## 5. 詳細

### 5.1. `@i9wa4`

<!-- 当該メンバーの活動詳細を以下の形式で列挙してください。 -->
<!-- - [status (Open/Closed/Merged)] [category (issue/pull request)] [issue/pull request title #number](URL) -->
<!-- 列挙したあとアルファベット順にソートしてください。 -->

- [Closed] [issue] [issue title #189](issue url)
- [Merged] [pull request] [pull request title #124](pull request url)
- [Open] [issue] [issue #106](issue url)

### 5.2. 他メンバーはこのような記述にする

<!-- 集計期間に活動があれば上記と同様の形式で記入してください。 -->
```

### 3.5. Comment (2)

``` markdown
## 6. Devin への指示内容

<!-- Devin へ指示した内容をそのまま引用符付きで記載してください。 -->
<!-- 例 -->

> 以下の Markdown の指示に従って GitHub issue を作成してください。
> <プロンプトとなるMarkdownのURL>
>
> 集計開始日：2025/03/12
> 集計終了日：2025/03/18
```

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-04-05-weekly-report-prompt-for-devin.html&text=Devin%20%E9%80%B1%E5%A0%B1%E4%BD%9C%E6%88%90%E7%94%A8%E3%83%97%E3%83%AD%E3%83%B3%E3%83%97%E3%83%88%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Devin%20%E9%80%B1%E5%A0%B1%E4%BD%9C%E6%88%90%E7%94%A8%E3%83%97%E3%83%AD%E3%83%B3%E3%83%97%E3%83%88%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-04-05-weekly-report-prompt-for-devin.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-04-05-weekly-report-prompt-for-devin.html&title=Devin%20%E9%80%B1%E5%A0%B1%E4%BD%9C%E6%88%90%E7%94%A8%E3%83%97%E3%83%AD%E3%83%B3%E3%83%97%E3%83%88%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
