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
# macOS でのインストール
brew install drawio poppler
```

### 2.5. レイアウトの微調整

SVG に変換後にレイアウトのズレが気になる場合、`.drawio` ファイルを直接編集して調整できる

**ズレを確認する方法**:

1. **人間による確認**
   - 生成された `.drawio.svg` をブラウザで開く
   - デプロイ後の PDF を確認する（より正確）
     - スライドの場合: `https://i9wa4.github.io/slides/<slide-name>.pdf`
     - テキストの位置、矢印との重なり、要素間の間隔などをチェック
   - 元の `.drawio` ファイルを draw.io アプリで開いて比較
     - draw.io での見た目と PDF での見た目が異なる場合がある
     - PDF での見た目を優先して調整する

2. **Claude Code による自動確認**
   - `.drawio` または `.drawio.svg` を PNG に変換して視覚的に確認してもらう
   - Claude Code は画像として読み込むことで、レイアウトのズレを検出できる

   ```sh
   # 方法1: .drawio から直接 PNG に変換
   drawio -x -f pdf -o /tmp/diagram.pdf assets/your-diagram.drawio
   pdftocairo -png -singlefile /tmp/diagram.pdf /tmp/diagram
   # 生成された /tmp/diagram.png を Claude Code に読み込んでもらう

   # 方法2: .drawio.svg から PNG に変換
   pdftocairo -png -singlefile assets/your-diagram.drawio.svg /tmp/diagram
   # 生成された /tmp/diagram.png を Claude Code に読み込んでもらう
   ```

   Claude Code に「この図のレイアウトをチェックして」と依頼すると、テキストの位置ズレや要素の配置の問題を指摘してくれる

**手順**:

1. `.drawio` ファイルをテキストエディタで開く（プレーンな XML 形式）
2. 調整したい要素の `mxCell` を探す（`value` 属性でテキストを検索）
3. `mxGeometry` タグの座標を調整
   - `x`: 左からの位置
   - `y`: 上からの位置
   - `width`: 幅
   - `height`: 高さ
4. 変換を実行して確認

**例**: 矢印上のテキストを中央に配置

```xml
<!-- 修正前: Y座標が矢印とズレている -->
<mxCell id="label" value="約25-50倍速" ...>
  <mxGeometry x="700" y="360" width="160" height="40" as="geometry"/>
</mxCell>

<!-- 修正後: Y座標を調整して矢印(Y=400)の中心と揃える -->
<mxCell id="label" value="約25-50倍速" ...>
  <mxGeometry x="700" y="380" width="160" height="40" as="geometry"/>
</mxCell>
```

**Tips**:

- 要素の中心座標 = `y + (height / 2)`
- 複数要素を揃える場合は中心座標を計算して合わせる
- 変更後は必ず `mise exec -- pre-commit run convert-drawio-to-svg --files <file>` で確認

### 2.6. CI での実行

GitHub Actions では drawio と pdftocairo の処理はスキップされる
