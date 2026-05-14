---
title: "lazygit の AI コミットメッセージを `codex exec` で生成する"
emoji: "🐴"
type: "tech"
topics:
  - "lazygit"
  - "git"
  - "codexcli"
published: true
published_at: 2026-05-14 20:30
---

## 1. はじめに

以前 lazygit のカスタムコマンドから Claude Code を `claude -p` で呼び出して、ステージ済み diff からコミットメッセージを生成する記事を書きました。

@[card](https://i9wa4.github.io/blog/2026-03-14-lazygit-commit-message.html)

今回はこの処理を `codex exec` に移しました。主な狙いは、AI によるコミットメッセージ生成をバックグラウンドで進めながら、そのまま `git commit` を開始して pre-commit hook と並行させることです。

@[card](https://support.claude.com/ja/articles/15036540-claude-%E3%83%97%E3%83%A9%E3%83%B3%E3%81%A7-claude-agent-sdk-%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%99%E3%82%8B)

こちらの Claude 公式記事の要点は、2026-06-15 から対象の Claude プランで Agent SDK 用の月次クレジットが用意され、Claude Code の `claude -p` もその対象になる、というものです。つまり、`claude -p` が単純に従量課金制へ変わったわけではありません。対象プランではまず別枠の月次クレジットを使い、超過分は追加使用量が有効な場合だけ標準 API レートに移ります。

`claude -p` への依存度を下げるためにコミットメッセージ生成処理を `codex exec` に移しました。

## 2. やりたいこと

やることはシンプルです。lazygit の `files` パネルで `Ctrl+G` を押すと、ステージ済み diff からコミットメッセージの下書きを作り、最後はエディタで確認してから通常の `git commit` として確定します。

以前の実装では `claude -p` を使っていましたが、ここでは前回との差分よりも、`codex exec` を先にバックグラウンドで走らせ、pre-commit hook の待ち時間と重ねる点を中心に見ます。AI に完全に任せるのではなく、下書きだけ作ってもらい、人間が直してからコミットする流れは変えていません。

## 3. 今の lazygit 設定

現在は、lazygit の長いカスタムコマンドを `config.yml` に直接書かず、別のシェルスクリプトに逃がしています。

読者がそのまま置くなら、`~/.config/lazygit/config.yml` は次のような形です。

```yaml:~/.config/lazygit/config.yml
customCommands:
  - key: <c-g>
    context: files
    output: terminal
    command: bash ~/.config/lazygit/lazygit-ai-commit.sh
```

`Ctrl+G` は `files` パネル用のカスタムコマンドとして登録し、`output: terminal` で通常のターミナル上に `git commit` とエディタを出します。
AI 呼び出しの中身は `~/.config/lazygit/lazygit-ai-commit.sh` に置きます。

## 4. codex exec 版の中身

`~/.config/lazygit/lazygit-ai-commit.sh` の全体は次の通りです。

:::details ~/.config/lazygit/lazygit-ai-commit.sh

```sh:~/.config/lazygit/lazygit-ai-commit.sh
#!/usr/bin/env bash

editor=$(mktemp /tmp/lazygit-ai-commit-editor.XXXXXX)
staged_diff=$(mktemp /tmp/lazygit-ai-commit-staged-diff.XXXXXX)
ai_message=$(mktemp /tmp/lazygit-ai-commit-ai-message.XXXXXX)
ai_status=$(mktemp /tmp/lazygit-ai-commit-ai-status.XXXXXX)
ai_stderr=$(mktemp /tmp/lazygit-ai-commit-ai-stderr.XXXXXX)
ai_pid=

cleanup() {
  if [ -n "$ai_pid" ] && kill -0 "$ai_pid" >/dev/null 2>&1; then
    kill "$ai_pid" >/dev/null 2>&1 || true
    wait "$ai_pid" >/dev/null 2>&1 || true
  fi
  rm -f "$editor" "$staged_diff" "$ai_message" "$ai_status" "$ai_stderr"
}
trap cleanup EXIT INT TERM

git diff --cached --no-ext-diff >"$staged_diff"

cat >"$editor" <<'AI_COMMIT_EDITOR'
#!/usr/bin/env bash
set -u

msg_file=$1
ai_message=$LAZYGIT_AI_COMMIT_MESSAGE
ai_status=$LAZYGIT_AI_COMMIT_STATUS

while [ ! -s "$ai_status" ]; do
  sleep 0.1
done

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
AI_COMMIT_EDITOR

chmod +x "$editor"

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

LAZYGIT_AI_COMMIT_MESSAGE="$ai_message" \
  LAZYGIT_AI_COMMIT_STATUS="$ai_status" \
  GIT_EDITOR="$editor" \
  git commit
```

:::

流れのポイントは次の通りです。

- `codex exec` にステージ済み diff を標準入力で渡す。
- `--output-last-message "$ai_message"` で最後の応答をファイルに保存する。
- `--sandbox read-only` と `approval_policy="never"` で、コミットメッセージ生成中にファイルを書き換えない前提にする。
- `--color never` で余計な制御文字を混ぜない。
- 返ってきた内容の1行目だけをコミットメッセージ候補として使う。
- `codex exec` はバックグラウンドで走らせ、そのまま `git commit` を開始する。

`claude -p` から `codex exec` に変えても、やっていることは同じです。ステージ済み diff を読み、1行のコミットメッセージだけを返してもらいます。

## 5. pre-commit hook と並行させる

AI が生成したメッセージは、そのまま `git commit -m` には渡していません。

このスクリプトでは `codex exec` をバックグラウンドで先に走らせ、その直後に `git commit` を始めます。pre-commit hook があるリポジトリでは、hook の実行と AI によるメッセージ生成が並行して進みます。

一時的な `GIT_EDITOR` は、AI の結果が出るまで待ってからコミットメッセージファイルの先頭に下書きを差し込み、最後に `vim` を開きます。つまり、hook 待ちの時間をコミットメッセージ生成に充てられます。

この形にしておくと、AI 生成が成功した場合は下書き入りでエディタが開きます。失敗した場合や `codex` がない場合でも、エディタは開くので通常の手入力コミットに戻れます。

## 6. 良かったこと

今回の変更で一番大きいのは、pre-commit hook の実行中に AI 生成も進むため、待ち時間を短くできることです。

設定面でも分かりやすくなりました。

- lazygit 側の設定は `Ctrl+G` からスクリプトを呼ぶだけ。
- AI 呼び出しの詳細は `lazygit-ai-commit.sh` に閉じ込める。
- pre-commit hook の実行中に AI 生成も進むため、待ち時間を短くできる。
- 失敗時はコミット作業そのものを止めず、エディタを開く。
- 最終的なコミットメッセージは必ず人間が確認する。

`config.yml` に長いプロンプトとコマンド列を入れるより、今の形の方が見通しが良いです。

## 7. 使い方

使い方はシンプルです。

1. lazygit でコミットしたい変更を stage する。
2. `files` パネルで `Ctrl+G` を押す。
3. `codex exec` が staged diff からコミットメッセージ候補を作る。
4. `vim` が開く。
5. 生成された1行を確認し、必要なら直して保存する。
6. 通常の `git commit` として確定する。

日常的には、AI が作った文言をそのまま採用することもあります。ただし、差分の意図とズレることは当然あるので、エディタでの確認は残しています。

## 8. まとめ

`claude -p` で作っていた lazygit の AI コミットメッセージ生成を、`codex exec` に移しました。

やっていることは大きく変えていません。`git diff --cached --no-ext-diff` を AI に渡し、Conventional Commits 形式の1行を作らせ、最後はエディタで確認してコミットします。

この形にすると、pre-commit hook と AI によるコミットメッセージ生成を並行して進められます。

Claude Agent SDK と `claude -p` の扱いが変わるタイミングでもあるので、こういう日々の自動化を `codex exec` 側に寄せるのは、ちょうど良い整理でした。
