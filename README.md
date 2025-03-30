# Crules

Cursor ルールを管理するための CLI ツール

## 概要

Crules は、Cursor IDE のルールを効率的に管理するためのコマンドラインツールです。プロジェクトのコーディング規約やガイドラインを簡単に設定・管理することができます。

## 機能

- プロジェクトタイプに応じたルールセットの生成
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

### 初期化（`init`）

```bash
crules init [--rule-set <rule_set>] [--force]
```

- `--rule-set`: 使用するルールセットを指定（デフォルト: default）
  - `flutter`: Flutter プロジェクト用のルールセット
  - `default`: 汎用的なルールセット
- `--force`: 既存のファイルを上書き

指定されたルールセットのテンプレートファイルが`.cursor/rules/`にコピーされます。

### ルールの追加（`add`）

```bash
crules add <rule_name> [--force]
```

- `rule_name`: 追加するルールの名前
- `--force`: 既存のファイルを上書き

`rule-template.md`を使用して新規ルールファイル（`.mdc`拡張子）を作成します。

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

   - 指定されたルールセットのディレクトリから全てのテンプレートをコピー
   - プロジェクトタイプ固有のルールやガイドラインを設定
   - `rule-template.md`はコピーされません（新規ルール作成時に使用）

2. `add`コマンド
   - `rule-template.md`を使用して新規ルールを作成
   - 作成されたルールは`.mdc`拡張子で保存

## ディレクトリ構造

```
.cursor/
└── rules/
    ├── 01-rule-name.mdc          # ルールファイル（例：AIアシスタントの行動指針）
    └── 02-rule-name.mdc          # ルールファイル（例：コーディング規約）
```

## 新しいルールセットの追加方法

1. `lib/crules/templates/templates/`に新しいルールセットのディレクトリを作成
2. テンプレートファイルを`.md`拡張子で配置
3. ルールセットの説明を`lib/crules/templates/templates/<rule_set>/README.md`に記述
   - この README.md は、ルールセットの説明として使用されます
   - 最初の行の見出しが、ルールセットの説明として表示されます

例：

```markdown
# Flutter ルールセット

Flutter プロジェクト用のルールセットです。以下のルールを含みます：

- AI アシスタントの行動指針
- コーディング規約
- アーキテクチャ設計ガイドライン
- エラーハンドリングガイド
```

この方法により：

- ルールセットの追加が容易になります
- 各ルールセットの説明が、そのルールセットのコンテキスト内で管理されます
- コードの変更なしで新しいルールセットを追加できます

## 開発

```bash
# 依存関係のインストール
bundle install

# テストの実行
bundle exec rspec

# ビルド
gem build crules.gemspec
```

## ライセンス

MIT License
