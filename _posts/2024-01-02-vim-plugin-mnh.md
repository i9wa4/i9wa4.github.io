---
layout: post
title:  "自作 Vim/Neovim プラグイン markdown-number-header.vim の紹介"
date:   2024-01-02 21:47:46 +0900
categories: blog
tags: vim dev
---

Table of Content:
- Table of Content
{:toc}

{% include tag.html %}

<!-- # h1 -->

こんにちは。i9wa4です。  
少し前に作った Vim/Neovim プラグインの紹介記事となります。

## 1. プラグイン概要

- [i9wa4/markdown-number-header.vim: Automatic numbering for headings.](https://github.com/i9wa4/markdown-number-header.vim)
    - Markdown の見出し番号を付ける or 更新するプラグインです。
    - Deno と Denops に依存しています。


## 2. プラグインを作ることになったきっかけ

- 下記 VSCode 拡張の Markdown 見出し番号を付ける機能を多用していたので Vim でも使いたかったのですが、探しても見つからなかったことがきっかけで自作しようと思い至りました。
    - [Markdown All in One - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)

## 3. Denops プラグインとして作ろうと思った理由

まず、自分が Vim 上でしか使わないため CLI アプリケーションとしてではなく Vim プラグインとして作ろうとは思ってました。  
そして私は Vim 使いなので Vim script で書くか Denops プラグインとして TypeScript で書くかの二択で、楽しそうなので後者を選びました。

## 4. 苦労した点

初めて Denops プラグインを作った & TypeScript に触れたことがなかったのですが意外と困ることは少なかったです。  
核となる見出し番号を振る処理は TypeScript の本領発揮という感じで楽に書けましたね。  
以下のドキュメントに従ってチュートリアルを終えて、あとは先人の Denops プラグインのリポジトリを覗きにいき完成させました。

チュートリアル
- [Deno で Vim/Neovim のプラグインを書く (denops.vim) | Zenn](https://zenn.dev/lambdalisue/articles/b4a31fba0b1ce95104c9)
    - 英語版: [Introduction - Denops Documentation](https://vim-denops.github.io/denops-documentation/)

## 5. 感想

毎日使っているプラグインなので「無いんだったら作ればいい」精神でフッ軽に作れたことを嬉しく思ってます。  
今後も必要なものは自分で作っていたいですね。
