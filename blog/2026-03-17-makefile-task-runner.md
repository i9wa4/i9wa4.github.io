# Makefile タスク・ランナーの供養
uma-chan
2026-03-17

## 1. はじめに

dotfiles リポジトリの `bin/Makefile`
をタスク・ランナーとして活用していました。OS 判定、Vim/Neovim
のソースビルド、WSL 設定の管理などをまとめていましたが、Nix
へ移行したため不要になりました。削除前に知見を残しておきます。

参考: [タスク・ランナーとしてのMake \#Makefile -
Qiita](https://qiita.com/shakiyam/items/cdd3c11eba978202a628)

## 2. Makefile 全体

<div class="code-with-filename">

**bin/Makefile**

``` makefile
# [タスク・ランナーとしてのMake \#Makefile - Qiita](https://qiita.com/shakiyam/items/cdd3c11eba978202a628)
SHELL := /bin/bash
.SHELLFLAGS := -o errexit -o nounset -o pipefail -c
.DEFAULT_GOAL := help
.ONESHELL:

# all targets are phony
PHONY_TARGETS := $(shell grep -E '^[a-zA-Z_-]+:' $(MAKEFILE_LIST) | sed 's/://')
.PHONY: $(PHONY_TARGETS)

help:  ## print this help
    @echo 'Usage: make [target]'
    @echo ''
    @echo 'Targets:'
    @awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


# --------------------------------------
# Global Variables
#
MF_GITHUB_DIR := $(shell ghq root)/github.com
MF_DETECTED_OS := $(shell \
    _uname="$$(uname -a)"; \
    if echo "$${_uname}" | grep -q Darwin; then \
        echo "macOS"; \
    elif echo "$${_uname}" | grep -q WSL2; then \
        echo "WSL2"; \
    elif echo "$${_uname}" | grep -q Ubuntu; then \
        echo "Ubuntu"; \
    else \
        echo "Unknown"; \
    fi)

MF_WIN_UTIL_DIR := /mnt/c/work/util


# nvim-build:  ## build Neovim from source
#   ghq get -p neovim/neovim
#   cd $(MF_GITHUB_DIR)/neovim/neovim && \
#   make distclean || true && \
#   make CMAKE_BUILD_TYPE=Release CMAKE_INSTALL_PREFIX="$${HOME}"/.local && \
#   make install && \
#   rm -rf build

# vim-build:  ## build Vim from source
#   ghq get -p vim/vim
# ifeq ($(MF_DETECTED_OS),macOS)
#   cd $(MF_GITHUB_DIR)/vim/vim/src && \
#   make distclean || true && \
#   ./configure \
#       --disable-gui \
#       --enable-clipboard \
#       --enable-darwin \
#       --enable-fail-if-missing \
#       --enable-multibyte \
#       --prefix="$${HOME}"/.local \
#       --with-features=huge \
#       --without-wayland && \
#   make && \
#   make install
# else
#   cd $(MF_GITHUB_DIR)/vim/vim/src && \
#   make distclean || true && \
#   ./configure \
#       --disable-gui \
#       --enable-clipboard \
#       --enable-fail-if-missing \
#       --enable-multibyte \
#       --prefix="$${HOME}"/.local \
#       --with-features=huge \
#       --without-x \
#       --without-wayland && \
#   make && \
#   make install
# endif


# --------------------------------------
# Ubuntu Tasks
#
ubuntu-apt:  ## update and upgrade packages in Ubuntu
    sudo apt-get update && sudo apt-get upgrade -y


# --------------------------------------
# WSL Tasks (Windows integration)
#
define MF_WSLCONF_IN_WSL
[boot]
systemd=true

[interop]
appendWindowsPath=true
endef
export MF_WSLCONF_IN_WSL

define MF_WSLCONFIG_IN_WINDOWS
[wsl2]
localhostForwarding=true
processors=2
swap=0

[experimental]
autoMemoryReclaim=gradual
endef
export MF_WSLCONFIG_IN_WINDOWS

win-copy:  ## copy config files for Windows (WSL only)
    # WSL2
    echo "$${MF_WSLCONF_IN_WSL}" | sudo tee /etc/wsl.conf
    # Windows
    echo "$${MF_WSLCONFIG_IN_WINDOWS}" | \
        tee $(MF_WIN_UTIL_DIR)/etc/dot.wslconfig
    rm -rf $(MF_WIN_UTIL_DIR)
    cp -rf $(MF_GITHUB_DIR)/i9wa4/dotfiles/bin $(MF_WIN_UTIL_DIR)
```

</div>

## 3. テクニック解説

### 3.1. 堅牢なシェル設定

``` makefile
SHELL := /bin/bash
.SHELLFLAGS := -o errexit -o nounset -o pipefail -c
.ONESHELL:
```

| 設定                 | 効果                                                |
|----------------------|-----------------------------------------------------|
| `SHELL := /bin/bash` | デフォルトの `/bin/sh` ではなく Bash を明示的に使用 |
| `-o errexit`         | コマンド失敗時に即座に停止 (`set -e` 相当)          |
| `-o nounset`         | 未定義変数の参照をエラーにする (`set -u` 相当)      |
| `-o pipefail`        | パイプライン中の失敗を検出 (`set -o pipefail` 相当) |
| `.ONESHELL:`         | レシピ内の複数行を単一のシェルプロセスで実行        |

`.ONESHELL:` がないとレシピの各行が別々のシェルで実行されるため、`cd`
した後のコマンドが期待通りに動かないことがあります。

### 3.2. 自己文書化 help ターゲット

``` makefile
help:  ## print this help
    @awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
```

ターゲット定義の行に `## コメント` を書くだけで `make help`
の出力に自動的に表示されます。`.DEFAULT_GOAL := help`
と組み合わせることで、引数なしの `make` で使い方が表示されます。

### 3.3. 動的 .PHONY 定義

``` makefile
PHONY_TARGETS := $(shell grep -E '^[a-zA-Z_-]+:' $(MAKEFILE_LIST) | sed 's/://')
.PHONY: $(PHONY_TARGETS)
```

ターゲット名を正規表現で抽出して全ターゲットを `.PHONY`
にしています。タスク・ランナーとしての Makefile
ではファイルを生成するターゲットがないため、全ターゲットを `.PHONY`
にするのが合理的です。

### 3.4. OS 判定

``` makefile
MF_DETECTED_OS := $(shell \
    _uname="$$(uname -a)"; \
    if echo "$${_uname}" | grep -q Darwin; then \
        echo "macOS"; \
    elif echo "$${_uname}" | grep -q WSL2; then \
        echo "WSL2"; \
    elif echo "$${_uname}" | grep -q Ubuntu; then \
        echo "Ubuntu"; \
    else \
        echo "Unknown"; \
    fi)
```

`uname -a` の出力から OS を判定しています。`ifeq`
と組み合わせることでターゲット内の処理を OS ごとに分岐できます。Vim
のビルドオプション (`--enable-darwin` vs `--without-x`)
の切り替えに使用していました。

### 3.5. define/endef による設定ファイル管理

``` makefile
define MF_WSLCONF_IN_WSL
[boot]
systemd=true

[interop]
appendWindowsPath=true
endef
export MF_WSLCONF_IN_WSL
```

`define`/`endef` で複数行テキストを変数に格納し、`tee`
で設定ファイルに書き出しています。WSL の設定ファイル (`/etc/wsl.conf`,
`.wslconfig`) を Makefile 内で一元管理できるのが利点です。

### 3.6. Vim/Neovim ソースビルド

コメントアウトされていますが、`ghq get -p`
でリポジトリを取得してからソースビルドするレシピが残っています。macOS
では `--enable-darwin` と `--enable-clipboard`、Linux では `--without-x`
を指定する点が OS ごとの差異です。Nix に移行後は `programs.vim`
で宣言的に管理しています。

## 4. まとめ

タスク・ランナーとしての Makefile は `.ONESHELL:` や `define`/`endef`
を活用すればシェルスクリプトの管理ツールとして十分機能します。特に自己文書化
help ターゲットは他のプロジェクトでも使える汎用的なパターンです。Nix
に移行した今は不要になりましたが、Nix
を使わない環境では今でも有用な選択肢だと思います。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-03-17-makefile-task-runner.html&text=Makefile%20%E3%82%BF%E3%82%B9%E3%82%AF%E3%83%BB%E3%83%A9%E3%83%B3%E3%83%8A%E3%83%BC%E3%81%AE%E4%BE%9B%E9%A4%8A%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Makefile%20%E3%82%BF%E3%82%B9%E3%82%AF%E3%83%BB%E3%83%A9%E3%83%B3%E3%83%8A%E3%83%BC%E3%81%AE%E4%BE%9B%E9%A4%8A%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-03-17-makefile-task-runner.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-03-17-makefile-task-runner.html&title=Makefile%20%E3%82%BF%E3%82%B9%E3%82%AF%E3%83%BB%E3%83%A9%E3%83%B3%E3%83%8A%E3%83%BC%E3%81%AE%E4%BE%9B%E9%A4%8A%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
