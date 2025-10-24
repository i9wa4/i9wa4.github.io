# Vim/Neovim の保存時の LSP フォーマットを :w! のときに無効化する方法
uma-chan
2025-06-04

## 1. はじめに

以下の記事を読んで Conform.nvim
は使っていなかったものの悩みごとが解決する！！！！と思ったので自分の環境でも試してみました。

[Conform.nvimの保存時フォーマットをスキップする方法 \| Atusy’s
blog](https://blog.atusy.net/2025/06/03/skip-conform-nvim-format-on-save/)

## 2. Vim での設定

dpp.vim で管理している TOML ファイルから vim-lsp-settings
向け設定を抜粋しました。

format on save 設定に `v:cmdbang` を使うことで、`:w!`
のときはフォーマットをスキップするようにしています。

``` toml
[[plugins]]
repo = 'mattn/vim-lsp-settings'
on_source = ['vim-lsp']
hook_source = '''
let g:lsp_diagnostics_float_cursor = v:true
let g:lsp_diagnostics_virtual_text_align = "after"
let g:lsp_diagnostics_virtual_text_wrap = "truncate"
let g:lsp_log_file = ''
let g:lsp_settings_enable_suggestions = v:false
let g:lsp_settings = {
\   'deno': {
\     'disabled': v:false,
\   },
\   'efm-langserver': {
\     'disabled': v:false,
\   },
\   'pylsp': {
\     'disabled': v:true,
\   },
\   'pylsp-all': {
\     'disabled': v:true,
\   },
\ }

augroup MyLspSetting
  autocmd!
  autocmd BufWritePost * if !v:cmdbang | execute 'LspDocumentFormatSync' | endif
augroup END
'''
```

## 3. Neovim での設定

同様に TOML で管理している nvim-lspconfig 設定を抜粋しました。

`vim.v.cmdbang` を使っています。

``` toml
[[plugins]]
repo = 'neovim/nvim-lspconfig'
on_event = ['VimEnter']
lua_source = '''
-- https://github.com/uga-rosa/ddc-source-lsp-setup
require('ddc_source_lsp_setup').setup()

-- https://github.com/neovim/nvim-lspconfig?tab=readme-ov-file#configuration
local lspconfig = require('lspconfig')
-- lspconfig.pylsp.setup{}
lspconfig.denols.setup{}
lspconfig.efm.setup{}

-- :help lsp-defaults-disable
vim.api.nvim_create_autocmd('LspAttach', {
  callback = function(ev)
    -- unset
    vim.bo[ev.buf].formatexpr = nil
    vim.bo[ev.buf].omnifunc = nil

    -- unmap
    -- vim.keymap.del('n', 'K', { buffer = ev.buf })

    -- map
    local opts = { buffer = bufnr, noremap = true, silent = true }
    vim.keymap.set('n', '<space>lf', vim.diagnostic.open_float, opts)
  end,
})

vim.api.nvim_create_autocmd('BufWritePost', {
  callback = function()
    if vim.v.cmdbang == 0 then
      vim.lsp.buf.format()
    end
  end,
})
'''
```

## 4. まとめ

これまでは保存したいけどフォーマットしたくない場面を回避するためにフォーマット用のキーバインドを用意して
format on save を無効化していました。

たまにフォーマットし忘れて辛かったのでこの対応でとってもハッピーになりました！
