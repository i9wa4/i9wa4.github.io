---
layout: post
title:  "PostgreSQL 向け Tips"
date:   2024-02-04 15:50:10 +0900
categories: blog
tags: tips
---

{% include tag.html %}

Table of Content:
- Table of Content
{:toc}

<!-- # h1 -->

こんにちは。i9wa4 です。

自分用に PostgreSQL 向けの Tips を書き残しておきます。

## 1. PostgreSQL 起動～データベースへのアクセス

いつも忘れるので取っかかりとしてコマンドを書いておきます。

```sh
pg_ctl restart
psql -U postgres -d db_name

pg_ctl restart
psql -U postgres
CREATE DATABASE db_name;
\c db_name
CREATE SCHEMA sc_name;
```
