---
title: "ターミナル上でのファイルビューアーとしてサクっと Neovim を使ってみる"
emoji: "🐴"
type: "tech"
topics:
  - "neovim"
  - "cli"
  - "terminal"
published: true
published_at: 2026-03-15 15:30
---

:::message
この記事は [Vim 駅伝](https://vim-jp.org/ekiden/) の 2026-03-11 の記事です。
:::

## 1. はじめに

Neovim と oil.nvim を使うと、ターミナル上でディレクトリやファイルをキーボードだけで手軽に閲覧できます。

設定ファイルは最小限で、インストールから使い始めまで数分で完了します。

## 2. インストール

macOS:

```sh
brew install neovim
```

Linux (Debian/Ubuntu):

```sh
sudo apt install neovim
```

## 3. init.lua

以下を `~/.config/nvim/init.lua` に追加します。

```lua:~/.config/nvim/init.lua
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.uv.fs_stat(lazypath) then
  vim.fn.system({ "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim", lazypath })
end
vim.opt.rtp:prepend(lazypath)
require("lazy").setup({
  {
    "stevearc/oil.nvim",
    opts = {},
    keys = { { "-", "<Cmd>Oil<CR>", desc = "Open parent directory" } },
  },
})
```

lazy.nvim が初回起動時に oil.nvim を自動でインストールして読み込みます。

初回起動時は lazy.nvim のプラグイン管理画面が表示されます。oil.nvim のインストールが終わったら `q` で閉じてください。

## 4. 起動

```sh
nvim
```

起動後 `-` を押すと oil.nvim が開きファイルビューアーとして機能します。

## 5. 基本操作

| キー      | 操作                            |
| --------- | ------------------------------- |
| `-`       | 親ディレクトリを開く            |
| `<Enter>` | ファイル/ディレクトリを開く     |
| `j`       | 1行下に移動                     |
| `k`       | 1行上に移動                     |
| `gg`      | 先頭エントリへ移動              |
| `G`       | 末尾エントリへ移動              |
| `:q`      | Neovim を終了する               |
| `:q!`     | 強制終了する (困ったときはこれ) |

ファイルを開いた後も `-` を押すと oil のディレクトリビューに戻れます。

### 5.1. ファイルを開いた後の操作

| キー     | 操作                 |
| -------- | -------------------- |
| `Ctrl-d` | 半ページ下スクロール |
| `Ctrl-u` | 半ページ上スクロール |
| `gg`     | ファイル先頭へ移動   |
| `G`      | ファイル末尾へ移動   |

## 6. まとめ

`nvim` で起動して `-` を押すだけで oil.nvim によるディレクトリビューが開きます。ファイルを開いた後も `-` で戻れ、確認が終わったら `:q` で終了できます。

行番号の表示など気になる設定が出てきたら、`init.lua` を AI に少しずつ育てさせましょう。
