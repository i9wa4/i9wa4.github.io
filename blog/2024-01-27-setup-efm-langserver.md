# efm-langserver を Vim/Neovim で利用する
uma-chan
2024-01-27

最近 Vim と Neovim に efm-langserver
を導入したので手順を説明していきます。

## 1. efm-langserver とは

mattn さんの記事を見るのが最良ですね。

[Big Sky :: Lint ツールを Language Server に対応させるコマンド
efm-langserver
作った。](https://mattn.kaoriya.net/software/lang/go/20190205190203.htm)

> どんな言語であろうとも Lint ツールが grep
> と同様の形式で結果を出力してくれさえすれば Language Server
> にしてしまうコマンド

Linter をインストールした後 Vim/Neovim で Info や Error
を画面内に表示させたいときに efm-langserver
が活用できると思えばよいです。

## 2. efm-langserver のインストール

Ubuntu 22.04 (WSL2) でのインストール手順を記載しておきます。

Go 言語を [Go Wiki: Ubuntu - The Go Programming
Language](https://go.dev/wiki/Ubuntu) に従ってインストールします。

``` sh
sudo add-apt-repository -y ppa:longsleep/golang-backports
sudo apt update
sudo apt install -y golang-go
```

efm-langserver を [GitHub - mattn/efm-langserver: General purpose
Language Server](https://github.com/mattn/efm-langserver#installation)
に従ってインストールします。

``` sh
go install github.com/mattn/efm-langserver@latest
```

`~/.profile` などに以下を追記して PATH を通しておきます。

``` sh
export PATH="${HOME}"/go/bin:"${PATH}"
```

## 3. config.yaml の作成

efm-langserver 用設定ファイル
`$XDG_CONFIG_HOME/efm-langserver/config.yaml`
に必要な設定を記述していきます。

[README](https://github.com/mattn/efm-langserver#example-for-configyaml)
を参考に shellcheck を使うための設定のみ抽出したものが以下です。

``` yaml
version: 2
root-markers:
  - .git/
lint-debounce: 1s

tools:
  sh-shellcheck: &sh-shellcheck
    lint-command: 'shellcheck -f gcc -x'
    lint-source: 'shellcheck'
    lint-formats:
      - '%f:%l:%c: %trror: %m'
      - '%f:%l:%c: %tarning: %m'
      - '%f:%l:%c: %tote: %m'

languages:
  sh:
    - <<: *sh-shellcheck
```

## 4. Vim の設定

プラグインマネージャー [dein.vim](https://github.com/Shougo/dein.vim) や
[dpp.vim](https://github.com/Shougo/dpp.vim) などで採用されている TOML
ファイルでのプラグイン設定箇所を抽出しました。遅延起動設定はお好みで。

``` toml
[[plugins]]
repo = 'prabirshrestha/vim-lsp'
on_event = ['VimEnter']

[[plugins]]
repo = 'mattn/vim-lsp-settings'
on_source = ['vim-lsp']
hook_source = '''
let g:lsp_auto_enable = 1
let g:lsp_log_file = ''
let g:lsp_settings = {
  \   'efm-langserver': {
  \     'disabled': v:false,
  \     'allowlist': ['sh'],
  \   }
  \ }
'''
```

## 5. Neovim の設定

Vim 同様に TOML
ファイルの記述を抽出しました。こちらも遅延起動設定はお好みで。

``` toml
[[plugins]]
repo = 'neovim/nvim-lspconfig'
on_event = ['VimEnter']
lua_source = '''
local lspconfig = require('lspconfig')
lspconfig.efm.setup{}
'''
```

## 6. 感想

Linter をインストールできていれば出力形式を見て自力で Language Server
として組み込める……素晴らしいですね！

Linter
は手動でインストールして設定ファイルを管理しておくのが結局一番分かりやすいなと実感しているのですが、その状態で簡単に
Vim/Neovim に反映できる efm-langserver はかなり有り難いです。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-01-27-setup-efm-langserver.html&text=efm-langserver%20%E3%82%92%20Vim%2FNeovim%20%E3%81%A7%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=efm-langserver%20%E3%82%92%20Vim%2FNeovim%20%E3%81%A7%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-01-27-setup-efm-langserver.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-01-27-setup-efm-langserver.html&title=efm-langserver%20%E3%82%92%20Vim%2FNeovim%20%E3%81%A7%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
