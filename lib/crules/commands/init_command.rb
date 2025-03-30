# frozen_string_literal: true

require_relative "base_command"

module Crules
  module Commands
    # ルールを初期化するコマンドクラス
    #
    # @example コマンドラインからの使用
    #   $ crules init
    #   ルールディレクトリを作成しました
    #   デフォルトルールをコピーしました
    #
    # @example プログラムからの使用
    #   command = InitCommand.new
    #   command.execute  # => ルールを初期化
    #
    # @note このコマンドは以下の機能を提供します：
    #   - ルールディレクトリの作成
    #   - デフォルトルールのコピー
    #   - エラー処理（ディレクトリが既に存在する場合など）
    class InitCommand < BaseCommand
      # @return [Hash] コマンドのオプション
      attr_reader :options

      # 新しいインスタンスを初期化する
      #
      # @param args [Array] コマンドライン引数
      # @param options [Hash] コマンドのオプション
      def initialize(args = [], options = {})
        @options = { force: false }.merge(options)
        @rule_set_finder = Utils::RuleSetFinder.new
      end

      # コマンドを実行する
      #
      # @return [void]
      def execute
        rule_set = options[:rule_set] || "default"
        available_rule_sets = @rule_set_finder.find_available_rule_sets

        unless available_rule_sets.key?(rule_set)
          puts "エラー: 無効なルールセット '#{rule_set}'"
          puts "利用可能なルールセット:"
          available_rule_sets.each do |name, desc|
            puts "  #{name}: #{desc}"
          end
          exit 1
        end

        begin
          @rule_set_finder.copy_rule_set(rule_set, options[:force])
          puts "ルールセット '#{rule_set}' の初期化が完了しました"
        rescue Errno::EACCES => e
          puts "ルールディレクトリの作成に失敗しました"
          puts "エラー: #{e.message}"
        rescue StandardError => e
          puts "デフォルトルールのコピーに失敗しました"
          puts "エラー: #{e.message}"
        end
      end
    end
  end
end 