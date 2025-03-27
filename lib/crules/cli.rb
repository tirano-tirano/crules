# frozen_string_literal: true

require "thor"
require "pastel"
require "crules/version"
require "fileutils"

module Crules
  class CLI < Thor
    package_name "crules"

    AVAILABLE_FRAMEWORKS = {
      "flutter" => "Flutterプロジェクト用のテンプレート",
      "default" => "汎用的なテンプレート"
    }.freeze

    def initialize(*args)
      super
      @pastel = Pastel.new
      @options = {}
    end

    attr_writer :options

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
    def init(*args)
      puts @pastel.green("🚀 Cursorルールの初期化を開始します...")

      framework = @options["framework"] || options[:framework]
      unless AVAILABLE_FRAMEWORKS.key?(framework)
        puts @pastel.red("❌ 無効なフレームワークです: #{framework}")
        puts "利用可能なフレームワーク:"
        AVAILABLE_FRAMEWORKS.each do |name, desc|
          puts "  - #{name}: #{desc}"
        end
        exit 1
      end

      puts @pastel.green("📦 フレームワーク: #{framework} (#{AVAILABLE_FRAMEWORKS[framework]})")

      create_rules_directory
      copy_template_files(framework)

      puts "\n" + @pastel.green("✨ 初期化が完了しました！")
    end

    desc "add RULE_NAME", "新しいルールファイルを追加"
    method_option :force, type: :boolean, default: false, aliases: "-f",
                 desc: "既存のファイルを上書き"
    method_option :framework, type: :string, default: "default",
                 desc: "使用するフレームワークを指定 (flutter, default)"
    def add(rule_name, *args)
      framework = @options["framework"] || options[:framework]
      unless AVAILABLE_FRAMEWORKS.key?(framework)
        puts @pastel.red("❌ 無効なフレームワークです: #{framework}")
        puts "利用可能なフレームワーク:"
        AVAILABLE_FRAMEWORKS.each do |name, desc|
          puts "  - #{name}: #{desc}"
        end
        exit 1
      end

      template_path = File.join(templates_dir, framework, "rule_template.md")
      target_path = File.join(rules_dir, "#{rule_name}.mdc")
      
      if File.exist?(target_path) && !(@options["force"] || options[:force])
        puts @pastel.red("❌ ルール '#{rule_name}' は既に存在します。上書きするには --force オプションを使用してください。")
        exit 1
      end

      copy_with_extension(template_path, target_path)
      puts @pastel.green("✨ ルール '#{rule_name}' を作成しました。")
    end

    private

    def create_rules_directory
      FileUtils.mkdir_p(rules_dir)
      FileUtils.mkdir_p(File.join(rules_dir, "errors"))
      puts @pastel.green("📁 ディレクトリを作成しました: #{rules_dir}")
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

        if File.exist?(target) && !(@options["force"] || options[:force])
          puts @pastel.yellow("⚠️ ファイルが既に存在します: #{target}")
          next
        end

        copy_with_extension(template, target)
        puts @pastel.green("✨ テンプレートをコピーしました: #{target}")
      end

      # rule_template.mdを必ずコピー
      template_path = File.join(templates_dir, framework, "rule_template.md")
      target_path = File.join(rules_dir, "rule_template.mdc")
      copy_with_extension(template_path, target_path)
    end

    def copy_with_extension(source, target)
      FileUtils.mkdir_p(File.dirname(target))
      FileUtils.cp(source, target)
    end

    def rules_dir
      File.join(Dir.pwd, ".cursor", "rules")
    end

    def templates_dir
      File.join(File.dirname(__FILE__), "templates")
    end
  end
end 