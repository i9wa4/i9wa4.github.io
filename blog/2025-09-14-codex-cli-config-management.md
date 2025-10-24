# Codex CLI の設定ファイルを dotfiles で管理する
uma-chan
2025-09-14

Codex CLI を使い始めたのですが dotfiles
使いにとっては辛い部分があり距離を置いてしまっていました。

今回力技で設定ファイルを dotfiles
で管理する方法を思いついたので紹介します。

## 1. Codex CLI の設定ファイルについて

Codex CLI の設定ファイルは `~/.config/codex/config.toml` です。

内容は例えば以下のような感じです。

``` toml
[projects."/Users/uma/ghq/github.com/i9wa4/dotfiles"]
trust_level = "trusted"
```

## 2. 問題点

`config.toml`
にはフルパスが書かれるため複数のマシンで設定を管理するのが面倒です。

かつどのプロジェクトを信頼するかの設定もマシンごとに異なることが多いので
`config.toml` をそのまま dotfiles で管理するのはイマイチと言えます。

## 3. 解決策

共通設定だけ dotfiles
の管理対象とし、プロジェクト別の設定はスクリプトで生成してしまうというものです。

これで困ることはほとんどないでしょう！

### 3.1. config.toml の生成スクリプト

共通設定を `~/.config/codex/config.common.toml`
に書いておき、プロジェクトごとの設定を自動生成して `config.toml`
を生成させます。

※リポジトリを ghq で管理していることを前提としています。

<div class="code-with-filename">

**~/.config/codex/generate_config.sh**

``` sh
#!/usr/bin/env bash
set -euo pipefail

GHQ_BASE="${HOME}"/ghq/github.com
COMMON="./config.common.toml"
OUTPUT="./config.toml"

cd "$(dirname "$0")"

# Copy common settings
cp -f "${COMMON}" "${OUTPUT}"

# Add project-specific settings
find "${GHQ_BASE}" -maxdepth 3 -type d -name ".git" 2>/dev/null \
  | sed 's|\.git$||' \
  | sort \
  | while read -r repo; do
    [[ -z ${repo} ]] && continue
    echo "
[projects.\"${repo}\"]
trust_level = \"trusted\""
  done >>"${OUTPUT}"

echo "Generated: ${OUTPUT}"
```

</div>

## 4. おわりに

dotfiles で管理しづらいから Codex CLI
と距離を置いていたみなさん、これで今日から使えるようになりましたよ！
