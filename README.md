# learn-maf-local

Microsoft Agent Framework (MAF) を、外部APIへの課金を一切気にせず、**完全ローカル環境（CPU推論）** で動かしながら学ぶためのハンズオンリポジトリです。

公式のサンプル構成をベースに、クラウド（OpenAI等）依存の部分をすべてローカルLLM（Ollama）仕様に書き換えて検証しています。

🔗 **連載解説記事（Qiita）:**
- [【脱・従量課金】CPUローカルLLM×Microsoft Agent Frameworkで始める次世代マルチエージェント開発 (導入／01-get-started編)]()

---

## 🚀 特徴
- **脱・従量課金 / 完全無料**: クラウドAPIを一切叩かず、PC内のローカルLLMのみで動作します。
- **圧倒的にセキュア**: 物理隔離されたローカル環境で完結するため、機密データの漏洩リスクがありません。
- **軽量・CPU動作**: 高価な外部GPU（dGPU）がなくても、潤沢なメインメモリ（推奨32GB）があれば一般的なノートPCで十分に実用動作します。

---

## 🛠️ 動作確認環境
- **OS**: Arch Linux (Windows / Mac / WSL2 等でも動作可能)
- **パッケージマネージャ**: `uv`
- **ローカルLLMサーバー**: `Ollama`
- **使用モデル**: `gemma4:12b` (お好みのモデルに差し替え可能)

---

## 📦 クイックスタート

### 1. Ollamaの準備
事前にOllamaがインストールされ、バックグラウンドで起動していることを確認してください。
その後、検証に使用するモデルをpullします。

```bash
ollama pull gemma4:12b
```

Ollamaが正常に常駐しているか（ http://localhost:11434 が応答するか）確認しておきます。

```bash
curl http://localhost:11434
# "Ollama is running" と返ってくればOK
```

### 2. リポジトリのクローンと環境構築
本リポジトリではPythonのパッケージ管理に uv を使用しています。手動での仮想環境の作成やアクティベートは不要です。

```bash
# クローン
git clone [https://github.com/KazutoMakino/learn-maf-local.git](https://github.com/KazutoMakino/learn-maf-local.git)
cd learn-maf-local

# 依存関係の同期（.venvの自動作成）
uv sync
```

### 3. サンプルの実行
```bash
# リポジトリ直下に居るとして、01-get-started/01_hello_agent.py を実行する例
uv run python 01-get-started/01_hello_agent.py

# 仮想環境に入って実行する場合は以下
source .venv/bin/activate
python 01-get-started/01_hello_agent.py
```

---

## 📝 ライセンス

[MIT License](./LICENSE)
