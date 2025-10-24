# Databricks Connect 実践編 - ローカルから Databricks コンピュートを利用
uma-chan
2025-07-28

本記事は3部構成の3本目です。

1.  [Claude Code 対応 Dev Container 環境構築編 - VS Code
    でもそれ以外でも](2025-07-28-article1-devcontainer.qmd)
2.  [Python 開発環境最適化編 - uv + pre-commit + GitHub
    Actions](2025-07-28-article2-python-env.qmd)
3.  [Databricks Connect 実践編 - ローカルから Databricks
    コンピュートを利用](2025-07-28-article3-databricks-connect.qmd)

## 1. はじめに

前回までの環境に Databricks Connect を追加して、ローカル開発環境から
Databricks の Spark セッションを利用できるようにします。

Databricks
上でもローカルでも同じコードが動作する汎用的なライブラリも紹介します。

## 2. 対象読者

- Databricks のコンピュートをローカルから利用したい方
- Databricks 上での開発に Claude Code を利用したい方
- Databricks 以外の DWH サービスを使っているが参考にしたい方

## 3. Databricks Connect とは

Databricks Connect は、ローカル開発環境から Databricks
クラスタに接続できるライブラリです。

これにより以下のメリットが得られます。

- VS Code や Claude Code などのローカル開発環境が利用できる
- ローカルでの開発と Databricks 上での実行で同じコードが使える

## 4. 環境設定

### 4.1. pyproject.toml への追加

前回の pyproject.toml に以下の依存関係を追加します。

<div class="code-with-filename">

**pyproject.toml**

``` toml
[project]
dependencies = [
    "databricks-connect~=16.4.0",
    "ipykernel",
    "jupyterlab",
    "matplotlib",
    "numpy",
    "pandas",
    "python-dotenv",
    "requests",
    "seaborn",
]

[tool.flake8]
extend-ignore = [
    "E203",  # Whitespace before ':'
    "E701",  # Multiple statements on one line (colon)
    "F821"   # undefined name (Databricks-specific module)
]
```

</div>

### 4.2. Dev Container設定の更新

devcontainer.json に以下の設定を追加します。

<div class="code-with-filename">

**.devcontainer/devcontainer.json**

``` json
{
    "runArgs": [
        "--cap-add=NET_ADMIN",
        "--cap-add=NET_RAW",
        "--network=host"
    ],
    "mounts": [
        "source=${localEnv:HOME}/.databrickscfg,target=/home/node/.databrickscfg,type=bind,consistency=cached",
    ]
}
```

</div>

### 4.3. 環境変数設定

`.env.example` ファイルを作成します。

<div class="code-with-filename">

**.env.example**

``` sh
# Databricks設定

# .databrickscfgのプロファイル名（推奨）
DATABRICKS_CONFIG_PROFILE=DEFAULT

# クラスター使用の場合（どちらか一方を設定）
# DATABRICKS_CLUSTER_ID=

# Serverless Compute使用の場合
DATABRICKS_SERVERLESS_COMPUTE_ID=auto

# バージョンチェック無効化
DATABRICKS_CONNECT_DISABLE_VERSION_CHECK=true
```

</div>

## 5. Spark セッション管理ライブラリ

Dev Container (ローカル) と Databricks の両方で同じように Spark
セッションを作成するためのライブラリを用意しました。

### 5.1. 使用方法

``` python
from databricks_spark import create_spark_session

# 新しいSparkセッションを作成
spark = create_spark_session()
df = spark.sql("SHOW CATALOGS")
df.show()
```

### 5.2. ライブラリ実装

