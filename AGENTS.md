# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## リポジトリの目的

Microsoft Agent Framework（以下 MAF）を、Azure のクラウドサービスやクラウド LLM に一切課金せず、**完全ローカル環境（Ollama + CPU 推論）** で動かしながら理解するためのハンズオンリポジトリです。

- 公式が Python 向けに展開しているサンプル（`microsoft/agent-framework` の `python/samples/`）を基に、Azure Foundry / Azure OpenAI などクラウド依存の部分をすべて `OllamaChatClient`（`agent_framework.ollama`）に書き換えてリメイクしていく。
- 学んだ内容は Qiita の連載記事として発信する（既存の投稿は README.md を参照）。

## 対話・コーディング規約（最重要）

- **思考過程（thinking）、私（ユーザー）との対話、コード中のコメントは全て日本語で書くこと。** 変数名・関数名などの識別子は英語のままでよい。
- 公式サンプルにある `# <tag>` 形式の XML風コメント（ドキュメント埋め込み用）は削除してよい。

## セットアップと実行

パッケージ管理は `uv` を使用（`.python-version` は 3.12）。仮想環境の手動作成・activate は不要。

```bash
# 依存関係の同期（.venv を自動作成）
uv sync

# Ollama が起動していることを確認（別途 `ollama pull <model>` が必要）
curl http://localhost:11434

# サンプルの実行（リポジトリ直下から）
uv run python 01-get-started/01_hello_agent.py
```

## Lint / Format / 型チェック

```bash
uv run ruff check .
uv run ruff format .
uv run mypy .

# pre-commit（ruff, ruff-format, mypy を一括実行）
uv run pre-commit run --all-files
```

- `ruff` は isort/pyflakes/pycodestyle/pydocstyle(google 規約) を有効化、line-length 120。
- `mypy` は `disallow_untyped_defs = true` だが `strict = false`。関数には型注釈を付けること。
- 自動テスト（pytest 等）はこのリポジトリには存在しない。動作確認は該当スクリプトを `uv run python <path>` で直接実行して行う。

## リポジトリ構成と重要な前提

ディレクトリ番号（`01-get-started`, `02-agents`, `03-workflows`, `04-hosting`, `05-end-to-end`）は、公式リポジトリの `python/samples/` 配下の構成にそのまま対応している。

- **`.org/agent-framework/`**（`.gitignore` 対象・非追跡）: 公式 `microsoft/agent-framework` リポジトリのローカルクローン。リメイク対象の原文サンプルを参照する際は、対応する `.org/agent-framework/python/samples/<同名パス>` を読むこと。
- **`01-get-started/`**（git 追跡対象）: Ollama 版へのリメイクが完了し、コミット済みのディレクトリ。現状ここが本リポジトリの実質的な成果物。
- **`02-agents/`, `03-workflows/`, `04-hosting/`, `05-end-to-end/`**（`.gitignore` により丸ごと非追跡）: 公式サンプルを取り込んで試行錯誤するための作業用ディレクトリ。ここにあるファイルは編集されていてもコミットされない前提のサンドボックスであり、リメイクが一段落した内容を正式に成果物へ反映する場合は、ユーザーに確認の上で `.gitignore` の該当行を外す・別ディレクトリへ移す等の判断が必要。

### リメイクのパターン

公式サンプルとの差分は基本的に以下の書き換えのみで、ロジックやサンプルの構成は変えない。

```python
# 変更前（公式サンプル、例: Foundry / Azure）
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

async with (
    AzureCliCredential() as credential,
    Agent(client=FoundryChatClient(credential=credential), ...) as agent,
):
    ...

# 変更後（本リポジトリ、Ollama）
from agent_framework.ollama import OllamaChatClient

async with Agent(
    client=OllamaChatClient(host="http://localhost:11434", model="gemma4:12b-it-qat", additional_properties=120.0),
    ...
) as agent:
    ...
```

