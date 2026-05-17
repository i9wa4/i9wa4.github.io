---
title: "Zsh compinit の仕組みを理解して起動時間を短縮する"
emoji: "🐴"
type: "tech"
topics:
  - "zsh"
published: true
---

## 1. はじめに

Zsh の起動時間を計測すると compinit 処理がボトルネックになっていることがあります。
compinit の仕組みを理解し、適切に設定することで起動時間を短縮する方法を紹介します。

Zinit を使った起動時間短縮については以下の記事も合わせてご覧ください。
以下の記事では compinit を遅延読み込みする方法も紹介しています。

@[card](https://zenn.dev/i9wa4/articles/2026-01-01-zsh-startup-optimization-zinit)

以降では compinit の実行時間を短縮する方法に焦点を当てます。

## 2. 環境

- macOS 26.2
- Zsh 5.9

## 3. compinit とは

compinit は Zsh の補完システムを初期化する関数です。

```zsh
autoload -Uz compinit
compinit
```

この2行で補完機能が有効になります。compinit を実行しないと Tab キーによる補完が機能しません。

## 4. zcompdump とは

compinit は処理結果を zcompdump ファイルにキャッシュします。

```text
~/.zcompdump
```

キャッシュの中身:

- ファイルメタデータ (補完ファイル数、zsh バージョン)
- コマンドと補完関数のマッピング
- 自動読み込み設定

## 5. compinit の自動判定機能

compinit は毎回実行時に以下をチェックします:

- fpath 内の補完ファイル数が変わったか
- Zsh のバージョンが変わったか

変わっていれば zcompdump を再生成し、変わっていなければキャッシュを使用します。

公式ドキュメント[^1]から引用:

> If the number of completion files changes, compinit will recognise this and produce a new dump file.

つまり、公式には毎回 `compinit` を実行すればよく、ユーザーが頻度を指定する必要はありません。

## 6. ベンチマーク

hyperfine で計測した結果です (10回実行の平均)。

| 方式                         | 実行時間 |
| ---------------------------- | -------- |
| compinit (キャッシュなし)    | 157.7ms  |
| compinit (キャッシュあり)    | 30.1ms   |
| compinit -C (キャッシュあり) | 18.1ms   |

### 6.1. 差分

| 比較                | 差            |
| ------------------- | ------------- |
| キャッシュの効果    | 約 128ms 短縮 |
| -C オプションの効果 | 約 12ms 短縮  |

キャッシュの存在が最も重要です。

## 7. -C オプションとは

compinit -C は判定処理をスキップします。

公式ドキュメント[^1]から引用:

> The check performed to see if there are new functions can be omitted by giving the option -C. In this case the dump file will only be created if there isn't one already.

スキップされる処理:

- compaudit (セキュリティチェック)
- 新規補完関数の自動検出
- ダンプファイルの再生成チェック

## 8. 高速化パターン

### 8.1. 公式の方式

```zsh
autoload -Uz compinit
compinit
```

毎回実行。内部で自動判定します。

### 8.2. 24時間キャッシュパターン

判定処理をスキップしつつ、定期的にフル実行するパターンです。

```zsh
autoload -Uz compinit
_zcompdump="${XDG_CACHE_HOME:-${HOME}/.cache}/zsh/.zcompdump-${HOST}-${ZSH_VERSION}"
mkdir -p "${_zcompdump:h}"

setopt extendedglob
if [[ -n "${_zcompdump}"(#qN.mh+24) ]]; then
  compinit -d "${_zcompdump}"
else
  compinit -C -d "${_zcompdump}"
fi
```

このパターンは ctechols の Gist[^2] がおそらく起源です。

### 8.3. glob qualifier の説明

`(#qN.mh+24)` は Zsh の glob qualifier です。

| 記号    | 意味                           |
| ------- | ------------------------------ |
| `#q`    | glob qualifier として解釈      |
| `N`     | マッチしなくてもエラーにしない |
| `.`     | 通常ファイルのみ               |
| `mh+24` | 修正時刻が24時間以上前         |

glob qualifier を使うには `setopt extendedglob` が必要です。

## 9. どちらを選ぶべきか

| 方式                 | メリット       | デメリット   |
| -------------------- | -------------- | ------------ |
| 公式 (毎回 compinit) | シンプル、確実 | 約 12ms 遅い |
| 24時間キャッシュ     | 約 12ms 速い   | 複雑、非公式 |

12ms の差が気になるなら 24時間キャッシュパターンを、シンプルさを重視するなら公式方式を選んでください。

## 10. おわりに

compinit の最適化はほんの僅かな効果ですが、気になる場合は試してみてください！

[^1]: [zsh: 20 Completion System](https://zsh.sourceforge.io/Doc/Release/Completion-System.html)

[^2]: [ctechols Gist - Speed up zsh compinit by only checking cache once a day](https://gist.github.com/ctechols/ca1035271ad134841284)
