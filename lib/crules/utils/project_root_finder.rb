# frozen_string_literal: true

module Crules
  module Utils
    class ProjectRootFinder
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

      def self.find
        new.find
      end

      def find
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
    end
  end
end 