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

Claude Code や Codex CLI を使っていると、調査メモ、作業計画、レビュー結果、検証ログのような Markdown ファイルがよく生まれます。

これらは一時ファイルではありますが、完全に捨ててよいものでもありません。作業中は後続のエージェントや自分が読み返しますし、完了報告では「何を根拠に DONE と言っているのか」を示す証拠にもなります。

そこで私は `mkmd` という小さなスクリプトを使っています。

一言でいうと、`mkmd` は AI エージェント用の Markdown 作業ファイルを、リポジトリの外側に、プロジェクト別・日付別・ブランチ別で作る `mktemp` wrapper です。

この記事では、`mkmd` を作った理由、出力パスの考え方、AI エージェントの task artifact としての使い方を紹介します。

## 2. リポジトリ内でも `/tmp` でもつらい

AI エージェントに少し重い作業を任せると、途中でメモを残したくなります。

たとえば次のようなファイルです。

- 調査対象と結論をまとめたメモ
- 実装前のチェックリスト
- レビュー観点と指摘一覧
- コマンド実行結果の抜粋
- DONE 報告に添える検証証跡

これらをリポジトリ内に置くと `git status` が汚れます。`.gitignore` を追加してもよいのですが、プロジェクトごとに名前を考えるのが面倒です。

一方で `/tmp` に置くと再起動や掃除で消えます。エージェントのセッションが長くなるほど、「さっきの調査メモはどこだっけ」が起きます。

欲しかったのは、次の条件を満たす置き場です。

- リポジトリを汚さない
- プロジェクトごとに自然に分かれる
- 日付とブランチで作業単位が分かる
- ファイル名が衝突しない
- コマンド一発で作れる
- エージェントが自律的に使える

`mkmd` はこのための薄い道具です。

## 3. `mkmd` の基本

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

| セグメント      | 意味                                           |
| --------------- | ---------------------------------------------- |
| `MKMD_BASE_DIR` | 既定では `$XDG_STATE_HOME/mkmd`                |
| `owner-repo`    | git remote から推定した owner と repository    |
| `YYYY-MM-DD`    | 実行日                                         |
| `branch`        | 現在の git branch。`/` は `-` に置換           |
| `dir`           | `--dir` で指定した分類                         |
| `label-random`  | `--label` と `mktemp` のランダムサフィックス   |

git リポジトリ外で実行した場合は、現在ディレクトリ名を使った `local-<dirname>` 系のパスへフォールバックします。

ポイントは、作業ファイルの分類をエージェントに毎回説明しなくても、コマンドが自然にプロジェクト・日付・ブランチを含めてくれることです。

## 4. task artifact として使う

`mkmd` の用途は単なるメモ置き場ではありません。

複数ステップの作業では、私は `mkmd` で作った Markdown を task artifact として扱います。ここでいう task artifact は、作業中に変わっていくチェックリスト、調査結果、検証結果、残ブロッカーを1つに集めたファイルです。

たとえば、エージェントに次のように指示します。

```markdown
Create one task artifact with `mkmd` before implementation.
Keep the original checklist there.
Before DONE, verify every checklist item against evidence.
```

すると、作業ファイルは次のような形になります。

```markdown
# Parser Fix Task

## Original Checklist

- [ ] Reproduce the parser failure
- [ ] Add a focused regression test
- [ ] Fix the parser
- [ ] Run the parser test suite
- [ ] Report remaining blockers

## Evidence

- command output
- changed files
- decisions
```

この形式にしておくと、会話ログが長くなっても「元の依頼に対して何が終わっているか」を見失いにくくなります。

tmux-a2a-postman のような Markdown mail の仕組みとも相性がよいです。ただし、`mkmd` 自体は postman 専用ではありません。postman は依頼や返信の配送を扱い、`mkmd` は作業の中身と証跡を置く場所を扱います。

後で日本語の tmux-a2a-postman 記事を書くとき、この分離は前提になります。手紙としての依頼と、検証可能な task artifact は別の層です。

## 5. エージェントに教える

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

これだけで、エージェントは必要に応じて `mkmd --help` を読み、自分で `--dir` と `--label` を選びます。

人間が毎回「この調査結果はこのファイルに書いて」と指定しなくてもよくなります。重要なのは、作業メモをリポジトリ内へ勝手に作らせないことです。

## 6. スクリプト

実装は Bash です。

私が使っている版は、git remote から owner/repo を取り、現在 branch をパスに含め、最後は `mktemp` で衝突しない名前を作ります。

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

実運用では、stdout にパスだけを出し、作成メッセージは stderr に出すのが地味に大事です。

別のスクリプトから次のように安全に受け取れます。

```sh
file=$(mkmd --dir tmp --label compact-save)
printf '# Context Save\n' >"$file"
```

## 7. 消しやすさも設計に入れる

`mkmd` の出力は作業用の state です。不要になったら日付単位で消してよい前提にしています。

```sh
rm -rf ~/.local/state/mkmd/i9wa4-i9wa4.github.io/2026-05-18-*
```

重要な成果物はリポジトリへ入れるべきです。一方で、作業中の調査メモや検証ログまで全部コミット対象にすると、リポジトリが作業場の散らかりを背負います。

`mkmd` はその境界線を作るための道具です。

## 8. まとめ

AI エージェントの作業は、コード変更だけでなく、調査、計画、レビュー、検証のメモを伴います。

そのメモをどこに置くかを決めていないと、リポジトリが汚れるか、必要な証跡が消えるか、会話ログの奥に埋もれます。

`mkmd` で Markdown 作業ファイルをリポジトリ外に作るようにしておくと、次の状態を作れます。

- `git status` は作業対象の差分だけを示す
- 作業メモはプロジェクト・日付・ブランチで整理される
- エージェントが自分で task artifact を作れる
- DONE 報告の根拠を後から確認しやすい
- 不要になった state は日付単位で消せる

大きな仕組みではありませんが、AI エージェントを日常的に使うなら、この小さな置き場の設計が効いてきます。
