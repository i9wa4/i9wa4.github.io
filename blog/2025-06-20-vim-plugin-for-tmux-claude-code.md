# tmux で Vim から Claude Code にテキストを送信するプラグインを作った
uma-chan
2025-06-20

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

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-20-vim-plugin-for-tmux-claude-code.html&text=tmux%20%E3%81%A7%20Vim%20%E3%81%8B%E3%82%89%20Claude%20Code%20%E3%81%AB%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%82%92%E9%80%81%E4%BF%A1%E3%81%99%E3%82%8B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=tmux%20%E3%81%A7%20Vim%20%E3%81%8B%E3%82%89%20Claude%20Code%20%E3%81%AB%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%82%92%E9%80%81%E4%BF%A1%E3%81%99%E3%82%8B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-20-vim-plugin-for-tmux-claude-code.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-06-20-vim-plugin-for-tmux-claude-code.html&title=tmux%20%E3%81%A7%20Vim%20%E3%81%8B%E3%82%89%20Claude%20Code%20%E3%81%AB%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%82%92%E9%80%81%E4%BF%A1%E3%81%99%E3%82%8B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
