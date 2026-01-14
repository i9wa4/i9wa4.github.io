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

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-10-bash-zsh-edit-and-execute-command.html&text=Bash%2FZsh%20%E3%81%A7%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%82%92%E3%82%A8%E3%83%87%E3%82%A3%E3%82%BF%E3%81%A7%E7%B7%A8%E9%9B%86%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Bash%2FZsh%20%E3%81%A7%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%82%92%E3%82%A8%E3%83%87%E3%82%A3%E3%82%BF%E3%81%A7%E7%B7%A8%E9%9B%86%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-10-bash-zsh-edit-and-execute-command.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-10-bash-zsh-edit-and-execute-command.html&title=Bash%2FZsh%20%E3%81%A7%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%82%92%E3%82%A8%E3%83%87%E3%82%A3%E3%82%BF%E3%81%A7%E7%B7%A8%E9%9B%86%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
