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
