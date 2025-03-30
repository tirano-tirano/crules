# frozen_string_literal: true

require "thor"
require "fileutils"
require "pathname"

require_relative "version"
require_relative "commands/init_command"
require_relative "commands/add_command"
require_relative "commands/version_command"

module Crules
  class CLI < Thor
    # プロジェクトルートの判定に使用するファイルやディレクトリ
    PROJECT_ROOT_INDICATORS = {
      # バージョン管理システム
      ".git" => :directory,
      ".svn" => :directory,
      ".hg" => :directory,
      # パッケージマネージャー
      "package.json" => :file,
      "pubspec.yaml" => :file,
      "Cargo.toml" => :file,
      "Gemfile" => :file,
      "requirements.txt" => :file,
      "pyproject.toml" => :file,
      "composer.json" => :file,
      "go.mod" => :file,
      # ビルドシステム
      "Makefile" => :file,
      "CMakeLists.txt" => :file,
      "build.gradle" => :file,
      "pom.xml" => :file,
      # IDE/エディタ
      ".idea" => :directory,
      ".vscode" => :directory,
      ".cursor" => :directory
    }.freeze

    def self.exit_on_failure?
      true
    end

    package_name "crules"

    desc "version", "バージョン表示"
    def version
      Commands::VersionCommand.new.execute
    end

    desc "init [--rule-set <rule_set>] [--force]", "ルールセットの初期化"
    method_option :rule_set, type: :string, default: "default", desc: "使用するルールセット"
    method_option :force, type: :boolean, default: false, desc: "既存のファイルを上書き"
    def init
      Commands::InitCommand.new(options).execute
    end

    desc "add <rule_name> [--force]", "新規ルールの追加"
    method_option :force, type: :boolean, default: false, desc: "既存のファイルを上書き"
    def add(rule_name)
      Commands::AddCommand.new([rule_name], options).execute
    end

    private

    def find_project_root
      current_dir = Dir.pwd
      loop do
        # プロジェクトルートの判定
        PROJECT_ROOT_INDICATORS.each do |indicator, type|
          path = File.join(current_dir, indicator)
          if (type == :directory && Dir.exist?(path)) || (type == :file && File.exist?(path))
            puts "📂 プロジェクトルートを検出: #{current_dir}"
            return current_dir
          end
        end

        # 親ディレクトリに移動
        parent_dir = File.dirname(current_dir)
        break if parent_dir == current_dir
        current_dir = parent_dir
      end

      puts "⚠️ プロジェクトルートが見つからないため、現在のディレクトリを使用します: #{Dir.pwd}"
      Dir.pwd
    end

    def find_available_rule_sets
      rule_sets = {}
      templates_dir = File.join(File.dirname(__FILE__), "templates", "templates")

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
      source_dir = File.join(File.dirname(__FILE__), "templates", "templates", rule_set)
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