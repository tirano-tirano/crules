# Crules

Cursor IDE のルールを効率的に管理するための CLI ツール

## 概要

Crules は、Cursor IDE のルールを効率的に管理するためのコマンドラインツールです。プロジェクトのコーディング規約やガイドラインを簡単に設定・管理することができます。

## 機能

- プロジェクト言語に応じたルールセットの生成（Ruby、Python など）
- ルールセットの初期化と管理
- カスタムルールセットのサポート
- 柔軟なルール設定と上書きオプション

## インストール

### gem としてインストールする場合

```bash
# GitHubから直接インストール
gem install bundler
bundle init
echo "source 'https://rubygems.org'" >> Gemfile
echo "gem 'crules', github: 'tirano-tirano/crules'" >> Gemfile
bundle install
bundle binstubs crules
```

## 使用方法

### 初期化（`init`）

```bash
crules init [--rule-set <rule_set>] [--force]
```

- `--rule-set`: 使用するルールセットを指定（デフォルト: default）
  - `default`: デフォルトのルールセット（Ruby、Python のルールを含む）
  - `custom`: カスタムルールセット
- `--force`: 既存のルールを上書き

指定されたルールセットのテンプレートファイルが`.cursor/rules/`ディレクトリにコピーされます。

### ルールファイルの構造

各ルールファイルは`.mdc`拡張子で、以下のような形式で記述します：

```markdown
---
description: "ルールの説明"
globs: "適用対象のファイルパターン"
alwaysApply: true
---

# ルールのタイトル

## 大原則

- **このルールズの意義**: このプルジェクトルールズは、単に AI への指示という意味だけでなく、開発を進める上で今までの開発内容を確認するためのドキュメントという意味合いをもっています。

## ルールの詳細

- ルールの具体的な内容
- 実装ガイドライン
- 検証方法
```

## ディレクトリ構造

```
.
├── .cursor/                   # Cursor IDE設定
│   └── rules/                # プロジェクトのルールディレクトリ
│       ├── 01-rule-name.mdc  # ルールファイル
│       └── 02-rule-name.mdc  # ルールファイル
└── lib/
    └── crules/
        ├── templates/        # ルールセットのテンプレート
        │   └── default/     # デフォルトのルールセット
        │       ├── 01-rule-name.md
        │       └── 02-rule-name.md
        └── utils/
            └── rule_set_finder.rb  # ルールセット管理クラス
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

## エラーハンドリング

Crules は以下のような状況で適切なエラーメッセージを表示します：

- 無効なルールセットが指定された場合
- ルールディレクトリの作成に失敗した場合
- ルールのコピーに失敗した場合

## ライセンス

MIT License
