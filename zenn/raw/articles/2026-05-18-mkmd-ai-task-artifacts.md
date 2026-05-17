---
title: "mkmd で AI エージェントの作業メモをリポジトリ外に逃がす"
emoji: "🐴"
type: "tech"
topics:
  - "aiagent"
  - "markdown"
  - "cli"
  - "bash"
  - "dotfiles"
published: true
published_at: 2026-05-18 01:30
---

## 1. はじめに

Claude Code や Codex CLI を日常的に使っていると、調査メモ、作業計画、レビュー結果、検証ログのような Markdown ファイルがよく生まれます。

これらは作業中だけ使うファイルですが、完全な一時ファイルとも言い切れません。あとから読み返したいこともありますし、完了報告の根拠として残したいこともあります。

そこで私は `mkmd` という小さなスクリプトを使っています。

`mkmd` は、AI エージェント用の Markdown 作業ファイルを、リポジトリの外側にプロジェクト別・日付別・ブランチ別で作る `mktemp` wrapper です。

## 2. 何が困るのか

AI エージェントに少し重い作業を任せると、途中でメモを残したくなります。

たとえば次のようなファイルです。

- 調査対象と結論をまとめたメモ
- 実装前のチェックリスト
- レビュー観点と指摘一覧
- コマンド実行結果の抜粋
- DONE 報告に添える検証証跡

これらをリポジトリ内に置くと `git status` が汚れます。`.gitignore` を追加してもよいのですが、プロジェクトごとに名前を考えるのが面倒です。

一方で `/tmp` に置くと、再起動や掃除で消えます。セッションが長くなるほど、「さっきの調査メモはどこだっけ」が起きます。

欲しかったのは、次の条件を満たす置き場です。

- リポジトリを汚さない
- プロジェクトごとに自然に分かれる
- 日付とブランチで作業単位が分かる
- ファイル名が衝突しない
- コマンド一発で作れる

`mkmd` はこのための薄い道具です。

## 3. どう便利か

### 3.1. あとから探せる

作業ファイルは `~/.local/state/mkmd/` 以下に、プロジェクト別・日付別・ブランチ別で整理されます。

```text
~/.local/state/mkmd/
├── i9wa4-dotfiles/
│   └── 2026-05-18-main/
│       ├── research/
│       │   └── nix-investigation-aB3xKq.md
│       └── plans/
│           └── plan-Xk9mZw.md
└── mycompany-api/
    └── 2026-05-18-feature-auth/
        └── reviews/
            └── completion-nW2vHj.md
```

ディレクトリ名を見れば、どのリポジトリの、いつの、どのブランチの作業かわかります。同じ日に複数のブランチを行き来しても混ざりません。

### 3.2. リポジトリが汚れない

出力先は `$XDG_STATE_HOME`、既定では `~/.local/state` です。git リポジトリには触れないので、作業用 Markdown のために `.gitignore` を増やす必要がありません。

### 3.3. AI エージェントが自律的に使える

AGENTS.md や CLAUDE.md に「作業ファイルは `mkmd` で作る」と書いておけば、エージェントが調査・計画・レビューの各フェーズで必要なファイルを自分で作れます。

```sh
mkmd --dir research --label api-investigation
```

複数ステップの作業では、`mkmd` で作った Markdown を task artifact として使うと便利です。元のチェックリスト、作業メモ、検証結果、残ブロッカーを1つのファイルに集めておくと、会話ログが長くなっても状況を追いやすくなります。

### 3.4. 消しやすい

`mkmd` の出力は作業用の state です。不要になったら日付単位で消せます。

```sh
rm -rf ~/.local/state/mkmd/i9wa4-dotfiles/2026-05-18-*
```

重要な成果物はリポジトリへ入れるべきですが、調査メモや検証ログまで全部コミット対象にする必要はありません。

## 4. `mkmd` の基本

使い方はこの形にしています。

```sh
mkmd --dir research --label api-investigation
```

実行すると、stdout には作成された Markdown ファイルのパスだけが出ます。

```text
~/.local/state/mkmd/myteam-api/2026-05-18-feature-auth/research/api-investigation-aB3xKq.md
```

パスの構造は次の通りです。

```text
$MKMD_BASE_DIR/<owner>-<repo>/YYYY-MM-DD-<branch>/<dir>/<label>-<random>.md
```

