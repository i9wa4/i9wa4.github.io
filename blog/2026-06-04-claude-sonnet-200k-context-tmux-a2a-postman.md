# Claude Sonnet 200k を普段使いするにはワークフローが要る
uma-chan
2026-06-04

## 1. コンテキストが大きくても、運用は勝手に整わない

Claude Sonnet 200k
は、今でも普段使いの現実的な基準だと思っています。ここでは、200k
トークン級のコンテキストウィンドウを持つ Claude Sonnet
モデルを指しています。

ただ、コンテキストが大きいことと、作業が回しやすいことは別です。読める量は増えますが、誰がタスクを持っているのか、レビューを誰に頼むのか、コンパクション後にどこから戻るのか、エージェント間でどう受け渡すのかまでは整理してくれません。

毎回 Claude Opus
に寄せないと安定しないなら、モデル選択だけの問題ではなく、Sonnet
で回す普段の作業経路に詰まりが残っているのかもしれません。

2026-06-02 時点で、私の Claude Code の `/model` メニューでは Claude
Sonnet 4.6 が普段使い、Claude Opus 4.8
が複雑な作業向けとして表示されていました。[Claude Code model
guide](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code)
も同じ整理です。

利用枠やコンテキスト上限の見え方は、UI、プラン、シート、バージョン、アカウント状態で変わります。[Claude
Code changelog](https://code.claude.com/docs/en/changelog)、[Max plan
page](https://support.claude.com/en/articles/11049741-what-is-the-max-plan)、[Team
plan
page](https://support.claude.com/en/articles/9266767-what-is-the-team-plan)、[paid-plan
context
page](https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans)、[API
context
page](https://support.claude.com/en/articles/8606395-how-large-is-the-claude-api-s-context-window)
を見ても、この辺りは条件付きの話が多いです。

それでも、Opus
の方が利用枠とコストを食いやすい傾向は変わりません。[pricing
page](https://platform.claude.com/docs/en/about-claude/pricing) でも
Opus は Sonnet より高く、[usage limits
page](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)
も利用量がモデル、会話の長さ、機能、ツールに依存すると説明しています。

なので私は、Claude Sonnet 200k
を厳密な上限値としてではなく、日常運用の基準として扱っています。まず
Sonnet で回る道を整える。そのうえで、本当に深い推論が効くターンだけ Opus
を選ぶ、という切り分けです。

失敗の多くは、モデルがファイルを読めなかったことより、運用が曖昧になったことから起きます。たとえば、誰がタスクを持っているか分からない。現在のチェックリストが古いターンに埋もれる。レビュー依頼に誰も返さない。コンパクション後に細かいが重要な条件が抜ける。この手のものです。

コンテキストは作業場です。1つのエージェントが計画、実装、レビュー、記憶、報告を全部抱えるなら、あとから参照したい依頼や証跡には別の置き場所が必要になります。

## 2. 役割を分けて、各エージェントのコンテキストを小さくする

1つの高性能なエージェントに、計画、編集、テスト、レビュー、報告まで任せることはできます。ただ、その全部を1つのセッションに積むと、古い選択肢、途中の確認、レビュー指摘、ユーザー向けの言い回し、実装詳細が混ざります。

私はここを責務ごとに分ける方が扱いやすいと思っています。

| 責務                   | 持たせる仕事                          |
|------------------------|---------------------------------------|
| ユーザー依頼を受ける   | messenger または入口の役割            |
| 計画して委譲する       | orchestrator role                     |
| 実装する               | worker role                           |
| 検証する               | reviewer role                         |
| ユーザーに要約して返す | messenger または orchestrator handoff |

これは、複数エージェントにすれば勝手に客観的になる、という話ではありません。レビュアーも見落としますし、オーケストレーターも委譲に失敗します。

利点はもっと地味です。各エージェントが、自分の役割に必要なコンテキストだけを濃く持てるようになります。大きなコンテキストウィンドウは、全員の履歴を1つに詰め続けるためではなく、役割を絞ったエージェントがファイル、ログ、証跡を深く調べるために使う方が効きます。

## 3. コンパクション後に役割へ戻れるようにする

自動コンパクションは、長いセッションを続けるには便利です。一方で、エージェントがすぐ参照できる文脈を圧縮して書き換えるので、そこが危なくもあります。

危ないのは、タスクの途中で要約から再開して、小さいけれど重要な指示が抜けたり弱くなったりすることです。コンパクション後は、動く前に次の足場を戻しておきたいです。

- 自分はどの役割か
- 誰と話せるか
- 今開いているタスクは何か
- 何をもって完了とする元チェックリストか
- トランスクリプトの外にどんな証跡があるか

Claude Code の after-compaction hook
が使えるなら、単一エージェントでは「この指示ファイルを読み、このタスクアーティファクトから続ける」と戻せます。

マルチエージェントでは、全ペインに同じリマインダーを入れるだけでは足りません。messenger、orchestrator、worker、reviewer
は、必要な役割、連絡先、安全ルールが違います。

tmux
ベースなら、ペインタイトルを役割名として使うのが分かりやすいです。`worker`
ペインは worker の役割に戻す。`orchestrator`
ペインは段取り役に戻す。`messenger` ペインは transport-only
のままにする。モデルのコンテキストの外にあり、ハーネスから見える情報なので、ローカルな復帰キーとして使いやすいです。

## 4. タスク状態は外に置く

長いコンテキストは推論には役立ちますが、タスクデータベースとしては弱いです。

1つの長いチャットには、古い意思決定、捨てた計画、コマンド出力、レビューコメント、横道の議論が混ざります。モデルから見ると長いテキストですが、こちらがほしいのは、現在の意思決定、アクティブなチェックリスト、検証サマリー、未解決のレビュー指摘、次の役割へ渡せるハンドオフです。

解決策はプロンプトをさらに長くすることではありません。プロンプトの外に、小さくて永続的な置き場所を作ることです。

メールは依頼を運ぶ。タスクアーティファクトは証跡を残す。コンテキストは推論に使う。この分担にすると、古いトークンの山から現在の状態を推測させずに済みます。

## 5. `tmux-a2a-postman` は受け渡しを残す層

私のローカル実装は
[`tmux-a2a-postman`](https://github.com/i9wa4/tmux-a2a-postman)
です。メールボックス層は
[以前の記事](https://i9wa4.github.io/../en/blog/2026-05-17-tmux-a2a-postman-markdown-mail-for-ai-agent-teams.md)
で紹介しました。この記事で見たいのは、Claude
の作業記憶を信用しすぎず、その周りに受け渡しを残す層を置くことです。

`tmux-a2a-postman` は Claude
を賢くしません。コンテキストウィンドウも増やしません。Claude Code、Codex
CLI、tmux、ネイティブサブエージェントを置き換えるものでもありません。

足しているのは、次のような薄い運用レイヤーです。

- 役割を `postman.md` で名前付けする
- 許可されたハンドオフを Mermaid の edge として定義する
- ノード識別に tmux のペインタイトルを使う
- メッセージを Markdown メールとして保存する
- 受信者が `pop` でメールを claim する
- reply-required な依頼に正確な入力リクエストを開く
- キュー、dead letter、`pending`、`waiting`、`ready`、`stale`
  を見えるようにする

最小限で役に立つトポロジーは小さくて十分です。

``` mermaid
graph LR
    messenger["messenger<br/>human-facing"]
    orchestrator["orchestrator<br/>task coordinator"]
    worker["worker<br/>implementation"]
    reviewer["reviewer<br/>verification"]

    messenger --- orchestrator
    orchestrator --- worker
    orchestrator --- reviewer

    class messenger entry
    class orchestrator,worker,reviewer role
    classDef entry fill:#dbeafe,stroke:#2563eb,color:#0f172a
    classDef role fill:#f8fafc,stroke:#64748b,color:#0f172a
```

worker は人間と話す手順を覚えなくてよい。reviewer
は実装の全履歴を抱えなくてよい。messenger
はファイルを調べなくてよい。orchestrator
が経路を持つことで、各役割のコンテキストを小さく保てます。

作業の単位は Markdown メールです。送信者は reply-required
な依頼を作る。受信者は `pop` で claim
する。終わったら正確な入力リクエストを閉じる。このくらいの形にしておくと、誰が何を持っているかがかなり怪しくなりにくいです。

``` bash
tmux-a2a-postman pop

tmux-a2a-postman send-heredoc \
  --to orchestrator \
  --fills-input-request-id <input-request-id> \
  --reply-to <message-id> <<'MESSAGE_BODY'
DONE: Article updated and verified.
Task artifact: <artifact-reference>
Original checklist: PASS
Remaining blockers: none
MESSAGE_BODY
```

ここで閉じるのは transport slot
です。作業が正しいことは、元チェックリスト、進捗、意思決定、検証証跡、ブロッカー、完了判定を持つタスクアーティファクトで示します。

## 6. 経験則

Claude Sonnet 200k 作業に対する私のルールは単純です。

> 推論はコンテキストに置く。依頼はメールに置く。証跡はアーティファクトに置く。

コンテキストウィンドウは強力な作業場です。信頼できる記憶システム、キュー、レビュープロセス、プロジェクトマネージャーではありません。

長いエージェント実行では、私は周辺に3つのものを置きたいです。

1.  各役割の仕事を小さくするマルチエージェント分解。
2.  コンパクション後に役割と状態を戻す復帰の仕組み。
3.  チェックリストと証跡をモデルの作業記憶の外に残すタスク管理。

`tmux-a2a-postman`
は、この運用モデルのローカル実装にすぎません。日常作業では Claude Sonnet
を使いやすく保ち、Claude Opus
を乱雑になった状態の救済策ではなく、意図して選ぶものにできます。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-06-04-claude-sonnet-200k-context-tmux-a2a-postman.html&text=Claude%20Sonnet%20200k%20%E3%82%92%E6%99%AE%E6%AE%B5%E4%BD%BF%E3%81%84%E3%81%99%E3%82%8B%E3%81%AB%E3%81%AF%E3%83%AF%E3%83%BC%E3%82%AF%E3%83%95%E3%83%AD%E3%83%BC%E3%81%8C%E8%A6%81%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Claude%20Sonnet%20200k%20%E3%82%92%E6%99%AE%E6%AE%B5%E4%BD%BF%E3%81%84%E3%81%99%E3%82%8B%E3%81%AB%E3%81%AF%E3%83%AF%E3%83%BC%E3%82%AF%E3%83%95%E3%83%AD%E3%83%BC%E3%81%8C%E8%A6%81%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-06-04-claude-sonnet-200k-context-tmux-a2a-postman.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-06-04-claude-sonnet-200k-context-tmux-a2a-postman.html&title=Claude%20Sonnet%20200k%20%E3%82%92%E6%99%AE%E6%AE%B5%E4%BD%BF%E3%81%84%E3%81%99%E3%82%8B%E3%81%AB%E3%81%AF%E3%83%AF%E3%83%BC%E3%82%AF%E3%83%95%E3%83%AD%E3%83%BC%E3%81%8C%E8%A6%81%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
