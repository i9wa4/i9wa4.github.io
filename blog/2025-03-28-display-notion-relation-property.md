# Notion データベースでリレーション元のプロパティを表示する
(2025年3月28日時点)
uma-chan
2025-03-23

## 1. はじめに

下図のように Notion データベースでリレーションプロパティ (列)
にはリレーション元のプロパティも併せて表示させると便利ですよね。

![リレーションプロパティの表示設定成功例](../assets/2025-03-28-display-notion-relation-property-as-section/goal.png)

タイトル記載日時点で公式ドキュメントに記載された通りに設定ができなかったので手順を共有します。

一応以下が公式ドキュメントです。

<https://www.notion.com/ja/help/relations-and-rollups#リレーションの表示オプション>

## 2. リレーションプロパティの表示設定

最も混乱しづらいであろう手順を以下に示します。

### 2.1. 利用するデータベースの説明

#### 2.1.1. item_master

リレーション元として利用します。

![](../assets/2025-03-28-display-notion-relation-property-as-section/item_master.png)

#### 2.1.2. transaction_a

item_master をプロパティに追加させたいデータベースです。

![](../assets/2025-03-28-display-notion-relation-property-as-section/transaction_a.png)

### 2.2. リレーションプロパティの追加

データベース全体の設定を行うのではなく、1アイテムを編集→全体適用でいきます。

1.  transaction_a の1アイテムをサイドピークで開く
2.  右上の「…」→「レイアウトをカスタマイズ」とクリックする
    ![](../assets/2025-03-28-display-notion-relation-property-as-section/01-customize-layout.png)
3.  「＋」をクリックする
    ![](../assets/2025-03-28-display-notion-relation-property-as-section/02-click-plus.png)
4.  リレーションプロパティを選択する
    ![](../assets/2025-03-28-display-notion-relation-property-as-section/03-add-relation.png)
5.  リレーション元として item_master を選択する
    ![](../assets/2025-03-28-display-notion-relation-property-as-section/04-add-item-master.png)
6.  リレーションを追加する
    ![](../assets/2025-03-28-display-notion-relation-property-as-section/05-add-relation.png)
7.  すべてのページに適用する
    ![](../assets/2025-03-28-display-notion-relation-property-as-section/06-apply.png)
8.  リレーションプロパティの「…」から表示させたいプロパティを選択する
    ![](../assets/2025-03-28-display-notion-relation-property-as-section/07-set-property.png)
9.  完了
    ![](../assets/2025-03-28-display-notion-relation-property-as-section/goal.png)
