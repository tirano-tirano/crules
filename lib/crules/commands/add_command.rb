# frozen_string_literal: true

module Crules
  module Commands
    # 新規ルールを追加するコマンドクラス
    #
    # @example コマンドラインからの使用
    #   $ crules add new-rule
    #   $ crules add existing-rule --force
    #
    # @example プログラムからの使用
    #   command = AddCommand.new(["new-rule"], {"force" => true})
    #   command.execute
    #
    # @note このコマンドは以下の機能を提供します：
    #   - テンプレートを使用した新規ルールファイルの作成
    #   - 既存のファイルの上書き制御
    #   - ルールファイルの配置先ディレクトリの自動作成
    class AddCommand < Thor::Group
      include Thor::Actions

      # コマンドライン引数の定義
      # @!attribute [r] rule_name
      #   @return [String] 追加するルールの名前
      argument :rule_name, type: :string, desc: "追加するルールの名前"

      # コマンドラインオプションの定義
      # @!attribute [r] options
      #   @return [Hash] コマンドラインオプション
      class_option :force, type: :boolean, default: false, desc: "既存のファイルを上書き"

      # コマンドを実行する
      #
      # @return [void]
      #
      # @raise [SystemExit] テンプレートファイルが見つからない場合
      # @raise [SystemExit] 既存のファイルが存在し、forceオプションが指定されていない場合
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