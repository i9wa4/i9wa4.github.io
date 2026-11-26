# Vimへの初コントリビューションの経緯と学び
uma-chan
2025-07-14

> [!NOTE]
>
> この記事は [Vim 駅伝](https://vim-jp.org/ekiden/) の 2025-07-14
> の記事です。
>
> 前回は 2025-07-11 NI57721 さんの [Vim が Wayland
> のクリップボードをサポート](https://zenn.dev/vim_jp/articles/wayland-clipboard-feature-in-vim)
> でした。

## 1. はじめに

Vim 本体に出したバグ修正の Pull Request がマージされました。

<https://github.com/vim/vim/commit/b3eaae21b9f681d23466e7caa0b9d7e32cb4b206>

以降でバグ発見の経緯と学びを共有します。

![私に Vim Contributor
表記が付与されている様子](https://i9wa4.github.io/assets/2025-07-14-my-first-vim-contribution/vim-contributor.png)

## 2. バグ発見の経緯

私は Vim の HEAD (main ブランチの最新コミット)
ビルドを日課にしています。

自分でビルドするとビルドオプションを指定できたり最新機能が使えたりして楽しいです。

そうしているうちにある日ビルトインのファイラープラグインである Netrw.vim
のファイル一覧に空行の入るバグが入ったことに気付きました。

気になって Vim 本体の Issue や Pull Request
を見ても同様のバグが報告されていなかったので自分で Pull Request
を出すことにしました。

……反省点として後述しますがこの判断はちょっと考慮が足りなかったです。

## 3. Pull Request 作成まで

OSS プロジェクトに Pull Request を出したことがなかったのですが、
CONTRIBUTING.md を読めばいいであろうということは知っていたので Vim
のリポジトリの CONTRIBUTING.md を読みました。

<https://github.com/vim/vim/blob/master/CONTRIBUTING.md>

今回については Signing-off commits
推奨ということくらいで特に細かく何かを守る必要はないのかなという理解をしました。

とは言えそれでは不安があったので直近の Netrw.vim 関連のコミットや Pull
Request をざっくり確認してみました。

実際の修正内容については Netrw.vim
プラグインの直近1-2週間の間に入ったコミットの影響であろうことは分かっていたので
Claude Code
にバグ混入コミットを特定してもらって、修正案も出してもらいました。

自分のマシン (macOS) では1行追加するだけで修正できることが分かり、勢いで
Pull Request を作成しました。

## 4. Pull Request のレビュー

Netrw.vim のメンテナの @saccarosium さんにレビューしていただき Upstream
と書き味を揃える Suggestion をいただきマージされました。

## 5. 学び

### 5.1. 反省点

Pull Request
を出すまでは近眼的になって気付かなかったのですが今回の修正対象のファイルのトップに

[vim/runtime/pack/dist/opt/netrw/autoload/netrw.vim](https://github.com/vim/vim/blob/68ee1cf7de36bdd6e642807c8beda751112aaab8/runtime/pack/dist/opt/netrw/autoload/netrw.vim)

> ``` vim
> " Upstream: <https://github.com/saccarosium/netrw.vim>
> ```

と書かれている通り Netrw.vim には Upstream のリポジトリ

<https://github.com/saccarosium/netrw.vim>

が存在します。

実際 Upstream では私が Pull Request
を作成する2日前に既に本件は修正済みとなっていました。

というわけで本来はこの Upstream
のリポジトリを最初に確認するのが正しい手順でした。

この状況を理解していた場合でも早めに Vim
本体側へ適用してほしい旨を相談することに変わりはなかったのですが、全てを知った上で行動するのが最善だったなあと思います。

だれがどのように関わって Vim
という巨大なリポジトリが成り立っているのかもっと知ろうと思うようになりました。

もう1つの反省点は、改行回りが関係するので macOS だけでなく Windows
についても考慮する必要があったという点です。

Vim
のクロスプラットフォーム対応って大変なことなんだなあと改めて実感しました。

### 5.2. Netrw.vim の理解度アップ

Netrw.vim
はメンテナ不在でバグも放置されていると言われていてここ数年その理解のままでした。

今回の Pull Request
をきっかけに新しいメンテナの方が精力的にリファクタリングを行っている現状を知ることができました。

(今回のバグはリファクタリングの影響で発生したものでした)

## 6. おわりに

理解が不十分なまま勢いで Pull Request を作成したもののメンテナの
@saccarosium さんの温情によりマージに至りました。

なんやかんやで自分は Netrw.vim
を毎日使っていて愛着があるなと自覚したのでこれ以降 Upstream
の最新版を利用してます。

また次のコントリビュートチャンスを狙っていきたいと思います。

## 7. おまけ

[vim-jp Slack](https://vim-jp.org/docs/chat.html) の \#dev
チャンネルにて成果報告した様子

vim-jp における \#dev チャンネルとはもちろん Vim
本体開発の話題を扱うチャンネルですよ！

<img
src="https://i9wa4.github.io/assets/2025-07-14-my-first-vim-contribution/vim-jp-igyo.png"
style="width:50.0%" alt="Vim Jp Igyo image" />

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-07-14-my-first-vim-contribution.html&text=Vim%E3%81%B8%E3%81%AE%E5%88%9D%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E7%B5%8C%E7%B7%AF%E3%81%A8%E5%AD%A6%E3%81%B3%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Vim%E3%81%B8%E3%81%AE%E5%88%9D%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E7%B5%8C%E7%B7%AF%E3%81%A8%E5%AD%A6%E3%81%B3%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-07-14-my-first-vim-contribution.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-07-14-my-first-vim-contribution.html&title=Vim%E3%81%B8%E3%81%AE%E5%88%9D%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E7%B5%8C%E7%B7%AF%E3%81%A8%E5%AD%A6%E3%81%B3%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
