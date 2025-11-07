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
- `.drawio.png` ファイルを直接編集しない
- pre-commit hook により自動生成される `.drawio.png` をスライド等で利用する
- YOU MUST: Quartoスライドで使用する図は、mxGraphModelタグに `defaultFontFamily="Noto Sans JP"` を指定する
  - これによりスライド本体のフォント (Noto Sans JP) と図のフォントが統一される
  - 例: `<mxGraphModel defaultFontFamily="Noto Sans JP" dx="1434" dy="844" ...>`

### 2.2. 自動変換ワークフロー

pre-commit hook により以下の変換が自動的に実行される

1. `.drawio` ファイルを検出
2. `drawio` CLI で高解像度 PNG を生成 (2倍スケール)
3. 生成された `.drawio.png` を自動的に git add

### 2.3. 手動で変換する場合

`.drawio` ファイルを更新した場合は、以下のいずれかの方法で手動変換できる

```sh
# 全ての .drawio ファイルを変換（図が少ない場合）
mise exec -- pre-commit run --all-files

# 特定の .drawio ファイルのみ変換（推奨）
mise exec -- pre-commit run convert-drawio-to-png --files assets/my-diagram.drawio

# スクリプトを直接実行（複数ファイル指定可能）
bash .github/scripts/convert-drawio-to-png.sh assets/diagram1.drawio assets/diagram2.drawio
```

### 2.4. 必要なツール

ローカルで変換を実行するには以下のツールが必要

- `drawio` CLI

```sh
# macOS でのインストール
brew install drawio
```

### 2.5. レイアウトの微調整

PNG 生成後にレイアウトのズレが気になる場合、`.drawio` ファイルを直接編集して調整できる

**ズレを確認する方法**:

1. **人間による確認**
   - 生成された `.drawio.png` をブラウザで開く
   - デプロイ後の PDF を確認する（より正確）
     - スライドの場合: `https://i9wa4.github.io/slides/<slide-name>.pdf`
     - テキストの位置、矢印との重なり、要素間の間隔などをチェック
   - 元の `.drawio` ファイルを draw.io アプリで開いて比較
     - draw.io での見た目と PDF での見た目が異なる場合がある
     - PDF での見た目を優先して調整する

2. **Claude Code による自動確認**
   - 生成された `.drawio.png` を直接読み込んで視覚的に確認してもらう
   - Claude Code は画像として読み込むことで、レイアウトのズレを検出できる

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
- 変更後は必ず `mise exec -- pre-commit run convert-drawio-to-png --files <file>` で確認

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

