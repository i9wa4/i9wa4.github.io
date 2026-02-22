# 今更ながら Vim に EditorConfig を導入しました
uma-chan
2025-05-06

## 1. はじめに

dotfiles で .editorconfig
を置いたままにしていたのですが利用できていなかったので今回利用していくこととしました。

## 2. 導入手順

EditorConfig プラグインが Vim
本体にビルトインされているのでインストールは不要です。

``` plaintext
:h editorconfig-install
```

で説明されていますが vimrc に以下を追加すればよいです。

``` plaintext
packadd! editorconfig
```

また `~/.editorconfig` を以下のように作成しました。

設定可能な項目は

[editorconfig/editorconfig-vim: EditorConfig plugin for
Vim](https://github.com/editorconfig/editorconfig-vim)

に記載されています。

<div class="code-with-filename">

**.editorconfig**

``` ini
# EditorConfig is awesome: https://EditorConfig.org
# top-most EditorConfig file
root = true

# https://github.com/editorconfig/editorconfig-vim
[*]
charset = utf-8
end_of_line = lf
indent_size = 4
indent_style = space
insert_final_newline = true
max_line_length = 80
trim_trailing_whitespace = true

# 2 space indentation
[{*.{css,mmd,sh,tf,tftpl,tfvars,toml,ts,vim,yaml,zshenv,zshrc},vimrc}]
indent_size = 2

# Tab indentation (no size specified)
[{*.go,Makefile}]
indent_style = tab

# Windows
[{*.{bat,cmd}]
end_of_line = crlf
```

</div>

最後に vimrc で FileType
イベントで設定していた上記と重複している設定を削除しました。

## 3. 感想

この設定は VS Code
等の他のエディタでも使えるので育成のしがいがあります。

EditorConfig プラグインの help
ファイルを見ると色々設定ができるっぽいのですが、あまり凝ったことはしなくていいかなと思っています。

設定項目を見回してみたのですが `max_line_length`
の効き方があまり理解できていないので追々学んでいきます。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-06-editorconfig-vim.html&text=%E4%BB%8A%E6%9B%B4%E3%81%AA%E3%81%8C%E3%82%89%20Vim%20%E3%81%AB%20EditorConfig%20%E3%82%92%E5%B0%8E%E5%85%A5%E3%81%97%E3%81%BE%E3%81%97%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=%E4%BB%8A%E6%9B%B4%E3%81%AA%E3%81%8C%E3%82%89%20Vim%20%E3%81%AB%20EditorConfig%20%E3%82%92%E5%B0%8E%E5%85%A5%E3%81%97%E3%81%BE%E3%81%97%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-06-editorconfig-vim.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-06-editorconfig-vim.html&title=%E4%BB%8A%E6%9B%B4%E3%81%AA%E3%81%8C%E3%82%89%20Vim%20%E3%81%AB%20EditorConfig%20%E3%82%92%E5%B0%8E%E5%85%A5%E3%81%97%E3%81%BE%E3%81%97%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
