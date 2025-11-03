# CONTRIBUTING

このプロジェクト固有の開発ルールを記載します。

## 1. pre-commit

pre-commit hook を利用してコード品質を保つため、以下のコマンドでセットアップしてください。

```sh
mise exec -- pre-commit install
```

## 2. draw.io

### 2.1. 図の作成ルール

- 図を作成・編集する際は `.drawio` ファイルのみを編集する
- `.drawio.svg` ファイルを直接編集しない
- pre-commit hook により自動生成される `.drawio.svg` をスライド等で利用する

### 2.2. 自動変換ワークフロー

pre-commit hook により以下の変換が自動的に実行される

1. `.drawio` ファイルを検出
2. `drawio` CLI で一時的な PDF を生成
3. `pdftocairo` (poppler-utils) で PDF → SVG に変換（テキストを自動的にパスに変換）
4. 生成された `.drawio.svg` を自動的に git add

この方式により、日本語を含むすべてのテキストがベクターパスに変換され、フォント依存なしで PDF 表示時も正しく表示される

### 2.3. 手動で変換する場合

`.drawio` ファイルを更新した場合は、以下のいずれかの方法で手動変換できる

```sh
# 全ての .drawio ファイルを変換（図が少ない場合）
mise exec -- pre-commit run --all-files

# 特定の .drawio ファイルのみ変換（推奨）
mise exec -- pre-commit run convert-drawio-to-svg --files assets/my-diagram.drawio

# スクリプトを直接実行（複数ファイル指定可能）
bash .github/scripts/convert-drawio-to-svg.sh assets/diagram1.drawio assets/diagram2.drawio
```

### 2.4. 必要なツール

ローカルで変換を実行するには以下のツールが必要

- `drawio` CLI
- `poppler-utils` (pdftocairo コマンドを含む)

```sh
# macOS での poppler-utils インストール
brew install poppler
```

### 2.5. CI での実行

GitHub Actions では drawio と pdftocairo の処理をスキップする（ローカルで変換済みのため）
