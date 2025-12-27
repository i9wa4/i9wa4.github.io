# systemd がユーザー権限でも使える
uma-chan
2024-06-28

<div class= "page-columns page-rows-contents page-layout-article"><div class="social-share"><a href="https://twitter.com/share?url=https://i9wa4.github.io/blog/2024-06-28-systemd-user.html&text=systemd がユーザー権限でも使える" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=systemd がユーザー権限でも使える https://i9wa4.github.io/blog/2024-06-28-systemd-user.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https://i9wa4.github.io/blog/2024-06-28-systemd-user.html&title=systemd がユーザー権限でも使える" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div></div>

systemd がユーザー権限でも設定できると知ったので記事にします。

## 1. 基本的な情報まとめ

- 設定ファイル格納先
  - `~/.config/systemd/user/`
- コマンド
  - `systemd --user`
  - user オプションを付けて通常の systemd と同様に使用する

## 2. timer 設定手順

私の用途では timer 設定ができれば OK です。

下記リポジトリの設定を使って説明していきます。

[i9wa4/minecraft-bedrock-server-setup/bin/init.sh](https://github.com/i9wa4/minecraft-bedrock-server-setup/blob/21631d662eb510f972dc0142faecdf27d804398f/bin/init.sh)

``` sh
# ~/.config/systemd/user/ に設定ファイルを配置する
ln -fs "${DIR_REPO}"/etc/mbs-backup.service \
  "${HOME}"/.config/systemd/user/mbs-backup.service
ln -fs "${DIR_REPO}"/etc/mbs-backup.timer \
  "${HOME}"/.config/systemd/user/mbs-backup.timer

# 設定ファイルを読み込む
systemctl --user daemon-reload

# timer をログイン時に実行する
systemctl --user enable mbs-backup.timer

# timer を実行する
systemctl --user start mbs-backup.timer

# サーバーの起動時にサービスを立ち上げる
sudo loginctl enable-linger i9wa4
```

## 3. 参考リンク

- [systemd/ユーザー -
  ArchWiki](https://wiki.archlinux.jp/index.php/Systemd/ユーザー)
- [サーバー起動時に非rootユーザーでsystemdを使ってサービスを立ち上げる
  \#systemd -
  Qiita](https://qiita.com/k0kubun/items/3c94473506e0e370a227)
