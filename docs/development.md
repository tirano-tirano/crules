# 開発者ガイド

## 概要

このドキュメントは、crules の開発に参加する開発者向けのガイドです。
コードの構造、開発プロセス、テストの方法などについて説明します。

## プロジェクト構造

```
crules/
├── bin/                    # 実行可能ファイル
├── lib/                    # メインのソースコード
│   └── crules/
│       ├── commands/      # コマンドの実装
│       ├── utils/         # ユーティリティクラス
│       ├── templates/     # ルールのテンプレート
│       ├── version.rb     # バージョン情報
│       └── cli.rb         # CLIのエントリーポイント
├── spec/                   # テストファイル
├── docs/                   # ドキュメント
└── .cursor/               # Cursor IDE設定
    └── rules/             # プロジェクトルール
```

## アーキテクチャ

crules は以下の主要なコンポーネントで構成されています：

1. **コマンド（Commands）**

   - 各コマンドは独立したクラスとして実装
   - Thor::Group を継承し、CLI インターフェースを提供
   - 単一責任の原則に従い、1 つのコマンドは 1 つの機能を担当

2. **ユーティリティ（Utils）**

   - 共通の機能を提供するヘルパークラス
   - 再利用可能なコードを集約
   - 単体テスト可能な形で実装

3. **テンプレート（Templates）**
   - ルールセットのテンプレートファイル
   - 各プロジェクトタイプに特化したルール
   - Markdown フォーマットで記述

## 開発プロセス

1. **環境設定**

   ```bash
   # リポジトリのクローン
   git clone https://github.com/tirano-tirano/crules.git
   cd crules

   # 依存関係のインストール
   bundle install
   ```

2. **テスト**

   ```bash
   # 全テストの実行
   bundle exec rspec

   # 特定のテストの実行
   bundle exec rspec spec/crules/utils/project_root_finder_spec.rb
   ```

3. **ドキュメント生成**

   ```bash
   # YARDドキュメントの生成
   bundle exec yard doc

   # ドキュメントのプレビュー
   bundle exec yard server
   ```

## コーディング規約

1. **一般的な規則**

   - 2 スペースインデント
   - UTF-8 エンコーディング
   - 行末の空白を削除
   - ファイル末尾に空行を 1 行追加

2. **命名規則**

   - クラス名: PascalCase（例: `ProjectRootFinder`）
   - メソッド名: snake_case（例: `find_project_root`）
   - 定数: SCREAMING_SNAKE_CASE（例: `VERSION`）

3. **コメント**
   - クラスとモジュールには必ずドキュメントコメントを付ける
   - パブリックメソッドには使用方法と戻り値の説明を記述
   - 複雑なロジックには適切な説明を追加

## エラーハンドリング

1. **基本方針**

   - 予期せぬエラーは`Crules::Error`を使用
   - ユーザーエラーは適切なメッセージを表示
   - デバッグ情報は開発モードでのみ表示

2. **エラーの種類**
   ```ruby
   module Crules
     class Error < StandardError; end
     class InvalidRuleSetError < Error; end
     class TemplateNotFoundError < Error; end
   end
   ```

## 貢献方法

1. **Issue 作成**

   - バグ報告や機能要望は Issue で管理
   - テンプレートに従って必要な情報を記入

2. **Pull Request**

   - 作業前に Issue を作成
   - トピックブランチで開発
   - テストとドキュメントを含める

3. **レビュー**
   - コードレビューは必須
   - CI/CD パイプラインのチェックをパス
   - コーディング規約に準拠
