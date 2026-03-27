---
title: "lazygit で AI コミットメッセージ生成"
emoji: "✍️"
type: "tech"
topics:
  - "lazygit"
  - "git"
  - "claudecode"
  - "nix"
published: true
published_at: 2026-03-14 00:00
---

## 1. はじめに

lazygit のカスタムコマンド機能を使い、ステージ済みの diff を Claude (Haiku) に渡してコミットメッセージを自動生成する設定を作りました。小ネタです。

## 2. 設定

```nix:lazygit.nix
programs.lazygit.settings.customCommands = [
  {
    key = "<c-g>";
    context = "files";
    output = "terminal";
    command = ''
      MSG=$(git diff --cached | claude --no-session-persistence --print --model haiku \
        'Generate ONLY a one-line Git commit message following Conventional Commits format \
        (type(scope): description). Types: feat, fix, docs, style, refactor, test, chore. \
        Based strictly on the diff from stdin. Output ONLY the message, nothing else.') \
        && git commit -e -m "$MSG"
    '';
  }
];
```

`output = "terminal"` にすることで `git commit -e` がターミナル上で動き、エディタが開きます。

## 3. 使い方

1. lazygit でファイルをステージする
2. files パネルで `Ctrl+G` を押す
3. Claude Haiku が diff を読んでコミットメッセージを生成する
4. エディタが生成されたメッセージを pre-fill した状態で開く
5. 内容を確認・修正してコミット

モデルは Haiku を指定しているので速くて安上がりです。

## 4. まとめ

`git diff --cached` をそのまま LLM に渡すシンプルな構成で、実用的な下書きが得られます。
最終確認はエディタで自分の目を通すので、完全に任せきりにならないのがちょうどいいバランスです。
