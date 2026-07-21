# Skill Filtering — FilteringSkillsSource

このサンプルは、`FilteringSkillsSource` を使って述語（predicate）を適用し、エージェントに見せるファイルベースのスキルを制御する方法を示す。

## 概念

| 概念 | 説明 |
|---------|-------------|
| **`FileSkillsSource`** | ディスク上の `SKILL.md` ファイルからスキルを発見する |
| **`FilteringSkillsSource`** | ソースをラップし、述語を適用してスキルを含めたり除外したりする |
| **`DeduplicatingSkillsSource`** | 重複するスキル名を取り除く（最初のものが優先される） |

## このサンプルに含まれるスキル

### volume-converter（残る）

`scripts/convert.py` でガロンとリットルを変換する。

### length-converter（除外される）

マイル↔km、フィート↔メートルを変換する。フィルタの述語によって除外され、エージェントからは一切見えない。

## 仕組み

```
┌──────────────────────────────────────────────────────────┐
│  FileSkillsSource("./skills")                            │
│    発見: volume-converter, length-converter               │
└─────────────┬────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────┐
│  FilteringSkillsSource(predicate=...)                     │
│    残す: volume-converter                                 │
│    除外: length-converter                                 │
└─────────────┬────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────┐
│  DeduplicatingSkillsSource → SkillsProvider              │
└──────────────────────────────────────────────────────────┘
```

> **Note:** `FilteringSkillsSource` はファイルベース・インメモリ・カスタムなど、どのソースとも組み合わせられる。
> 1つのスキルしか必要ない場合は、フィルタリングせずに `FileSkillsSource` をそのスキルのディレクトリに直接向けるとよい。

## 事前準備

Ollama をローカルで起動し、`gemma4:12b-it-qat` を pull しておく。

## サンプルの実行

```bash
uv run python 02-agents/skills/skill_filtering/skill_filtering.py
```

## ディレクトリ構成

```
skill_filtering/
├── skill_filtering.py
├── README.md
└── skills/
    ├── volume-converter/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── convert.py
    └── length-converter/
        ├── SKILL.md
        └── scripts/
            └── convert.py
```

## 参考リンク

- [File-Based Skills サンプル](../file_based_skill/)
- [Mixed Skills サンプル](../mixed_skills/)
- [Code-Defined Skills サンプル](../code_defined_skill/)
- [Agent Skills Specification](https://agentskills.io/)
