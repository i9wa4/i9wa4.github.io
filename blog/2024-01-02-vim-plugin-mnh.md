# 自作 Vim/Neovim プラグイン markdown-number-header.vim の紹介
uma-chan
2024-01-02

少し前に作った Vim/Neovim プラグインの紹介記事となります。

## 1. プラグイン概要

- <https://github.com/i9wa4/markdown-number-header.vim>
  - Markdown の見出し番号を付ける or 更新するプラグインです。
  - Deno と Denops に依存しています。

## 2. プラグインを作ることになったきっかけ

[Markdown All in
One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)
という VSCode 拡張の Markdown 見出し番号を付ける機能を Vim
でも使いたかったのですが、CLI アプリケーション (Formatter) や Vim
プラグインを探しても見つからなかったので自作しようと思い至りました。

## 3. Denops プラグインとして作ろうと思った理由

まず、自分が Vim 上でしか使わないため CLI アプリケーションとしてではなく
Vim プラグインとして作ろうとは思ってました。 そして私は Vim 使いなので
Vim script で書くか Denops プラグインとして TypeScript
で書くかの二択で、楽しそうなので後者を選びました。

## 4. Denops プラグイン開発体験について

初めて Denops プラグインを作ったし、しかも TypeScript
にも触れたことがなかったのですが意外と困ることは少なかったです。
核となる見出し番号を振る処理は TypeScript
の本領発揮という感じで楽に書けましたね。
まず以下のドキュメントに従ってチュートリアルを終えて、あとは先人の
Denops
プラグインのリポジトリを覗いてお作法を学びつつプラグインを完成させました。

- 参考ページ:
  - [Deno で Vim/Neovim のプラグインを書く (denops.vim) \|
    Zenn](https://zenn.dev/lambdalisue/articles/b4a31fba0b1ce95104c9)
  - [Introduction - Denops
    Documentation](https://vim-denops.github.io/denops-documentation/)
    (英語版)

## 5. 感想

今も毎日使っているプラグインなので「無いんだったら作ればいい」精神でフッ軽に作れたことを嬉しく思ってます。
今後も必要なものは自分で作っていたいですね。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-01-02-vim-plugin-mnh.html&text=%E8%87%AA%E4%BD%9C%20Vim%2FNeovim%20%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%20markdown-number-header.vim%20%E3%81%AE%E7%B4%B9%E4%BB%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=%E8%87%AA%E4%BD%9C%20Vim%2FNeovim%20%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%20markdown-number-header.vim%20%E3%81%AE%E7%B4%B9%E4%BB%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-01-02-vim-plugin-mnh.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-01-02-vim-plugin-mnh.html&title=%E8%87%AA%E4%BD%9C%20Vim%2FNeovim%20%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%20markdown-number-header.vim%20%E3%81%AE%E7%B4%B9%E4%BB%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