4. PNG を再生成
   ```sh
   mise exec -- pre-commit run convert-drawio-to-png --all-files
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

6. **ラベルと見出しのテキスト配置**
   - YOU MUST: ラベルや見出しは適切に改行・1行化して読みやすくする
   - YOU MUST: 不自然な2行表記は避け、意味のある単位で改行する
   - YOU MUST: 改行が必要な場合は `&lt;br&gt;` タグを使用する
   - IMPORTANT: 改行後は必ず PNG で視覚確認し、レイアウトが崩れていないか確認する

   良い例:
   ```xml
   <!-- サービス名だけなら1行 -->
   <mxCell id="label" value="Amazon ECR" .../>

   <!-- 補足情報がある場合は改行 -->
   <mxCell id="label" value="GitHub Actions&lt;br&gt;ビルド: 5分" .../>
   <mxCell id="label" value="開発者&lt;br&gt;インターン生" .../>
   ```

   悪い例:
   ```xml
   <!-- 不要な改行で2行になっている -->
   <mxCell id="label" value="Amazon ECR&lt;br&gt;Container Registry" .../>
   <!-- ECR = Elastic Container Registry なので Registry が二重 -->

   <!-- 無理に1行にして読みづらい -->
   <mxCell id="label" value="GitHub Actionsビルド: 5分" .../>
   ```

   判断基準:
   - サービス名のみ: 1行
   - サービス名 + 補足情報: 改行して2行
   - 役割 + 詳細: 改行して2行
   - 冗長な表記 (例: ECR Container Registry): 短縮して1行

7. **矢印配置の基本原則**
   - YOU MUST: 矢印は要素の中心座標 (アイコンやラベルの中心) に接続する
   - YOU MUST: 矢印がラベルのテキストと被らないように配置する
   - YOU MUST: 矢印の起点・終点はラベルの下辺から十分離す (最低20px以上)
   - YOU MUST: 修正後は必ず PNG で視覚確認し、被りがないか確認する
   - IMPORTANT: テキスト要素への接続は `exitX/exitY` が効かないため、明示的な座標 (`sourcePoint`/`targetPoint`) を使用する

   良い例:
   ```xml
   <!-- アイコン中心: (119, 419) ラベル下辺: y=500 -->
   <!-- 起点を y=540 に設定してラベルから40px離す -->
   <mxCell id="arrow" style="edgeStyle=orthogonalEdgeStyle;..." edge="1" parent="1">
     <mxGeometry relative="1" as="geometry">
       <mxPoint x="1279" y="540" as="sourcePoint"/>
       <mxPoint x="119" y="540" as="targetPoint"/>
       <Array as="points">
         <mxPoint x="1279" y="650"/>
         <mxPoint x="119" y="650"/>
       </Array>
     </mxGeometry>
   </mxCell>
   ```

   悪い例:
   ```xml
   <!-- 起点が y=500 でラベル下辺 (y=500) と一致 → テキストに被る -->
   <mxCell id="arrow" style="..." edge="1" parent="1">
     <mxGeometry relative="1" as="geometry">
       <mxPoint x="1279" y="500" as="sourcePoint"/>
       <mxPoint x="119" y="500" as="targetPoint"/>
     </mxGeometry>
   </mxCell>
   ```

   座標計算:
   - アイコン中心 X: `icon.x + (icon.width / 2)`
   - ラベル下辺 Y: `label.y + label.height`
   - 矢印起点 Y: `label.y + label.height + 余白 (20px以上)`

8. **矢印と他の要素の重なりを絶対に避ける**

   YOU MUST: 矢印は他の要素 (テキストラベル、ボックス、アイコン等) と絶対に被らないように配置する

   NEVER: 矢印が他の要素を貫通したり重なったりしてはいけない

   IMPORTANT: 修正後は必ず PNG で視覚確認し、どこにも被りがないことを確認する

   確認ポイント

   - 矢印がテキストラベルを貫通していないか
   - 矢印が他のボックスやアイコンを横切っていないか
   - 矢印が他のボックスの内部を通過していないか
   - 複数の矢印が交差して見づらくなっていないか

   対処方法

   1. テキストの位置を移動
      - 矢印の経路上にあるテキストを安全な場所に移動
      - 例: ボックス内のテキストがボックス外からの矢印と被る場合、テキストをボックス外に移動

   2. 矢印の経路を調整
      - `<Array as="points">` で中継点を追加し、他の要素を迂回させる
      - orthogonalEdgeStyle を使って直角に曲げ、他の要素を避ける

   3. 要素の配置を見直す
      - 矢印が複雑に絡み合う場合は、要素自体の配置を変更する

   4. PNG で視覚確認 (必須)
      - draw.io 上では気づかない重なりが PNG で見つかることがある
      - 特に複数の矢印がある場合は必ず確認

   悪い例

   ```
   Snowflake → Notebook の矢印が Snowflake ボックス内のテキストと被っている
   Job → S3 の矢印が Snowflake ボックスを貫通している
   ```

   良い例

   ```
   テキストをボックス外に移動して矢印との被りを完全に解消
   矢印の経路を調整してボックスとの重なりをゼロにした
   ```

9. **外部ロゴ・画像を使用する場合の注意点**

   draw.io で外部のロゴや画像 (例: Snowflake, Docker など) を取り込む場合、背景色との組み合わせに注意する

   確認ポイント

   1. ロゴの色と背景色のコントラストが適切か
      - 青いロゴなら白背景が見やすい
      - 白いロゴなら濃い背景が必要

   2. テキストの視認性
      - 背景色に応じて文字色を調整 (白背景なら黒文字、濃い背景なら白文字)

   3. PNG で実際の見た目を確認
      - draw.io のプレビューと PDF/PNG での見た目が異なる場合がある
      - 必ず変換後の PNG で最終確認する

   良い例

   - Snowflake ロゴ (青) + 白背景 + 黒枠線
   - ロゴの青色が映える
   - テキストも濃い青で読みやすい

   悪い例

   - Snowflake ロゴ (青) + 青背景 + 白文字
   - ロゴが背景に埋もれて見づらい
   - コントラストが低い

10. **AWS アイコンとサービス名**
   - YOU MUST: サービス名は AWS が示す正式名称・正しい略称を使用する
   - YOU MUST: アイコンは draw.io 内で利用できる最新版 (`mxgraph.aws4.*`) を使用する
   - NEVER: 古いアイコン (`mxgraph.aws3.*`) や非公式アイコンは使用しない
   - IMPORTANT: サービス名とアイコンが一致していることを確認する

   正しいサービス名の例:
   - Amazon ECS (not "AWS ECS" or "ECS")
   - Amazon ECR (not "AWS ECR" or "ECR")
   - Amazon S3 (not "AWS S3" or "S3")
   - AWS Lambda (Lambda は AWS 始まり)
   - Amazon CloudWatch (not "AWS CloudWatch" or "CloudWatch")
   - Amazon RDS (not "AWS RDS" or "RDS")

   正しいアイコン指定:
   ```xml
   <!-- Amazon ECS -->
   <mxCell id="ecs" value="" style="sketch=0;points=[[0,0,0],...];shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecs;" .../>

   <!-- Amazon ECR -->
   <mxCell id="ecr" value="" style="sketch=0;points=[[0,0,0],...];shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecr;" .../>

   <!-- Amazon CloudWatch -->
   <mxCell id="cloudwatch" value="" style="sketch=0;points=[[0,0,0],...];shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;" .../>
   ```

   確認方法:
   - draw.io で AWS Architecture Icons ライブラリを開く
   - サービス名で検索して正しい名称を確認
   - アイコンを挿入して XML の `resIcon` 属性を確認
   - `mxgraph.aws4.*` であることを確認 (aws3 は古い)

**チェックリスト**

- [ ] 背景色が設定されていないか (page="0" であること)
- [ ] フォントサイズは適切か (大きめ推奨)
- [ ] 矢印が最背面に配置されているか
- [ ] 矢印がラベルと被っていないか (PNG で確認)
- [ ] 矢印の起点・終点がラベルから十分離れているか (最低20px以上)
- [ ] 矢印が他のボックスやアイコンを貫通していないか (PNG で確認)
- [ ] 矢印が他のテキストと重なっていないか (PNG で確認)
- [ ] 外部ロゴ・画像を使用している場合、背景色との組み合わせは適切か (PNG で確認)
- [ ] AWS サービス名が正式名称・正しい略称になっているか
- [ ] AWS アイコンが最新版 (mxgraph.aws4.*) か
- [ ] 不要な要素が残っていないか
- [ ] PNG に変換して視覚的に確認したか


### 2.8. テキストラベルへの矢印接続

draw.io でテキスト要素（`style="text;..."`）に矢印を接続する場合、`exitY=1` や `entryY=1` などの接続点パラメータが期待通りに動作しない場合がある。

**問題**:
- `exitX=0.5;exitY=1` を指定してもテキストの中央に接続される
- テキストラベルの下辺に接続したい場合に正しく配置されない

**解決策**:
明示的な座標指定（`sourcePoint` と `targetPoint`）を使用する

```xml
<!-- 悪い例: source/target でラベル要素を指定 + exitY/entryY を使用 -->
<mxCell id="arrow" style="..." edge="1" parent="1" source="label1" target="label2">
  <mxGeometry relative="1" as="geometry">
    <!-- exitY=1 を指定してもテキストの中央に接続される場合がある -->
  </mxGeometry>
