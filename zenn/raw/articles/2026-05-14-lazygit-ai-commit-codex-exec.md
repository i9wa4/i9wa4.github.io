---
title: "lazygit の AI コミットメッセージを `codex exec` で生成する"
emoji: "🐴"
type: "tech"
topics:
  - "lazygit"
  - "git"
  - "codexcli"
published: true
published_at: 2026-05-14 16:00
---

## 1. はじめに

以前、lazygit のカスタムコマンドから Claude Code を `claude -p` で呼び出して、ステージ済み diff からコミットメッセージを生成する記事を書きました。

@[card](https://i9wa4.github.io/blog/2026-03-14-lazygit-commit-message.html)

そのときは `claude -p` を使っていました。今回は、その実装を `codex exec` に移しました。

リンク先の Anthropic ヘルプセンター記事では、2026-06-15 から対象の Claude プランで Agent SDK 用の月次クレジットが提供され、その対象に Claude Agent SDK と Claude Code の `claude -p` が含まれること、またこの利用は通常のサブスクリプション使用制限とは別に扱われることが説明されています。`claude -p` 自体は使い続けられますが、LazyGit のコミットメッセージ生成は Git 操作のたびに何度も走る小さな補助処理です。そこで、このワークフローでは `claude -p` を使うのをやめ、Claude プラン側の Agent SDK クレジットや非対話実行の扱いに依存しないように、同じ下書き生成を `codex exec` に移しました。

@[card](https://support.claude.com/ja/articles/15036540-claude-%E3%83%97%E3%83%A9%E3%83%B3%E3%81%A7-claude-agent-sdk-%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%99%E3%82%8B)

この記事は 2026-05-14 時点の手元の dotfiles と Anthropic ヘルプセンター記事を見て書いています。ヘルプセンター記事では、2026-06-15 からの Claude Agent SDK 月次クレジットと `claude -p` の扱いが説明されています。

## 2. 前回の構成

前回の記事では、lazygit の `files` パネルで `Ctrl+G` を押すと Claude がコミットメッセージを生成し、その内容を `git commit -e -m "$MSG"` に渡す構成でした。

該当する考え方は次のようなものです。

```bash
MSG=$(git diff --cached | claude --no-session-persistence -p --model haiku \
  'Generate ONLY a one-line Git commit message following Conventional Commits format \
  (type(scope): description). Types: feat, fix, docs, style, refactor, test, chore. \
  Based strictly on the diff from stdin. Output ONLY the message, nothing else.') \
  && git commit -e -m "$MSG"
```

これはかなりシンプルで、ステージ済み diff をそのまま LLM に渡し、返ってきた1行をコミットメッセージの初期値にするだけです。

良かった点は、最後に必ずエディタで確認できることです。AI に完全に任せるのではなく、下書きだけ作ってもらい、人間が直してからコミットします。

## 3. 今の LazyGit 設定

現在は、lazygit の長いカスタムコマンドを `config.yml` に直接書かず、別のシェルスクリプトに逃がしています。

読者がそのまま置くなら、`~/.config/lazygit/config.yml` は次のような形です。

```yaml
gui:
  scrollHeight: 15

customCommands:
  - key: <c-g>
    context: files
    output: terminal
    command: bash ~/.config/lazygit/lazygit-ai-commit.sh
```

`Ctrl+G` は `files` パネル用のカスタムコマンドとして登録し、`output: terminal` で通常のターミナル上に `git commit` とエディタを出します。AI 呼び出しの中身は `~/.config/lazygit/lazygit-ai-commit.sh` に置きます。

## 4. codex exec 版の中身

新しい `lazygit-ai-commit.sh` は、まずステージ済み diff を一時ファイルに保存します。

```bash
git diff --cached --no-ext-diff >"$staged_diff"
```

その後、`codex` コマンドが存在する場合だけ `codex exec` を実行します。

```bash
if command -v codex >/dev/null 2>&1; then
  {
    prompt='Generate ONLY a one-line Git commit message following Conventional Commits format (type(scope): description). Types: feat, fix, docs, style, refactor, test, chore. Based strictly on the diff from stdin. Output ONLY the message, nothing else.'
    if codex exec -m gpt-5.4-mini --ephemeral --ignore-rules --sandbox read-only -c approval_policy='"never"' -c model_reasoning_effort='"low"' --color never --output-last-message "$ai_message" "$prompt" <"$staged_diff" >/dev/null 2>"$ai_stderr"; then
      msg=$(head -n 1 "$ai_message")
      if [ -n "$msg" ]; then
        printf '%s\n' "$msg" >"$ai_message"
        printf '%s\n' 'ok' >"$ai_status"
      else
        printf '%s\n' 'AI commit message generation returned an empty message; opening editor without AI message.' >"$ai_status"
      fi
    else
      printf '%s\n' 'AI commit message generation failed; opening editor without AI message.' >"$ai_status"
    fi
  } &
  ai_pid=$!
else
  printf '%s\n' 'codex not found; opening editor without AI message.' >"$ai_status"
fi
```

ポイントは次の通りです。

- `codex exec` にステージ済み diff を標準入力で渡す。
- `--output-last-message "$ai_message"` で最後の応答をファイルに保存する。
- `--sandbox read-only` と `approval_policy="never"` で、コミットメッセージ生成中にファイルを書き換えない前提にする。
- `--color never` で余計な制御文字を混ぜない。
- 返ってきた内容の1行目だけをコミットメッセージ候補として使う。

`claude -p` から `codex exec` に変えても、やっていることは同じです。ステージ済み diff を読み、1行のコミットメッセージだけを返してもらいます。

## 5. エディタで確認する流れは残した

AI が生成したメッセージは、そのまま `git commit -m` には渡していません。

スクリプト内では一時的な `GIT_EDITOR` を作り、AI の出力があればコミットメッセージファイルの先頭に差し込んでから `vim` を開きます。

```bash
if [ -s "$ai_message" ]; then
  buffer=$(mktemp /tmp/lazygit-ai-commit-editor-buffer.XXXXXX)
  {
    head -n 1 "$ai_message"
    printf '\n'
    cat "$msg_file"
  } >"$buffer"
  cat "$buffer" >"$msg_file"
  rm -f "$buffer"
elif ! grep -qx 'ok' "$ai_status"; then
  cat "$ai_status" >&2
fi

exec vim "$msg_file"
```

最後は通常の `git commit` です。

```bash
LAZYGIT_AI_COMMIT_MESSAGE="$ai_message" \
  LAZYGIT_AI_COMMIT_STATUS="$ai_status" \
  GIT_EDITOR="$editor" \
  git commit
```

ここで `codex exec` はバックグラウンドで先に走らせています。そのまま `git commit` を始めるため、pre-commit hook があるリポジトリでは、hook の実行と AI によるメッセージ生成が並行して進みます。エディタ側は AI の結果が出るまで待つので、hook 待ちの時間をコミットメッセージ生成に充てられます。

この形にしておくと、AI 生成が成功した場合は下書き入りでエディタが開きます。失敗した場合や `codex` がない場合でも、エディタは開くので通常の手入力コミットに戻れます。

## 6. 移行して良かったこと

今回の変更で一番大きいのは、LazyGit のコミットメッセージ生成を Claude Code の非対話実行から分離できたことです。

自分の中では、Claude Code は対話的な開発作業で使う場面が多いです。一方で、コミットメッセージ生成は、Git 操作の途中で何度も走る小さな補助処理です。同じ AI CLI でも、用途ごとに使い分けた方が気持ちよく運用できます。

また、設定面でも分かりやすくなりました。

- LazyGit 側の設定は `Ctrl+G` からスクリプトを呼ぶだけ。
- AI 呼び出しの詳細は `lazygit-ai-commit.sh` に閉じ込める。
- pre-commit hook の実行中に AI 生成も進むため、待ち時間を短くできる。
- 失敗時はコミット作業そのものを止めず、エディタを開く。
- 最終的なコミットメッセージは必ず人間が確認する。

`config.yml` に長いプロンプトとコマンド列を入れるより、今の形の方が見通しが良いです。

## 7. 使い方

使い方は前回とほとんど同じです。

1. lazygit でコミットしたい変更を stage する。
2. `files` パネルで `Ctrl+G` を押す。
3. `codex exec` が staged diff からコミットメッセージ候補を作る。
4. `vim` が開く。
5. 生成された1行を確認し、必要なら直して保存する。
6. 通常の `git commit` として確定する。

日常的には、AI が作った文言をそのまま採用することもあります。ただし、差分の意図とズレることは当然あるので、エディタでの確認は残しています。

## 8. まとめ

`claude -p` で作っていた LazyGit の AI コミットメッセージ生成を、`codex exec` に移しました。

やっていることは大きく変えていません。`git diff --cached --no-ext-diff` を AI に渡し、Conventional Commits 形式の1行を作らせ、最後はエディタで確認してコミットします。

変えたのは、どの CLI にその小さな補助処理を担当させるかです。

Claude Agent SDK と `claude -p` の扱いが変わるタイミングなので、こういう日々の自動化を `codex exec` 側に寄せるのは、ちょうど良い整理でした。
