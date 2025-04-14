# Crules パッケージ

## 概要

Crules は、プロジェクトルール管理のための Python パッケージです。このパッケージは、プロジェクトごとのルールとノートを効率的に管理・配置するための機能を提供します。

## インストール

### Homebrew を使用する場合（推奨）

1. tap の追加:

```bash
brew tap tirano-tirano/crules
```

2. crules のインストール:

```bash
brew install crules
```

または、1 つのコマンドで実行:

```bash
brew install tirano-tirano/crules/crules
```

### アップデート

crules を最新バージョンにアップデートするには、以下のいずれかの方法を使用します：

1. crules のみをアップデート:

```bash
brew upgrade crules
```

2. すべてのパッケージをアップデート（推奨）:

```bash
brew update
brew upgrade
```

3. 特定のバージョンにアップデート:

```bash
brew upgrade crules@<version>
```

注意:

- アップデート前に`brew update`を実行することを推奨します
- アップデート後は`crules --version`で新しいバージョンが正しくインストールされたことを確認できます
- 問題が発生した場合は、アンインストールして再インストールすることもできます

### アンインストール

crules のアンインストール:

```bash
brew uninstall crules
```

tap の削除:

```bash
brew untap tirano-tirano/crules
```

注意: tap の削除は自動的にパッケージをアンインストールしません。完全に削除する場合は、両方のコマンドを実行してください。

### 前提条件

- macOS
- Homebrew がインストール済み
- Intel または Apple Silicon Mac（両アーキテクチャをサポート）

### トラブルシューティング

インストールで問題が発生した場合:

1. Homebrew の更新:

```bash
brew update
```

2. 競合の確認:

```bash
brew doctor
```

3. 問題が解決しない場合は、再インストールを試してください:

```bash
brew uninstall crules
brew untap tirano-tirano/crules
brew tap tirano-tirano/crules
brew install crules
```

## プロジェクト構造

```
crules/
├── __init__.py      # パッケージの初期化ファイル
├── cli.py           # CLIコマンドの実装
├── commands/        # 各コマンドの実装
│   ├── __init__.py
│   ├── deploy.py    # デプロイコマンド
│   ├── init.py      # 初期化コマンド
│   └── list.py      # 一覧表示コマンド
├── config/          # 設定関連
│   ├── __init__.py
│   └── settings.py  # 設定管理
├── templates/       # テンプレート
│   ├── __init__.py
│   └── loader.py    # テンプレートローダー
└── utils/           # ユーティリティ
    ├── __init__.py
    ├── file.py      # ファイル操作
    └── logger.py    # ロギング
```

## 主要コンポーネント

### CLI (cli.py)

- Click フレームワークを使用した CLI インターフェース
- コマンドの登録と実行
- エラーハンドリング

### コマンド (commands/)

- `init`: プロジェクトの初期化
- `deploy`: ファイルの配置
- `list`: 利用可能なルールの一覧表示

### 設定 (config/)

- プロジェクト設定の管理
- テンプレートディレクトリの設定
- 環境変数の管理

### テンプレート (templates/)

- テンプレートファイルの管理
- テンプレートのロードと検証
- カスタムテンプレートのサポート

### ユーティリティ (utils/)

- ファイル操作のヘルパー関数
- ロギング機能
- エラーハンドリング

## 開発者向け情報

### 依存関係

- click >= 8.1.7
- pyyaml >= 6.0.1
- markdown >= 3.4.3

### テスト

```bash
# テストの実行
python -m pytest tests/

# カバレッジレポートの生成
python -m pytest --cov=crules tests/
```

### コードスタイル

- PEP 8 に準拠
- Black フォーマッターを使用
- isort でインポートを整理

## ライセンス

MIT
