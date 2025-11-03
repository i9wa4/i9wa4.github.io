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

### 2.6. フォントサイズ変更時の注意点

フォントサイズを変更した場合、レイアウトが崩れる可能性がある

**よくある問題**:

1. **ラベルが要素からはみ出す**
   - 例: 吹き出しの上にラベルが飛び出す
   - 解決策: ラベルの Y 座標と高さを調整して、親要素の内側に収める
   ```xml
   <!-- 修正前: Y=110 で吹き出し (Y=140) の外に出ている -->
   <mxCell id="label" value="タイトル" ...>
     <mxGeometry x="400" y="110" width="200" height="30" as="geometry"/>
   </mxCell>

   <!-- 修正後: Y=145 で吹き出しの内側に配置 -->
   <mxCell id="label" value="タイトル" ...>
     <mxGeometry x="350" y="145" width="280" height="35" as="geometry"/>
   </mxCell>
   ```

2. **テキストが詰まって改行されない**
   - 例: 複数の短いテキストが横並びで、幅が足りず詰まる
   - 解決策: `<br>` タグで明示的に改行するか、レイアウトを再構成
   ```xml
   <!-- 修正前: 5つのテキストが横並びで詰まっている -->
   <mxCell id="feature1" value="✓ 機能A" ...>
     <mxGeometry x="450" y="680" width="200" height="30" as="geometry"/>
   </mxCell>
   <mxCell id="feature2" value="✓ 機能B" ...>
     <mxGeometry x="680" y="680" width="200" height="30" as="geometry"/>
   </mxCell>
   ...

   <!-- 修正後: 改行タグで縦並びにグループ化 -->
   <mxCell id="feature1" value="✓ 機能A&lt;br&gt;✓ 機能B" ...>
     <mxGeometry x="450" y="680" width="280" height="60" as="geometry"/>
   </mxCell>
   ```

3. **矢印が他の要素の上に重なる**
   - 解決策: 矢印を最背面に移動
   - draw.io では XML の順序が描画順なので、矢印を先頭（Title の直後）に配置
   ```xml
   <!-- Title -->
   <mxCell id="title" value="..." .../>

   <!-- Arrow (最背面) -->
   <mxCell id="arrow" style="shape=flexArrow;..." .../>

   <!-- Other elements (前面に表示される) -->
   <mxCell id="box1" .../>
   ```

**一括変更後の確認フロー**:

1. 全図を PNG に変換して視覚的に確認
   ```sh
   mkdir -p /tmp/drawio-review
   for drawio in assets/**/*.drawio; do
     base=$(basename "$drawio" .drawio)
     drawio -x -f pdf -o "/tmp/drawio-review/${base}.pdf" "$drawio"
     pdftocairo -png -singlefile "/tmp/drawio-review/${base}.pdf" "/tmp/drawio-review/${base}"
   done
   ```

2. Claude Code に全図のレイアウトチェックを依頼

3. 問題のある図を個別に修正

4. SVG を再生成
   ```sh
   mise exec -- pre-commit run convert-drawio-to-svg --all-files
   ```

### 2.7. draw.io 図作成のベストプラクティス

**基本原則**:

1. **背景色を設定しない**
   - `background="#ffffff"` は削除すること
   - 透明背景にすることで、様々なテーマに対応できる

2. **フォントサイズは1.5倍推奨**
   - PDF表示で読みやすくするため、標準フォントサイズの1.5倍を使用
   - 一括変更する場合は、レイアウトの微調整が必要

3. **矢印は必ず最背面に配置**
   - draw.io では XML の順序が描画順
   - 矢印を Title の直後に配置することで、他の要素の下に表示される
   ```xml
   <!-- Title -->
   <mxCell id="title" value="..." .../>

   <!-- Arrows (最背面) -->
   <mxCell id="arrow1" style="edgeStyle=..." .../>
   <mxCell id="arrow2" style="edgeStyle=..." .../>

   <!-- Other elements (前面に表示される) -->
   <mxCell id="box1" .../>
   ```

4. **不要な要素を削除**
   - 文脈に不要な装飾アイコンは削除
   - 例: ECR (Container Registry) があれば、別途 Docker アイコンは不要

5. **絵文字を活用**
   - draw.io の shape が正しく表示されない場合は絵文字で代用
   - 例: Docker アイコン → 🐳

6. **AWS アイコンは最新版**
   - `shape=mxgraph.aws4.resourceIcon` を使用
   - draw.io で提供される AWS Architecture Icons は最新版

**チェックリスト**:

- [ ] 背景色が設定されていないか
- [ ] フォントサイズは適切か（大きめ推奨）
- [ ] 矢印が最背面に配置されているか
- [ ] 不要な要素が残っていないか
- [ ] PNG に変換して視覚的に確認したか

### 2.8. CI での実行

GitHub Actions では drawio と pdftocairo の処理はスキップされる
