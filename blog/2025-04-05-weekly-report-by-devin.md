# Devin に週報を書いてもらった
uma-chan
2025-04-05

## 1. はじめに

最近 Devin で遊びながら勘所を掴んでいる最中です。
題材として丁度よかったので週報作成を Devin
にやらせてみることにしました。

## 2. 週報作成の概要

集計期間の GitHub の issue と pull request
の情報を基に各メンバーの活動の概要と詳細を issue にまとめてもらいます。

## 3. Devin へのプロンプト

長文プロンプトを用意する必要があります。 Devin では Playbook
を利用すればよいですね。 今回はリポジトリ内の Markdown
ファイルを参照させてます。

プロンプトは別記事に分けてます。

[Devin
週報作成用プロンプト](https://i9wa4.github.io/2025-04-05-weekly-report-prompt-for-devin.md)

上に書いたような長文プロンプトを用意した上で以下のように Devin
に指示を出します。

> 以下の Markdown の指示に従って情報収集を行った上で GitHub issue
> を作成してください。 <プロンプトとなるMarkdownのURL>
>
> 集計開始日：2025/03/12 集計終了日：2025/03/18

## 4. Devin へのプロンプトを書く上でのコツ

### 4.1. Devin というか LLM の忘れっぽさへの対処

長文だとどうしても近眼的に周囲数行の記述に引っぱられてしまうので、大枠の構造を提示しつつ、詳細は具体例とピンポイントなコメントという書き味にすることで出力が安定しました。

今回各メンバーを列挙する箇所がありますが、横着せず愚直に列挙しました。
冗長だなあと思いつつもこうすることで Devin
が忘れずに全メンバーの情報収集をしてくれました。

### 4.2. GitHub CLI の仕様への対処

Devin がうまく情報収集してくれないことがあるので GitHub CLI
の仕様を理解し適切なコマンドを実行できているか見ておく必要があります。
今回は `--state all` オプションを指定して閉じられた issue
なども取得させるように指示を出しています。

また、issue の description
が長文になると文章を分割して編集追加させなければならなくなるので issue
の description
とコメントの行数を想定した上で適度に分割しておくと良いでしょう。
もし長文投稿させたい場合は作成した issue を読み込ませて見切れてないか
Devin に確認させるのも良いかもしれません。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-04-05-weekly-report-by-devin.html&text=Devin%20%E3%81%AB%E9%80%B1%E5%A0%B1%E3%82%92%E6%9B%B8%E3%81%84%E3%81%A6%E3%82%82%E3%82%89%E3%81%A3%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Devin%20%E3%81%AB%E9%80%B1%E5%A0%B1%E3%82%92%E6%9B%B8%E3%81%84%E3%81%A6%E3%82%82%E3%82%89%E3%81%A3%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-04-05-weekly-report-by-devin.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-04-05-weekly-report-by-devin.html&title=Devin%20%E3%81%AB%E9%80%B1%E5%A0%B1%E3%82%92%E6%9B%B8%E3%81%84%E3%81%A6%E3%82%82%E3%82%89%E3%81%A3%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
