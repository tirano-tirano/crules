# frozen_string_literal: true

module Crules
  class CLI < Thor
    package_name "crules"

    AVAILABLE_FRAMEWORKS = {
      "flutter" => "Flutterプロジェクト用のテンプレート",
      "default" => "汎用的なテンプレート"
    }.freeze

    desc "version", "バージョン情報を表示"
    def version
      puts "crules v#{VERSION}"
    end
    map %w[--version -v] => :version

    desc "init", "Cursorルールを初期化"
    method_option :force, type: :boolean, default: false, aliases: "-f",
                 desc: "既存のファイルを上書き"
    method_option :framework, type: :string, default: "default",
                 desc: "使用するフレームワークを指定 (flutter, default)"
    def init
      puts "🚀 Cursorルールの初期化を開始します...".green

      framework = options[:framework]
      unless AVAILABLE_FRAMEWORKS.key?(framework)
        puts "❌ 無効なフレームワークです: #{framework}".red
        puts "利用可能なフレームワーク:"
        AVAILABLE_FRAMEWORKS.each do |name, desc|
          puts "  - #{name}: #{desc}"
        end
        exit 1
      end

      puts "📦 フレームワーク: #{framework} (#{AVAILABLE_FRAMEWORKS[framework]})".green

      create_rules_directory
      copy_template_files(framework)

      puts "\n✨ 初期化が完了しました！".green
    end

    desc "add RULE_NAME", "新しいルールファイルを追加"
    method_option :force, type: :boolean, default: false, aliases: "-f",
                 desc: "既存のファイルを上書き"
    method_option :framework, type: :string, default: "default",
                 desc: "使用するフレームワークを指定 (flutter, default)"
    def add(rule_name)
      framework = options[:framework]
      unless AVAILABLE_FRAMEWORKS.key?(framework)
        puts "❌ 無効なフレームワークです: #{framework}".red
        puts "利用可能なフレームワーク:"
        AVAILABLE_FRAMEWORKS.each do |name, desc|
          puts "  - #{name}: #{desc}"
        end
        exit 1
      end

      template_path = File.join(templates_dir, framework, "rule_template.md")
      target_path = File.join(rules_dir, "#{rule_name}.mdc")
      
      if File.exist?(target_path) && !options[:force]
        puts "❌ ルール '#{rule_name}' は既に存在します。上書きするには --force オプションを使用してください。".red
        exit 1
      end

      copy_with_extension(template_path, target_path)
      puts "✨ ルール '#{rule_name}' を作成しました。".green
    end

    private

    def create_rules_directory
      FileUtils.mkdir_p(rules_dir)
      FileUtils.mkdir_p(File.join(rules_dir, "errors"))
      puts "📁 ディレクトリを作成しました: #{rules_dir}".green
    end

    def copy_template_files(framework)
      puts "\n📝 テンプレートファイルをコピーしています..."

      template_files = Dir[File.join(templates_dir, framework, "*.md")]
      template_files.each do |template|
        filename = File.basename(template, ".md")
        target = if filename == "error_logging_guide"
                  File.join(rules_dir, "errors", "#{filename}.mdc")
                else
                  File.join(rules_dir, "#{filename}.mdc")
                end

        if File.exist?(target) && !options[:force]
          puts "  ⏩ #{filename}.mdc (スキップ: 既に存在します)".yellow
        else
          copy_with_extension(template, target)
          puts "  ✅ #{filename}.mdc".green
        end
      end
    end

    def copy_with_extension(source, target)
      content = File.read(source)
      File.write(target, content)
    end

    def rules_dir
      File.join(Dir.pwd, ".cursor", "rules")
    end

    def templates_dir
      File.expand_path("../crules/templates", File.dirname(__FILE__))
    end
  end
end 