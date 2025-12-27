# Bash/Zsh でコマンドをエディタで編集する
uma-chan
2025-05-10

<div class= "page-columns page-rows-contents page-layout-article"><div class="social-share"><a href="https://twitter.com/share?url=https://i9wa4.github.io/blog/2025-05-10-bash-zsh-edit-and-execute-command.html&text=Bash/Zsh でコマンドをエディタで編集する" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Bash/Zsh でコマンドをエディタで編集する https://i9wa4.github.io/blog/2025-05-10-bash-zsh-edit-and-execute-command.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https://i9wa4.github.io/blog/2025-05-10-bash-zsh-edit-and-execute-command.html&title=Bash/Zsh でコマンドをエディタで編集する" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div></div>

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
