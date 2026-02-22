# 最近の Vim プラグイン開発のアイデア
uma-chan
2024-09-22

dotfiles から切り離したくなってきたらそれがプラグインの作り時。

今温めているアイデアをメモしておきます。

## 1. ローカル設定の読み込み

おそらく以下が近い気がしていて、自分の dotfiles
の設定を切り出しつつ自分が使いやすい形で作りたいです。

[thinca/vim-localrc: Enable configuration file of each
directory.](https://github.com/thinca/vim-localrc)

## 2. Terminal 管理

Vim/Neovim
のターミナルを気軽に開いたり選択範囲のコマンドを流し込むためのプラグイン。

dotfiles の中で温めてはいるものの、tmux
に対する優位性を見い出せずあまり使ってません。

他には REPL (IPython) 向けの設定もあります。ただ、細々とした Python
コードを Vim で動作確認したいユースケースがあるのかなあ？

## 3. Jupytext と ipynb の同期

Jupytext で ipynb と py を同期させるプラグイン。

通常は Jupytext をコマンドで実行させると思いますが、非同期で同期させる
(？) 挙動をさせたいですね。

Jupytext に変換しておくと Git 管理しやすくなるものの、Jupytext
がマイナー過ぎてチーム開発で自分が他人に推奨できない点がネックで最近あまり使わなくなりつつあります。

みんな ipynb の管理どうしているんだろう。。

## 4. Tabline 設定

頑張って書き上げたため切り離してもよいかも。

ちなみに最近 Statusline は使ってません！

## 5. \[2024-10-25 追記\] virtualtext を活用したメモプラグイン

コードリーディング中にメモを残すためのプラグイン。

メモ一覧をリポジトリ内に保持しておきたい。

Linter
を参考にすればいけそうだけど、コードの行追加削除に追従させるのは自分の技術力では難しそう。

## 6. \[2024-11-25 追記\] dbt プラグイン (Deno)

Vim/Neovim 両対応で最低限の機能をもったものがほしい。

## 7. \[2024-11-25 追記\] Zenn \<–\> Quarto の本文変換

コードブロックの書き方を変換するだけで足りる？

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-09-22-vim-plugin-idea.html&text=%E6%9C%80%E8%BF%91%E3%81%AE%20Vim%20%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E9%96%8B%E7%99%BA%E3%81%AE%E3%82%A2%E3%82%A4%E3%83%87%E3%82%A2%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=%E6%9C%80%E8%BF%91%E3%81%AE%20Vim%20%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E9%96%8B%E7%99%BA%E3%81%AE%E3%82%A2%E3%82%A4%E3%83%87%E3%82%A2%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-09-22-vim-plugin-idea.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-09-22-vim-plugin-idea.html&title=%E6%9C%80%E8%BF%91%E3%81%AE%20Vim%20%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E9%96%8B%E7%99%BA%E3%81%AE%E3%82%A2%E3%82%A4%E3%83%87%E3%82%A2%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
