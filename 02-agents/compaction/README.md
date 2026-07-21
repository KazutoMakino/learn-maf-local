# コンテキスト圧縮（Compaction）サンプル

このフォルダは、ADR-0019 で導入されたコンテキスト圧縮パターンを示す。

## ファイル一覧

- `basics.py` — ローカルのメッセージリストを作り、組み込みの各戦略を1つずつ適用する。
- `advanced.py` — `TokenBudgetComposedStrategy` で複数の戦略を組み合わせる。
- `agent_client_overrides.py` — クライアントのデフォルト値、エージェントレベルの上書き、実行単位（per-run）の上書きを示す。
- `custom.py` — `CompactionStrategy` プロトコルを実装したカスタム戦略を定義する。
- `tiktoken_tokenizer.py` — `tiktoken` を使った `TokenizerProtocol` の実装例。
- `compaction_provider.py` — `CompactionProvider` をエージェント・`InMemoryHistoryProvider` と組み合わせて使う。

`basics.py`, `advanced.py`, `agent_client_overrides.py`, `custom.py`, `tiktoken_tokenizer.py` はチャットクライアントを
一切使わない（ローカルのメッセージリストのみを操作する）ロジックのサンプルなので、Ollama の起動は不要。
`compaction_provider.py` のみ `OllamaChatClient` を使うので、Ollama をローカルで起動し `gemma4:12b-it-qat` を
pull しておくこと。

```bash
uv run python 02-agents/compaction/basics.py
uv run python 02-agents/compaction/advanced.py
uv run python 02-agents/compaction/agent_client_overrides.py
uv run python 02-agents/compaction/custom.py
uv run python 02-agents/compaction/tiktoken_tokenizer.py
uv run python 02-agents/compaction/compaction_provider.py
```
