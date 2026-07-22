# ファイルベースの Agent Skills

このサンプルは、Microsoft Agent Framework で `SkillsProvider` を使い**ファイルベースの Agent Skills** を利用する方法を示す。ファイルベースのスキルはディスク上の `SKILL.md` ファイルから発見され、参考資料や実行スクリプトを含められる。

## Agent Skills とは

Agent Skills は、AIエージェントが専門的なタスクを実行できるようにする、instructions と resources のモジュール型パッケージ。[Agent Skills specification](https://agentskills.io/) に準拠し、プログレッシブディスクロージャーを実装している。

1. **Advertise（広告）**: 名前＋説明（スキルあたり約100トークン）でスキルが広告される
2. **Load（読み込み）**: `load_skill` ツールで完全な instructions をオンデマンドで読み込む
3. **Resources（リソース）**: `read_skill_resource` ツールで参考資料などのファイルを読み込む
4. **Scripts（スクリプト）**: `run_skill_script` ツールで実行可能なスクリプトを動かす

## 含まれるスキル

### unit-converter
[agentskills.io のガイドライン](https://agentskills.io/skill-creation/using-scripts)に従い、乗算係数を使って一般的な単位（miles↔km、pounds↔kg）を変換する。
- `references/CONVERSION_TABLES.md` — 対応する変換の一覧と係数
- `scripts/convert.py` — `--value` / `--factor` フラグ、JSON出力、`--help` に対応した実行スクリプト

## 主要コンポーネント

- **`SkillsProvider`** — ディレクトリ内の `SKILL.md` ファイルからスキルを発見し、エージェント用のツールを登録する
- **`subprocess_script_runner`** — スクリプトをローカルのPythonサブプロセスとして実行する `SkillScriptRunner` コールバックで、`run_skill_script` ツールを機能させる。引数のdictをCLIフラグに変換する（例: `{"value": 26.2, "factor": 1.60934}` → `--value 26.2 --factor 1.60934`）。[`../subprocess_script_runner.py`](../subprocess_script_runner.py) として各サンプルで共有されている。

## プロジェクト構成

```
file_based_skill/
├── file_based_skill.py
├── README.md
└── skills/
    └── unit-converter/
        ├── SKILL.md
        ├── references/
        │   └── CONVERSION_TABLES.md
        └── scripts/
            └── convert.py
```

## サンプルの実行

### 事前準備
- Ollama をローカルで起動し、`gemma4:12b-it-qat` を pull しておく

### 実行

```bash
uv run python 02-agents/skills/file_based_skill/file_based_skill.py
```

## 参考リンク

- [Agent Skills Specification](https://agentskills.io/)
- [Code-Defined Skills サンプル](../code_defined_skill/)
- [Mixed Skills サンプル](../mixed_skills/)
