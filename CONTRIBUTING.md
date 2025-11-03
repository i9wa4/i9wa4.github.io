# CONTRIBUTING

このプロジェクト固有の開発ルールを記載します。

## 1. draw.io

### 1.1. 図の作成ルール

- 図を作成・編集する際は `.drawio` ファイルのみを編集する
- `.drawio.svg` ファイルを直接編集しない
- pre-commit hook により自動生成される `.drawio.svg` をスライド等で利用する

### 1.2. 自動変換ワークフロー

pre-commit hook により以下の変換が自動的に実行される

1. `.drawio` ファイルを検出
2. `drawio` CLI で `.drawio.svg` に変換
3. `inkscape` でテキストをパスに変換（PDF表示時の文字化け防止）
4. 生成された `.drawio.svg` を自動的に git add

### 1.3. 手動で変換する場合

`.drawio` ファイルを更新した場合は、以下のいずれかの方法で手動変換できる

```sh
# 全ての .drawio ファイルを変換（図が少ない場合）
mise exec -- pre-commit run --all-files

# 特定の .drawio ファイルのみ変換（推奨）
mise exec -- pre-commit run convert-drawio-to-svg --files assets/my-diagram.drawio

# スクリプトを直接実行（複数ファイル指定可能）
bash .github/scripts/convert-drawio-to-svg.sh assets/diagram1.drawio assets/diagram2.drawio
```

### 1.4. CI での実行

GitHub Actions では drawio と inkscape の処理をスキップする（ローカルで変換済みのため）
