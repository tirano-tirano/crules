# frozen_string_literal: true

module Crules
  module Commands
    # 全コマンドの基底クラス
    #
    # @abstract 各コマンドクラスはこのクラスを継承して実装します
    class BaseCommand
      # コマンドを実行する
      #
      # @abstract 各コマンドクラスでオーバーライドして実装します
      # @return [void]
      def execute
        raise NotImplementedError, "#{self.class}##{__method__} must be implemented"
      end
    end
  end
end 