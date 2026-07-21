# Agent Framework Observability（可観測性）

これらのサンプルは、OpenTelemetry標準に基づき、Agent Framework の可観測性データを好きなAPM（Application Performance Management）バックエンドに送る方法を示す。

サンプルは [Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)、[Aspire Dashboard](https://learn.microsoft.com/en-us/dotnet/aspire/fundamentals/dashboard/overview?tabs=bash)、コンソールを対象としているが、OTLP互換のバックエンドであればどれでも動作する。

> **クイックスタート**: Azureのセットアップなしでローカル開発したい場合は、[Aspire Dashboard](https://learn.microsoft.com/en-us/dotnet/aspire/fundamentals/dashboard/standalone)（Docker上でローカル起動）や、[AI Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio) 組み込みのトレースモジュールを使うとよい。

> [Prometheus](https://prometheus.io/docs/introduction/overview/) など他のバックエンドにも対応している。全リストは [OpenTelemetry Python exporters](https://opentelemetry.io/docs/languages/python/exporters/) のページを参照。

詳細については以下のリソースを参照。

1. [Azure Monitor OpenTelemetry Exporter](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/monitor/azure-monitor-opentelemetry-exporter)
2. [Aspire Dashboard for Python Apps](https://learn.microsoft.com/en-us/dotnet/aspire/fundamentals/dashboard/standalone-for-python?tabs=flask%2Cwindows)
3. [AI Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
4. [Python Logging](https://docs.python.org/3/library/logging.html)
5. [Observability in Python](https://www.cncf.io/blog/2022/04/22/opentelemetry-and-python-a-complete-instrumentation-guide/)

## 何が得られるか

Agent Framework Python SDK は**ネイティブに計装（instrumented）**されており、エージェント／モデル呼び出しやツール実行を通じてログ・トレース・メトリクスを出力するので、AIアプリケーションのパフォーマンスを監視しトークン消費量を追跡できる。計装は OpenTelemetry の [Semantic Conventions for GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/) に従っており、ワークフローもエンドツーエンドの可視性のために独自のスパンを発行する。

可観測性のセットアップも簡単：`agent_framework.observability` モジュールの `configure_otel_providers()` を1回呼ぶだけで、トレース・ログ・メトリクスの各プロバイダが配線される。標準的なOpenTelemetry環境変数を読み取り、自動でエクスポーターを設定する。

### 可観測性を設定する5つのパターン

> 可観測性のセットアップは2つの部分に分かれる：(1) **計装（instrumentation）** — テレメトリを生成するコード、(2) **エクスポーター／プロバイダの設定** — そのテレメトリの送り先を決める部分。Agent Framework はネイティブに計装されており**デフォルトで有効**なので、通常は(2)だけを扱えばよい。

やり方は主に5通りある。

**1. 標準のOTel環境変数を使う（あらかじめ用意されている）**

最もシンプルな方法 — すべて環境変数で設定する。

```python
from agent_framework.observability import configure_otel_providers

# OTEL_EXPORTER_OTLP_* 環境変数を自動的に読み取る
configure_otel_providers()
```

コンソールへのエクスポートだけでよければ：

```python
from agent_framework.observability import configure_otel_providers

configure_otel_providers(enable_console_exporters=True)
# configure_otel_providers() をパラメータ付きで呼ぶ代わりに、
# 環境変数で ENABLE_CONSOLE_EXPORTERS=true を設定することも可能。
# フレームワークが自動的にそれを読み取り、コンソールエクスポーターを設定する。
```

これが、まず試すのに**推奨される方法**。

**2. カスタムエクスポーター**

より細かく制御したい場合は、エクスポーターを自分で構築して `configure_otel_providers()` に渡す。プロバイダの生成自体はフレームワークが引き続き行う。

```python
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.exporter import Compression
from agent_framework.observability import configure_otel_providers

# 個別設定を持つカスタムエクスポーターを作成
exporters = [
    OTLPSpanExporter(endpoint="http://localhost:4317", compression=Compression.Gzip),
    OTLPLogExporter(endpoint="http://localhost:4317"),
    OTLPMetricExporter(endpoint="http://localhost:4317"),
]

# 環境変数から設定されたエクスポーターと併用して追加される
configure_otel_providers(exporters=exporters)
```

**3. サードパーティ製のセットアップ**

多くのサードパーティ製OTelパッケージは、独自のセットアップヘルパーを提供している（例: Azure Monitor の `configure_azure_monitor()`）。Agent Framework の計装はデフォルトで有効なので、追加の配線なしにそれらを直接使える。機微なデータも取得したい場合は、`agent_framework.observability` の `enable_sensitive_telemetry()` を呼ぶ。

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from agent_framework.observability import create_resource, enable_sensitive_telemetry

# まず Azure Monitor を設定
configure_azure_monitor(
    connection_string="InstrumentationKey=...",
    resource=create_resource(),  # OTEL_SERVICE_NAME などを使用
    enable_live_metrics=True,
)

# 任意: 機微なデータの取得をオプトインする
enable_sensitive_telemetry()
```

Microsoft Foundry プロジェクトの場合は、プロジェクトから接続文字列を取得してすべて設定してくれる `client.configure_azure_monitor()` を使う（※本リポジトリの対象範囲外の機能）。

```python
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

client = FoundryChatClient(
    project_endpoint="https://your-project.services.ai.azure.com",
    model="gpt-4o",
    credential=AzureCliCredential(),
)

# プロジェクトの接続文字列で Azure Monitor を自動設定
await client.configure_azure_monitor(enable_sensitive_data=True)
```

[Langfuse](https://langfuse.com/integrations/frameworks/microsoft-agent-framework) の場合：

```python
# environment should be setup correctly, with langfuse urls and keys
from agent_framework.observability import enable_sensitive_telemetry
from langfuse import get_client

langfuse = get_client()

# 接続確認
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

# Agent Framework の計装はデフォルトで有効。
# 任意: 機微なデータの取得をオプトインする
enable_sensitive_telemetry()
```

[Comet Opik](https://www.comet.com/docs/opik/integrations/microsoft-agent-framework) の場合：

```python
import os

from agent_framework.observability import enable_sensitive_telemetry

# プロジェクト設定にある Opik の OTLP 設定を使う
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "<opik_otlp_endpoint>"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = "<opik_otlp_headers>"

# Agent Framework の計装はデフォルトで有効。
# 任意: 機微なデータの取得をオプトインする
enable_sensitive_telemetry()
```

**4. 手動セットアップ**

完全に制御したい場合は、プロバイダとエクスポーターを自分でセットアップする。トレース・ログ・メトリクスをすべてコンソールに送る完全な例は [advanced_manual_setup_console_output.py](./advanced_manual_setup_console_output.py) を参照。`agent_framework.observability` の `create_resource()` ヘルパーを使うと、環境変数（または妥当なデフォルト値）から適切なサービス名・バージョンを持つリソースを構築できるが、このサンプルでは使用していない。

**5. コード変更なしのプロバイダ／エクスポーター設定**

Agent Framework は OpenTelemetry で**ネイティブに計装**されているため、フレームワーク自体を自動計装する必要はない。ただし [`opentelemetry-instrument`](https://opentelemetry.io/docs/zero-code/python/) というCLIラッパーを使えば、プロセス起動時に環境変数（またはCLIフラグ）からグローバルなtracer/meterプロバイダとエクスポーターを設定できる。この場合、アプリケーションコード側で `configure_otel_providers()` を呼ぶ必要はなく、Agent Framework のネイティブなスパン・メトリクスがグローバルに設定されたパイプラインに拾われる。例は [advanced_zero_code.py](./advanced_zero_code.py) を参照。

### MCPのトレース伝播

アクティブなOpenTelemetryスパンコンテキストがある場合、Agent Framework は `tools/call` リクエストの `params._meta` フィールド経由で、トレースコンテキストをMCPサーバーへ自動的に伝播する。グローバルに設定されたOpenTelemetryプロパゲータ（デフォルトではW3C Trace Contextで、`traceparent` と `tracestate` を生成）を使うため、カスタムプロパゲータ（B3、Jaegerなど）にも対応する。これにより、[MCP `_meta` specification](https://modelcontextprotocol.io/specification/2025-11-25/basic#_meta) に準拠した、エージェント〜MCPサーバー間の分散トレーシングが可能になる。

**適用範囲:** 自動 `_meta` 注入は、エージェントプロセス自身が開くMCPセッション（`MCPStreamableHTTPTool`、`MCPStdioTool`、`MCPWebsocketTool`、あるいはクライアント側で開くその他の `MCPTool` サブクラス）にのみ適用される。`FoundryChatClient.get_mcp_tool(...)`、`OpenAIChatClient.get_mcp_tool(...)`、`AnthropicClient.get_mcp_tool(...)`、`GeminiChatClient.get_mcp_tool(...)` や、toolbox経由で取得したツール（例: `toolbox = await client.get_toolbox(...)` の後 `Agent(tools=toolbox.tools)`）といった、ホスト型／プロバイダ管理のMCPツール設定には**適用されない**。これらのケースでは `tools/call` メッセージがエージェントプロセスではなくプロバイダのサービスランタイムから発行されるため、その境界を越えて `traceparent`/`tracestate` を伝播するのはサービスランタイム側の責務となる。下流のMCPサーバーまでエンドツーエンドの分散トレーシングが必要な場合は、ホスト型コネクタではなくクライアント側で開くMCPトランスポートを使うこと。

## 設定

### 依存関係

Agent Framework のコアは **`opentelemetry-api`** にのみ依存している — この API パッケージだけで計装フック（スパン、メーター、ログレコード）がテレメトリを出力するのに十分であり、プロバイダが未設定の場合でも実行時に副作用は発生しない。

`configure_otel_providers()` でフレームワークにプロバイダ／エクスポーターをセットアップさせたい場合（あるいは `create_resource()` / `create_metric_views()` ヘルパーを使いたい場合）は、OpenTelemetry SDK も必要になる。

```bash
pip install opentelemetry-sdk
```

`opentelemetry-sdk` がない場合、これらのヘルパー関数はインストールを促す明確な `ImportError` を送出する。それ以外の日常的な計装は、他の何か（`azure-monitor-opentelemetry`、アプリケーションの起動処理、APMエージェントなど）がグローバルなOpenTelemetryプロバイダを設定していれば、SDKなしでも動作する。

エクスポーターは**デフォルトではインストールされない** — 必要なものだけを入れる。
- **Application Insights**: `azure-monitor-opentelemetry`
- **Aspire Dashboard や他のOTLP/gRPCバックエンド**: `opentelemetry-exporter-otlp-proto-grpc`
- **OTLP over HTTP**: `opentelemetry-exporter-otlp-proto-http`

他のバックエンドについては、それぞれのエクスポーターのドキュメントを参照。

### 環境変数

Agent Framework は以下の環境変数を読み取る。

| 変数 | デフォルト | 用途 |
|----------|---------|---------|
| `ENABLE_INSTRUMENTATION` | `true` | `false` にするとネイティブ計装を無効化する。sticky（固定）な挙動を持つプログラム的な代替方法は [計装の無効化](#計装の無効化) を参照。 |
| `ENABLE_SENSITIVE_DATA` | `false` | `true` にすると機微なデータ（プロンプト、レスポンスなど）を出力する。 |
| `ENABLE_CONSOLE_EXPORTERS` | `false` | `true` にするとコンソールエクスポーターを追加する。`configure_otel_providers()` でのみ使用される。 |
| `VS_CODE_EXTENSION_PORT` | 未設定 | [AI Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio#tracing) のトレース連携が使うポート。`configure_otel_providers()` でのみ使用される。 |

`agent_framework.observability` の `enable_sensitive_telemetry()` を呼べば、機微データ取得をプログラム的にオプトインすることもできる。

> **Note**: 機微なデータには、プロンプト・レスポンス・ツール引数が含まれる。本番環境ではユーザーやシステムの秘密情報が漏れる可能性があるため、開発・テスト環境でのみ有効にすること。

### 計装の無効化

Agent Framework のネイティブ計装をオフにする方法は2つあり、それぞれ**適用範囲が異なる**。

| 方法 | 適用範囲 | Sticky（固定）か | 後でフレームワークコードが `enable_instrumentation()` を呼ぶとどうなるか |
|----------|-------|---------|---------------------------------------------------------------------------|
| 環境変数 `ENABLE_INSTRUMENTATION=false` | 初期設定のみ | いいえ | 計装は**再び有効**に戻る。 |
| コードから `disable_instrumentation()` を呼ぶ | プロセス全体、sticky | はい | 計装は**無効のまま** — ユーザーの無効化の意図が優先される。 |

テレメトリをオフにして**そのままオフを維持したい**場合は、`disable_instrumentation()` を使う。

#### Sticky（固定）な挙動 — なぜ重要か

フレームワークの連携機能やサードパーティのライブラリは、自身のセットアップの一部として `enable_instrumentation()`、`enable_sensitive_telemetry()`、`configure_otel_providers()` を呼ぶことがある。例えば `FoundryChatClient.configure_azure_monitor()` は、Azure Monitor を配線した後に `enable_instrumentation()` を呼ぶ。通常はこれで問題ないが、**あなた自身**が明示的にオプトアウトしていた場合、それらの呼び出しによってテレメトリが黙って再有効化されるのは望ましくない。

`disable_instrumentation()` は、明示的に解除するまで有効であり続ける **sticky（固定）**なフラグを `OBSERVABILITY_SETTINGS` に立てることでこれを解決する。このフラグが立っている間：

1. `OBSERVABILITY_SETTINGS.enable_instrumentation` と `enable_sensitive_data` は、保存されている値に関わらず **`False` として読み取られる**。
2. `enable_instrumentation()` と `enable_sensitive_telemetry()` は**何もせず**（no-op）、infoレベルのメッセージをログ出力するだけになる。
3. `configure_otel_providers()` は引き続きプロバイダ／エクスポーター／viewを設定するが（後で強制的に有効化する際に使えるように）、計装自体は有効にしない。
4. `OBSERVABILITY_SETTINGS.enable_instrumentation = True` のような、どのコードからの直接的な属性書き込みも**黙って無視される**（多層防御）。
5. `OBSERVABILITY_SETTINGS.is_user_disabled` を確認する連携機能（`FoundryChatClient.configure_azure_monitor()`、`FoundryAgent.configure_azure_monitor()` など）は**セットアップ自体をスキップする**ため、グローバルな Azure Monitor プロバイダが不必要にインストールされることはない。

```python
from agent_framework.observability import disable_instrumentation

# この呼び出しの後、Agent Framework はテレメトリのオプトアウト意図を表明する。
# ライブラリやフレームワークのコードは、この意図を尊重し、計装を勝手に
# 再度有効化しない（enable_instrumentation()、enable_sensitive_telemetry()、
# OBSERVABILITY_SETTINGS の公開属性への書き込みなどを行わない）ことが
# 期待される。フレームワークは公開の enable 系パスを能動的に短絡させ、
# ユーザーの意図を優先する。force=True を渡すか、プライベート（`_`始まり）
# 属性を直接書き換えれば依然として回避可能だが、これらは契約外の
# エスケープハッチであり、連携機能がユーザーに代わって使うべきではない。
disable_instrumentation()
```

#### 無効化後に強制的に再有効化する

`disable_instrumentation()` の後に意図的にテレメトリを再有効化するには、2つの公開enableヘルパーのどちらかに `force=True` を渡す。これがstickyな無効化を解除する唯一の方法であり、ユーザーのオプトアウトは意図的なオプトインによってのみ覆せる。

```python
from agent_framework.observability import (
    disable_instrumentation,
    enable_instrumentation,
    enable_sensitive_telemetry,
)

disable_instrumentation()

# force=True なしでは、無効化がstickyな間は何もしない：
enable_instrumentation()              # infoログを出すだけで何もしない
enable_sensitive_telemetry()          # infoログを出すだけで何もしない

# force=True を付けると、stickyな無効化が解除され処理が進む：
enable_instrumentation(force=True)
# または
enable_sensitive_telemetry(force=True)

# 強制的に再有効化した後、再び disable_instrumentation() を呼べば
# stickyな無効化を再度セットできる。
```

#### 連携機能から無効化状態を確認する

副作用としてテレメトリのセットアップを行う連携機能（サードパーティのエクスポーターをプロビジョニングするなど）を書く場合は、読み取り専用の公開プロパティ `is_user_disabled` を確認し、立っている場合は早期リターンする。

```python
from agent_framework.observability import OBSERVABILITY_SETTINGS

if OBSERVABILITY_SETTINGS.is_user_disabled:
    logger.info(
        "Skipping telemetry setup because the user called disable_instrumentation()."
    )
    return
```

組み込みの `FoundryChatClient.configure_azure_monitor()` と `FoundryAgent.configure_azure_monitor()` もこれを行っている — そのため `disable_instrumentation()` を呼べば、これらのヘルパーによる Azure Monitor のグローバルプロバイダのインストールを確実に防げる。

#### `disable_instrumentation()` が**行わない**こと

- 無効化呼び出し以前に既にセットアップされていた OpenTelemetry プロバイダ、エクスポーター、実行中のスパンを解体することはない。Agent Framework のコードパスによる**今後の**取得だけをゲートする。
- Agent Framework の外側で配線されたサードパーティの計装（`azure-monitor-opentelemetry` のシステムメトリクスなど）からのテレメトリを止めることはない。必要であれば別途設定すること。
- プロセスをまたいで永続化しない。各Pythonプロセスは無効化フラグがクリアされた状態で開始するため、ある環境で常にテレメトリをオフにしたい場合は、プログラムからの呼び出しに加えて（またはその代わりに）環境変数 `ENABLE_INSTRUMENTATION=false` を設定すること。

#### `configure_otel_providers()` 用の環境変数

`configure_otel_providers()` 関数は、エクスポーターを設定するために**標準のOpenTelemetry環境変数**を自動的に読み取る。

**OTLP設定**（Aspire Dashboard、Jaegerなど向け）:
- `OTEL_EXPORTER_OTLP_ENDPOINT` - 全シグナル共通のベースエンドポイント（例: `http://localhost:4317`）
- `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` - トレース専用エンドポイント（ベースを上書き）
- `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` - メトリクス専用エンドポイント（ベースを上書き）
- `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` - ログ専用エンドポイント（ベースを上書き）
- `OTEL_EXPORTER_OTLP_PROTOCOL` - 使用するプロトコル（`grpc` または `http`、デフォルト: `grpc`）
- `OTEL_EXPORTER_OTLP_HEADERS` - 全シグナル共通のヘッダー（例: `key1=value1,key2=value2`）
- `OTEL_EXPORTER_OTLP_TRACES_HEADERS` - トレース専用ヘッダー（ベースを上書き）
- `OTEL_EXPORTER_OTLP_METRICS_HEADERS` - メトリクス専用ヘッダー（ベースを上書き）
- `OTEL_EXPORTER_OTLP_LOGS_HEADERS` - ログ専用ヘッダー（ベースを上書き）

**サービス識別**:
- `OTEL_SERVICE_NAME` - サービス名（デフォルト: `agent_framework`）
- `OTEL_SERVICE_VERSION` - サービスバージョン（デフォルト: パッケージバージョン）
- `OTEL_RESOURCE_ATTRIBUTES` - 追加のリソース属性（例: `key1=value1,key2=value2`）

> **Note**: これらは標準のOpenTelemetry環境変数。詳細は [OpenTelemetry spec](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/) を参照。

#### ロギング

標準のPythonロギング設定を使って、ログとテレメトリ出力を揃える。

```python
import logging

logging.basicConfig(
    format="[%(asctime)s - %(pathname)s:%(lineno)d - %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

どのログをエクスポートするか制御するには、ルートロガーのレベルを調整する — 他のロガーはデフォルトでこれを継承する。

```python
import logging

logging.getLogger().setLevel(logging.NOTSET)
```

## サンプル

このフォルダには、さまざまなシナリオでテレメトリを使う方法を示す複数のサンプルが入っている。

| サンプル | 説明 |
|--------|-------------|
| [configure_otel_providers_with_env_var.py](./configure_otel_providers_with_env_var.py) | **まずはここから**: 標準のOpenTelemetry環境変数（`OTEL_EXPORTER_OTLP_*`）でテレメトリを設定する。 |
| [configure_otel_providers_with_parameters.py](./configure_otel_providers_with_parameters.py) | 個別設定を持つカスタムエクスポーターを作成し、`configure_otel_providers()` に渡す。 |
| [agent_observability.py](./agent_observability.py) | ツール呼び出しを伴うエージェントアプリケーションのテレメトリ収集。 |
| [workflow_observability.py](./workflow_observability.py) | 複数のexecutorとメッセージパッシングを持つワークフローのテレメトリ収集。モデルクライアントは使わず、純粋なワークフローロジックのみ。 |
| [advanced_manual_setup_console_output.py](./advanced_manual_setup_console_output.py) | 上級編: エクスポーターとプロバイダをコンソール出力付きで手動セットアップする — 可観測性の内部動作を理解するのに役立つ。 |
| [advanced_zero_code.py](./advanced_zero_code.py) | 上級編: `opentelemetry-instrument` CLIラッパーを使った、コード変更なしのプロバイダ／エクスポーター設定。 |

### サンプルの実行

全サンプルが `OllamaChatClient` を使うよう書き換えられているので、Ollama をローカルで起動し
`gemma4:12b-it-qat` を pull しておけばモデル側の設定は不要。

OTel のエクスポート先を指定したい場合は、`OTEL_EXPORTER_OTLP_ENDPOINT` などの環境変数をシェルで
export するか、`configure_otel_providers(env_file_path=".env")` のように明示的に `.env` を渡す。
何も設定しない場合は `ENABLE_CONSOLE_EXPORTERS=true` を立てるとコンソール出力で確認できる。

```bash
uv run python 02-agents/observability/configure_otel_providers_with_env_var.py
```

> プロバイダを手動でセットアップした場合（Azure Monitorなど）も、Agent Framework の計装はデフォルトで有効なまま。機微なデータも取得したい場合は `enable_sensitive_telemetry()` を呼ぶこと。Agent Framework にエクスポーターとプロバイダを設定させたい場合は `configure_otel_providers(...)` を呼ぶこと。

> 各サンプルは Operation/Trace ID を出力するので、Application Insights や Aspire Dashboard でログ・トレースを絞り込む際に使える。

# 付録

## Azure Monitor クエリ

Azure Monitor でスパンの全体像を見るには、Logsセクションで以下のクエリを実行する。

```kusto
dependencies
| where operation_Id in (dependencies
    | project operation_Id, timestamp
    | order by timestamp desc
    | summarize operations = make_set(operation_Id), timestamp = max(timestamp) by operation_Id
    | order by timestamp desc
    | project operation_Id
    | take 2)
| evaluate bag_unpack(customDimensions)
| extend tool_call_id = tostring(["gen_ai.tool.call.id"])
| join kind=leftouter (customMetrics
    | extend tool_call_id = tostring(customDimensions['gen_ai.tool.call.id'])
    | where isnotempty(tool_call_id)
    | project tool_call_duration = value, tool_call_id)
    on tool_call_id
| project-keep timestamp, target, operation_Id, tool_call_duration, duration, gen_ai*
| order by timestamp asc
```

### Application Insights データを使った Grafana ダッシュボード

Application Insights のネイティブUIに加えて、Grafanaで同じテレメトリデータを可視化することもできる。すぐに使える2つの専用ダッシュボードが用意されている。

#### Agent Overview ダッシュボード
Azureポータルでダッシュボードを開く: <https://aka.ms/amg/dash/af-agent>
![Agent Overview dashboard](https://github.com/Azure/azure-managed-grafana/raw/main/samples/assets/grafana-af-agent.gif)

#### Workflow Overview ダッシュボード
Azureポータルでダッシュボードを開く: <https://aka.ms/amg/dash/af-workflow>
![Workflow Overview dashboard](https://github.com/Azure/azure-managed-grafana/raw/main/samples/assets/grafana-af-workflow.gif)

## 移行ガイド

計装は現在**デフォルトで有効**になっており（起動時に `enable_instrumentation()` を呼んでオプトインする必要はもうない）、機微なペイロードの取得をオプトインする方法は専用の関数として独立した。

以前のコードが以下のようになっていた場合：

```python
from agent_framework.observability import enable_instrumentation

enable_instrumentation(enable_sensitive_data=True)
```

以下のように置き換える：

```python
from agent_framework.observability import enable_sensitive_telemetry

enable_sensitive_telemetry()
```

`enable_sensitive_telemetry()` は、計装が有効であることを保証したうえで、機微イベントの取得も1回の呼び出しでオンにする。`enable_instrumentation()` は、機微データを有効にせずプログラム的に計装を強制有効化したい稀なケース（例えば `ENABLE_INSTRUMENTATION=false` を上書きする場合）向けに引き続き存在し、今では以前の `disable_instrumentation()` を解除する `force=True` も受け付ける — [計装の無効化](#計装の無効化) を参照。

> **Note**: 機微なデータには、プロンプト・レスポンス・ツール引数が含まれる。本番環境ではユーザーやシステムの秘密情報が漏れる可能性があるため、開発・テスト環境でのみ有効にすること。

## Aspire Dashboard

[Aspire Dashboard](https://learn.microsoft.com/en-us/dotnet/aspire/fundamentals/dashboard/standalone) は、Azureのセットアップなしで優れた体験でOpenTelemetryデータを閲覧できる、ローカルのテレメトリ閲覧ツール。

### Dockerで Aspire Dashboard をセットアップする

Aspire Dashboard をローカルで動かす一番簡単な方法はDockerを使うこと。

```bash
# Aspire Dashboard コンテナを pull して実行
docker run --rm -it -d \
    -p 18888:18888 \
    -p 4317:18889 \
    --name aspire-dashboard \
    mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

これで以下を伴ってダッシュボードが起動する。

- **Web UI**: <http://localhost:18888> で利用可能
- **OTLPエンドポイント**: アプリケーションがテレメトリデータを送信する `http://localhost:4317` で利用可能

### アプリケーションの設定

`.env` ファイルにOTLPエンドポイントを含めておく。

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

または、サンプル実行時に環境変数として設定する。

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 uv run python 02-agents/observability/configure_otel_providers_with_env_var.py
```

### テレメトリデータの閲覧

> テレメトリデータを受け取れるよう、ダッシュボードを起動しておくこと。

サンプルの実行が終わったら、ブラウザで <http://localhost:18888> を開いてテレメトリデータを確認する。ダッシュボードへの認証やトレース・ログ・メトリクスの探索方法は、[Aspire Dashboard exploration guide](https://learn.microsoft.com/en-us/dotnet/aspire/fundamentals/dashboard/explore) を参照。
