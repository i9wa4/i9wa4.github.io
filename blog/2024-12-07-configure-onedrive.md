# 事故らない OneDrive 設定変更手順
uma-chan
2024-12-07

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

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-12-07-configure-onedrive.html&text=%E4%BA%8B%E6%95%85%E3%82%89%E3%81%AA%E3%81%84%20OneDrive%20%E8%A8%AD%E5%AE%9A%E5%A4%89%E6%9B%B4%E6%89%8B%E9%A0%86%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=%E4%BA%8B%E6%95%85%E3%82%89%E3%81%AA%E3%81%84%20OneDrive%20%E8%A8%AD%E5%AE%9A%E5%A4%89%E6%9B%B4%E6%89%8B%E9%A0%86%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-12-07-configure-onedrive.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-12-07-configure-onedrive.html&title=%E4%BA%8B%E6%95%85%E3%82%89%E3%81%AA%E3%81%84%20OneDrive%20%E8%A8%AD%E5%AE%9A%E5%A4%89%E6%9B%B4%E6%89%8B%E9%A0%86%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
