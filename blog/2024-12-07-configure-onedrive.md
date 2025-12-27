# 事故らない OneDrive 設定変更手順
uma-chan
2024-12-07

<div class= "page-columns page-rows-contents page-layout-article"><div class="social-share"><a href="https://twitter.com/share?url=https://i9wa4.github.io/blog/2024-12-07-configure-onedrive.html&text=事故らない OneDrive 設定変更手順" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=事故らない OneDrive 設定変更手順 https://i9wa4.github.io/blog/2024-12-07-configure-onedrive.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https://i9wa4.github.io/blog/2024-12-07-configure-onedrive.html&title=事故らない OneDrive 設定変更手順" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div></div>

## 1. はじめに

OneDrive
でありがちな勝手にデスクトップのファイルが同期されている状況の回避策をポストしたところ反響がまあまあありました。

<https://x.com/i9wa4_/status/1864940454409834645>

意外と OneDrive
って難しいのでこういった手順は需要があると分かり記事に残しておこうと思います。

業務用PCが Windows ではなく Mac
になってしまい詳細手順をスクショ付きで書けないので日和って個人ブログに書きます。

## 2. 想定するユースケース

同期対象を「デスクトップ」や「ドキュメント」そのものではなく、明示的に作成したフォルダだけとしたい場合です。

## 3. 事故らない OneDrive セットアップ手順

1.  全フォルダを OneDrive の同期対象から外す
2.  同期対象から外した「デスクトップ」や「ドキュメント」はこの時点では
    OneDrive
    フォルダ配下に置かれているので右クリックして「プロパティ→場所→標準に戻す」で元の場所
    (`%USERPROFILE%` 直下) に戻す
3.  明示的にバックアップ対象としたいフォルダを OneDrive
    の同期対象に設定する
4.  ブラウザで OneDrive にアクセスして不要なデータを削除する
5.  OneDrive の同期を再開する

## 4. おわりに

OneDrive
の操作手順を詳細に書けず心苦しいのですが、きっと何とかなるはず。信じてます。
