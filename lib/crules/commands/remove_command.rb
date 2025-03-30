# frozen_string_literal: true

require_relative "base_command"

module Crules
  module Commands
    # ルールを削除するコマンドクラス
    #
    # @example コマンドラインからの使用
    #   $ crules remove ruby
    #   ルール 'ruby' を削除しました
    #
    # @example プログラムからの使用
    #   command = RemoveCommand.new("ruby")
    #   command.execute  # => ルールを削除
    #
    # @note このコマンドは以下の機能を提供します：
    #   - 指定されたルールの削除
    #   - 削除結果の表示
    #   - エラー処理（ルールが存在しない場合など）
    class RemoveCommand < BaseCommand
      # @return [String] 削除対象のルール名
      attr_reader :rule_name

      # 新しいインスタンスを初期化する
      #
      # @param rule_name [String] 削除対象のルール名
      def initialize(rule_name)
        @rule_name = rule_name
      end

      # コマンドを実行する
      #
      # @return [void]
      def execute
        rules_dir = File.join(Dir.pwd, "rules")
        unless Dir.exist?(rules_dir)
          puts "ルールディレクトリが見つかりません"
          return
        end

        rule_file = File.join(rules_dir, "#{rule_name}.yml")
        unless File.exist?(rule_file)
          puts "ルール '#{rule_name}' が見つかりません"
          return
        end

        begin
          File.delete(rule_file)
          puts "ルール '#{rule_name}' を削除しました"
        rescue StandardError => e
          puts "ルール '#{rule_name}' の削除に失敗しました"
          puts "エラー: #{e.message}"
        end
      end
    end
  end
end 