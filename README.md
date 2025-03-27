# Crules

Cursor ルールを管理するための CLI ツール

## 概要

Crules は、Cursor IDE のルールを効率的に管理するためのコマンドラインツールです。プロジェクトのコーディング規約やガイドラインを簡単に設定・管理することができます。

## 機能

- Flutter プロジェクト用の初期 Cursor ルールセットの生成
- テンプレートを使用した新規ルールファイルの追加
- エラーログとデバッグ文書の管理
- カスタムルールテンプレートのサポート

## インストール

### Homebrew を使用する場合

```bash
brew tap johnsmith/crules
brew install crules
```

### 手動インストール

```bash
# 依存関係のインストール
bundle install

# ビルド
gem build crules.gemspec

# インストール
gem install ./crules-*.gem
```

## 使用方法

### 初期化

```bash
crules init [--framework <framework>] [--force]
```

- `--framework`: 使用するフレームワークを指定（デフォルト: default）
  - `flutter`: Flutter プロジェクト用のテンプレート
  - `default`: 汎用的なテンプレート
- `--force`: 既存のファイルを上書き

### ルールの追加

```bash
crules add <rule_name> [--force]
```

- `rule_name`: 追加するルールの名前
- `--force`: 既存のファイルを上書き

## ルールファイルの構造

### Frontmatter

各ルールファイルの先頭には、以下のような Frontmatter を記述します：

```yaml
---
description: ルールの簡潔な説明
globs: 適用対象のファイルパターン（例: "*.dart", "lib/**/*.ts"）
alwaysApply: true  # 常にルールを適用するかどうか
---
```

- `description`: ルールの目的や概要を簡潔に説明
- `globs`: ルールを適用するファイルのパターンを指定（glob 形式）
- `alwaysApply`: ルールを常に適用するかどうかを指定（true/false）

### 本文の構造

- ルールの目的
- ルールの詳細
- 実装ガイドライン
- 検証方法
- 例外処理
- メンテナンス情報

## テンプレートの使用方針

1. `init`コマンド

   - 指定されたフレームワークのディレクトリから全てのテンプレートをコピー
   - フレームワーク固有のルールやガイドラインを設定

2. `add`コマンド
   - 常に`default/rule_template.md`を使用
   - 汎用的なルールテンプレートから新規ルールを作成

## ディレクトリ構造

```
.cursor/
└── rules/
    ├── errors/
    │   └── error_logging_guide.mdc
    ├── 01_ai_behavior.mdc
    ├── 02_general_coding_style.mdc
    ├── 03_requirements.mdc
    ├── 04_architecture.mdc
    ├── 05_specification.mdc
    ├── 06_flutter_style.mdc
    ├── 07_module.mdc
    └── rule_template.mdc
```

## 新しいフレームワークの追加方法

1. `lib/crules/templates/`に新しいフレームワークのディレクトリを作成
2. テンプレートファイルを`.md`拡張子で配置
3. `AVAILABLE_FRAMEWORKS`に新しいフレームワークを追加

例：

```ruby
AVAILABLE_FRAMEWORKS = {
  "flutter" => "Flutterプロジェクト用のテンプレート",
  "react" => "Reactプロジェクト用のテンプレート",
  "default" => "汎用的なテンプレート"
}.freeze
```

## 開発

```bash
# 依存関係のインストール
bundle install

# テストの実行
bundle exec rspec

# ビルド
gem build crules.gemspec
```

## コントリビューション

1. リポジトリをフォーク
2. 機能ブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'feat: 素晴らしい機能を追加'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを作成

## ライセンス

MIT License
