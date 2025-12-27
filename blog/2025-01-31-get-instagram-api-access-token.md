# Instagram API のアクセストークンを取得する
uma-chan
2025-01-31

<div class= "page-columns page-rows-contents page-layout-article"><div class="social-share"><a href="https://twitter.com/share?url=https://i9wa4.github.io/blog/2025-01-31-get-instagram-api-access-token.html&text=Instagram API のアクセストークンを取得する" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Instagram API のアクセストークンを取得する https://i9wa4.github.io/blog/2025-01-31-get-instagram-api-access-token.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https://i9wa4.github.io/blog/2025-01-31-get-instagram-api-access-token.html&title=Instagram API のアクセストークンを取得する" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div></div>

こういった作業ってテックブログ見るしかないですよね。 やっていきます。

## 1. 参考ページ

- [Instagram API
  のアクセストークン取得手順](https://zenn.dev/kimuracoki/articles/9f086639604d57)
- [超簡単！Instagram graph APIのアクセストークンを取得する - to inc
  マーケティングを企業のスタンダードに](https://to-inc.co.jp/socialbook/?p=2189)

## 2. 手順

1.  Facebook アカウント作成
    - 会社メールアドレスで個人アカウントに該当するアカウントを作成してます
2.  meta for Developers アカウント作成
3.  新規アプリ作成
    - ユースケース：その他
    - アプリタイプ：ビジネス
4.  作成したアプリの設定
    - アプリID・app secret を控える
5.  meta for Developers の「ツール」→「グラフ API
    エクスプローラ」を起動する
6.  ページ作成
    1.  「ページアクセストークンの取得」を選択
    2.  「現在のページにのみオプトイン」を選択
    3.  ページを作成する
    4.  (ここでページ名がユニークである必要があるようで、エラーを起こしてページ作成制限を受けてしまいました😢また挑戦します)
