# crules

プロジェクトルール管理 CLI ツール

## 概要

crules は、プロジェクトごとに異なるルールとノートを効率的に管理・配置するための CLI ツールです。

## インストール方法

### Homebrew を使用したインストール

```bash
brew tap tirano-tirano/crules
brew install crules
```

### 開発環境でのインストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/crules.git
cd crules

# 仮想環境を作成して有効化
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# パッケージをインストール
pip install -e .
```

## 基本的な使い方

### プロジェクトの初期化

テンプレートからプロジェクトルールとノートを配置します。

```bash
# プロジェクトのルートディレクトリで実行
crules init
# または、テンプレートディレクトリ名を指定
crules init flutter
```

### 編集済みファイルの配置

編集したファイルを適切な位置に配置します。

```bash
# 編集済みファイルを配置
crules deploy
# または、テンプレートディレクトリ名を指定
crules deploy flutter
```

### 利用可能なルールの一覧表示

現在利用可能なルールの一覧を表示します。

```bash
# 利用可能なルールの一覧を表示
crules list
# または、テンプレートディレクトリ名を指定
crules list flutter
```

## ライセンス

MIT
