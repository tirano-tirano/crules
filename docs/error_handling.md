# エラーハンドリングガイド

## 概要

このドキュメントは、crules におけるエラーハンドリングの方針と実装方法について説明します。
適切なエラー処理により、ユーザーフレンドリーなエラーメッセージとデバッグ可能な情報を提供します。

## エラーの種類

1. **ユーザーエラー**

   - ユーザーの入力や操作に起因するエラー
   - 回復可能で、適切なガイダンスを提供
   - 例：無効なルールセット名、既存ファイルの上書き

2. **システムエラー**

   - システムの状態に起因するエラー
   - 一時的な問題で回復可能な場合がある
   - 例：ファイルシステムの権限、リソースの不足

3. **プログラムエラー**
   - プログラムのバグに起因するエラー
   - 開発者の対応が必要
   - 例：未定義のメソッド、不正な状態

## エラークラス階層

```ruby
module Crules
  # 基本エラークラス
  class Error < StandardError; end

  # ユーザーエラー
  class UserError < Error; end
  class InvalidRuleSetError < UserError; end
  class FileExistsError < UserError; end
  class InvalidArgumentError < UserError; end

  # システムエラー
  class SystemError < Error; end
  class FileSystemError < SystemError; end
  class ResourceError < SystemError; end

  # プログラムエラー
  class ProgramError < Error; end
  class StateError < ProgramError; end
  class ConfigurationError < ProgramError; end
end
```

## エラーメッセージのガイドライン

1. **ユーザーエラーメッセージ**

   - 問題を明確に説明
   - 解決方法を提示
   - 技術的な詳細は最小限に

   ```ruby
   begin
     rule_set = find_rule_set(name)
   rescue InvalidRuleSetError => e
     puts "エラー: 無効なルールセット '#{name}'"
     puts "利用可能なルールセット:"
     available_rule_sets.each { |n, d| puts "  #{n}: #{d}" }
     exit 1
   end
   ```

2. **システムエラーメッセージ**

   - エラーの性質を説明
   - 可能な対処方法を提示
   - 一時的な問題かどうかを明示

   ```ruby
   begin
     copy_files(source, target)
   rescue FileSystemError => e
     puts "エラー: ファイルのコピーに失敗しました"
     puts "原因: #{e.message}"
     puts "以下を確認してください:"
     puts "- ディスク容量"
     puts "- ファイルの権限"
     puts "- ディレクトリの書き込み権限"
     exit 1
   end
   ```

3. **プログラムエラーメッセージ**

   - エラーの詳細をログに記録
   - ユーザーには一般的なメッセージを表示
   - バグ報告の方法を案内

   ```ruby
   begin
     process_command(args)
   rescue ProgramError => e
     logger.error "プログラムエラー: #{e.message}"
     logger.error e.backtrace.join("\n")
     puts "申し訳ありません。予期せぬエラーが発生しました"
     puts "このエラーを報告する場合は、以下の情報を含めてください:"
     puts "- エラーID: #{generate_error_id}"
     puts "- 実行したコマンド: #{ARGV.join(' ')}"
     exit 1
   end
   ```

## デバッグ情報の記録

1. **ログレベル**

   - ERROR: エラーイベント
   - WARN: 警告メッセージ
   - INFO: 一般的な情報
   - DEBUG: デバッグ情報

2. **ログフォーマット**

   ```ruby
   logger.formatter = proc do |severity, datetime, progname, msg|
     "[#{datetime}] #{severity} #{progname}: #{msg}\n"
   end
   ```

3. **環境別の設定**
   ```ruby
   case ENV['CRULES_ENV']
   when 'production'
     logger.level = Logger::INFO
   when 'development'
     logger.level = Logger::DEBUG
   when 'test'
     logger.level = Logger::ERROR
   end
   ```

## エラーハンドリングのベストプラクティス

1. **早期リターン**

   ```ruby
   def process_rule_set(name)
     return error("ルールセット名が必要です") if name.nil?
     return error("無効なルールセット名です") unless valid_name?(name)
     # 処理を続行
   end
   ```

2. **適切なスコープ**

   ```ruby
   def copy_rule_set
     validate_arguments  # 引数の検証
     prepare_directories # ディレクトリの準備
     copy_files         # ファイルのコピー
   rescue UserError => e
     handle_user_error(e)
   rescue SystemError => e
     handle_system_error(e)
   rescue StandardError => e
     handle_unexpected_error(e)
   end
   ```

3. **エラー情報の集約**
   ```ruby
   def validate_rule_set(name)
     errors = []
     errors << "名前が空です" if name.empty?
     errors << "無効な文字が含まれています" unless valid_chars?(name)
     errors << "既に存在します" if exists?(name)
     raise InvalidRuleSetError, errors.join(", ") if errors.any?
   end
   ```

## テスト

1. **エラーケースのテスト**

   ```ruby
   RSpec.describe RuleSetValidator do
     context "無効な入力の場合" do
       it "空の名前でエラーを発生させる" do
         expect { validator.validate("") }
           .to raise_error(InvalidRuleSetError, "名前が空です")
       end
     end
   end
   ```

2. **エラーメッセージのテスト**
   ```ruby
   RSpec.describe ErrorHandler do
     context "ユーザーエラーの場合" do
       it "適切なメッセージを表示する" do
         error = InvalidRuleSetError.new("テスト")
         expect { handler.handle(error) }
           .to output(/エラー: テスト/).to_stdout
       end
     end
   end
   ```
