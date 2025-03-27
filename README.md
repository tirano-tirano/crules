# Crules

Flutter プロジェクト用の Cursor ルール（.mdc ファイル）を生成・管理するためのコマンドラインツールです。

## 機能

- Flutter プロジェクト用の初期 Cursor ルールセットの生成
- テンプレートを使用した新規ルールファイルの追加
- エラーログとデバッグ文書の管理
- カスタムルールテンプレートのサポート

## インストール

### Homebrew を使用する場合

```bash
# リポジトリの追加
brew tap yourusername/crules

# インストール
brew install crules
```

### 手動インストール

```bash
git clone https://github.com/yourusername/crules.git
cd crules
bundle install
bundle exec rake install
```

## 使用方法

### Cursor ルールの初期化

```bash
crules init
```

これにより、`.cursor/rules/` に以下のファイルが作成されます：

- `dart_style.mdc` - Dart コーディング規約
- `requirements.mdc` - プロジェクト要件定義
- `specification.mdc` - システム仕様書
- `architecture.mdc` - アーキテクチャ設計書
- `ai_behavior.mdc` - AI アシスタントガイドライン
- `errors/error_logging_guide.mdc` - エラーログテンプレート

### 新規ルールの追加

```bash
crules add my_new_rule
```

これにより、テンプレートを使用して新しいルールファイルが作成されます。

### バージョン表示

```bash
crules --version
```

## 開発

### セットアップ

```bash
bundle install
```

### テストの実行

```bash
bundle exec rspec
```

### コードスタイル

```bash
bundle exec rubocop
```

## コントリビューション

1. リポジトリをフォーク
2. 機能ブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m '素晴らしい機能を追加'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを作成

## ライセンス

このプロジェクトは MIT ライセンスの下で提供されています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。
