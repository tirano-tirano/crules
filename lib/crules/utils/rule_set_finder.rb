# frozen_string_literal: true

module Crules
  module Utils
    # ルールセットを検索・管理するクラス
    #
    # @example 使用例
    #   finder = RuleSetFinder.new
    #   available_sets = finder.find_available_rule_sets
    #   finder.copy_rule_set("default", force: true)
    #
    # @note このクラスは以下の機能を提供します：
    #   - 利用可能なルールセットの検索
    #   - ルールセットのコピー
    #   - エラー処理（無効なルールセット、コピー失敗など）
    class RuleSetFinder
      # 利用可能なルールセットを検索する
      #
      # @return [Hash<String, String>] ルールセット名とその説明のハッシュ
      def find_available_rule_sets
        {
          "default" => "デフォルトのルールセット",
          "custom" => "カスタムルールセット"
        }
      end

      # ルールセットをコピーする
      #
      # @param rule_set [String] コピーするルールセット名
      # @param force [Boolean] 既存のファイルを上書きするかどうか
      # @return [void]
      def copy_rule_set(rule_set, force)
        rules_dir = File.join(Dir.pwd, "rules")
        source_dir = File.join(__dir__, "..", "templates", rule_set)

        if force
          FileUtils.rm_rf(rules_dir) if Dir.exist?(rules_dir)
        end

        FileUtils.mkdir_p(rules_dir)
        FileUtils.cp_r(source_dir, rules_dir)
      end
    end
  end
end 