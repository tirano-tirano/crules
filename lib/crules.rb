#!/usr/bin/env ruby
# frozen_string_literal: true

require 'thor'
require 'fileutils'
require 'json'
require 'colorize'

module Crules
  class CLI < Thor
    package_name 'crules'
    map '-v' => :version

    desc 'init', 'Initialize Cursor rules for Flutter project'
    method_option :force, type: :boolean, default: false, aliases: '-f'
    def init
      say 'Initializing Cursor rules for Flutter project...'.green

      # Create .cursor/rules directory
      rules_dir = '.cursor/rules'
      FileUtils.mkdir_p(rules_dir)

      # Create errors directory
      errors_dir = File.join(rules_dir, 'errors')
      FileUtils.mkdir_p(errors_dir)

      # Generate rule files
      generate_rule_files(rules_dir, errors_dir)
    end

    desc 'add [RULE_NAME]', 'Add a new rule file'
    def add(rule_name)
      say "Adding new rule: #{rule_name}...".green

      rules_dir = '.cursor/rules'
      FileUtils.mkdir_p(rules_dir)

      template_path = File.join(File.dirname(__FILE__), 'templates', 'rule_template.mdc')
      target_path = File.join(rules_dir, "#{rule_name}.mdc")

      if File.exist?(target_path) && !options[:force]
        say "Rule file #{target_path} already exists. Use --force to overwrite.".red
        exit 1
      end

      FileUtils.cp(template_path, target_path)
      say "Created new rule file: #{target_path}".green
    end

    desc 'version', 'Show version'
    def version
      say "crules #{Crules::VERSION}"
    end

    private

    def generate_rule_files(rules_dir, errors_dir)
      templates = {
        'dart_style' => generate_dart_style,
        'requirements' => generate_requirements,
        'specification' => generate_specification,
        'architecture' => generate_architecture,
        'ai_behavior' => generate_ai_behavior,
        'errors/error_logging_guide' => generate_error_logging_guide
      }

      templates.each do |name, content|
        target_path = File.join(rules_dir, "#{name}.mdc")
        if File.exist?(target_path) && !options[:force]
          say "Rule file #{target_path} already exists. Skipping...".yellow
          next
        end

        File.write(target_path, content)
        say "Created #{target_path}".green
      end
    end

    def generate_dart_style
      <<~MARKDOWN
        ---
        description: "Dart Style Guide and best practices for this project"
        globs: "**/*.dart"
        alwaysApply: false
        ---

        # Dart Coding Style

        ## 命名規則
        - **クラス名**は`PascalCase`（単語の先頭を大文字）で記述する
        - **メソッド・変数名**は`camelCase`（最初の単語は小文字、以降の単語頭字を大文字）で記述する
        - **ファイル名・ディレクトリ名**は`lowercase_with_underscores`（全て小文字＋単語間アンダースコア）で記述する
        - **定数**は原則として`lowerCamelCase`。ただしグローバル定数や環境変数は必要に応じて全大文字スネークケース（e.g. `MAX_COUNT`）を使用する

        ## フォーマットとコーディング習慣
        - **インデント**はスペース2つ。公式フォーマッタ `dart format` に従い、自動フォーマットを適用する
        - **行の長さ**は80文字以内に収めることを優先する
        - **波括弧** `{}` はすべての制御構文 (`if`, `for` 等) において省略せずに記述する
        - **ファイルインポート順**: 組み込みの`dart:`パッケージ→サードパーティの`package:`→相対パスの順にソートする
      MARKDOWN
    end

    def generate_requirements
      <<~MARKDOWN
        ---
        description: "Project requirements and user stories"
        globs: 
        alwaysApply: false
        ---

        # 要件定義

        ## プロジェクト概要
        - **ターゲットユーザー**: 新規顧客および既存顧客（スマートフォンアプリ利用者）
        - **課題と目的**: ユーザーが〇〇できるようにすることで△△という課題を解決する
        - **基本コンセプト**: シンプルで直感的なUI、高速な動作、オフライン対応

        ## 機能要件
        1. **ユーザー登録と認証**: 新規ユーザー登録、ログイン、パスワードリセット機能
        2. **プロフィール管理**: ユーザーが自身のプロフィール情報（名前、アイコン等）を閲覧・編集できる
        3. **〇〇機能**: ユーザーが△△を行えるようにするコア機能

        ## 非機能要件
        - **パフォーマンス**: アプリ起動時に3秒以内にホーム画面を表示。主要機能操作は1秒以内のレスポンス
        - **対応OS**: iOS 14以上、Android 11以上
        - **セキュリティ**: ユーザーデータは端末内に暗号化して保存。通信は常にSSL/TLSを使用
      MARKDOWN
    end

    def generate_specification
      <<~MARKDOWN
        ---
        description: "Functional and system specifications for the app"
        globs: 
        alwaysApply: false
        ---

        # 仕様書

        ## 画面仕様
        - **ログイン画面**: ユーザー名とパスワードを入力する。入力検証（未入力チェック、パスワードは8文字以上など）を行い、エラーはフォーム下部に赤字表示
        - **ホーム画面**: 認証後に表示。ユーザーの〇〇情報をリスト表示し、各項目をタップすると詳細画面へ遷移。プルダウンによる再読込に対応

        ## データ仕様
        - **データモデル**: ユーザー情報（フィールド: id, name, email, created_at, ...）、〇〇エンティティ（フィールド: ...）など主要なデータ構造を定義
        - **API仕様**: 
          - `/api/v1/xxx` (GET) – △△の一覧を取得
          - `/api/v1/yyy` (POST) – △△を新規作成

        ## 振る舞いとビジネスロジック
        - **〇〇機能フロー**: ユーザーが△△を行った際の処理手順
        - **バックグラウンド処理**: アプリ起動時に前回取得データのキャッシュを検証し、一定条件で自動更新を行う
      MARKDOWN
    end

    def generate_architecture
      <<~MARKDOWN
        ---
        description: "High-level architecture and design principles"
        globs: 
        alwaysApply: false
        ---

        # アーキテクチャ設計

        ## システム構成とレイヤー
        - **プレゼンテーション層**: UIとユーザー操作を扱う。FlutterのWidgetで画面構成し、状態管理はBusiness層から提供されたProviderを利用
        - **ビジネスロジック層**: アプリケーションのドメインロジックを担当。ViewModelやUseCaseクラスとして実装し、プレゼンテーション層とデータ層の仲介を行う
        - **データ層**: リポジトリパターンを採用。`Repository`インターフェースを通じてAPIクライアントやローカルDBからデータ取得

        ## フォルダ構成
        - **lib/** 配下に主要コードを配置:
          - lib/ui/… （UI層: 画面ごとのディレクトリとWidgetクラス）
          - lib/domain/… （ビジネスロジック層: ViewModelやサービスクラス、ユースケース）
          - lib/data/… （データ層: モデル定義、リポジトリ実装、API・DBアクセス）
          - lib/common/… （共通ユーティリティやテーマ、定数定義）

        ## デザイン指針・技術選定
        - **状態管理**: Riverpodを使用し、グローバルな状態とScopedな状態を適切に使い分ける
        - **非同期処理**: `Future`/`Stream`とasync/awaitパターンで記述
        - **依存関係**: UIは直接データ層に依存せず、必ずビジネスロジック層を経由する
      MARKDOWN
    end

    def generate_ai_behavior
      <<~MARKDOWN
        ---
        description: "Guidelines for AI behavior and rule evolution"
        globs: 
        alwaysApply: true
        ---

        # AIアシスタント行動ガイド

        ## 応答スタイルガイド
        - **明瞭簡潔**: 回答はできるだけ簡潔に、しかし必要な詳細は含めて記述する
        - **根拠の提示**: コード提案や助言には、可能な限り根拠や参照を含める
        - **一貫性**: 用語や命名はプロジェクト内で一貫したものを使う
        - **敬意と協調**: ユーザー（開発者）の意図を尊重し、必要に応じて質問を投げかけながら共同作業する

        ## 作業手順に関する指針
        - **段階的提案**: 複雑な問題は一度に結論を出そうとせず、ステップバイステップで考え提案する
        - **安全なコード**: 可能な限りバグや脆弱性を生まない実装を心がける
        - **ルール遵守**: 他の.mdcファイルに書かれた内容に反しない回答をする
        - **ルール更新提案**: プロジェクトのルールに不足があると感じた場合、ルールの更新を提案する
      MARKDOWN
    end

    def generate_error_logging_guide
      <<~MARKDOWN
        ---
        description: "How to document errors and debugging outcomes"
        globs: "errors/*.mdc"
        alwaysApply: false
        ---

        # エラー記録ガイド

        ## エラー概要 (Error Description)
        - **発生日時**: YYYY-MM-DD HH:mm 頃
        - **現象**: 発生したエラーの簡潔な説明
        - **エラーメッセージ/コード**: 実際のエラーメッセージやスタックトレースの要約

        ## 仮説 (Hypothesis)
        - 原因として考えられることを箇条書き

        ## 検証方法 (Verification Steps)
        1. 再現手順: エラーを再現するための具体的手順
        2. デバッグまたはログ調査の方法: ログ出力やブレークポイントを用いてどこで問題が起きているか確認
        3. 仮説ごとの検証: 各仮説についての検証内容

        ## 検証結果と結論 (Results & Conclusion)
        - 各仮説の検証結果
        - **判明した原因**: 特定された原因
        - **対応策**: 実施した対応内容

        ## 修正と再発防止 (Fix & Prevention)
        - コミットID: 修正を含むコミットのハッシュ
        - **修正内容**: 具体的な修正内容
        - **テスト結果**: 修正後のテスト結果
        - **備考**: 追加の注意点や教訓
      MARKDOWN
    end
  end
end

Crules::CLI.start(ARGV) 