- 環境変数（`FOUNDRY_PROJECT_ENDPOINT` 等）による設定切り替えは行わず、`OllamaChatClient` の引数に直接ホストとモデル名を書く。`load_dotenv()` や `azure.identity` の import ごと削除する。
- `AzureCliCredential` による認証が絡む `async with (...)` の入れ子は、認証処理ごと削除して1段浅くする（上記参照）。
- `default_options={"store": False}` のような、Foundry/OpenAI 固有でOllamaに対応する概念がないオプションは削除する（無理に移植しない）。
- CPU 推論はレスポンスが遅くなりがちなので、`OllamaChatClient(...)` には `additional_properties=120.0` を付けてタイムアウトを伸ばすのが基本形。

#### モデル選定

標準モデルは `gemma4:12b-it-qat`（`tools` / `thinking` / `vision` / `audio` の capability を持つ）。**公式サンプルのコメントにある「マルチモーダルは gemma3系、推論は qwen3系を試すとよい」といった記述は、移植元（Foundry/OpenAI版）を前提にしたものなので鵜呑みにしない。** 別モデルの追加が必要かどうかは、必ず以下で実際の capability を確認してから判断する。

```bash
curl http://localhost:11434/api/show -d '{"name":"gemma4:12b-it-qat"}'
# capabilities: ["completion", "vision", "audio", "tools", "thinking"] などが返る
```

対応済みの capability であれば、モデルを増やさず `gemma4:12b-it-qat` に統一する（pull するモデルが1つで済み、READMEの記載もシンプルになる）。

### 大規模なサンプル群をリメイクする際の手順（`02-agents/` 以降で採用）

`02-agents/` 以降のディレクトリは、公式リポジトリの構成をそのままコピーすると数百ファイル規模になり、その大半が
Azure Foundry / OpenAI / Amazon Bedrock / Anthropic / Cosmos DB / Redis など外部サービス前提で書かれている。
全部を機械的に変換するのではなく、以下の手順でスコープを絞ってから着手する。

1. **全体を俯瞰し、クラウド依存の度合いで仕分ける** — チャットクライアントを使わない純粋ロジックのサンプル（変更不要）、
   Ollamaで完結できるもの（変換対象）、外部サービス必須のもの（対象外）に分類する。
2. **スコープをユーザーに確認する** — どのテーマ／ディレクトリを対象にするか、対象外はどう扱うか（削除してよいか）を
   `AskUserQuestion` 等で確認してから着手する。目分量で全部やらない。
3. **対象外のファイルは残さず削除する** — 中途半端に変換されていないクラウド専用サンプルを残すと、後から見て
   どれが動くサンプルか分からなくなる。ユーザーの許可を得たら `rm` で丸ごと削除する。
4. **コード変換とREADME翻訳は同じパスで行う** — 各ディレクトリの `README.md` も、コードと同時に日本語化・実態に合わせて
   更新する（後回しにすると抜け漏れが発生する）。削除したディレクトリ・ファイルへの相互参照リンクも合わせて修正する。
5. **最後に lint / コンパイルチェックで一括検証する** — `uv run ruff check <dir>` と
   `find <dir> -name "*.py" -print0 | xargs -0 -n1 uv run python -m py_compile` で機械的に確認する
   （`02-agents` のようなディレクトリ名は mypy がパッケージとして解釈できず失敗することがあるため、mypy は個別ファイル
   指定か対象外として扱う）。

## Qiita 連載記事

- [Vol.1 導入／01-get-started編](https://qiita.com/KazutoMakino/items/b7664ec375d6c9014350)
- https://qiita.com/KazutoMakino/items/b7b10c53b0d62e139ecb
- https://qiita.com/KazutoMakino/items/cfd2374a6c9edd0d6605

新しいディレクトリのリメイクが完了した際は、対応する Qiita 記事の投稿・README.md へのリンク追記も作業範囲に含まれ得る（ユーザーからの指示に従う）。

記事ドラフトは `docs/` 配下に `.md` ファイルとして作成する（コピペしやすいように）。文体・構成、および
「セッション内の対話がそのまま記事に漏れていないか」「未検証の内容を体験談として書いていないか」といった
執筆時の必須チェックは **[docs/qiita-writing-guide.md](docs/qiita-writing-guide.md) に従うこと**。

`docs/` は `.gitignore` で意図的に除外している。GitHub上には公開せず、Qiita記事のドラフトを保存しておくための
個人用ワークスペースという位置づけなので、`.gitignore` からこの行を外す必要はない。