</mxCell>

<!-- 良い例: sourcePoint/targetPoint で明示的に座標を指定 -->
<mxCell id="arrow" style="..." edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="1279" y="500" as="sourcePoint"/>
    <mxPoint x="119" y="500" as="targetPoint"/>
    <Array as="points">
      <mxPoint x="1279" y="560"/>
      <mxPoint x="119" y="560"/>
    </Array>
  </mxGeometry>
</mxCell>
```

**座標の計算方法**:
- テキストラベルの下辺中央: `x = label.x + (label.width / 2)`, `y = label.y + label.height`
- 例: `<mxGeometry x="1219" y="460" width="120" height="40"/>` の場合
  - 中央 X 座標: 1219 + 60 = 1279
  - 下辺 Y 座標: 460 + 40 = 500

### 2.9. PNG プレビューによる視覚的確認

draw.io 図の修正時、PDF の最終的な見た目を確認するため、生成された PNG をレビューする。

**レビュー時の運用ルール**:

- YOU MUST: 生成された `.drawio.png` を直接確認する
- IMPORTANT: ユーザーがブラウザで PNG を開いてレビューする

**手順**:

```bash
# PNG を生成
mise exec -- pre-commit run convert-drawio-to-png --files assets/your-diagram.drawio

# 生成された assets/your-diagram.drawio.png をブラウザで確認
```

**利点**:
- PDF の実際の見た目を素早く確認できる
- フォントサイズ変更やレイアウト調整の効果を視覚的に検証
- 矢印の重なりやテキストの配置ミスを発見しやすい
- Claude Code に PNG を読み込ませて自動レビュー可能

### 2.10. Codex MCP を活用した効率的なレビュー

draw.io 図の品質を保つため、Codex MCP（Model Context Protocol）を使った自動レビューを活用する

レビューの進め方

1. 優先順位をつけて3つずつレビュー
   - 一度に全画像をレビューすると時間がかかりすぎる
   - 問題が多そうな図から優先的にレビュー
   - 各ラウンドで点数を記録し、改善の進捗を可視化

2. Codex に十分な文脈を提供
   - Codex は毎回新しいセッションで、前回の内容を記憶していない
   - スライドの qmd ファイルの内容（タイトル、メッセージ、各図の役割）を共有
   - 前回のレビュー結果と修正内容を説明
   - 目標点数を明示（例: 平均8.5点以上）

3. レビュー観点の明確化
   - 矢印がラベルと被っていないか
   - 矢印の起点・終点がラベルから十分離れているか（最低20px以上）
   - AWS サービス名が正式名称・正しい略称になっているか
   - スライドのメッセージが明確に伝わるか
   - 全体的なレイアウトバランスに問題がないか

レビュー結果の活用

- 各画像について「改善された点」「残存する問題点」「点数」を記録
- 平均点が目標に達するまで修正を繰り返す
- 最終的に全画像の平均点が8.5点以上になることを目指す

edgeLabel の offset 調整テクニック

矢印ラベルを矢印から離すには、edgeLabel の offset 属性を調整する

```xml
<!-- 矢印の上側に配置（マイナス値で離す） -->
<mxCell id="arrow-label" value="ラベル" style="edgeLabel;..." vertex="1" connectable="0" parent="arrow">
  <mxGeometry x="-0.1" y="2" relative="1" as="geometry">
    <mxPoint x="0" y="-40" as="offset"/>  <!-- Y座標をマイナスにして上に離す -->
  </mxGeometry>
