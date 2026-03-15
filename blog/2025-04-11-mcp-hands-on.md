# MCP に入門した
uma-chan
2025-04-11

## 1. 直近 MCP でやりたいこと

非エンジニアに Databricks でデータ分析をしてもらう

## 2. 参考リンク

以下の順に触っていけばよいはず

1.  [MCP入門](https://zenn.dev/mkj/articles/0ed4d02ef3439c)
2.  [MCP (Model Context Protocol) の仕組みを知りたい！ \#Python -
    Qiita](https://qiita.com/megmogmog1965/items/79ec6a47d9c223e8cffc)
3.  [SiteMCP:
    任意のサイトを丸ごとMCPサーバー化](https://zenn.dev/ryoppippi/articles/1eb7fbe9042a88)
    - Databricks 公式ドキュメントを投げつける用途で使いたい
4.  [CursorにおけるDatabricks MCPサーバーの活用 \#cursor -
    Qiita](https://qiita.com/taka_yayoi/items/eea79a88bd638847beb8)
5.  [CursorでDatabricks Connect(とMCPサーバー)を使ってみる \#cursor -
    Qiita](https://qiita.com/taka_yayoi/items/dae7053118c7f60e980d)

## 3. MCP 入門

全体を読みサンプルコードを実行してみる

### 3.1. MCPクライアントを実行する

``` sh
(myenv3.12) [2025-04-10 22:50:25] -zsh [~/ghq/github.com/i9wa4/mcp-hands-on] (main) 9e297f01
$ python mini_client.py
Processing request of type CallToolRequest
Tool result: [TextContent(type='text', text='Hello, MCP!', annotations=None)]
```

## 4. MCP (Model Context Protocol) の仕組みを知りたい！

ちょこっと理解が深まった

## 5. Cursor を MCP クライアントとして使う (SiteMCP)

``` json
{
  "mcpServers": {
    "sitemcp": {
      "command": "npx",
      "args": [
        "-y",
        "sitemcp@latest",
        "https://i9wa4.github.io/"
      ]
    }
  }
}
```

MCPサーバ設定をこのように記載して Cursor の Agent
でサイトのインデックス取得を命令していくことで内容に関する質問ができるようになりました。

![Cursor Sitemcp
image](https://i9wa4.github.io/assets/2025-04-11-mcp-hands-on/cursor-sitemcp.png)

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-04-11-mcp-hands-on.html&text=MCP%20%E3%81%AB%E5%85%A5%E9%96%80%E3%81%97%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=MCP%20%E3%81%AB%E5%85%A5%E9%96%80%E3%81%97%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-04-11-mcp-hands-on.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-04-11-mcp-hands-on.html&title=MCP%20%E3%81%AB%E5%85%A5%E9%96%80%E3%81%97%E3%81%9F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