> [!NOTE]
>
> ### 5.2.1. `databricks_spark.py`
>
> <div class="code-with-filename">
>
> **databricks_spark.py**
>
> ``` python
> """
> Databricks Spark セッション管理
> Databricksとローカル両対応の1ファイル完結型ライブラリ
>
> 使用方法:
>     from databricks_spark import create_spark_session
>
>     # 新しいSparkセッションを作成
>     spark = create_spark_session()
>     df = spark.sql("SHOW CATALOGS")
>     df.show()
> """
>
> import logging
> import os
> import sys
>
> # ロガー設定
> _logger = logging.getLogger(__name__)
> if not _logger.handlers:
>     _logger.setLevel(logging.INFO)
>     formatter = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
>     handler = logging.StreamHandler(sys.stdout)
>     handler.setFormatter(formatter)
>     _logger.addHandler(handler)
>
>
> def is_databricks_environment() -> bool:
>     """Databricks環境で実行されているかを判定"""
>     return os.environ.get("DATABRICKS_RUNTIME_VERSION") is not None
>
>
> def get_environment_type() -> str:
>     """実行環境のタイプを取得"""
>     if is_databricks_environment():
>         return "databricks"
>     else:
>         return "local"
>
>
> def create_databricks_native_session():
>     """Databricks上でのネイティブSparkセッション作成"""
>     try:
>         from pyspark.sql import SparkSession
>
>         spark = SparkSession.getActiveSession()
>         if spark is None:
>             spark = SparkSession.builder.appName("DatabricksNotebook").getOrCreate()
>
>         _logger.info("✅ Databricks native Sparkセッション取得完了")
>         _logger.info(f"📊 Spark version: {spark.version}")
>         return spark
>
>     except ImportError:
>         raise ImportError("Databricks環境でPySparkが利用できません")
>
>
> def create_local_connect_session():
>     """ローカルでのDatabricksConnect Sparkセッション作成"""
>     try:
>         from databricks.connect import DatabricksSession
>
>         # 環境変数のデフォルト値を設定
>         os.environ.setdefault("DATABRICKS_CONFIG_PROFILE", "DEFAULT")
>         os.environ.setdefault("DATABRICKS_SERVERLESS_COMPUTE_ID", "auto")
>         os.environ.setdefault("DATABRICKS_CONNECT_DISABLE_VERSION_CHECK", "true")
>
>         # .env読み込み（オプション）
>         try:
>             from dotenv import find_dotenv, load_dotenv
>
>             env_file = find_dotenv()
>             if env_file:
>                 load_dotenv(env_file)
>                 _logger.info(f"📁 .env読み込み: {env_file}")
>         except ImportError:
>             _logger.info("📁 dotenvモジュールなし - 環境変数のみ使用")
>
>         # プロファイル指定チェック
>         profile_name = os.environ.get("DATABRICKS_CONFIG_PROFILE")
>
>         if profile_name:
>             _logger.info(f"🔧 .databrickscfgプロファイル使用: {profile_name}")
>
>             if os.environ.get("DATABRICKS_CLUSTER_ID"):
>                 cluster_id = os.environ.get("DATABRICKS_CLUSTER_ID")
>                 spark = (
>                     DatabricksSession.builder.profile(profile_name)
>                     .clusterId(cluster_id)
>                     .getOrCreate()
>                 )
>                 _logger.info(f"🆔 クラスター使用: {cluster_id}")
>             else:
>                 spark = (
>                     DatabricksSession.builder.profile(profile_name)
>                     .serverless(True)
>                     .getOrCreate()
>                 )
>                 _logger.info("🚀 Serverless Compute使用")
>         else:
>             _logger.info("🔧 環境変数から直接接続")
>
>             required_vars = ["DATABRICKS_HOST", "DATABRICKS_TOKEN"]
>             missing_vars = [var for var in required_vars if not os.environ.get(var)]
>
>             if missing_vars:
>                 raise ValueError(f"環境変数が未設定: {missing_vars}")
>
>             if os.environ.get("DATABRICKS_CLUSTER_ID"):
>                 cluster_id = os.environ.get("DATABRICKS_CLUSTER_ID")
>                 spark = DatabricksSession.builder.clusterId(cluster_id).getOrCreate()
>                 _logger.info(f"🆔 クラスター使用: {cluster_id}")
>             else:
>                 spark = DatabricksSession.builder.serverless(True).getOrCreate()
>                 _logger.info("🚀 Serverless Compute使用")
>
>         # DataFrame表示最適化（Serverless環境では一部設定が制限される）
>         try:
>             spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
>         except Exception:
>             # Serverless Computeでは設定できない場合があるのでスキップ
>             pass
>
>         _logger.info("✅ Databricks Connect Sparkセッション作成完了")
>         _logger.info(f"📊 Spark version: {spark.version}")
>         _logger.info(f"🌐 接続先: {spark.client.host}")
>         return spark
>
>     except ImportError as e:
>         raise ImportError(f"databricks-connectが利用できません: {e}")
>
>
> def create_spark_session():
>     """実行環境に応じて適切なSparkセッションを作成"""
>     env_type = get_environment_type()
>     _logger.info(f"🔍 実行環境検出: {env_type}")
>
>     try:
>         if env_type == "databricks":
>             return create_databricks_native_session()
>         else:  # local環境（VS Code、Cursor、Dev Container CLI等）
>             return create_local_connect_session()
>
>     except Exception as e:
>         error_msg = str(e)
>         _logger.error(f"❌ Sparkセッション作成失敗: {error_msg}")
>
>         # バージョン不整合の検出と対応提案
>         if "Unsupported combination" in error_msg and "Databricks Runtime" in error_msg:
>             _logger.error("🔧 バージョン不整合が検出されました")
>             _logger.error("💡 以下のいずれかの対応を行ってください:")
>             _logger.error(
>                 "   1. DatabricksConnectをクラスターのランタイムに合わせてダウングレード:"
>             )
>             _logger.error(
>                 "      uv add 'databricks-connect~=[クラスターのランタイムバージョン]'"
>             )
>             _logger.error("   2. Databricksクラスターのランタイムをアップグレード")
>
>         _logger.error(f"💡 環境タイプ: {env_type}")
>         raise
>
>
> # 明示的にcreate_spark_session()を呼び出してセッションを作成してください
> # 例: spark = create_spark_session()
> ```
>
> </div>

