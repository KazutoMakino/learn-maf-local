# Ollama サンプル

Agent Framework でローカルの Ollama モデルを使う方法を示すサンプル集。

## 事前準備

1. **Ollama をインストール**: [ollama.com](https://ollama.com/) からダウンロードしてインストール
2. **Ollama を起動**: ローカルマシン上で Ollama が動作していることを確認
3. **モデルを pull**: `ollama pull gemma4:12b-it-qat`

`gemma4:12b-it-qat` は `tools` / `thinking` / `vision` の capability を備えているため、本ディレクトリの
全サンプル（ツール呼び出し・推論・マルチモーダル）をこの1モデルだけで動かせる。
モデルが対応している capability は `curl http://localhost:11434/api/show -d '{"name":"<model>"}'` で確認できる。

## 推奨アプローチ

Agent Framework で Ollama を使う推奨方法は、`agent-framework-ollama` パッケージのネイティブ `OllamaChatClient` を使うこと。推論（thinking）モードなど Ollama 固有機能をフルサポートする。

代わりに、ローカルの Ollama サーバーを指す `OpenAIChatClient` を使うこともできる。OpenAI クライアントのインターフェースに慣れている場合に有用。

## サンプル一覧

| ファイル | 説明 |
|------|-------------|
| [`ollama_agent_basic.py`](ollama_agent_basic.py) | ネイティブ Ollama Chat Client を使ったツール呼び出しの基本例。ストリーミング／非ストリーミング両方を示す。 |
| [`ollama_agent_reasoning.py`](ollama_agent_reasoning.py) | ネイティブ Ollama Chat Client の推論（reasoning/thinking）モードを有効化する例。 |
| [`ollama_chat_client.py`](ollama_chat_client.py) | Agent を介さず、ネイティブ Ollama Chat Client を直接使ってツール呼び出しを行う例。 |
| [`ollama_chat_multimodal.py`](ollama_chat_multimodal.py) | Ollama Chat Client でマルチモーダル（画像）入力を扱う例。 |
| [`ollama_with_openai_chat_client.py`](ollama_with_openai_chat_client.py) | OpenAI Chat Client をローカル Ollama サーバーに向けて使う代替アプローチ。 |

## 設定

本リポジトリの方針として、環境変数による切り替えは行わず、`OllamaChatClient`（または `OpenAIChatClient`）の引数に直接ホストとモデル名を指定する。ホスト・モデルを変更したい場合は各サンプルのコードを直接編集すること。
