# 最近の Vim プラグイン開発のアイデア
uma-chan
2025-02-20

[少し前の Vim
プラグイン開発のアイデア記事](https://i9wa4.github.io/./2024-09-22-vim-plugin-idea.md)
で7個のアイデアを書いてました。

## 1. ローカル設定の読み込み

おそらく以下が近い気がしていて、自分の dotfiles
の設定を切り出しつつ自分が使いやすい形で作りたいです。

[thinca/vim-localrc: Enable configuration file of each
directory.](https://github.com/thinca/vim-localrc)

相変わらず自作のローカル設定読み込みは活用してます。設定ファイル作成コマンドと最下層のローカル設定ファイルにジャンプするキーバインドが結構お気に入り。

## 2. Terminal 管理

Vim/Neovim
のターミナルを気軽に開いたり選択範囲のコマンドを流し込むためのプラグイン。

dotfiles の中で温めてはいるものの、tmux
に対する優位性を見い出せずあまり使ってません。

他には REPL (IPython) 向けの設定もあります。ただ、細々とした Python
コードを Vim で動作確認したいユースケースがあるのかなあ？

やっぱり tmux
をゴリゴリ使ってるので用途が結構限定的ですね。CWDに対してちょっとしたコマンドを実行したいときなんかは重宝してます。

## 3. Jupytext と ipynb の同期

Jupytext で ipynb と py を同期させるプラグイン。

最近 Databricks を使うようになったのですが、 Databricks では .ipynb を
.py
として保存する機能がもともと備わっていたので尚のこと必要でなくなってしまいました。次回はこの項目を削除しようかな。

## 4. Tabline 設定

頑張って書き上げたため切り離してもよいかも。

Tabline 用と Statusline
用の2関数だけだし既存プラグインとの差別化には至らないのでこの項目も削除かな。

## 5. virtualtext を活用したメモプラグイン

コードリーディング中にメモを残すためのプラグイン。

メモ一覧をリポジトリ内に保持しておきたい。

Linter
を参考にすればいけそうだけど、コードの行追加削除に追従させるのは自分の技術力では難しそう。

## 6. dbt プラグイン (Deno)

これは作りました！一応以下が紹介記事です。

[Vim/Neovimのdbt開発環境の現状とVimを救う話](https://zenn.dev/genda_jp/articles/2024-12-02-vim-neovim-environment-for-dbt)

バグ取りをする必要あり。

## 7. Zenn \<–\> Quarto の本文変換

コードブロックの書き方を変換するだけで足りる？

個人執筆記事については Quarto で書いて Zenn
に連携という流れにしたいので、利用機会があまりなさそう。。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-02-20-vim-plugin-idea.html&text=%E6%9C%80%E8%BF%91%E3%81%AE%20Vim%20%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E9%96%8B%E7%99%BA%E3%81%AE%E3%82%A2%E3%82%A4%E3%83%87%E3%82%A2%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=%E6%9C%80%E8%BF%91%E3%81%AE%20Vim%20%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E9%96%8B%E7%99%BA%E3%81%AE%E3%82%A2%E3%82%A4%E3%83%87%E3%82%A2%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-02-20-vim-plugin-idea.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-02-20-vim-plugin-idea.html&title=%E6%9C%80%E8%BF%91%E3%81%AE%20Vim%20%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E9%96%8B%E7%99%BA%E3%81%AE%E3%82%A2%E3%82%A4%E3%83%87%E3%82%A2%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
