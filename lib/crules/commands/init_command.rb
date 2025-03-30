# frozen_string_literal: true

require_relative "../utils/rule_set_finder"

module Crules
  module Commands
    class InitCommand < Thor::Group
      include Thor::Actions

      class_option :rule_set, type: :string, default: "default", desc: "使用するルールセット"
      class_option :force, type: :boolean, default: false, desc: "既存のファイルを上書き"

      def initialize(*args)
        super
        @rule_set_finder = Utils::RuleSetFinder.new
      end

      def execute
        rule_set = options[:rule_set]
        available_rule_sets = @rule_set_finder.find_available_rule_sets

        unless available_rule_sets.key?(rule_set)
          puts "エラー: 無効なルールセット '#{rule_set}'"
          puts "利用可能なルールセット:"
          available_rule_sets.each do |name, desc|
            puts "  #{name}: #{desc}"
          end
          exit 1
        end

        @rule_set_finder.copy_rule_set(rule_set, options[:force])
        puts "ルールセット '#{rule_set}' の初期化が完了しました"
      end
    end
  end
end 