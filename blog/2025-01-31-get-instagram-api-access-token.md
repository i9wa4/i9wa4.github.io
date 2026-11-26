# Instagram API のアクセストークンを取得する
uma-chan
2025-01-31

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

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-01-31-get-instagram-api-access-token.html&text=Instagram%20API%20%E3%81%AE%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%82%92%E5%8F%96%E5%BE%97%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Instagram%20API%20%E3%81%AE%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%82%92%E5%8F%96%E5%BE%97%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-01-31-get-instagram-api-access-token.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-01-31-get-instagram-api-access-token.html&title=Instagram%20API%20%E3%81%AE%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%82%92%E5%8F%96%E5%BE%97%E3%81%99%E3%82%8B%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
