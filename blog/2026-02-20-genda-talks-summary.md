# GENDAデータチームの登壇まとめ (2025年12月〜2026年1月)
uma-chan
2026-02-20

## 1. はじめに

2025年12月から2026年1月にかけてデータチームは3回登壇しました。

それぞれ別のイベントですが、振り返ってみると共通しているテーマがありました。Databricksを軸にして、開発環境・権限管理・AIエージェント配布という3つの方向から「使いにくさを取り除く」という話をしていました。

まとめて記事にしておきます。

## 2. 登壇一覧

| 日付 | イベント | タイトル | 資料 |
|----|----|----|----|
| 2025-12-12 | Databricks Data+AI World Tour After Party | Databricks向けJupyter KernelでデータサイエンティストをAI-Readyにする | [スライド](https://i9wa4.github.io/../slides/2025-12-12-databricks-notebook-ai-ready.md) |
| 2025-12-22 | AEON TECH HUB \#22 | M&Aで拡大し続けるGENDAのデータ活用を促すためのDatabricks権限管理 | [スライド](https://i9wa4.github.io/../slides/2025-12-22-aeon-tech-hub-databricks.md) |
| 2026-01-27 | JEDAI 2026 新春 Meetup! | Mosaic AI Gatewayでコーディングエージェントを配るための運用Tips | [スライド](https://i9wa4.github.io/../slides/2026-01-27-jedai-ai-gateway.md) |

## 3. 各登壇の詳細

### 3.1. Databricks向けJupyter KernelでデータサイエンティストをAI-Readyにする (2025-12-12)

Databricks Notebookはクラウド上で動くので、ローカルのVS
CodeなどのエディタからAIコーディングアシスタントを使おうとするとうまくいかないんですよね。データサイエンティストがAI活用で損をしている状態でずっと気になっていました。

そこでjupyter-databricks-kernelというJupyterのカーネルを自作しました
(自信作)。ローカルVS
CodeからDatabricksのコンピュートに接続できるようになり、`jupyter execute notebook.ipynb`
でノートブックをCLI実行できます。AIコーディングアシスタントがローカルファイルとして扱えるのが重要なポイントです。

ツールだけ入れても環境として機能しないので、あわせて4つの構成も紹介しました。

- Skinny Notebook Wrapper + Pure Python —
  ノートブックは薄いラッパーにして、メインロジックは .py
  に切り出すパターン
- uvによる依存関係管理 — Pythonパッケージのバージョンを明示管理
- mise + pre-commit + Renovateによるガードレール —
  AIが触っても崩れにくいコード品質の自動担保
- CLIでの実行例 — `jupyter execute notebook.ipynb`

### 3.2. M&Aで拡大し続けるGENDAのデータ活用を促すためのDatabricks権限管理 (2025-12-22)

GENDAはM&Aでグループ企業が増え続けています。新しい会社が増えるたびにDatabricksの権限設計を見直すのは大変で、データエンジニア・MLエンジニア・データアナリスト・ビジネスメンバーとロールごとに必要な機能が違うのでさらに複雑になります。

今やっているのはワークスペースレベルの権限とUnity
Catalogのデータアクセス権限を2層で管理する設計です。どちらもグループ単位で管理していて、新メンバーのオンボーディングはグループに追加するだけで完結します。新規M&A企業が増えてもグループを作ってテンプレートの権限を付与すればすぐ動けるようになります。

本番環境はService
Principal（非人間アカウント）経由でのみ操作できる構造にしていて、人間が直接本番を触れないようにしています。まだWIPで改善を続けている段階ですが、概ね機能するようになってきました。

### 3.3. Mosaic AI Gatewayでコーディングエージェントを配るための運用Tips (2026-01-27)

インターンや外部協力者、技術部門以外のメンバーにAIコーディング環境を渡したいけど、APIキーの管理や利用量の監視、環境セットアップのハードルが高いという問題があります。

Mosaic AI
Gatewayを使うと複数のLLM（Claude、GPTなど）への接続を一本化できて、システムテーブルで利用量をモニタリングしながら予算超過時に自動遮断もできます。認証はOAuth
U2Mで完結するのでPersonal Access
Tokenを各自で管理してもらう必要がなく、これが地味に助かります。

ローカル側はBlock社のOSSコーディングエージェントGooseをDev
Containerに組み込む構成にしました。GooseはDatabricksをネイティブサポートしているのでOAuth
U2M認証がそのまま通ります。普段Claude CodeやCodex
CLIを使い込んでいる目線だと物足りない部分は正直ありますが、Dev
ContainerのセットアップでOAuth
U2M認証を済ませるスクリプトを書いておけばほぼ自動で環境構築が終わるので、渡す側としては便利です。jupyter-databricks-kernelとの組み合わせでノートブックの読み取り・編集・実行もGooseに任せられます。

## 4. まとめ

3つとも「Databricksの機能を使って、使えない人を減らす」という話でした。

データサイエンティストのAI活用の壁、M&A後のオンボーディングの壁、非エンジニアへのAIツール配布の壁、それぞれ全部まだきれいに解決しているわけではないですが、取り組みとしての方向性は固まってきた気がします。

引き続き改善しながら発信していきます。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-02-20-genda-talks-summary.html&text=GENDA%E3%83%87%E3%83%BC%E3%82%BF%E3%83%81%E3%83%BC%E3%83%A0%E3%81%AE%E7%99%BB%E5%A3%87%E3%81%BE%E3%81%A8%E3%82%81%20%282025%E5%B9%B412%E6%9C%88%E3%80%9C2026%E5%B9%B41%E6%9C%88%29%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=GENDA%E3%83%87%E3%83%BC%E3%82%BF%E3%83%81%E3%83%BC%E3%83%A0%E3%81%AE%E7%99%BB%E5%A3%87%E3%81%BE%E3%81%A8%E3%82%81%20%282025%E5%B9%B412%E6%9C%88%E3%80%9C2026%E5%B9%B41%E6%9C%88%29%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-02-20-genda-talks-summary.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2026-02-20-genda-talks-summary.html&title=GENDA%E3%83%87%E3%83%BC%E3%82%BF%E3%83%81%E3%83%BC%E3%83%A0%E3%81%AE%E7%99%BB%E5%A3%87%E3%81%BE%E3%81%A8%E3%82%81%20%282025%E5%B9%B412%E6%9C%88%E3%80%9C2026%E5%B9%B41%E6%9C%88%29%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
