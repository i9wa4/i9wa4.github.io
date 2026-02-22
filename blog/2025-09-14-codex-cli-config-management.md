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

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-09-14-codex-cli-config-management.html&text=Codex%20CLI%20%E3%81%AE%E8%A8%AD%E5%AE%9A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%20dotfiles%20%E3%81%A7%E7%AE%A1%E7%90%86%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Codex%20CLI%20%E3%81%AE%E8%A8%AD%E5%AE%9A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%20dotfiles%20%E3%81%A7%E7%AE%A1%E7%90%86%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-09-14-codex-cli-config-management.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-09-14-codex-cli-config-management.html&title=Codex%20CLI%20%E3%81%AE%E8%A8%AD%E5%AE%9A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%20dotfiles%20%E3%81%A7%E7%AE%A1%E7%90%86%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
