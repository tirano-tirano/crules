# frozen_string_literal: true

require_relative "../version"

module Crules
  module Commands
    # バージョン情報を表示するコマンドクラス
    #
    # @example コマンドラインからの使用
    #   $ crules version
    #   crules 0.2.2
    #
    # @example プログラムからの使用
    #   command = VersionCommand.new
    #   command.execute  # => "crules 0.2.2"を出力
    #
    # @note このコマンドは以下の機能を提供します：
    #   - crulesのバージョン情報の表示
    class VersionCommand < Thor::Group
      include Thor::Actions

      # コマンドを実行する
      #
      # @return [void]
      def execute
        puts "crules #{Crules::VERSION}"
      end
    end
  end
end 