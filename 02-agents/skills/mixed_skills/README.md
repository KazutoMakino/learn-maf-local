# Mixed Skills — コード・クラス・ファイルのスキルを混在させる

このサンプルは、`SkillsProvider` を使って**コード定義スキル**・**クラスベーススキル**・**ファイルベーススキル**を1つのエージェントに組み合わせる方法を示す。

## 概念

| 概念 | 説明 |
|---------|-------------|
| **コードスキル** | `@skill.script` デコレータでインプロセスの呼び出し可能関数を、`@skill.resource` で動的コンテンツを持たせた、Pythonで作る `Skill` |
| **クラススキル** | instructions・resources・scripts をまとめた、`ClassSkill` を継承する自己完結型のスキルクラス |
| **ファイルスキル** | ディスク上の `SKILL.md` ファイルから発見される、参考資料と実行スクリプトを持つスキル |
| **`script_runner`** | `SkillScriptRunner` プロトコルを満たす呼び出し可能オブジェクト（同期・非同期どちらも可）— ファイルスキルがスクリプトを持つ場合に必須 |
| **`SkillsProvider`** | コード定義・クラスベース・ファイルベースのスキルを1つのプロバイダにまとめて登録する |

## このサンプルに含まれるスキル

### volume-converter（コードスキル）

デコレータを使い、Pythonコードだけで定義：

- **`@skill.resource`** — `conversion-table`: ガロン↔リットルの変換係数
- **`@skill.script`** — `convert`: 乗算係数で値を変換する

コードスクリプトは**インプロセス**で実行される — サブプロセスや外部ランナーは不要。

### temperature-converter（クラススキル）

`ClassSkill` を継承した `TemperatureConverterSkill` クラスとして定義：

- **`@ClassSkill.resource`** — `temperature-conversion-formulas`: °F↔°C↔K の変換式
- **`@ClassSkill.script`** — `convert-temperature`: 温度スケール間を変換する

クラスベースのスクリプトも**インプロセス**で実行される — サブプロセスや外部ランナーは不要。

### unit-converter（ファイルスキル）

`skills/unit-converter/SKILL.md` から発見される：

- **参考資料**: `references/CONVERSION_TABLES.md` — 対応する単位変換とその係数
- **スクリプト**: `scripts/convert.py` — 乗算係数で値を変換する（例: マイル→キロメートル）

ファイルスクリプトは `script_runner` コールバック経由で**ローカルのPythonサブプロセス**として実行される。

## 仕組み

```
┌─────────────────────────────────────────────────────────────┐
│  SkillsProvider(                                            │
│    DeduplicatingSkillsSource(                               │
│      AggregatingSkillsSource([                              │
│        FileSkillsSource("./skills",       # ファイルスキル   │
│            script_runner=runner),                            │
│        InMemorySkillsSource([                               │
│            volume_skill,                  # コードスキル     │
│            temp_converter,                # クラススキル     │
│        ]),                                                  │
│      ])                                                     │
│    )                                                        │
│  )                                                          │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  script_runner(skill, script, args)                          │
│                                                             │
│  • コードスクリプト (@skill.script) → インプロセス呼び出し   │
│  • クラススクリプト (@ClassSkill.script) → インプロセス呼び出し │
│  • ファイルスクリプト (scripts/*.py) → コールバック関数経由の │
│    サブプロセス                                              │
└─────────────────────────────────────────────────────────────┘
```

## 事前準備

Ollama をローカルで起動し、`gemma4:12b-it-qat` を pull しておく。

## サンプルの実行

```bash
uv run python 02-agents/skills/mixed_skills/mixed_skills.py
```

## ディレクトリ構成

```
mixed_skills/
├── mixed_skills.py                # メインサンプル — コード＋ファイルスキルを結線する
├── README.md
└── skills/
    └── unit-converter/            # ファイルベースのスキル（SKILL.md から発見される）
        ├── SKILL.md
        ├── references/
        │   └── CONVERSION_TABLES.md
        └── scripts/
            └── convert.py
```

## 参考リンク

- [File-Based Skills サンプル](../file_based_skill/)
- [Code-Defined Skills サンプル](../code_defined_skill/)
- [Script Approval サンプル](../script_approval/)
- [Agent Skills Specification](https://agentskills.io/)
