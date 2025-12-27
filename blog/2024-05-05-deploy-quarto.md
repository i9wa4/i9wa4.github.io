# Quarto で作ったスライドを GitHub Pages にデプロイする
uma-chan
2024-05-05

<div class= "page-columns page-rows-contents page-layout-article"><div class="social-share"><a href="https://twitter.com/share?url=https://i9wa4.github.io/blog/2024-05-05-deploy-quarto.html&text=Quarto で作ったスライドを GitHub Pages にデプロイする" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Quarto で作ったスライドを GitHub Pages にデプロイする https://i9wa4.github.io/blog/2024-05-05-deploy-quarto.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https://i9wa4.github.io/blog/2024-05-05-deploy-quarto.html&title=Quarto で作ったスライドを GitHub Pages にデプロイする" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div></div>

> [!WARNING]
>
> ### Deprecated
>
> この記事の内容は古くなっています。最新の情報は以下の記事を参照してください。
>
> [uv + Quarto でブログやスライドを作成して GitHub Pages で公開する
> (HTML エクスポートにも対応)](https://i9wa4.github.io/2025-12-15-uv-quarto-intro.md)

## 1. 前提

スライドをできるだけ Git で管理したいので Markdown
をスライドに変換する方向性で色々なツールを比較検討していて、 Quarto
(<https://quarto.org/>) に決めました。

.qmd
ファイルという見慣れないファイルを利用しますが、利点としては以下ですね。

- 環境構築が pip で完了する
- VS Code で開くと Jupyter Notebook っぽくセルを実行できる

## 2. やったこと

下記リポジトリを整備しました。

<https://github.com/i9wa4/slides>

README.md にも書いてますが

[Quartoでスライドを作ってGitHub Pagesで公開する \#GitHubActions -
Qiita](https://qiita.com/cm-ayf/items/512728ebea65467ba874)

を参考にしてます。

## 3. 感想

GitHub Actions
はまだよく分かってないままなのですが、一旦動くようになってよかったです。
