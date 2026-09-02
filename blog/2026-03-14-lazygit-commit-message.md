# lazygit で AI コミットメッセージ生成
uma-chan
2026-03-14

## 1. はじめに

lazygit のカスタムコマンド機能を使い、ステージ済みの diff を Claude
(Haiku)
に渡してコミットメッセージを自動生成する設定を作りました。小ネタです。

## 2. 設定

<div class="code-with-filename">

**lazygit.nix**

``` nix
programs.lazygit.settings.customCommands = [
  {
    key = "<c-g>";
    context = "files";
    output = "terminal";
    command = ''
      MSG=$(git diff --cached | claude --no-session-persistence --print --model haiku \
        'Generate ONLY a one-line Git commit message following Conventional Commits format \
        (type(scope): description). Types: feat, fix, docs, style, refactor, test, chore. \
        Based strictly on the diff from stdin. Output ONLY the message, nothing else.') \
        && git commit -e -m "$MSG"
    '';
  }
];
```

</div>

`output = "terminal"` にすることで `git commit -e`
がターミナル上で動き、エディタが開きます。

## 3. 使い方

1.  lazygit でファイルをステージする
2.  files パネルで `Ctrl+G` を押す
3.  Claude Haiku が diff を読んでコミットメッセージを生成する
4.  エディタが生成されたメッセージを pre-fill した状態で開く
5.  内容を確認・修正してコミット

モデルは Haiku を指定しているので速くて安上がりです。

## 4. まとめ

`git diff --cached` をそのまま LLM
に渡すシンプルな構成で、実用的な下書きが得られます。
最終確認はエディタで自分の目を通すので、完全に任せきりにならないのがちょうどいいバランスです。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-03-14-lazygit-commit-message.html&text=lazygit%20%E3%81%A7%20AI%20%E3%82%B3%E3%83%9F%E3%83%83%E3%83%88%E3%83%A1%E3%83%83%E3%82%BB%E3%83%BC%E3%82%B8%E7%94%9F%E6%88%90%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=lazygit%20%E3%81%A7%20AI%20%E3%82%B3%E3%83%9F%E3%83%83%E3%83%88%E3%83%A1%E3%83%83%E3%82%BB%E3%83%BC%E3%82%B8%E7%94%9F%E6%88%90%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-03-14-lazygit-commit-message.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-03-14-lazygit-commit-message.html&title=lazygit%20%E3%81%A7%20AI%20%E3%82%B3%E3%83%9F%E3%83%83%E3%83%88%E3%83%A1%E3%83%83%E3%82%BB%E3%83%BC%E3%82%B8%E7%94%9F%E6%88%90%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
