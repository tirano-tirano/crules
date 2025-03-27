# frozen_string_literal: true

require "thor"
require "fileutils"
require "pathname"
require_relative "version"

module Crules
  class CLI < Thor
    AVAILABLE_FRAMEWORKS = {
      "flutter" => "Flutterプロジェクト用のテンプレート",
      "default" => "汎用的なテンプレート"
    }.freeze

    class_option :framework, type: :string, default: "default"
    class_option :force, type: :boolean, default: false

    desc "version", "バージョン情報を表示"
    def version
      puts "crules v#{Crules::VERSION}"
    end

    desc "init", "Cursorルールを初期化"
    def init
      puts "🚀 Cursorルールの初期化を開始します..."

      framework = options[:framework]
      unless AVAILABLE_FRAMEWORKS.key?(framework)
        puts "❌ 無効なフレームワークです: #{framework}"
        puts "利用可能なフレームワーク:"
        AVAILABLE_FRAMEWORKS.each do |name, description|
          puts "  - #{name}: #{description}"
        end
        exit 1
      end

      rules_dir = File.join(Dir.pwd, ".cursor", "rules")
      FileUtils.mkdir_p(rules_dir)

      copy_template_files(framework, rules_dir)
      puts "✅ Cursorルールの初期化が完了しました"
    end

    desc "add <rule_name>", "新しいルールを追加"
    def add(rule_name)
      rules_dir = File.join(Dir.pwd, ".cursor", "rules")
      unless Dir.exist?(rules_dir)
        puts "❌ .cursor/rulesディレクトリが見つかりません"
        puts "先に`crules init`を実行してください"
        exit 1
      end

      rule_file = File.join(rules_dir, "#{rule_name}.mdc")
      if File.exist?(rule_file) && !options[:force]
        puts "❌ ルールファイルが既に存在します: #{rule_file}"
        puts "上書きする場合は`--force`オプションを使用してください"
        exit 1
      end

      template_file = File.join(File.dirname(__FILE__), "templates", "default", "rule_template.md")
      unless File.exist?(template_file)
        puts "❌ テンプレートファイルが見つかりません: #{template_file}"
        exit 1
      end

      FileUtils.cp(template_file, rule_file)
      puts "✅ ルールファイルを作成しました: #{rule_file}"
    end

    private

    def copy_template_files(framework, target_dir)
      source_dir = File.join(File.dirname(__FILE__), "templates", framework)
      unless Dir.exist?(source_dir)
        puts "❌ テンプレートディレクトリが見つかりません: #{source_dir}"
        exit 1
      end

      # ディレクトリ構造を保持しながら、.mdファイルを.mdcにコピー
      Dir.glob(File.join(source_dir, "**", "*.md")).each do |source_file|
        relative_path = Pathname.new(source_file).relative_path_from(Pathname.new(source_dir))
        target_file = File.join(target_dir, relative_path.to_s.sub(/\.md$/, ".mdc"))
        target_dir_path = File.dirname(target_file)

        # 既存のファイルをチェック
        if File.exist?(target_file) && !options[:force]
          puts "❌ ファイルが既に存在します: #{target_file}"
          puts "上書きする場合は`--force`オプションを使用してください"
          exit 1
        end

        # ディレクトリを作成してファイルをコピー
        FileUtils.mkdir_p(target_dir_path)
        FileUtils.cp(source_file, target_file)
      end
    end
  end
end 