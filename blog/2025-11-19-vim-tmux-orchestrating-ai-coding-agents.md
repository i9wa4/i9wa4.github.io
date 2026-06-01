# Vim と tmux で複数の AI エージェントを操作する
uma-chan
2025-11-19

> [!NOTE]
>
> この記事は [Vim 駅伝](https://vim-jp.org/ekiden/) の 2025-11-19
> の記事です。
>
> 前回は 2025-11-17 ぺりー さんの
> [ドットコマンドで再現可能な編集を設計する \|
> Medium](https://satorunooshie.medium.com/designing-repeatable-edits-8ec574ff0acd)
> でした。

## 1. AIエージェント並行実行の現在地 (2025年11月時点)

Claude Code や Codex CLI
を1つのタスクに対して複数起動させると便利ですが取り回しが難しいですよね。

この需要に応えたのが2025年10月29日にリリースされた Cursor 2.0 でした。

> **マルチエージェント**
>
> 新しいエディタでエージェントを管理。サイドバーでエージェントとプランを一覧・操作できます。
>
> 1つのプロンプトで最大8つのエージェントを並列実行できます。ファイル競合を防ぐために、git
> worktree
> またはリモートマシンを使用します。各エージェントは、コードベースの独立したコピー上で個別に動作します。

[新しいコード生成モデルとエージェントインターフェース ·
Cursor](https://cursor.com/changelog/2-0)

これはかなり強力な機能追加ですが今のところ Cursor
以外で同様の体験を得るのは難しいです。

Vim と tmux
で似たような操作を実現させるアイデアを共有するので、ターミナルでの AI
エージェント操作についても盛り上げていきましょう！

## 2. 対象読者

- 必須
  - Vim & tmux を利用できる方
- 推奨
  - Vim 補完プラグイン [ddc.vim](https://github.com/Shougo/ddc.vim)
    を利用できる方

## 3. Vim と tmux による複数のAIエージェント操作実演

構築後の操作画面を先にお見せします。Claude Code *1 と Codex CLI* 2
に同じプロンプトを送っている様子です。

![](<https://www.youtube.com/watch?v=AyE-ruGOGCc>)

## 4. 利用ツール等の解説

### 4.1. zeno.zsh

<https://github.com/yuki-yano/zeno.zsh>

動画の冒頭で vde-layout 起動時に利用している zeno.zsh
のスニペット設定例を共有します。

<div class="code-with-filename">

**~/.config/zeno/config.yml**

``` yaml
snippets:
  - name: (vde-layout) dev
    keyword: vd
    snippet:
      vde-layout dev

  - name: (vde-layout) review
    keyword: vr
    snippet:
      vde-layout review
```

</div>

### 4.2. vde-layout

<https://github.com/yuki-yano/vde-layout>

`vde-layout` コマンドを実行することで予め設定した tmux
レイアウトを適用できます。

設定ファイル例は以下となります。

<div class="code-with-filename">

**~/.config/vde/layout.yml**

``` yaml
presets:
  review:
    name: review
    description: review
    windowMode: current-window
    layout:
      type: horizontal
      ratio: [1, 1]
      panes:
        - type: vertical
          ratio: [3, 1]
          panes:
            - name: editor
              command: vim -c "execute 'edit' '.i9wa4/temp.md'->expand()"
              focus: true
            - name: codex
              command: codex --yolo
        - type: vertical
          ratio: [3, 1]
          panes:
            - name: claude
              command: claude --dangerously-skip-permissions
            - name: codex
              command: codex --yolo
```

</div>

### 4.3. ddc-source-slash-commands

<https://github.com/i9wa4/ddc-source-slash-commands>

Vim 補完プラグイン [ddc.vim](https://github.com/Shougo/ddc.vim)
のソースプラグインです。

カスタムスラッシュコマンドを補完候補として表示するために利用します。

カスタムスラッシュコマンドに対応していない AI
エージェントの場合はファイルのフルパスを送信すれば問題ないです。

柔軟にプロンプトを調整できるのが Vim で操作するメリットですね。

### 4.4. vim-tmux-send-to-ai-cli

<https://github.com/i9wa4/vim-tmux-send-to-ai-cli>

Vim から tmux 経由で AI
エージェント起動中のペインにプロンプトを送信するためのプラグインです。

送信先：

- (デフォルト) 同一ウインドウの中で最も小さい番号のペインに送信
- 同一ウインドウの特定のペインに送信
- 同一ウインドウの全てのペインに送信

送信内容：

- カーソル行
- 段落
- 選択範囲
- ファイル全体
- 行範囲 (例: 10～20行目)

### 4.5. ペイン間の競合を回避するプロンプト

複数の AI
エージェントを並行実行する際、中間生成するドキュメントの競合を避けるために
`.i9wa4/` ディレクトリ (私の環境で global gitignore
されているディレクトリ) と tmux ペイン番号を活用します。

``` md
- 生成するファイル名は `YYYYMMDD-pN-xxxx.md` の形式とする
    - `YYYYMMDD`: 日付 (例: `20251105`)
    - `pN`: tmux ペイン番号 (例: `p0`, `p1`, `p2`)
    - `xxxx`: ファイルの目的 (例: `review`, `plan`, `memo`)
    - 例: `.i9wa4/20251105-p2-review.md`
- tmux ペイン番号Nは `tmux display-message -p -t "$${TMUX_PANE}" '#{pane_index}'` で取得する
```

このプロンプトによって AI
エージェントが生成する中間ファイルが他ペインと競合しなくなります。

ちなみに global gitignore
なディレクトリについては以下のポストを参考にしました。

<blockquote class="twitter-tweet">

<p lang="ja" dir="ltr">

自分の Git 環境ではグローバルな gitignore で .mizchi/\*
が無視されており、どうもならんときはここに .mizchi/run.sh
などが置かれています
<a href="https://t.co/b7r4omHnPs">https://t.co/b7r4omHnPs</a>
</p>

— mizchi (@mizchi)
<a href="https://twitter.com/mizchi/status/1914543131888066561?ref_src=twsrc%5Etfw">April
22, 2025</a>
</blockquote>

<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## 5. おわりに

足りない部分を自作して補うことで Vim と tmux で複数の AI
エージェントを操作するアイデアを共有しました。

今後もターミナルでの AI
エージェント操作が盛り上がっていくことを願っています！

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-11-19-vim-tmux-orchestrating-ai-coding-agents.html&text=Vim%20%E3%81%A8%20tmux%20%E3%81%A7%E8%A4%87%E6%95%B0%E3%81%AE%20AI%20%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88%E3%82%92%E6%93%8D%E4%BD%9C%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Vim%20%E3%81%A8%20tmux%20%E3%81%A7%E8%A4%87%E6%95%B0%E3%81%AE%20AI%20%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88%E3%82%92%E6%93%8D%E4%BD%9C%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-11-19-vim-tmux-orchestrating-ai-coding-agents.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-11-19-vim-tmux-orchestrating-ai-coding-agents.html&title=Vim%20%E3%81%A8%20tmux%20%E3%81%A7%E8%A4%87%E6%95%B0%E3%81%AE%20AI%20%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88%E3%82%92%E6%93%8D%E4%BD%9C%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
