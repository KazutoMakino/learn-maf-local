# Script Approval — スキルスクリプトの Human-in-the-Loop

このサンプルは、`SkillsProvider` の `require_script_approval=True` オプションを使い、スキルスクリプトの実行前に**人間の承認**を必須にする方法を示す。

## 仕組み

`require_script_approval=True` を設定すると、エージェントはスキルスクリプトを実行する前に一時停止し、承認リクエストを返す。

1. エージェントが `run_skill_script` を呼び出そうとする — 実行は一時停止する
2. `result.user_input_requests` に、関数名と引数を含む承認リクエストが入る
3. アプリケーション側が各リクエストを確認し、承認するか却下するかを決める
4. `request.to_function_approval_response(approved=True|False)` でレスポンスを作る
5. `agent.run(approval_response, session=session)` でレスポンスを送り返す
6. 承認されればスクリプトが実行され、却下されればエージェントはエラーを受け取る

## 主要コンポーネント

- **`require_script_approval=True`** — 全スクリプト実行を人間の承認によってゲートする
- **`result.user_input_requests`** — `agent.run()` 実行後、保留中の承認リクエストを保持する
- **`request.to_function_approval_response()`** — 承認または却下のレスポンスを作る

## サンプルの実行

### 事前準備
- Ollama をローカルで起動し、`gemma4:12b-it-qat` を pull しておく

### 実行

```bash
uv run python 02-agents/skills/script_approval/script_approval.py
```

## 参考リンク

- [File-Based Skills サンプル](../file_based_skill/)
- [Code-Defined Skills サンプル](../code_defined_skill/)
- [Mixed Skills サンプル](../mixed_skills/)
- [Agent Skills Specification](https://agentskills.io/)
