# frozen_string_literal: true

module Crules
  module Utils
    class RuleSetFinder
      def self.find_available_rule_sets
        new.find_available_rule_sets
      end

      def find_available_rule_sets
        rule_sets = {}
        templates_dir = File.join(File.dirname(__FILE__), "..", "templates", "templates")

        Dir.entries(templates_dir).each do |entry|
          next if entry.start_with?(".")
          next unless File.directory?(File.join(templates_dir, entry))

          readme_path = File.join(templates_dir, entry, "README.md")
          if File.exist?(readme_path)
            content = File.read(readme_path)
            if content =~ /^#\s+(.+)$/
              rule_sets[entry] = $1.strip
            else
              rule_sets[entry] = entry
            end
          else
            rule_sets[entry] = entry
          end
        end

        rule_sets
      end

      def copy_rule_set(rule_set, force = false)
        source_dir = File.join(File.dirname(__FILE__), "..", "templates", "templates", rule_set)
        target_dir = File.join(".cursor", "rules")

        unless File.directory?(source_dir)
          puts "エラー: ルールセットディレクトリが見つかりません: #{source_dir}"
          exit 1
        end

        FileUtils.mkdir_p(target_dir)

        Dir.glob(File.join(source_dir, "**", "*.md")).each do |source_file|
          next if File.basename(source_file) == "README.md"
          relative_path = Pathname.new(source_file).relative_path_from(Pathname.new(source_dir)).to_s
          target_file = File.join(target_dir, relative_path.sub(/\.md$/, ".mdc"))

          if File.exist?(target_file) && !force
            puts "警告: ファイルが既に存在します: #{target_file}"
            puts "スキップします。上書きするには --force オプションを使用してください"
            next
          end

          FileUtils.mkdir_p(File.dirname(target_file))
          FileUtils.cp(source_file, target_file)
        end
      end
    end
  end
end 