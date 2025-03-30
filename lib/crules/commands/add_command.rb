# frozen_string_literal: true

module Crules
  module Commands
    class AddCommand < Thor::Group
      include Thor::Actions

      argument :rule_name, type: :string, desc: "追加するルールの名前"
      class_option :force, type: :boolean, default: false, desc: "既存のファイルを上書き"

      def execute
        template_path = File.join(File.dirname(__FILE__), "..", "templates", "rule-template.md")
        target_path = File.join(".cursor", "rules", "#{rule_name}.mdc")

        unless File.exist?(template_path)
          puts "エラー: テンプレートファイルが見つかりません: #{template_path}"
          exit 1
        end

        if File.exist?(target_path) && !options[:force]
          puts "エラー: ファイルが既に存在します: #{target_path}"
          puts "上書きするには --force オプションを使用してください"
          exit 1
        end

        FileUtils.mkdir_p(File.dirname(target_path))
        FileUtils.cp(template_path, target_path)
        puts "ルールファイルを作成しました: #{target_path}"
      end
    end
  end
end 