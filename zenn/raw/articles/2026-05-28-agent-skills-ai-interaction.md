---
title: "Agent Skills で AI への依頼を設計する"
emoji: "🐴"
type: "tech"
topics:
  - "aiagent"
  - "agentskills"
  - "github"
  - "prompt"
publication_name: "genda_jp"
published: false
---

## 1. はじめに

AI コーディングエージェントに任せる作業が増えると、毎回同じような指示を書いていることに気づきます。

- このリポジトリではどの確認コマンドを使うのか
- ドキュメントではどの書き方を守るのか
- 変更してはいけない範囲はどこか
- 完了報告にはどの証跡を入れてほしいのか

毎回プロンプトに全部書くと長いです。
一方で省略すると、AI は足りない前提を推測で埋めます。

この記事では Agent Skills を、単なる便利機能ではなく「AI への依頼をどう設計するか」という話として整理します。

主題は、AI に何を任せるかではありません。
AI にどの判断材料を渡すかです。

:::message
本記事の内容は 2026年5月時点での検証結果に基づいています。
特に `gh skill` は preview 扱いなので、細かい挙動は変わる可能性があります。
:::

## 2. 弱いプロンプトとは何か

弱いプロンプトは、短いプロンプトのことではありません。

必要な判断材料が外に出ていないプロンプトです。

| 足りないもの | 起きること                     |
| ------------ | ------------------------------ |
| Context      | どの前提で作業するか推測される |
| Workflow     | 作業順序が毎回変わる           |
| Constraints  | やってはいけないことが漏れる   |
| Validation   | 確認せずに完了したことになる   |
| Evidence     | 何を根拠に完了したか残らない   |

たとえば「この記事を直して」だけでも、相手が人間なら暗黙の前提を汲んでくれるかもしれません。
しかし AI エージェントにとっては、どの文体に寄せるのか、どのファイルを触ってよいのか、確認は何を通せばよいのか、報告には何を含めるべきかが曖昧です。

プロンプトを長くすれば解決することもあります。
ただ、それを毎回書くのはつらいです。
忘れるし、古くなるし、別の作業に流用したときに壊れます。

そこで、繰り返し必要になる判断材料を reusable operating knowledge として外に出します。
Agent Skills は、その operating knowledge を package する方法の 1 つです。

## 3. Agent Skills は何を package するのか

Agent Skills は、AI エージェント向けの小さな専門手順書と考えると分かりやすいです。

最低限は `SKILL.md` を置きます。
`SKILL.md` の frontmatter に、名前と説明を書きます。
本文には、実際に作業するときの手順や制約を書きます。

