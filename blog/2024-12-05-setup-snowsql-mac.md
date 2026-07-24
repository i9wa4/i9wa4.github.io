# SnowSQL セットアップ (Mac)
uma-chan
2024-12-05

PC を新調するとセットアップがつきものですね。

ではいきます。

## 1. SnowSQL インストール

[SnowSQL のインストール \| Snowflake
Documentation](https://docs.snowflake.com/ja/user-guide/snowsql-install-config#installing-snowsql-on-macos-using-homebrew-cask)

1.  Homebrew でインストールします。

    ``` sh
    brew install --cask snowflake-snowsql
    ```

2.  エイリアス設定を `~/.zshrc` に記載して再読み込み or
    シェルの再起動を行います。

    ``` sh
    alias snowsql=/Applications/SnowSQL.app/Contents/MacOS/snowsql
    ```

## 2. `~/.snowsql/config` 作成

[SnowSQL を介した接続 \| Snowflake
Documentation](https://docs.snowflake.com/ja/user-guide/snowsql-start#using-named-connections)

1.  `snowsql` コマンドを実行します。

    ``` sh
    $ snowsql
    Usage: snowsql [OPTIONS]
    ```

2.  `~/.snowsql/config` が作成されているので編集していきます。

    ``` yml
    [connections.connection_name1]
    accountname = myorganization-myaccount
    username = jsmith
    password = xxxxx
    rolename = myrole
    warehousename = mywh
    ```

## 3. コマンド実行

[SnowSQLの使用 \| Snowflake
Documentation](https://docs.snowflake.com/ja/user-guide/snowsql-use#executing-commands)

1.  以下のコマンドで接続します。

    ``` sh
    # どちらでも OK
    snowsql --connection connection_name1
    snowsql -c connection_name1
    ```

2.  接続後は SQL 文を直接実行できます。

    - 必要に応じて `USE ROLE xxxxxx;` で権限を切り替えることができます。

3.  各種コマンドは `!help` で参照できます。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-12-05-setup-snowsql-mac.html&text=SnowSQL%20%E3%82%BB%E3%83%83%E3%83%88%E3%82%A2%E3%83%83%E3%83%97%20%28Mac%29%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=SnowSQL%20%E3%82%BB%E3%83%83%E3%83%88%E3%82%A2%E3%83%83%E3%83%97%20%28Mac%29%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-12-05-setup-snowsql-mac.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2024-12-05-setup-snowsql-mac.html&title=SnowSQL%20%E3%82%BB%E3%83%83%E3%83%88%E3%82%A2%E3%83%83%E3%83%97%20%28Mac%29%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
