# frozen_string_literal: true

require "yaml"
require_relative "base_command"

module Crules
  module Commands
    # ルール一覧を表示するコマンドクラス
    #
    # @example コマンドラインからの使用
    #   $ crules list
    #   Ruby
    #   Python
    #   合計: 2件
    #
    # @example プログラムからの使用
    #   command = ListCommand.new
    #   command.execute  # => ルール一覧を出力
    #
    # @note このコマンドは以下の機能を提供します：
    #   - ルール一覧の表示
    #   - ルールの総数の表示
    class ListCommand < BaseCommand
      # コマンドを実行する
      #
      # @return [void]
      def execute
        rules_dir = File.join(Dir.pwd, "rules")
        unless Dir.exist?(rules_dir)
          puts "ルールが存在しません"
          puts "合計: 0件"
          return
        end

        rules = Dir.glob(File.join(rules_dir, "*.yml")).map do |file|
          YAML.load_file(file)["name"]
        end

        if rules.empty?
          puts "ルールが存在しません"
          puts "合計: 0件"
        else
          rules.each { |rule| puts rule }
          puts "合計: #{rules.size}件"
        end
      end
    end
  end
end 