# Databricks向けJupyter
Kernelでデータサイエンティストの開発環境をAI-Readyにする
Mawatari Daiki
2025-12-12

## 自己紹介

<div style="font-size: 1.3em;">

Mawatari Daiki / uma-chan

株式会社GENDA

IT戦略部 データチーム

データエンジニア / MLOpsエンジニア

</div>

<div style="margin-top: 2em;">

[<img
src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fcdn.qiita.com%2Fassets%2Fpublic%2Fadvent_calendar%2Fogp%2Fcalendar-ogp-background-c24e7570f8dc39b6f4e1323cbd83d11f.jpg?ixlib=rb-4.0.0&amp;w=1200&amp;mark-x=142&amp;mark-y=128&amp;mark64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ0eHQtYWxpZ249bGVmdCUyQ3RvcCZ0eHQtY29sb3I9JTIzRkZGRkZGJnR4dC1mb250PUhpcmFnaW5vJTIwU2FucyUyMFc2JnR4dC1zaXplPTU2JnR4dD1EYXRhYnJpY2tzJTIwQWR2ZW50JTIwQ2FsZW5kYXIlMjAyMDI1Jnc9OTE2Jmg9MzU2JnM9OTQ0ODc2YWVlN2VkMTI0YzcwYTQwMzhkYWNlMmQyMzA&amp;blend-mode=normal&amp;blend-x=142&amp;blend-y=491&amp;blend64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ0eHQtYWxpZ249bGVmdCUyQ3RvcCZ0eHQtY29sb3I9JTIzRkZGRkZGJnR4dC1mb250PUhpcmFnaW5vJTIwU2FucyUyMFc2JnR4dC1zaXplPTM2JnR4dD0lNDB0YWthX3lheW9pJnc9OTE2JnM9ZmYyNDVhNzRjMjJmOTJhZjZlMGViZWNmMTc3ODVlNTE&amp;s=5dcabafd2696c55e5b657bcf9f5535e6"
height="350" />](https://qiita.com/advent-calendar/2025/databricks)

12/19に本日の登壇内容と同様の記事を投稿予定です！

</div>

## 課題提起

### 従来のDatabricks Notebook開発の課題

<img
src="https://i9wa4.github.io/assets/2025-12-12-databricks-notebook-ai-ready/notebook-challenges.drawio.png"
style="height:85.0%" alt="Notebook Challenges image" />

### AI時代の新たな課題

<img
src="https://i9wa4.github.io/assets/2025-12-12-databricks-notebook-ai-ready/ai-era-challenges.drawio.png"
height="900" alt="Ai Era Challenges image" />

## Databricks Notebook開発体験改善策

### jupyter-databricks-kernel

<div style="font-size: 1.1em;">

Jupyterにおけるカーネルとは

- ノートブックのセルを処理し、結果をフロントエンド (VS Codeなど)
  に送信するもの

</div>

<div style="margin-top: 1.5em; font-size: 1.1em;">

ローカル開発環境を改善すべくDatabricks
Computeに接続できるカーネルを作りました！

``` sh
jupyter execute notebook.ipynb
```

でノートブック実行できます！

</div>

<div style="margin-top: 1.5em;">

[github.com/i9wa4/jupyter-databricks-kernel](https://github.com/i9wa4/jupyter-databricks-kernel)

</div>

### jupyter-databricks-kernel

<img
src="https://i9wa4.github.io/assets/2025-12-12-databricks-notebook-ai-ready/jupyter-databricks-kernel.drawio.png"
style="height:85.0%" alt="Jupyter Databricks Kernel image" />

### Skinny Notebook Wrapper + Pure Python

<div style="font-size: 1.1em;">

以下の構成が使いやすいです

- ノートブックは便利なので使い続ける
- メインロジックは .py
  ファイルに切り出してノートブックからそれを実行する

</div>

<div style="margin-top: 1.5em;">

詳細は記事に書きました

[<img
src="https://res.cloudinary.com/zenn/image/upload/s--8_Ei_lHe--/c_fit%2Cg_north_west%2Cl_text:notosansjp-medium.otf_55:Databricks%25E3%2581%25AE%25E3%2583%258E%25E3%2583%25BC%25E3%2583%2588%25E3%2583%2596%25E3%2583%2583%25E3%2582%25AF%25E7%25AE%25A1%25E7%2590%2586%25E6%2596%25B9%25E6%25B3%25952%25E9%2581%25B8%2Cw_1010%2Cx_90%2Cy_100/g_south_west%2Cl_text:notosansjp-medium.otf_34:uma-chan%2Cx_220%2Cy_108/bo_3px_solid_rgb:d6e3ed%2Cg_south_west%2Ch_90%2Cl_fetch:aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3plbm4tdXNlci11cGxvYWQvYXZhdGFyLzNiM2M1MjhkNjguanBlZw==%2Cr_20%2Cw_90%2Cx_92%2Cy_102/co_rgb:6e7b85%2Cg_south_west%2Cl_text:notosansjp-medium.otf_30:GENDA%2Cx_220%2Cy_160/bo_4px_solid_white%2Cg_south_west%2Ch_50%2Cl_fetch:aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3plbm4tdXNlci11cGxvYWQvYXZhdGFyLzIyMjZhYmJjODIuanBlZw==%2Cr_max%2Cw_50%2Cx_139%2Cy_84/v1627283836/default/og-base-w1200-v2.png"
height="350" />](https://zenn.dev/genda_jp/articles/2025-12-10-organize-databricks-notebook-management)

</div>

### Skinny Notebook Wrapper + Pure Python

<img
src="https://i9wa4.github.io/assets/2025-12-12-databricks-notebook-ai-ready/skinny-notebook-wrapper.drawio.png"
style="height:85.0%" alt="Skinny Notebook Wrapper image" />

### uvによる依存関係管理

<div style="font-size: 1.1em;">

uvでPythonパッケージのバージョン管理をしていくと色々と便利になります

</div>

<div style="margin-top: 1.5em;">

詳細は記事に書きました

[<img
src="https://res.cloudinary.com/zenn/image/upload/s---Xntff5x--/c_fit%2Cg_north_west%2Cl_text:notosansjp-medium.otf_55:Databricks%2520%25E3%2581%25A7%2520uv%2520%25E3%2582%2592%25E6%25B4%25BB%25E7%2594%25A8%25E3%2581%2597%25E3%2581%25A6%25E4%25BE%259D%25E5%25AD%2598%25E9%2596%25A2%25E4%25BF%2582%25E3%2582%2592%25E7%25AE%25A1%25E7%2590%2586%25E3%2581%2599%25E3%2582%258B%2Cw_1010%2Cx_90%2Cy_100/g_south_west%2Cl_text:notosansjp-medium.otf_34:uma-chan%2Cx_220%2Cy_108/bo_3px_solid_rgb:d6e3ed%2Cg_south_west%2Ch_90%2Cl_fetch:aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3plbm4tdXNlci11cGxvYWQvYXZhdGFyLzNiM2M1MjhkNjguanBlZw==%2Cr_20%2Cw_90%2Cx_92%2Cy_102/co_rgb:6e7b85%2Cg_south_west%2Cl_text:notosansjp-medium.otf_30:GENDA%2Cx_220%2Cy_160/bo_4px_solid_white%2Cg_south_west%2Ch_50%2Cl_fetch:aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3plbm4tdXNlci11cGxvYWQvYXZhdGFyLzIyMjZhYmJjODIuanBlZw==%2Cr_max%2Cw_50%2Cx_139%2Cy_84/v1627283836/default/og-base-w1200-v2.png"
height="350" />](https://zenn.dev/genda_jp/articles/2025-12-11-use-uv-in-databricks)

</div>

### uvによる依存関係管理

<img
src="https://i9wa4.github.io/assets/2025-12-12-databricks-notebook-ai-ready/uv-management.drawio.png"
style="height:85.0%" alt="Uv Management image" />

### ガードレール

<div style="font-size: 1.1em;">

AI時代にも適応するガードレールを構築していきましょう！

</div>

<div style="margin-top: 1.5em;">

詳細は記事に書きました

[<img
src="https://res.cloudinary.com/zenn/image/upload/s--N_cJO-Dq--/c_fit%2Cg_north_west%2Cl_text:notosansjp-medium.otf_55:mise%2520%252B%2520pre-commit%2520%252B%2520Renovate%2520%25E3%2581%25A7%25E4%25BD%259C%25E3%2582%258B%25E3%2583%25A1%25E3%2583%25B3%25E3%2583%2586%25E3%2581%2597%25E3%2582%2584%25E3%2581%2599%25E3%2581%2584%25E3%2582%25AC%25E3%2583%25BC%25E3%2583%2589%25E3%2583%25AC%25E3%2583%25BC%25E3%2583%25AB%2Cw_1010%2Cx_90%2Cy_100/g_south_west%2Cl_text:notosansjp-medium.otf_34:uma-chan%2Cx_220%2Cy_108/bo_3px_solid_rgb:d6e3ed%2Cg_south_west%2Ch_90%2Cl_fetch:aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3plbm4tdXNlci11cGxvYWQvYXZhdGFyLzNiM2M1MjhkNjguanBlZw==%2Cr_20%2Cw_90%2Cx_92%2Cy_102/co_rgb:6e7b85%2Cg_south_west%2Cl_text:notosansjp-medium.otf_30:GENDA%2Cx_220%2Cy_160/bo_4px_solid_white%2Cg_south_west%2Ch_50%2Cl_fetch:aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3plbm4tdXNlci11cGxvYWQvYXZhdGFyLzIyMjZhYmJjODIuanBlZw==%2Cr_max%2Cw_50%2Cx_139%2Cy_84/v1627283836/default/og-base-w1200-v2.png"
height="350" />](https://zenn.dev/genda_jp/articles/2025-12-06-ai-guardrails-local-cloud)

</div>

### ガードレール

<img
src="https://i9wa4.github.io/assets/2025-12-12-databricks-notebook-ai-ready/guardrails.drawio.png"
style="height:85.0%" alt="Guardrails image" />

## まとめ

### 紹介した改善策の全体像

<img
src="https://i9wa4.github.io/assets/2025-12-12-databricks-notebook-ai-ready/ai-ready-overview.drawio.png"
style="height:85.0%" alt="Ai Ready Overview image" />
