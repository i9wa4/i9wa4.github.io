---
title: "ターミナル上でのファイルビューアーとしての Neovim 入門"
emoji: "🐴"
type: "tech"
topics:
  - "neovim"
  - "cli"
  - "terminal"
  - "dotfiles"
published: false
---

## 1. はじめに

Neovim と oil.nvim を使うと、ターミナル上でディレクトリやファイルをキーボードだけで手軽に閲覧できます。

## 2. インストール

Homebrew (macOS):

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

起動後 `-` を押すと oil.nvim が開きファイルビュアーとして機能します。

## 5. 基本操作

| キー      | 操作                        | 説明                                           |
| --------- | --------------------------- | ---------------------------------------------- |
| `-`       | 親ディレクトリを開く        | カレントバッファの親ディレクトリに移動         |
| `<Enter>` | ファイル/ディレクトリを開く | カーソル位置のエントリを開く                   |
| `j`       | 1行下に移動                 | 標準 Neovim モーション                         |
| `k`       | 1行上に移動                 | 標準 Neovim モーション                         |
| `gg`      | 先頭エントリへ移動          | 標準 Neovim モーション                         |
| `G`       | 末尾エントリへ移動          | 標準 Neovim モーション                         |

ファイルを開いた後も `-` を押すと oil のディレクトリビューに戻れます。

### 5.1. ファイルを開いた後の操作

| キー     | 動作                             |
| -------- | -------------------------------- |
| `Ctrl-d` | 半ページ下スクロール             |
| `Ctrl-u` | 半ページ上スクロール             |
| `gg`     | ファイル先頭へ移動               |
| `G`      | ファイル末尾へ移動               |
| `:q`     | ウィンドウを閉じる               |
| `:q!`    | 強制終了する (困ったときはこれ)  |

## 6. まとめ

init.lua を追加するだけで始められます。行番号を表示したいなど気になる設定が出てきたら、`init.lua` を AI に修正してもらおう。
