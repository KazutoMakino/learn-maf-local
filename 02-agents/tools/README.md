# Tools

エージェントの関数ツールを定義・設定・制御する方法を示すサンプル群 —
基本的な宣言から、承認、呼び出し回数の制限、セッション注入、動的（プログレッシブ）なツール公開まで。

## 関数ツール

| ファイル | 内容 |
|------|--------------|
| [`function_tool_with_explicit_schema.py`](function_tool_with_explicit_schema.py) | 明示的なJSONスキーマでツールを定義する。 |
| [`function_tool_declaration_only.py`](function_tool_declaration_only.py) | 宣言のみのツール（ローカル実装を持たないスキーマ）。 |
| [`function_tool_with_kwargs.py`](function_tool_with_kwargs.py) | ツールに追加のキーワード引数を渡す。 |
| [`function_tool_from_dict_with_dependency_injection.py`](function_tool_from_dict_with_dependency_injection.py) | dictから定義したツールへの依存性注入。 |
| [`function_tool_with_session_injection.py`](function_tool_with_session_injection.py) | ツールにセッションを注入する。 |
| [`tool_in_class.py`](tool_in_class.py) | クラスのメソッドをツールとして使う。 |
| [`agent_as_tool_with_session_propagation.py`](agent_as_tool_with_session_propagation.py) | セッション伝播つきでエージェントをツールとして公開する。 |

## 承認と呼び出し制御

| ファイル | 内容 |
|------|--------------|
| [`function_tool_with_approval.py`](function_tool_with_approval.py) | ツール実行前に人間の承認を必須にする。 |
| [`function_tool_with_approval_and_sessions.py`](function_tool_with_approval_and_sessions.py) | ツール承認とセッションを組み合わせる。 |
| [`function_invocation_configuration.py`](function_invocation_configuration.py) | 関数呼び出しの設定（最大イテレーション回数など）を行う。 |
| [`control_total_tool_executions.py`](control_total_tool_executions.py) | ツールの実行回数を制限するあらゆる方法。 |
| [`function_tool_with_max_invocations.py`](function_tool_with_max_invocations.py) | ツールごとの呼び出し回数を制限する。 |
| [`function_tool_with_max_exceptions.py`](function_tool_with_max_exceptions.py) | ツールが送出できる例外の回数を制限する。 |
| [`function_tool_recover_from_failures.py`](function_tool_recover_from_failures.py) | エラーを返してエージェントがツールの失敗から復帰できるようにする。 |

## プログレッシブなツール公開（動的ロード）

| ファイル | 内容 |
|------|--------------|
| [`dynamic_tool_exposure.py`](dynamic_tool_exposure.py) | `FunctionInvocationContext` 経由で実行時にツールを追加する「ローダー」ツール。 |

モデルに最初から何百個ものツールを見せると、ツール選択精度が落ち、コンテキストが肥大化し、コストも上がる。
代わりに、少数のローダーツールから始めて、必要に応じてモデルに追加のツールを取得させるとよい。
ツール内では、注入される `ctx: FunctionInvocationContext` を通じてライブな `ctx.tools` リストと、
`ctx.add_tools(...)` / `ctx.remove_tools(...)` ヘルパーが使える。追加・削除したツールは、
関数呼び出しループの**次のイテレーション**から反映される。

> [!NOTE]
> プログレッシブなツール公開は、標準の関数呼び出しループに対して適用される。
> （このリポジトリでは、ハイパーバイザ/サンドボックスを要する CodeAct 系プロバイダ
> `agent-framework-monty` / `agent-framework-hyperlight` は対象外としている。）

## ローカルシェル

| パス | 内容 |
|------|--------------|
| [`local_shell_with_allowlist.py`](local_shell_with_allowlist.py) | 厳格なコマンド許可リストで制限した `LocalShellTool`。 |
| [`local_shell_with_environment_provider.py`](local_shell_with_environment_provider.py) | `ShellEnvironmentProvider` と組み合わせた `LocalShellTool`。 |
