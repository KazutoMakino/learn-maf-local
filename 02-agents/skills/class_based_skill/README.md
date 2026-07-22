# クラスベースの Agent Skills

このサンプルは、`ClassSkill` を使って **Agent Skills を Python クラスとして定義する**方法を示す。

## 内容

- `ClassSkill` を継承したクラスとしてスキルを作る
- 名前・説明・instructions・resources・scripts を1つのクラスにまとめる
- `@ClassSkill.resource` デコレータでリソースを自動発見させる
- `@ClassSkill.script` デコレータでスクリプトを自動発見させる
- resources と scripts の遅延読み込みとキャッシュ
- クラスベースのスキルを `SkillsProvider` に登録する

## 含まれるスキル

### unit-converter（クラスベース）

一般的な単位を変換する `UnitConverterSkill` クラス。`class_based_skill.py` で定義。

- `conversion-table` — 変換係数の表を持つ静的リソース
- `convert` — `value × factor` の変換を行うスクリプト

## プロジェクト構成

```
class_based_skill/
├── class_based_skill.py
└── README.md
```

## サンプルの実行

### 事前準備

- Ollama をローカルで起動し、`gemma4:12b-it-qat` を pull しておく

### 実行

```bash
uv run python 02-agents/skills/class_based_skill/class_based_skill.py
```

### 出力例

```
Converting units with class-based skills
------------------------------------------------------------
Agent: Here are your conversions:

1. **26.2 miles → 42.16 km** (a marathon distance)
2. **75 kg → 165.35 lbs**
```

## 参考リンク

- [Agent Skills Specification](https://agentskills.io/)
- [Code-Defined Skills サンプル](../code_defined_skill/)
- [Mixed Skills サンプル](../mixed_skills/)
