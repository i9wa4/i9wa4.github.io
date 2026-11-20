# AIと働く環境を育て続ける
Mawatari Daiki
2026-11-04

## 1. はじめに

### 1.1. 自己紹介

<style>
.reveal .presentation-diagram svg[id^="mermaid"] {
  width: var(--diagram-width) !important;
  max-width: 100% !important;
  height: auto !important;
}
</style>

Mawatari Daiki \| 馬渡 大樹

2026年10月にジョインしました

直近はExpert稼動分析に着手しています

- 他の仕事
  - GENDA
    - データエンジニア
    - MLOpsエンジニア
    - データサイエンスチームマネージャー
  - PIVOT (業務委託)
    - データエンジニア
- 趣味
  - ターミナル
    - 先日 Terminal Night 3 に登壇してきました

## 2. AIに対する課題

### 2.1. 開発に使うAIエージェント：自分の手先の延長にしづらい

どうしても提供された形をそのまま使ったり有志のTipsがあったりしてしっくりこなかった
(2025年末あたりで特にそう思った)

## 3. AIに対する課題へのアプローチ

### 3.1. tmux上のAIチームをつなぐツールを作っている

縛りを設けて自分や環境の成長を狙う

<https://github.com/i9wa4/tmux-a2a-postman>

<div class="presentation-diagram" style="--diagram-width: 1800px">

``` mermaid
flowchart LR
    H((人間)) <-->|"依頼・進捗"| PA
    subgraph parent["ghq/github.com/"]
        PA["agent<br/>人間との対話"] <--> PO["orchestrator<br/>全体を管理"]
        PO <--> PM["messenger<br/>interface_node"]
        PO <--> PW["worker"]
        PO <--> PR["reviewer"]
        PO <--> PAP["approver"]
    end
    subgraph dotfiles["ghq/github.com/org/pj2"]
        DM["messenger<br/>interface_node"] <--> DO["orchestrator"]
        DO <--> DW["worker"]
        DO <--> DR["reviewer"]
        DO <--> DAP["approver"]
    end
    subgraph postman["ghq/github.com/org/pj1"]
        TM["messenger<br/>interface_node"] <--> TO["orchestrator"]
        TO <--> TW["worker"]
        TO <--> TR["reviewer"]
        TO <--> TAP["approver"]
    end
    PM <-->|"親子間の連絡"| DM
    PM <-->|"親子間の連絡"| TM
    classDef human fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef dialogue fill:#e0f2fe,stroke:#0891b2,color:#164e63
    classDef interface fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef orchestration fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef implementation fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef review fill:#fce7f3,stroke:#db2777,color:#831843
    classDef approval fill:#ffedd5,stroke:#ea580c,color:#7c2d12
    class H human
    class PA dialogue
    class PM,DM,TM interface
    class PO,DO,TO orchestration
    class PW,DW,TW implementation
    class PR,DR,TR review
    class PAP,DAP,TAP approval
    style parent fill:#eff6ff,stroke:#1d4ed8,stroke-width:3px
    style dotfiles fill:#f8fafc,stroke:#94a3b8
    style postman fill:#f8fafc,stroke:#94a3b8
```

</div>

### 3.2. \[縛り1\] 各AIエージェントの仕事を小さくする

**仮説：担当する仕事を絞るワークフローがうまく回るとワークフロー自体をスケールできるのでは**

- メリット
  - 責務が小さいと動きの一貫性を追求しやすい
  - こなせるタスクの数や量を増やしやすい
- デメリット
  - 役割分担をするとエッジの数だけ情報の欠落や認識齟齬が増えやすくなる
  - 各担当の完了報告の真偽判定が難しい

**ゴール：各AIエージェントの責務は小さくした上で本質的な課題解決に必要なトークンや時間を最小化したい**

- 現状
  - 人間の関与が減り本質を見失うことがある
  - それぞれがコンテキストを維持しつつあまり共有しないことで敵対的レビューが成功しやすい
    (そもそも敵対的レビューをやめたほうがいいのかもしれないが)
  - 問題を小さくしているためかトークンはかなり減らせるが所要時間はなかなか短縮できていない

### 3.3. \[縛り2\] 小さな道具とテキストでマルチエージェントオーケストレーションを成立させる

**UNIX哲学を意識して大きな飛躍の余地を残す**

| 部品     | 責務                                 |
|----------|--------------------------------------|
| tmux     | AIエージェントの作業場所             |
| CLI      | 通信基盤                             |
| Markdown | 送受信内容、設定ファイルとしての利用 |

**世界のハーネスの進化に追従できる特徴**

- AIエージェントの動きを邪魔しない
- 透明性が高く追跡ができる
- プリミティブな構成なので最新理論やトレンドを取り込むことができる

**ツールの自己改善ループを組めるようになった理由**

- デーモンレス化で常駐サービスをなくす
- doc / skillをバイナリに内包しコンテキストの更新サイクルも揃える

### 3.4. \[縛り3\] 端末やAIが変わっても変わらず作業が続けられる

- **いま試していること**
  - 複数のPCやスマホのAIアプリでメールボックスを共有して仕事を進める
- **その先に目指すこと**
  - この先どのように環境の変化が起きても
    **人間に最適化されたインタフェース層** と **業務遂行に適した環境**
    をシームレスに繋ぎ続ける

## 4. AI時代の今後について

### 4.1. 育て続けられる環境に賭ける

自環境をベンダーロックインさせず本質的な事柄に向き合って改善を続けたい

<div class="presentation-diagram" style="--diagram-width: 600px">

``` mermaid
flowchart TD
    use["タスクを進める"] --> gap["課題と原因を抽出させる"]
    gap --> change["環境改善を試みる"]
    change --> check["検証する"]
    check --> use
```

</div>

改善には **削除・統合・簡素化** も含めるので人間が剪定し続けておきたい

縛りの中で課題を解き続けることで **自分も環境も強くする！**