| セグメント      | 意味                                         |
| --------------- | -------------------------------------------- |
| `MKMD_BASE_DIR` | 既定では `$XDG_STATE_HOME/mkmd`              |
| `owner-repo`    | git remote から推定した owner と repository  |
| `YYYY-MM-DD`    | 実行日                                       |
| `branch`        | 現在の git branch。`/` は `-` に置換         |
| `dir`           | `--dir` で指定した分類                       |
| `label-random`  | `--label` と `mktemp` のランダムサフィックス |

git リポジトリ外で実行した場合は、現在ディレクトリ名を使った `local-<dirname>` 系のパスへフォールバックします。

## 5. スクリプト

実装は Bash です。

:::details mkmd

```bash:mkmd
#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail
set -o posix

BASE_DIR="${MKMD_BASE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/mkmd}"

print_usage() {
  cat <<EOF
Usage:
  mkmd --dir DIR --label LABEL

mktemp wrapper that creates a markdown working file.

Creates:
  \$MKMD_BASE_DIR/<owner>-<repo>/YYYY-MM-DD-<branch>/<DIR>/<LABEL>-<XXXXXX>.md

Environment:
  MKMD_BASE_DIR  Override base directory

Options:
  --dir DIR      Directory name under the daily session
  --label LABEL  File label included in the filename
  -h, --help     Show this help and exit
EOF
}

LABEL=""
DIR=""

while [[ $# -gt 0 ]]; do
  case $1 in
  -h | --help)
    print_usage
    exit 0
    ;;
  --dir)
    DIR="$2"
    shift 2
    ;;
  --label)
    LABEL="$2"
    shift 2
    ;;
  -*)
    echo "Unknown option: $1" >&2
    exit 1
    ;;
  *)
    echo "Error: Unknown argument: $1" >&2
    exit 1
    ;;
  esac
done

if [[ -z $DIR || -z $LABEL ]]; then
  echo "Error: --dir and --label are required" >&2
  print_usage >&2
  exit 1
fi

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"

if [[ -n $repo_root ]]; then
  remote_url="$(git remote get-url origin 2>/dev/null || true)"
  if [[ -n $remote_url ]]; then
    remote_url="${remote_url%.git}"
    project_name="${remote_url##*/}"
    remote_url="${remote_url%/*}"
    project_owner="${remote_url##*[:/]}"
  else
    project_owner="local"
    project_name="$(basename "$repo_root")"
  fi
  branch_name="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
  branch_name="${branch_name//\//-}"
else
  project_owner="local"
  project_name="$(basename "$(pwd -P)")"
  branch_name="local"
fi

date_dir="$(date +%Y-%m-%d)-${branch_name}"
target_dir="${BASE_DIR}/${project_owner}-${project_name}/${date_dir}/${DIR}"

mkdir -p "$target_dir"
temp_path="$(mktemp "${target_dir}/${LABEL}-XXXXXX")"
trap 'rm -f "$temp_path"' EXIT
file_path="${temp_path}.md"
mv "$temp_path" "$file_path"
trap - EXIT

echo "$file_path"
echo "Created: $file_path" >&2
```

:::

stdout にパスだけを出し、作成メッセージは stderr に出すのが地味に大事です。

別のスクリプトから次のように受け取れます。

```sh
file=$(mkmd --dir tmp --label compact-save)
printf '# Context Save\n' >"$file"
```

## 6. エージェントに教える

私の環境では、AGENTS.md や CLAUDE.md に次のようなルールを書いています。

```markdown
- Create working files (not tracked by git) with `mkmd` (`mkmd --help`)
- Common dir/label combinations:

    | --dir    | --label                    |
    | -------- | -------------------------- |
    | draft    | `${topic}`                 |
    | research | `${feature}-investigation` |
    | plans    | plan                       |
    | reviews  | completion                 |
    | tmp      | `${purpose}`               |
```

これだけで、エージェントは必要に応じて `mkmd --help` を読み、自分で `--dir` と `--label` を選びます。人間が毎回「この調査結果はこのファイルに書いて」と指定しなくてもよくなります。

## 7. まとめ

AI エージェントの作業は、コード変更だけでなく、調査、計画、レビュー、検証のメモを伴います。

`mkmd` で Markdown 作業ファイルをリポジトリ外に作るようにしておくと、次の状態を作れます。

- `git status` は作業対象の差分だけを示す
- 作業メモはプロジェクト・日付・ブランチで整理される
- エージェントが自分で作業ファイルを作れる
- 不要になった state は日付単位で消せる

大きな仕組みではありませんが、AI エージェントを日常的に使うなら、この小さな置き場の設計が効いてきます。
