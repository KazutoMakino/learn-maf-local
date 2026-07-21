# 会話・セッション管理サンプル

Agent Framework で会話履歴とセッション状態を管理する、さまざまなアプローチを示すサンプル集。

## サンプル一覧

| ファイル | 説明 |
|------|-------------|
| [`suspend_resume_session.py`](suspend_resume_session.py) | 会話セッションの中断・再開を、`Agent` を async context manager として使う方法と、通常の `Agent` インスタンスを使う方法の両方で示す。 |
| [`custom_history_provider.py`](custom_history_provider.py) | `HistoryProvider` を継承してカスタム履歴プロバイダを実装し、任意のストレージバックエンドに会話を永続化する。 |
| [`file_history_provider.py`](file_history_provider.py) | 実験的機能の `FileHistoryProvider` を `OllamaChatClient` と関数ツールで使い、ローカルの JSON Lines ファイルにツール呼び出しループ全体を記録する。 |
| [`file_history_provider_conversation_persistence.py`](file_history_provider_conversation_persistence.py) | `FileHistoryProvider` でツール駆動の天気会話を永続化し、保存された JSONL レコードを確認しながら別の都市について会話を続ける。 |

## 事前準備

全サンプルが `OllamaChatClient` を使うよう書き換えられている。Ollama をローカルで起動し、
`gemma4:12b-it-qat` を pull しておけばよい（環境変数の設定は不要）。

`file_history_provider.py` / `file_history_provider_conversation_persistence.py` は会話ログを
プレーンテキストの JSONL としてローカルディスクに書き出すので、信頼できるディレクトリを使うこと
（暗号化や機密情報の秘匿は行われない）。
