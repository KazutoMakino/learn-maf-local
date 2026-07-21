# DevUI サンプル

このフォルダには、Agent Framework DevUI（エージェントを対話的に実行・テストするための軽量Webインターフェース）と連携するサンプルのエージェント・ワークフローが入っている。

## DevUI とは

DevUI は以下を提供するサンプルアプリケーション：

- エージェント・ワークフローをテストするWebインターフェース
- OpenAI互換のAPIエンドポイント
- ディレクトリベースのエンティティ探索
- インメモリでのエンティティ登録
- サンプルエンティティのギャラリー

> **Note**: DevUI は開発・テスト用のサンプルアプリ。本番運用では Agent Framework SDK を使って独自のインターフェースを構築すること。

すべてのサンプルは `OllamaChatClient` を使うよう書き換えられている。Ollama をローカルで起動し、
`gemma4:12b-it-qat` を pull しておけば、環境変数の設定なしにそのまま動かせる。

## クイックスタート

### 方法1: インメモリモード（コードでの登録）

サンプルを直接実行する方法。DevUIのディレクトリ探索機能を使わず、コード上でエージェントとワークフローを登録するやり方を示す。

```bash
uv run python 02-agents/devui/in_memory_mode.py
```

ブラウザで http://localhost:8090 が開き、Ollamaベースのエージェント2つとシンプルなテキスト変換ワークフローが確認できる。

### 方法2: ディレクトリ探索

フォルダ単位のランチャーを実行し、このフォルダに対してディレクトリ探索モードでDevUIを起動する。

```bash
uv run python 02-agents/devui/main.py
```

http://localhost:8080 でサーバーが起動し、発見可能な全エージェント・ワークフローが利用できる。

### 方法3: `devui` CLIによるディレクトリ探索

CLIを直接使いたい場合は、このフォルダから起動することもできる。

```bash
cd 02-agents/devui
devui .
```

## サンプルの構成

DevUIは、`agent` または `workflow` をエクスポートするPythonパッケージからサンプルを発見する。

典型的なエージェントの構成：

```
agent_name/
├── __init__.py      # agent = ... をエクスポートすること
└── agent.py         # エージェントの実装
```

典型的なワークフローの構成：

```
workflow_name/
├── __init__.py      # workflow = ... をエクスポートすること
├── workflow.py      # ワークフローの実装
└── workflow.yaml    # 宣言的定義（任意）
```

## 用意されているサンプル

### エージェント

| サンプル | 内容 |
| ------ | -------------------- |
| [**agent_weather/**](agent_weather/) | Ollamaベースの天気エージェント。チャットミドルウェア、関数ミドルウェア、ツール呼び出し、承認必須ツールと自動承認ツールの併用を示す。 |

### ワークフロー

| サンプル | 内容 |
| ------ | -------------------- |
| [**workflow_declarative/**](workflow_declarative/) | `WorkflowFactory` で読み込むYAML定義のワークフロー。年齢による入れ子分岐を持ち、モデルクライアントのコードは一切ない。 |
| [**workflow_with_agents/**](workflow_with_agents/) | エージェントをexecutorとして使うコンテンツレビューワークフロー。構造化された審査結果に基づいてルーティングする（`Writer -> Reviewer -> Editor/Publisher -> Summarizer`）。 |
| [**workflow_spam/**](workflow_spam/) | 人間承認（human-in-the-loop）を組み込んだ多段階スパム検知ワークフロー。スパム／正当メッセージで分岐し、最終レポートを生成する。モデルクライアントは使わず、純粋なワークフローロジックのみ。 |
| [**workflow_fanout/**](workflow_fanout/) | 並列バリデーション・複数の変換・QA・集約・失敗デモ用トグルを持つ、大きめのファンアウト/ファンインデータ処理ワークフロー。モデルクライアントは使わず、純粋なワークフローロジックのみ。 |

### 単体サンプル

| サンプル | 内容 |
| ------ | -------------------- |
| [**in_memory_mode.py**](in_memory_mode.py) | Ollamaベースのエージェント2つとシンプルなワークフローを、ディレクトリ探索なしで1ファイルの中で `serve()` にまとめて渡す。 |

## 自分のエージェントをDevUIに登録する

自分のエージェントをDevUIから発見できるようにするには：

1. エージェント用のフォルダを作る
2. `agent` または `workflow` をエクスポートする `__init__.py` を追加する

例：

```python
# my_agent/__init__.py
from agent_framework import Agent
from agent_framework.ollama import OllamaChatClient

agent = Agent(
    name="MyAgent",
    description="My custom agent",
    client=OllamaChatClient(host="http://localhost:11434", model="gemma4:12b-it-qat"),
    # ... 各種設定
)
```

そして実行：

```bash
devui /path/to/my/agents/folder
```

## API の使い方

DevUIはOpenAI互換のエンドポイントを公開している。

```bash
curl -X POST http://localhost:8080/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agent-framework",
    "input": "What is the weather in Seattle?",
    "extra_body": {"entity_id": "agent_directory_weather-agent_<uuid>"}
  }'
```

利用可能なエンティティの一覧取得：

```bash
curl http://localhost:8080/v1/entities
```

## トラブルシューティング

**インポートエラー**: devuiパッケージがインストールされているか確認する。

```bash
uv add agent-framework-devui --prerelease=allow
```

**ポートの衝突**: DevUIはデフォルトでポート8080（ディレクトリモード）と8090（インメモリモード）を使う。他のサービスを止めるか、別のポートを指定する。

```bash
devui --port 8888
```
