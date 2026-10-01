# SKK + 絵文字辞書でどこからでも絵文字を打つ
uma-chan
2026-04-30

## 1. 課題：絵文字を打つのが面倒

絵文字を打つとき毎回IMEで適当にキーワードを入力したり、Slackであれば `:`
で絵文字検索したりしていました。

いつでもどこでも同じ方法で絵文字を入力するために SKK
を使って実現することにしました。

## 2. 英語名を覚えるとどこでも打てる

SKK には abbrev モードという入力モードがあります。

`/`
を打って英語キーワードを入力すると、辞書に登録されたエントリを変換候補として引けます。

``` text
/tada          → 🎉
/partying_face → 🥳
/fire          → 🔥
```

スニペット展開に近い感覚です。`tada`
と打てば変換できますが、そのためには `tada`
というキーワードが登録されていることを知っている必要があります。結局は英語名を覚えることが前提です。

[emoji-cheat-sheet](https://github.com/ikatyang/emoji-cheat-sheet)
は絵文字の英語名を一覧できるリファレンスです。「この絵文字は英語で何と呼ぶか」をここで確認しながら覚えておけば、SKK
が動いている環境ならどこでも絵文字が打てるようになります。

スマホでもキーワードを覚えていれば絵文字をヒットさせることができる場合があるので、その点でも便利です。

## 3. skk-emoji-jisyo

[skk-emoji-jisyo](https://github.com/uasi/skk-emoji-jisyo) は SKK
用の絵文字辞書です。gemoji の shortcode
名をキーとした英語のみのエントリで構成されています。

``` text
tada /🎉/
partying_face /🥳/
fire /🔥/
clinking_glasses /🥂/
star /⭐/
```

この辞書を追加しておくことで、abbrev モードでの英語変換が機能します。

## 4. クライアント別設定

### 4.1. skkeleton (Vim / Neovim)

[skkeleton](https://github.com/vim-skk/skkeleton) は Vim / Neovim 用の
SKK プラグインです。

私の環境では [dpp.vim](https://github.com/Shougo/dpp.vim)
で辞書リポジトリ自体をプラグインとして管理しています。`skk-dev/dict` と
`uasi/skk-emoji-jisyo` を dpp に登録しておくと
`$XDG_CACHE_HOME/dpp/repos/` 以下にクローンされるので、そのパスを
`globalDictionaries` に渡しています。

``` vim
let s:skk_dev_path = $XDG_CACHE_HOME->expand() .. '/dpp/repos/github.com/skk-dev/dict'
let s:skk_emoji_path = $XDG_CACHE_HOME->expand() .. '/dpp/repos/github.com/uasi/skk-emoji-jisyo'
call skkeleton#config({
\   'globalDictionaries': [
\     s:skk_dev_path .. '/SKK-JISYO.L',
\     s:skk_dev_path .. '/SKK-JISYO.jinmei',
\     s:skk_dev_path .. '/SKK-JISYO.assoc',
\     s:skk_emoji_path .. '/SKK-JISYO.emoji.utf8',
\   ],
\   'userDictionary': '~/path/to/skkdict.utf8',
\ })
call skkeleton#register_keymap('input', ';', 'henkanPoint')
imap <C-k> <Plug>(skkeleton-enable)
```

### 4.2. macSKK (macOS)

[macSKK](https://github.com/mtgto/macSKK) は macOS
の入力ソースとして動作する SKK クライアントです。IME
として登録するため、ブラウザ・Slack・ターミナル・あらゆるアプリで同じ辞書が使えます。

macSKK は sandbox の制約で
`~/Library/Containers/net.mtgto.inputmethod.macSKK/Data/Documents/Dictionaries/`
以下にしか辞書ファイルを置けません。

私は Nix home-manager の activation スクリプトで dpp
キャッシュから自動コピーしています。

``` nix
home.activation.setupMacSkkDict = lib.hm.dag.entryAfter [ "writeBoundary" ] ''
  macSkkDir="$HOME/Library/Containers/net.mtgto.inputmethod.macSKK/Data/Documents/Dictionaries"
  dppSkkDev="${XDG_CACHE_HOME:-$HOME/.cache}/dpp/repos/github.com/skk-dev/dict"
  dppSkkEmoji="${XDG_CACHE_HOME:-$HOME/.cache}/dpp/repos/github.com/uasi/skk-emoji-jisyo"
  mkdir -p "$macSkkDir"
  [[ -f "$dppSkkDev/SKK-JISYO.L" ]] && cp -f "$dppSkkDev/SKK-JISYO.L" "$macSkkDir/SKK-JISYO.L"
  [[ -f "$dppSkkEmoji/SKK-JISYO.emoji.utf8" ]] && cp -f "$dppSkkEmoji/SKK-JISYO.emoji.utf8" "$macSkkDir/SKK-JISYO.emoji.utf8"
'';
```

`home-manager switch` を実行するだけで辞書が同期されます。dpp
を一度でも起動してキャッシュが作られていることが前提です。

Nix を使っていない場合は、手動で `SKK-JISYO.emoji.utf8`
を上記のディレクトリにコピーすれば動きます。

## 5. まとめ

- SKK abbrev モード (`/` + 英語名) で絵文字変換できる
- 英語名を覚えることが本質で、[emoji-cheat-sheet](https://github.com/ikatyang/emoji-cheat-sheet)
  がその辞書になる
- [skk-emoji-jisyo](https://github.com/uasi/skk-emoji-jisyo)
  を追加することで gemoji shortcode 名で絵文字を変換できるようになる
- macSKK なら OS レベルで動くのでどのアプリでも使える
- skkeleton なら Vim / Neovim 内で完結する

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-04-30-type-emoji-everywhere-with-skk.html&text=SKK%20%2B%20%E7%B5%B5%E6%96%87%E5%AD%97%E8%BE%9E%E6%9B%B8%E3%81%A7%E3%81%A9%E3%81%93%E3%81%8B%E3%82%89%E3%81%A7%E3%82%82%E7%B5%B5%E6%96%87%E5%AD%97%E3%82%92%E6%89%93%E3%81%A4%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=SKK%20%2B%20%E7%B5%B5%E6%96%87%E5%AD%97%E8%BE%9E%E6%9B%B8%E3%81%A7%E3%81%A9%E3%81%93%E3%81%8B%E3%82%89%E3%81%A7%E3%82%82%E7%B5%B5%E6%96%87%E5%AD%97%E3%82%92%E6%89%93%E3%81%A4%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-04-30-type-emoji-everywhere-with-skk.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-04-30-type-emoji-everywhere-with-skk.html&title=SKK%20%2B%20%E7%B5%B5%E6%96%87%E5%AD%97%E8%BE%9E%E6%9B%B8%E3%81%A7%E3%81%A9%E3%81%93%E3%81%8B%E3%82%89%E3%81%A7%E3%82%82%E7%B5%B5%E6%96%87%E5%AD%97%E3%82%92%E6%89%93%E3%81%A4%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
