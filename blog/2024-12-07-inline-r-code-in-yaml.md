# Quarto の YAML ヘッダにコードを埋め込みたい
uma-chan
2024-12-07

R Markdown では実現できてるんですが Quarto ではまだダメなんですねぇ。

[Inline R code in YAML · quarto-dev/quarto-cli · Discussion
\#606](https://github.com/quarto-dev/quarto-cli/discussions/606)

変数対応していてそちらは上手く動いてくれました！

<https://github.com/quarto-dev/quarto-cli/discussions/606#discussioncomment-8351008>

ということは GitHub Actions 内で生成できる値を Quarto
で作ったページに埋め込むことができますね。

Quarto 向けの Publish Workflow も対応させたいので PR 作りたいです。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-12-07-inline-r-code-in-yaml.html&text=Quarto%20%E3%81%AE%20YAML%20%E3%83%98%E3%83%83%E3%83%80%E3%81%AB%E3%82%B3%E3%83%BC%E3%83%89%E3%82%92%E5%9F%8B%E3%82%81%E8%BE%BC%E3%81%BF%E3%81%9F%E3%81%84%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Quarto%20%E3%81%AE%20YAML%20%E3%83%98%E3%83%83%E3%83%80%E3%81%AB%E3%82%B3%E3%83%BC%E3%83%89%E3%82%92%E5%9F%8B%E3%82%81%E8%BE%BC%E3%81%BF%E3%81%9F%E3%81%84%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-12-07-inline-r-code-in-yaml.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-12-07-inline-r-code-in-yaml.html&title=Quarto%20%E3%81%AE%20YAML%20%E3%83%98%E3%83%83%E3%83%80%E3%81%AB%E3%82%B3%E3%83%BC%E3%83%89%E3%82%92%E5%9F%8B%E3%82%81%E8%BE%BC%E3%81%BF%E3%81%9F%E3%81%84%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
