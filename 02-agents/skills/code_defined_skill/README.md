# コード定義の Agent Skills

このサンプルは、ディスク上に `SKILL.md` ファイルを置かずに **Agent Skills** をPythonコードだけで作る方法を示す。unit-converter スキルで3通りのアプローチを紹介する。

## 内容

1. **静的リソース** — `Skill` を構築する際に `resources` パラメータでインラインコンテンツを渡す
2. **動的リソース** — `@skill.resource` デコレータで、実行時に計算したコンテンツを返す呼び出し可能な関数を紐づける
3. **動的スクリプト** — `@skill.script` デコレータで呼び出し可能なスクリプトを紐づける（factor パラメータ1つによる単位変換）

これら3つは、ファイルベースのスキルと1つの `SkillsProvider` に混在させることもできる。

## プロジェクト構成

```
code_defined_skill/
├── code_defined_skill.py
└── README.md
```

## サンプルの実行

### 事前準備
- Ollama をローカルで起動し、`gemma4:12b-it-qat` を pull しておく

### 実行

```bash
uv run python 02-agents/skills/code_defined_skill/code_defined_skill.py
```

## 参考リンク

- [Agent Skills Specification](https://agentskills.io/)
- [File-Based Skills サンプル](../file_based_skill/)
- [Mixed Skills サンプル](../mixed_skills/)
