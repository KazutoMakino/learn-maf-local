# Agent Skills サンプル

これらのサンプルは、**Agent Skills**（エージェントの能力を拡張する、instructions・resources・scriptsをまとめたモジュール型パッケージ）の使い方を示す。Skills は [Agent Skills specification](https://agentskills.io/) に準拠し、トークン消費を抑えるためプログレッシブディスクロージャー（段階的開示）を採用している。

## 学習の進め方

まずファイルベース／コード定義のスキルから始め、それらを組み合わせたり承認ワークフローを追加したりする方法へ進むとよい。

| サンプル | 説明 |
|--------|-------------|
| [**file_based_skill**](file_based_skill/) | ディスク上の `SKILL.md` ファイルとしてスキルを定義し、参考資料と実行スクリプトを持たせる。unit-converter スキルを使用。 |
| [**code_defined_skill**](code_defined_skill/) | `Skill`、`@skill.resource`、`@skill.script` デコレータを使い、Pythonコードだけでスキルを定義する。コード定義の unit-converter スキルを使用。 |
| [**class_based_skill**](class_based_skill/) | `ClassSkill` と `@ClassSkill.resource` / `@ClassSkill.script` デコレータを使い、自動発見可能なPythonクラスとしてスキルを定義する。クラスベースの unit-converter スキルを使用。 |
| [**mixed_skills**](mixed_skills/) | コード定義・クラスベース・ファイルベースのスキルを1つのエージェントに混在させる。コード定義の volume-converter、クラスベースの temperature-converter、ファイルベースの unit-converter を使用。 |
| [**mcp_based_skill**](mcp_based_skill/) | `MCPSkillsSource` 経由で [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 越しに配信されるスキルを発見する。SEP-2640 規約に従って `skill://...` リソースを公開するリモートMCPサーバーに接続する。 |
| [**script_approval**](script_approval/) | スキルスクリプトの実行前に人間の承認（human-in-the-loop）を必須にする |

## 主要な概念

### プログレッシブディスクロージャー（段階的開示）

スキルはトークン消費を最小化するため、3段階のやり取りモデルを採用している。

1. **Advertise（広告）** — スキル名と説明（各約100トークン）がシステムプロンプトに注入される
2. **Load（読み込み）** — `load_skill` ツールで、必要になったときに完全な instructions がオンデマンドで読み込まれる
3. **Access（アクセス）** — resources は `read_skill_resource` で読み、scripts は `run_skill_script` で実行する

### ファイルベース vs コード定義 vs クラスベース

| 観点 | ファイルベース | コード定義 | クラスベース |
|--------|-----------|--------------|-------------|
| 定義方法 | ディスク上の `SKILL.md` ファイル | Pythonの `Skill` インスタンス | `ClassSkill` を継承したクラス |
| リソース | `references/` / `assets/` ディレクトリ内の静的ファイル | `@skill.resource` デコレータ付きの呼び出し可能な関数 | `@ClassSkill.resource` デコレータ（自動発見） |
| スクリプト | `scripts/` ディレクトリ内のPythonファイル（サブプロセスで実行） | `@skill.script` デコレータ付きの関数（インプロセス実行） | `@ClassSkill.script` デコレータ（インプロセス実行） |
| 発見方法 | `skill_paths` パラメータで自動 | `skills` パラメータで明示的に指定 | `skills` パラメータで明示的に指定 |
| 動的コンテンツ | 不可（静的ファイルのみ） | 可能（関数が実行時にコンテンツを生成できる） | 可能（関数が実行時にコンテンツを生成できる） |
| 共有パターン | スキルディレクトリをコピー | インラインまたは共有インスタンス | 共有ライブラリ/PyPIにパッケージ化 |

3種類すべてを1つの `SkillsProvider` に混在させることも可能 — [mixed_skills](mixed_skills/) サンプルを参照。

### スクリプトの実行

スキルには実行可能なスクリプトを含められる。実行方法は定義方法によって異なる。

| | コード定義スクリプト | ファイルベーススクリプト |
|---|---|---|
| **定義方法** | `@skill.script` デコレータ | `scripts/` ディレクトリ内の `.py` ファイル |
| **実行方式** | インプロセス（直接の関数呼び出し） | `script_runner` に委譲 |
| **`script_runner` は必要か** | 不要 — 自動的にインプロセスで実行される | **必要** |

`SkillsProvider` の `script_runner` パラメータは**ファイルベース**スクリプトにのみ適用される。コード定義スクリプトはこの設定に関わらず常にインプロセスで実行される。サブプロセスランナーを使う `SkillScriptRunner` の例は [file_based_skill](file_based_skill/) を、ランナー不要なインプロセススクリプトの例は [code_defined_skill](code_defined_skill/) を参照。

## 事前準備

本リポジトリでは全サンプルが `OllamaChatClient` を使うよう書き換えられている。Ollama をローカルで起動し、
`gemma4:12b-it-qat` を pull しておけばよい（環境変数の設定は不要）。

`mcp_based_skill` サンプルのみ、スキルを配信するリモート MCP サーバーが別途必要で、
`MCP_SKILLS_SERVER_URL` 環境変数でそのエンドポイントを指定する。

## 実験的機能の警告を抑制する

これらのサンプルで使う Agent Skills API はまだ実験的機能。各サンプルの import 付近には、
コメントアウトされた短い `warnings.filterwarnings(...)` の記述がある。実験的APIを使う前に
Skills の警告を抑制したい場合は、コメントを外すこと。