## 6. Databricks側の設定

### 6.1. 接続先クラスタ設定

Spark config で以下を設定します。

    spark.databricks.service.server.enabled true

### 6.2. Databricks 接続設定

Databricks へ接続する場合は `~/.databrickscfg`
に以下の内容を記述します。

``` ini
[DEFAULT]
host = https://your-databricks-workspace.cloud.databricks.com
token = your-access-token
```

- `host`: Databricks ワークスペースの URL
- `token`: Databricks アクセストークン

## 7. 利用手順

### 7.1. `.env` 作成

1.  `.env` ファイルを作成します

    ``` sh
    cp .env.example .env
    ```

2.  必要であれば `.env` ファイルの内容を変更してください

### 7.2. 開発ワークフロー

1.  Dev Container を起動
2.  Python カーネルを選択
3.  Spark セッションを作成して開発開始

``` python
from databricks_spark import create_spark_session

# Sparkセッション作成
spark = create_spark_session()

# データの取得
df = spark.sql("SELECT * FROM your_table LIMIT 10")
df.show()

# データ分析
df.groupBy("category").count().show()
```

## 8. ノートブックでの Python モジュールインストール方法

Databricks での実行時のみ Python パッケージをインストールする HACK
な方法です。

uv を使っていない場合は `%pip install <package>` で大丈夫です。

``` py
import os
if os.environ.get("DATABRICKS_RUNTIME_VERSION"):
    %pip install uv
    %pip install -r <(uv pip compile pyproject.toml --color never)
```

## 9. トラブルシューティング

### 9.1. バージョン不整合エラー

Databricks Connect
のバージョンとクラスタのランタイムバージョンが合わない場合があります

``` sh
# クラスタのランタイムに合わせてダウングレード
uv add 'databricks-connect~=14.3.0'  # この場合は DBR 14.3 に対応
```

### 9.2. 接続エラー

設定ファイルが存在せずマウントされていない場合が考えられるので、devcontainer.json
の `mounts` 設定を確認してください。

## 10. おわりに

これでローカル開発環境から Databricks の Spark
クラスタを利用できるようになりました。

Claude Code
にノートブック実行とデバッグを任せることでデータサイエンスや機械学習の作業効率が爆上がりですね！

Claude Code
にこの手の作業を任せるときは時間がかかるので並行して他の作業に取り組むのがオススメです。

## 11. (おまけ) Claude Code に読ませると便利なルール

<div class="code-with-filename">

**CONTRIBUTING.md**

``` md
# CONTRIBUTING

## 重要なルール

### pre-commit 設定について

- **NEVER**: pre-commit を無効化してはならない
- **NEVER**: `pre-commit skip` や `git commit --no-verify` を使用してはならない
- **IMPORTANT**: pre-commit のチェックに失敗した場合は、必ずコードを修正してからコミットする

## Jupyter Notebook 実行方法

### デフォルトの実行方法

Notebook全体を実行する指示を受けた際は、以下のコマンドを使用する

`uv run jupyter nbconvert --to notebook --execute <notebook_path> --inplace --ExecutePreprocessor.timeout=300`

#### 使用例

`uv run jupyter nbconvert --to notebook --execute /workspace/notebooks/databricks-connect-sample.ipynb --inplace --ExecutePreprocessor.timeout=300`

#### オプション説明

- `--to notebook`: Notebook形式で出力
- `--execute`: セルを実際に実行
- `--inplace`: 元のファイルに実行結果を上書き
- `--ExecutePreprocessor.timeout=300`: タイムアウトを300秒に設定

### 実行ログの確認

実行時のログを確認したい場合は以下のように実行する

`uv run jupyter nbconvert --to notebook --execute <notebook_path> --inplace --ExecutePreprocessor.timeout=300 2>&1 | tee /tmp/notebook_execution.log`

### 注意事項

- 実行前に必要な環境変数（`.env`ファイル等）が適切に設定されていることを確認する
- 長時間実行されるセルがある場合は`--ExecutePreprocessor.timeout`の値を調整する
- VS Codeで開いている場合は実行後にファイルの更新を確認する
```

</div>
