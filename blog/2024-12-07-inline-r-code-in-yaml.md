# Quarto の YAML ヘッダにコードを埋め込みたい
uma-chan
2024-12-07

<div class= "page-columns page-rows-contents page-layout-article"><div class="social-share"><a href="https://twitter.com/share?url=https://i9wa4.github.io/blog/2024-12-07-inline-r-code-in-yaml.html&text=Quarto の YAML ヘッダにコードを埋め込みたい" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Quarto の YAML ヘッダにコードを埋め込みたい https://i9wa4.github.io/blog/2024-12-07-inline-r-code-in-yaml.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https://i9wa4.github.io/blog/2024-12-07-inline-r-code-in-yaml.html&title=Quarto の YAML ヘッダにコードを埋め込みたい" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div></div>

R Markdown では実現できてるんですが Quarto ではまだダメなんですねぇ。

[Inline R code in YAML · quarto-dev/quarto-cli · Discussion
\#606](https://github.com/quarto-dev/quarto-cli/discussions/606)

変数対応していてそちらは上手く動いてくれました！

<https://github.com/quarto-dev/quarto-cli/discussions/606#discussioncomment-8351008>

ということは GitHub Actions 内で生成できる値を Quarto
で作ったページに埋め込むことができますね。

Quarto 向けの Publish Workflow も対応させたいので PR 作りたいです。