</mxCell>

<!-- 矢印の下側に配置（プラス値で離す） -->
<mxCell id="arrow-label" value="ラベル" style="edgeLabel;..." vertex="1" connectable="0" parent="arrow">
  <mxGeometry x="-0.1" y="2" relative="1" as="geometry">
    <mxPoint x="0" y="40" as="offset"/>  <!-- Y座標をプラスにして下に離す -->
  </mxGeometry>
</mxCell>

<!-- 矢印の横に配置 -->
<mxCell id="arrow-label" value="ラベル" style="edgeLabel;..." vertex="1" connectable="0" parent="arrow">
  <mxGeometry x="-0.1" y="2" relative="1" as="geometry">
    <mxPoint x="-60" y="0" as="offset"/>  <!-- X座標を調整して横に離す -->
  </mxGeometry>
</mxCell>
```

重要なポイント

- labelBackgroundColor で白背景をつけても、矢印から20px以上離す必要がある
- フローチャートの分岐ラベル（YES/NO等）でも、視認性のために矢印から離す
- offset の値は、実際の矢印位置とラベルサイズ（fontSize × 行数）を考慮して決定
- 修正後は必ず PNG で視覚確認し、20px以上の余白が確保されているか確認

### 2.11. Codex MCP サーバーが応答しない場合の対処法

Codex MCP サーバー（`mcp__codex-mcp__codex` ツール）を使用してレビューを依頼した際、"Tool ran without output or errors" というメッセージが返ってくる場合がある

原因と対処法

- Codex MCP サーバーは外部プロセスとして動作しており、タイムアウトや接続エラーが発生する場合がある
- この場合、以下の手順で対処する

対処手順

1. 再試行する
   - 同じプロンプトで再度 `mcp__codex-mcp__codex` ツールを呼び出す
   - 1-2回の再試行で成功する場合が多い

2. 再試行しても応答がない場合は代替手段に切り替える
   - Claude Code の Read ツールで PNG を直接読み込んで目視レビューする
   - 人間が最終的にブラウザで `/tmp/drawio-review/*.png` を確認する

3. 問題が続く場合はプロセスを確認
   ```sh
   ps aux | grep -i codex | grep -v grep
   ```

代替レビュー手順

```sh
# PNG を読み込んで自分でレビュー
Read /tmp/drawio-review/diagram.png

# 目視で以下の観点をチェック
# - フォントサイズのバランス
# - 不自然な改行の有無
# - 文字の重なり・被り（20px以上の余白）
# - サービス名の正確性
```

重要なポイント

- Codex MCP サーバーは便利だが、必ず応答するとは限らない
- 応答がない場合は無理に待たず、代替手段に切り替える
- 最終的な品質確認は人間の目視が最も確実
