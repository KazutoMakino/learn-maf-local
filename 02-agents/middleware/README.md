# ミドルウェアサンプル

このフォルダには、`Agent`・チャットクライアント・ツール・セッション・実行時コンテキストの挙動に焦点を当てたミドルウェアサンプルが入っている。

## ファイル一覧

| ファイル | 説明 |
|------|-------------|
| [`agent_and_run_level_middleware.py`](./agent_and_run_level_middleware.py) | エージェントレベルと実行（run）レベルのミドルウェアを組み合わせる例。 |
| [`chat_middleware.py`](./chat_middleware.py) | モデル呼び出しを観測・変更・上書きできる、クラスベース／関数ベースのチャットミドルウェア。 |
| [`class_based_middleware.py`](./class_based_middleware.py) | クラスベースのエージェント・関数ミドルウェア。 |
| [`decorator_middleware.py`](./decorator_middleware.py) | デコレータによるミドルウェア登録の例。 |
| [`exception_handling_with_middleware.py`](./exception_handling_with_middleware.py) | ミドルウェアで失敗を処理し、きれいに復帰させる例。 |
| [`function_based_middleware.py`](./function_based_middleware.py) | 関数ベースのエージェント・関数ミドルウェア。 |
| [`middleware_termination.py`](./middleware_termination.py) | ミドルウェアのパイプラインを途中で止める例。 |
| [`override_result_with_middleware.py`](./override_result_with_middleware.py) | ミドルウェアで通常・ストリーミング両方の結果を差し替え、最終レスポンスを後処理する例。 |
| [`runtime_context_delegation.py`](./runtime_context_delegation.py) | 実行時コンテキストのデータを引数として委譲する例。 |
| [`session_behavior_middleware.py`](./session_behavior_middleware.py) | セッションを伴う実行とミドルウェアがどう相互作用するかを示す例。 |
| [`shared_state_middleware.py`](./shared_state_middleware.py) | ミドルウェア呼び出しをまたいで可変な状態を共有する例。 |
| [`usage_tracking_middleware.py`](./usage_tracking_middleware.py) | 非ストリーミング／ストリーミングのツールループ実行それぞれで、呼び出しごとの使用量を追跡する単一のチャットミドルウェア関数。 |

## 実行方法

本リポジトリでは全サンプルが `OllamaChatClient` を使うよう書き換えられており、環境変数の設定は不要。
Ollama をローカルで起動し、`gemma4:12b-it-qat` を pull した状態で以下のように実行する。

```bash
uv run python 02-agents/middleware/usage_tracking_middleware.py
```

`usage_tracking_middleware.py` はツール呼び出しを強制するので、非ストリーミング／ストリーミング両方のモードで
各内部モデル呼び出しごとのミドルウェア出力を確認できる。
