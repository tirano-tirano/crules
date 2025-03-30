# frozen_string_literal: true

module Crules
  module Utils
    # プロジェクトのルートディレクトリを検出するためのユーティリティクラス
    #
    # @example 基本的な使用方法
    #   finder = ProjectRootFinder.new
    #   root_path = finder.find  # => "/path/to/project"
    #
    # @example クラスメソッドを使用した検出
    #   root_path = ProjectRootFinder.find  # => "/path/to/project"
    #
    # @note このクラスは以下のような指標を使用してプロジェクトルートを判定します：
    #   - バージョン管理システムのディレクトリ（.git, .svn, .hg）
    #   - パッケージマネージャーの設定ファイル（package.json, Gemfile等）
    #   - ビルドシステムの設定ファイル（Makefile, build.gradle等）
    #   - IDE/エディタの設定ディレクトリ（.idea, .vscode, .cursor）
    class ProjectRootFinder
      # プロジェクトルートの判定に使用するファイルやディレクトリ
      #
      # @return [Hash<String, Symbol>] 指標名とそのタイプ（:directory または :file）のマッピング
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

      # プロジェクトルートを検出する（クラスメソッド）
      #
      # @return [String] 検出されたプロジェクトルートのパス
      # @see #find インスタンスメソッドの実装
      def self.find
        new.find
      end

      # プロジェクトルートを検出する
      #
      # @return [String] 検出されたプロジェクトルートのパス
      # @note プロジェクトルートが見つからない場合は現在のディレクトリを返します
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