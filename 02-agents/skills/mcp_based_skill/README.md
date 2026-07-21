# MCPベースの Agent Skills サンプル

このサンプルは、`Agent` で **MCP経由で配信される Agent Skills** を発見する方法を示す。

## 内容

- SEP-2640 規約に従ってスキルリソースを公開するリモートMCPサーバーに、streamable HTTP経由で接続する。
- `MCPSkillsSource` から `SkillsProvider` を構築する。これは `skill://index.json`（SEP-2640の正規の発見方法）を読み取り、インデックスのエントリからスキルを構築する。
- MCP越しのプログレッシブディスクロージャー：広告 → 読み込み → リソース読み取り、という流れはファイルシステムベースのスキルと全く同じ。

## サンプルの実行

### 事前準備

- Python 3.10+
- Ollama をローカルで起動し、`gemma4:12b-it-qat` を pull しておく
- SEP-2640 のスキルリソースをホストしているMCPサーバー（下記「MCPサーバーの用意」を参照）

### セットアップ

MCPサーバーのエンドポイントを設定する（`.env` ファイルまたはシェルで）。

```bash
export MCP_SKILLS_SERVER_URL="https://your-mcp-server.example.com/mcp"
```

### 実行

```bash
uv run python 02-agents/skills/mcp_based_skill/mcp_based_skill.py
```

## MCPサーバーの用意

このサンプルは**利用側（consumer）**であり、MCPサーバー自体はホストしない。エンドツーエンドで試すには、SEP-2640のスキルリソース（`skill://index.json` と各スキルの `SKILL.md`）を公開するMCPサーバーが必要。

- Agent Framework 経由でMCPサーバーをホストする例は、公式リポジトリの `mcp/agent_as_mcp_server.py` を参照（本リポジトリでは対象外のため未収録）。
- Model Context Protocol ワーキンググループが、リファレンス実装のMCP-skillsサーバーを
  [`modelcontextprotocol/experimental-ext-skills`](https://github.com/modelcontextprotocol/experimental-ext-skills)
  で公開している。
