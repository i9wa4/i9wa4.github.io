# tmux で Vim から Claude Code にテキストを送信するプラグインを作った
uma-chan
2025-06-20

<div class= "page-columns page-rows-contents page-layout-article"><div class="social-share"><a href="https://twitter.com/share?url=https://i9wa4.github.io/blog/2025-06-20-vim-plugin-for-tmux-claude-code.html&text=tmux で Vim から Claude Code にテキストを送信するプラグインを作った" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=tmux で Vim から Claude Code にテキストを送信するプラグインを作った https://i9wa4.github.io/blog/2025-06-20-vim-plugin-for-tmux-claude-code.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https://i9wa4.github.io/blog/2025-06-20-vim-plugin-for-tmux-claude-code.html&title=tmux で Vim から Claude Code にテキストを送信するプラグインを作った" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div></div>

## 1. はじめに

昨日 Claude Code デビューしました！🙌

Claude Code 入力欄に Vim からテキストを送信したかったので Claude Code で
Vim プラグインを作りました。

## 2. プラグインの概要

こちらが作成した Vim プラグインです。

[![](https://i9wa4.github.io/assets/2025-06-20-vim-plugin-for-tmux-claude-code/vim-tmux-send-to-claude-code.jpeg)](https://github.com/i9wa4/vim-tmux-send-to-claude-code)

<https://github.com/i9wa4/vim-tmux-send-to-claude-code>

tmux で同一ウインドウ内の特定の Claude Code ペイン (変数で指定可)
に対して Vim ペインから以下のテキストを送信できます。

- バッファ全体
- ヤンクしたテキスト
- Visual モードで選択したテキスト
- 指定した行範囲のテキスト

## 3. Claude Code を使ってみた感想

もともとヤンクしたテキストを tmux
のペイン間で送信するためのプラグインを作ろうと思っていました。

Claude Code
に任せつつ私のアイデアを共有したところ、気の効いた機能追加やドキュメント整備をサクッとやってくれました。

README.md
で紹介されているプラグインマネージャーが古かったり、キーバインドをデフォルトで押し付けてこようとしたりと既存のプラグインのリポジトリの特徴を掴んでいて面白いかったです。

キーバインド押し付けは主義に反するので直してもらいましたが、プラグインマネージャーは古いままにしておきましょうかね。笑