@[card](https://agentskills.io/specification)

たとえば最小形はこんなイメージです。

```yaml:skills/example/SKILL.md
---
name: example
license: MIT
description: |
  USE FOR: Documentation authoring in this repository.
  DO NOT USE FOR: Build failures, release safety, or unrelated writing.
---

# Example

## Workflow

1. Inspect the relevant files.
2. Read only the needed references.
3. Make the smallest scoped change.
4. Run the nearest validation.
5. Report changed files, evidence, and residual risk.
```

大事なのは、Agent Skills を「ドキュメント置き場」にしないことです。

普通のドキュメントは、背景理解や詳細説明に向いています。
Agent Skills は、作業時に AI が使う判断材料に向いています。

| 観点       | 普通のドキュメント | Agent Skills                           |
| ---------- | ------------------ | -------------------------------------- |
| 読み手     | 人間               | AI エージェントと人間                  |
| 目的       | 背景理解           | 作業時の判断と実行                     |
| 起動条件   | 人間が探して読む   | task に応じて agent が選ぶ             |
| 重要な項目 | 説明の網羅性       | trigger、workflow、validation、handoff |

Agent Skills は全部入りの資料ではなく入口です。
入口を小さくして、必要なら `references/` や `scripts/` を追加で読ませる形にすると扱いやすいです。

## 4. プロンプトから外に出すもの

短いプロンプトを強くするには、情報を捨てるのではなく、毎回書かなくても読まれる場所に移します。

| Prompt に残すもの       | Agent Skills に移すもの                    |
| ----------------------- | ------------------------------------------ |
| 今回やってほしい task   | いつもの workflow                          |
| 今回の対象 file / scope | いつもの禁止事項と確認順                   |
| 今回だけの判断          | いつも必要な validation と report evidence |

たとえば、毎回次のような依頼を書いているなら、後半は Agent Skills 側に寄せられます。

```text
この記事を Zenn 向けに直してください。
既存の記事の文体に寄せてください。
Markdown の code fence は Zenn の通常形式にしてください。
作業後に rumdl を実行してください。
変更したファイルと確認結果を報告してください。
```

最後に残したいのは、もっと短い依頼です。

```text
この記事を Zenn 向けに直してください。
```

これだけで済むようにするには、文体、Markdown ルール、検証コマンド、報告形式が別の場所に package されている必要があります。

## 5. AI が deterministic になるわけではない

ここはかなり大事です。

Agent Skills を入れても、AI の出力が完全に deterministic になるわけではありません。
同じ入力に対して常に同じ答えを返す実行環境になるわけではないです。

ただし、毎回渡す判断材料を揃えることはできます。

- どの context を見るか
- どの workflow で進めるか
- 何を禁止するか
- どの validation を走らせるか
- 何を evidence として返すか

目的は「完全に同じ答えを出す」ことではありません。
「同じ判断材料を毎回渡す」ことです。

これだけでも、作業開始から完了報告までの揺れはかなり小さくなります。

## 6. `USE FOR` と `DO NOT USE FOR`

Agent Skills では、AI が読むべき場面と読まない場面をはっきりさせるのが重要です。

私は `description` に `USE FOR` と `DO NOT USE FOR` を書く形が分かりやすいと思っています。

```yaml
description: |
  USE FOR: Markdown authoring, code block style, and article checks.
  DO NOT USE FOR: Build failures, release safety, or unrelated prose editing.
```

注意点として、これは GitHub Agent Skills の必須構文ではありません。
Agent Skills の仕様として必須なのは、たとえば `name` と `description` のような frontmatter です。

一方で、Waza はこの書き方と相性がよいです。
確認した Waza 0.33.0 では、`USE FOR:` や `DO NOT USE FOR:` が trigger / anti-trigger の signal として扱われます。
また、scope reduction や trigger grader の文脈でもこの形式が使われます。

つまり、これは「GitHub が要求する構文」ではなく「Waza で評価されやすく、人間にも読みやすい convention」として扱うのがよさそうです。

## 7. 日本語でどこまで書くか

日本語の手順を書くこと自体は禁止されていません。
むしろ、日本語の記事や日本語の運用手順を扱うなら、本文や `references/` は日本語の方が読みやすいです。

ただし、入口になる metadata は英語寄りにした方が安定しやすいです。

| 場所          | 実務上のおすすめ                                     |
| ------------- | ---------------------------------------------------- |
| `name`        | lowercase ASCII、digits、hyphen                      |
| `description` | English の `USE FOR` / `DO NOT USE FOR` を基本にする |
| 本文          | 対象作業に合わせて日本語でもよい                     |
| `references/` | 人間と agent が読む実務資料として日本語でもよい      |
| eval prompt   | 日本語 task を扱うなら日本語の prompt case も入れる  |

理由は、metadata が最初に読まれる catalog だからです。
agent や tooling が最初に見る入口は、検索性と trigger の安定性を優先した方が扱いやすいです。

## 8. `waza` と `gh skill` は補助輪として使う

Agent Skills の話をすると tooling の話に寄りがちですが、主役はあくまで「AI に渡す判断材料」です。
`waza` と `gh skill` は、その判断材料を package した後に形を確認する補助輪として見るのがよいと思います。

@[card](https://microsoft.github.io/waza/about/)

@[card](https://cli.github.com/manual/gh_skill)

ざっくり分けるとこうです。

| Tool       | 何を見るか                                                   | 見ないもの                                  |
| ---------- | ------------------------------------------------------------ | ------------------------------------------- |
| `waza`     | Agent Skills の readiness、token budget、eval、grader の入口 | GitHub release と install 先の package 管理 |
| `gh skill` | GitHub CLI としての search / install / update / publish      | trigger quality や eval の実行品質          |

### 8.1. `waza check`

`waza check` は、Agent Skills を作った後の readiness check として使えます。

```sh
waza --no-update-check check skills/<name> --format json
```

確認した Waza 0.33.0 では、`ready` の gate は主に次のようなものです。

- compliance score が `Medium-High` 以上か
- spec check が落ちていないか
- token budget を超えていないか
- link や schema に blocking error がないか

Advisory checks は別枠の warning です。
procedure、body structure、progressive disclosure、scope などの改善材料にはなりますが、それだけで `ready=false` になるわけではありません。

Waza の公式 CLI reference でも `waza check` は compliance と readiness の確認として説明されています。
また、Waza の出力では scope reduction などの改善材料が advisory checks として分かれて出ます。

@[card](https://microsoft.github.io/waza/reference/cli/)

### 8.2. `gh skill publish --dry-run`

`gh skill` は GitHub CLI の agent skills 用 command です。

この環境で確認した `gh` 2.92.0 では、独立した validate subcommand はありません。
validation-only の入口は `gh skill publish --dry-run` です。

```sh
gh skill --help
gh skill publish --dry-run
```

`gh skill publish --dry-run` は、skill packaging の validation として扱うのが安全です。
たとえば、skill name、directory match、required frontmatter、`allowed-tools` の型、install metadata などを確認します。

topic、tag、release 作成は dry-run 後の publish flow の話です。
dry-run 自体は validation-only として扱います。

@[card](https://cli.github.com/manual/gh_skill_publish)

## 9. prompt case で選択を確認する

Agent Skills は作って終わりではありません。
実際の依頼文に近い prompt case で、期待した Agent Skills が読まれるかを見るのが大事です。

たとえば、次のような観点を残します。

| 見るもの              | 確認すること                         |
| --------------------- | ------------------------------------ |
| Prompt case           | 実際の依頼文に近いか                 |
| Expected Agent Skills | 読まれてほしい Agent Skills はどれか |
| Observed Agent Skills | 実際に選ばれた Agent Skills はどれか |
| Result                | pass / fail / blocked を記録できるか |

Waza では、eval の grader として `trigger` や `skill_invocation` も用意されています。

@[card](https://microsoft.github.io/waza/guides/graders/)

最初から大きな eval suite を作る必要はありません。
まずは、自分がよく投げる短い依頼をいくつか並べて、想定どおりの Agent Skills が選ばれるかを見るだけでも十分役に立ちます。

## 10. まとめ

Agent Skills は、AI との向き合い方を運用可能にする仕組みの 1 つです。

この記事で言いたかったことは次の通りです。

- 弱いプロンプトは、短いプロンプトではなく missing context のあるプロンプト
- 繰り返す判断材料は operating knowledge として外に出す
- Agent Skills は context、workflow、constraints、validation、evidence を package できる
- AI が deterministic になるわけではないが、毎回渡す判断材料を揃えられる
- `USE FOR` / `DO NOT USE FOR` は GitHub の必須構文ではなく、Waza と相性のよい convention
- `waza` と `gh skill publish --dry-run` は、作った Agent Skills の形を確認する補助輪

一撃必殺プロンプトは、魔法の一文ではありません。
短い依頼の裏側に、必要な判断材料がすでに package されている状態です。

AI への依頼が不安定だと感じたら、プロンプトをさらに長くする前に、何を再利用可能な operating knowledge として外に出せるかを考えるとよさそうです。
