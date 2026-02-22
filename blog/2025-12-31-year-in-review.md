# 2025年の総括：AI駆動人生
uma-chan
2025-12-31

## 1. はじめに

2025年が終わろうとしています。

[2024年度を振り返る](https://i9wa4.github.io/./2025-04-02-looking-back-on-2024.md)

これ、去年の振り返りです。
めちゃめちゃ内容が薄くて笑っちゃうくらい今年は濃い1年でした。

ある程度年齢も重ねているのですが、これまで伸び悩んでいた分を一気に取り戻すような1年になったと感じています。

大晦日に2025年を総括します。

## 2. 2025年の数字

### 2.1. GitHub活動

ほぼ個人リポジトリでの活動です (private contributions は除外)。

| 項目            |  数値 |
|:----------------|------:|
| 総Contributions | 4,902 |
| コミット        | 2,975 |
| Issue           |   135 |
| PR              |   142 |

dotfilesへのコミットが1,307回 (yabai)。

外部OSSへのコントリビューションとして vim/vim (Vim本体)
へのPRがマージされて Vim Contributor になれました。

記事はこちら
[Vimへの初コントリビューションの経緯と学び](https://i9wa4.github.io/./2025-07-14-my-first-vim-contribution.md)

### 2.2. アウトプット

| 種類       | 本数 |
|:-----------|-----:|
| ブログ記事 |   40 |
| スライド   |    7 |
| Zenn記事   |   21 |
| 寄稿       |    3 |

合計71本の記事を書きました。週1本以上のペースです。

### 2.3. 登壇

4回の外部登壇を行いました。

| 日付 | 登壇先 | 資料 |
|:---|:---|:---|
| 2025/12/23 | [モダンデータ基盤の最前線：現場から学ぶ実践と挑戦 - connpass](https://aeon.connpass.com/event/375097/) | [M&Aで拡大し続けるGENDAのデータ活用を促すためのDatabricks権限管理 / AEON TECH HUB \#22 - Speaker Deck](https://speakerdeck.com/genda/aeon-tech-hub-22-mawatari) |
| 2025/12/12 | [Databricks Data + AI World Tour Tokyo After Party](https://events.databricks.com/daiwt-tokyo-after-party/registration-closed) | [Databricks向けJupyter Kernelでデータサイエンティストの開発環境をAI-Readyにする / Data+AI World Tour Tokyo After Party - Speaker Deck](https://speakerdeck.com/genda/data-ai-world-tour-tokyo-after-party-mawatari) |
| 2025/11/07 | [試されDATA SAPPORO \#1 - connpass](https://tamesaredatahokkaido.connpass.com/event/369741/) | [GENDA の機械学習環境を AWS から Databricks に移行してみた](https://i9wa4.github.io/../slides/2025-11-07-tamesare-data-sapporo-uma-chan.md) |
| 2025/05/22 | AIネイティブ開発 Tips 1000本ノック (ミダスキャピタル投資先企業勉強会) | [Cursorのおすすめ設定 & Cursorにデータ分析を任せる方法](https://i9wa4.github.io/../slides/2025-05-22-midas-cursor-tips.md) |

これまでの人生では登壇したことがなかったのですが今年シレッと4回も登壇してます。

初登壇、イベント主催、Databricks
公式イベント、オンラインで大勢の前で話すなど様々な経験ができました。

## 3. 2025年の主な成果

### 3.1. AI駆動開発環境の構築

Claude Code と Codex CLIを中心に据えた Vim + tmux + Alacritty + Zsh + AI
CLI という開発環境の利便性向上に注力してきました。

### 3.2. Vimプラグイン開発

2本のVimプラグインを開発・更新しました。

- [vim-tmux-send-to-ai-cli](https://github.com/i9wa4/vim-tmux-send-to-ai-cli)
  - Vimからtmux経由でAI CLIにプロンプトを送信するプラグイン
- [ddc-source-slash-commands](https://github.com/i9wa4/ddc-source-slash-commands)
  - カスタムスラッシュコマンド補完用の ddc.vim ソースプラグイン

6月にはVim本体へ初めてコントリビューションできたのでまだ当面喜んでいようと思います。

### 3.3. OSS 開発

- [jupyter-databricks-kernel](https://github.com/i9wa4/jupyter-databricks-kernel)
  - Databricks をバックエンドにした Jupyter Kernel (自信作)
- [databricks-marimo-executor](https://github.com/i9wa4/databricks-marimo-executor)
  - Databricks をバックエンドにした Marimo Executor
    (飽きてまだ実装できてない)
- [mcp-databricks-server](https://github.com/i9wa4/mcp-databricks-server)
  - Databricks でクエリを実行するための MCP Server (ちょっと自信作)

jupyter-databricks-kernel
は12月の登壇でも紹介していて、データサイエンティストの開発環境をAI-Readyにするための取り組みとして発表しました。

Databricks さんが API 開発してくれたら Serverless Compute
対応もしたいですぅ！
(技術力は足りないかもだけどモチベだけは高いから私にやらせてくれとめっちゃ思ってる)

Command Execution API
に興味があるの世界で自分だけなのではと思いながらこのプロジェクトを進めましたが、割と反響があって嬉しいです。

### 3.4. Databricks開発環境のAI-Ready化

データサイエンティストの開発環境という未開拓の改善の余地のある分野を見つけていて色々試行錯誤してきました。
2025年はDatabricks開発環境のAI-Ready化に注力しました。 Claude
CodeやCursorなどのAIコーディングアシスタントをDatabricks開発で活用するための環境整備です。

[Databricks Notebook 開発環境を AI-Ready
にする](https://zenn.dev/genda_jp/articles/2025-12-19-databricks-notebook-ai-ready)

もしくは

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/58be33da57d84a5eb9914aa8a8c903ec" title="Databricks向けJupyter Kernelでデータサイエンティストの開発環境をAI-Readyにする / Data+AI World Tour Tokyo After Party" allowfullscreen="true" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" data-ratio="1.7777777777777777">

</iframe>

を読んでください！

### 3.5. データエンジニアリング実務

仕事ではdbt、Databricks、BigQuery、Terraformを使ったデータ基盤開発に取り組みました。

ここは大きな成果というよりも継続的な取り組みですね。

権限整理についてはチームで取り組んだ内容を登壇資料にまとめています。

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/477b4da9eb5e4fdeb8164a3ccaae9a75" title="M&amp;Aで拡大し続けるGENDAのデータ活用を促すためのDatabricks権限管理 / AEON TECH HUB #22" allowfullscreen="true" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" data-ratio="1.7777777777777777">

</iframe>

6月からはPIVOT株式会社での業務委託も開始しました。BigQuery x dbt
Coreのデータマート構築を担当し、リファラ分析モデルの新規構築やincrementalモデル設計によるパフォーマンス最適化は記事にまとめています
(次節参照)。

### 3.6. 寄稿

所属企業のブログに3本の記事を寄稿しました。

- [データ分析を促進する dbt incremental モデル設計 ―
  全期間追跡の低コスト化](https://zenn.dev/pivotmedia/articles/pivot-incremental-friendly-dbt-model)
  (PIVOT)
- [GENDAのデータサイエンティスト開発体験向上の取り組み紹介―AWS
  ECSからDatabricksへの移行](https://zenn.dev/genda_jp/articles/724a597e8f18ff)
  (GENDA)
- [成長を支えるハブとなりたい。データドリブンな組織を加速させるデータ基盤とMLOps](https://note.com/genda_jp/n/n94def6811d47)
  (GENDA note)

## 4. Recap

<blockquote class="twitter-tweet">

<p lang="ht" dir="ltr">

Zenn 2025 Recap
<a href="https://t.co/JPaMQaoUEc">pic.twitter.com/JPaMQaoUEc</a>
</p>

— uma-chan🌲 (@i9wa4\_)
<a href="https://twitter.com/i9wa4_/status/2006361739995287761?ref_src=twsrc%5Etfw">December
31, 2025</a>
</blockquote>

<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<blockquote class="twitter-tweet">

<p lang="ja" dir="ltr">

12月に1000コミットしてたらしい<br>public
なものだけなので仕事は別カウントだよー<a href="https://t.co/fGxl14pSs5">https://t.co/fGxl14pSs5</a>
<a href="https://t.co/As8jEiPvC7">pic.twitter.com/As8jEiPvC7</a>
</p>

— uma-chan🌲 (@i9wa4\_)
<a href="https://twitter.com/i9wa4_/status/2006369271031681135?ref_src=twsrc%5Etfw">December
31, 2025</a>
</blockquote>

<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<blockquote class="twitter-tweet">

<p lang="ja" dir="ltr">

LAPRASがまとめた、私の今年のアウトプットや成果がこちら！<a href="https://twitter.com/hashtag/LAPRAS_Recap2025?src=hash&amp;ref_src=twsrc%5Etfw">\#LAPRAS_Recap2025</a>
<a href="https://twitter.com/hashtag/2025%E5%B9%B4%E3%81%AE%E3%81%B5%E3%82%8A%E3%81%8B%E3%81%88%E3%82%8A?src=hash&amp;ref_src=twsrc%5Etfw">\#2025年のふりかえり</a><a href="https://t.co/TdJrOpfvvp">https://t.co/TdJrOpfvvp</a>
<a href="https://t.co/QJ60UyjiXf">pic.twitter.com/QJ60UyjiXf</a>
</p>

— uma-chan🌲 (@i9wa4\_)
<a href="https://twitter.com/i9wa4_/status/2006361171377684797?ref_src=twsrc%5Etfw">December
31, 2025</a>
</blockquote>

<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## 5. 月別の主な出来事

| 月   | 主な出来事                                                 |
|:-----|:-----------------------------------------------------------|
| 1月  | Zenn記事執筆、コミュニティイベント参加開始                 |
| 2月  | SQL Tips記事、Vimプラグインアイデア                        |
| 3月  | Terraformモノリポ作成、インフラコード試行錯誤開始          |
| 4月  | AIコーディングエージェント試用開始 (Aider, Devin)、MCP入門 |
| 5月  | uvに完全移行、Terraform + MCP Lambda実装に集中             |
| 6月  | Vim本体へ初コントリビューション、PIVOT業務委託開始         |
| 7月  | Claude Code本格導入、ターミナル最適化記事                  |
| 8月  | Devcontainer x Databricks Connect 記事                     |
| 9月  | Codex CLI導入、BigQuery dbt incremental記事                |
| 10月 | dotfiles月間コミット数263で過去最高 (yabai)                |
| 11月 | 試されDATA SAPPORO登壇、Vimプラグイン開発加速              |
| 12月 | 2回の登壇、jupyter-databricks-kernel公開、総括             |

## 6. 振り返り

### 6.1. うまくいったこと

AIコーディングエージェントの台頭にうまく乗っていけました。今年の踏ん張りが絶対に来年以降に活きると思います。

アウトプットの習慣も定着しました。記事執筆と登壇が増えましたね！

### 6.2. 課題として残ったこと

Terraformモノレポを個人用に作ってみたものの使う機会が少なかったです。使わないのにメンテナンスコストがかかり続けるというデメリットを感じました。

### 6.3. 2026年に向けて

**AIが動きやすくなるための環境整備を続けていきます！**
これは自分の趣味嗜好とも合うし、ついでに世の中の役にも立てるのでWin-Winです。

あとはターミナル、tmux、Vim、CI/CD、IaCへのこだわりが強いのでこの辺りで何か成果を出したい気持ちでいます。
純粋100%データエンジニアだとこの辺りを楽しむ余地が少ないので、MLOpsも引き続き楽しみたいですねぇ。

外部発信も頑張っていきたいです。

## 7. おわりに

2025年はAI駆動開発に本格参戦し、ツールを使う側からツールを作る側にもなれた1年でした。

これはAIの波に乗って、今まではやれなかったようなことを実現できたからこそだと思います。

あと月並みな話ですが、たくさんの出会いがあって人生変わったなと実感してます
(会ってくださった皆様ありがとうございました！また飲みましょう！)。

2024年始まった頃なんて自分は本当にしょぼい何もできないエンジニアだったなと思います。今は自信をもって話せる分野ができたり、居場所が確保できていたりと年齢は重ねてますがまだまだ伸びしろを感じられていて嬉しいです。

所属先それぞれでバリューを発揮できるように頑張りますので、引き続きよろしくお願いいたします。

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-12-31-year-in-review.html&text=2025%E5%B9%B4%E3%81%AE%E7%B7%8F%E6%8B%AC%EF%BC%9AAI%E9%A7%86%E5%8B%95%E4%BA%BA%E7%94%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=2025%E5%B9%B4%E3%81%AE%E7%B7%8F%E6%8B%AC%EF%BC%9AAI%E9%A7%86%E5%8B%95%E4%BA%BA%E7%94%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-12-31-year-in-review.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-12-31-year-in-review.html&title=2025%E5%B9%B4%E3%81%AE%E7%B7%8F%E6%8B%AC%EF%BC%9AAI%E9%A7%86%E5%8B%95%E4%BA%BA%E7%94%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
