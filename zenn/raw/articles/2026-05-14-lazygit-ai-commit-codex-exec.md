---
title: "lazygit のコミットメッセージを `codex exec` で生成する"
emoji: "🐴"
type: "tech"
topics:
  - "lazygit"
  - "git"
  - "codexcli"
published: true
published_at: 2026-05-14 21:30
---

## 1. はじめに

以前 lazygit のカスタムコマンドから Claude Code を `claude -p` で呼び出して、ステージ済み diff からコミットメッセージを生成する記事を書きました。

@[card](https://i9wa4.github.io/blog/2026-03-14-lazygit-commit-message.html)

今回はこの処理を Codex CLI の `codex exec` に移しました。狙いは、コミットメッセージ生成をバックグラウンドで進めながら、そのまま `git commit` を開始して pre-commit hook と並行させることです。

@[card](https://support.claude.com/ja/articles/15036540-claude-%E3%83%97%E3%83%A9%E3%83%B3%E3%81%A7-claude-agent-sdk-%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%99%E3%82%8B)

背景として、こちらの Claude 公式記事では、2026-06-15 から対象プランで Claude Code の `claude -p` が Agent SDK 用の月次クレジット対象になると説明されています。

## 2. やりたいこと

lazygit の `files` パネルで `Ctrl+G` を押すと、ステージ済み diff からコミットメッセージの下書きを作り、最後はエディタで確認してから通常の `git commit` として確定します。

## 3. 今の lazygit 設定

lazygit の長いカスタムコマンドは `config.yml` に直接書かず、別のシェルスクリプトに逃がしています。

```yaml:~/.config/lazygit/config.yml
customCommands:
  - key: <c-g>
    context: files
    output: terminal
    command: bash ~/.config/lazygit/lazygit-ai-commit.sh
```

`Ctrl+G` は `files` パネル用のカスタムコマンドとして登録し、`output: terminal` で通常のターミナル上に `git commit` とエディタを出します。

## 4. codex exec の中身

`~/.config/lazygit/lazygit-ai-commit.sh` の全体は次の通りです。

Codex CLI v0.130.0 で動作確認をしたスクリプトになります。

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

このスクリプトが AI に任せる範囲は、ステージ済み diff を読んで1行のコミットメッセージだけを返すところまでです。

## 5. pre-commit hook と並行させる

このスクリプトでは `codex exec` をバックグラウンドで先に走らせ、その直後に `git commit` を始めます。
pre-commit hook があるリポジトリでは、hook の実行と AI によるメッセージ生成が並行して進みます。

pre-commit hook と AI コミットメッセージ生成が成功した場合は下書き入りでエディタが開きます。
Codex CLI がない場合でも、エディタは開くので通常の手入力コミットに戻れます。

## 6. 良かったこと

この形で一番大きいのは pre-commit hook の実行中に AI コミットメッセージ生成も進むため待ち時間を短くできることです。
自動コミットと違ってコミットメッセージを一応確認するという半自動な点も lazygit の利用体験にマッチしていて気に入っています。

## 7. まとめ

仕様変更に振り回されがちですが自分の道具として磨いていきましょう！
Codex CLI も同等の制限が入る可能性があるのでそのときはローカル LLM を模索したいと思います。
