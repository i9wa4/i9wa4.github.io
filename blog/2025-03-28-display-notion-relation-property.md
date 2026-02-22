# Notion データベースでリレーション元のプロパティを表示する
(2025年3月28日時点)
uma-chan
2025-03-23

## 1. はじめに

下図のように Notion データベースでリレーションプロパティ (列)
にはリレーション元のプロパティも併せて表示させると便利ですよね。

![リレーションプロパティの表示設定成功例](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/goal.png)

タイトル記載日時点で公式ドキュメントに記載された通りに設定ができなかったので手順を共有します。

一応以下が公式ドキュメントです。

<https://www.notion.com/ja/help/relations-and-rollups#リレーションの表示オプション>

## 2. リレーションプロパティの表示設定

最も混乱しづらいであろう手順を以下に示します。

### 2.1. 利用するデータベースの説明

#### 2.1.1. item_master

リレーション元として利用します。

![Item Master
image](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/item_master.png)

#### 2.1.2. transaction_a

item_master をプロパティに追加させたいデータベースです。

![Transaction A
image](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/transaction_a.png)

### 2.2. リレーションプロパティの追加

データベース全体の設定を行うのではなく、1アイテムを編集→全体適用でいきます。

1.  transaction_a の1アイテムをサイドピークで開く
2.  右上の「…」→「レイアウトをカスタマイズ」とクリックする ![01
    Customize Layout
    image](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/01-customize-layout.png)
3.  「＋」をクリックする ![02 Click Plus
    image](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/02-click-plus.png)
4.  リレーションプロパティを選択する ![03 Add Relation
    image](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/03-add-relation.png)
5.  リレーション元として item_master を選択する ![04 Add Item Master
    image](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/04-add-item-master.png)
6.  リレーションを追加する ![05 Add Relation
    image](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/05-add-relation.png)
7.  すべてのページに適用する ![06 Apply
    image](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/06-apply.png)
8.  リレーションプロパティの「…」から表示させたいプロパティを選択する
    ![07 Set Property
    image](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/07-set-property.png)
9.  完了 ![Goal
    image](https://i9wa4.github.io/assets/2025-03-28-display-notion-relation-property-as-section/goal.png)

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-03-28-display-notion-relation-property.html&text=Notion%20%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%81%A7%E3%83%AA%E3%83%AC%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E5%85%83%E3%81%AE%E3%83%97%E3%83%AD%E3%83%91%E3%83%86%E3%82%A3%E3%82%92%E8%A1%A8%E7%A4%BA%E3%81%99%E3%82%8B%20%282025%E5%B9%B43%E6%9C%8828%E6%97%A5%E6%99%82%E7%82%B9%29%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Notion%20%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%81%A7%E3%83%AA%E3%83%AC%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E5%85%83%E3%81%AE%E3%83%97%E3%83%AD%E3%83%91%E3%83%86%E3%82%A3%E3%82%92%E8%A1%A8%E7%A4%BA%E3%81%99%E3%82%8B%20%282025%E5%B9%B43%E6%9C%8828%E6%97%A5%E6%99%82%E7%82%B9%29%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-03-28-display-notion-relation-property.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-03-28-display-notion-relation-property.html&title=Notion%20%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%81%A7%E3%83%AA%E3%83%AC%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E5%85%83%E3%81%AE%E3%83%97%E3%83%AD%E3%83%91%E3%83%86%E3%82%A3%E3%82%92%E8%A1%A8%E7%A4%BA%E3%81%99%E3%82%8B%20%282025%E5%B9%B43%E6%9C%8828%E6%97%A5%E6%99%82%E7%82%B9%29%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
