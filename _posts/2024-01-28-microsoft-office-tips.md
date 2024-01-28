---
layout: post
title:  "Microsoft Office 向け Tips"
date:   2024-01-28 00:34:12 +0900
categories: blog
tags: tips
---

{% include tag.html %}

Table of Content:
- Table of Content
{:toc}

<!-- # h1 -->

こんにちは。i9wa4 です。

自分用に Microsoft Office 向けの Tips を書き残しておきます。

## 1. Excel

### 1.1. Excel VBA

- アドイン追加先
    - `%USERPROFILE%\AppData\Roaming\Microsoft\AddIns`

### 1.2. Excel 関数

- シート名を記載したセルB2を利用したハイパーリンク作成
    - `=HYPERLINK("#'"&B2&"'!$A$1",B2)`

## 2. Word

### 2.1. Normal.dotm 作成

1. `%APPDATA%\Microsoft\Templates\Normal.dotm` 削除
1. デザインを作成し既定に設定する
    - テーマ設定
        - 見出し: 游ゴシック Arial
        - 本文: 游ゴシック Medium Arial
    - アウトライン --> 新しいアウトラインの定義 --> オプション --> レベルと対応付ける見出しスタイル
    - 本文: 10.5pt
    - 見出し 1: 18pt Bold
