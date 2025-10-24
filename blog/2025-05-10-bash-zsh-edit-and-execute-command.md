# Bash/Zsh でコマンドをエディタで編集する
uma-chan
2025-05-10

## 1. はじめに

Bash/Zsh
で入力中のコマンドの編集にエディタが使えるという便利機能の話です。名前がパッと出てこないのでメモ代わりに記事にしておきます。

## 2. Bash

`C-x C-e` で `$VISUAL` で指定したエディタが開きます。

[bash で入力中のコマンドをエディタで編集して実行するショートカットキー
\#Bash - Qiita](https://qiita.com/oirik/items/1253a12d7f4b88c4ffe0)

## 3. Zsh

Bash と同等の機能を実現させるには以下のように設定します。

<div class="code-with-filename">

**~/.zshrc**

``` sh
autoload -Uz edit-command-line
zle -N edit-command-line
bindkey '^x^e' edit-command-line
```

</div>

## 4. おわりに

**edit-and-execute-command** あるいは **edit-command-line**
と呼ばれる機能であると覚えましょう！
