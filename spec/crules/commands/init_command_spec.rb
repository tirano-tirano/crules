# frozen_string_literal: true

require "spec_helper"

RSpec.describe Crules::Commands::InitCommand do
  let(:rule_set_finder) { instance_double(Crules::Utils::RuleSetFinder) }
  let(:available_rule_sets) do
    {
      "default" => "デフォルトのルールセット",
      "custom" => "カスタムルールセット"
    }
  end

  before do
    allow(Crules::Utils::RuleSetFinder).to receive(:new).and_return(rule_set_finder)
    allow(rule_set_finder).to receive(:find_available_rule_sets).and_return(available_rule_sets)
  end

  describe "#execute" do
    context "デフォルトのルールセットを指定した場合" do
      let(:command) { described_class.new([], { rule_set: "default" }) }

      it "デフォルトのルールセットをコピーする" do
        allow(rule_set_finder).to receive(:copy_rule_set).with("default", false)
        expect { command.execute }.to output(/ルールセット 'default' の初期化が完了しました/).to_stdout
      end
    end

    context "存在するカスタムルールセットを指定した場合" do
      let(:command) { described_class.new([], { rule_set: "custom" }) }

      it "指定したルールセットをコピーする" do
        allow(rule_set_finder).to receive(:copy_rule_set).with("custom", false)
        expect { command.execute }.to output(/ルールセット 'custom' の初期化が完了しました/).to_stdout
      end
    end

    context "forceオプションを指定した場合" do
      let(:command) { described_class.new([], { rule_set: "default", force: true }) }

      it "強制上書きオプション付きでルールセットをコピーする" do
        allow(rule_set_finder).to receive(:copy_rule_set).with("default", true)
        expect { command.execute }.to output(/ルールセット 'default' の初期化が完了しました/).to_stdout
      end
    end

    context "存在しないルールセットを指定した場合" do
      let(:command) { described_class.new([], { rule_set: "nonexistent" }) }

      it "エラーメッセージを表示して終了する" do
        expect { command.execute }.to output(/エラー: 無効なルールセット 'nonexistent'/).to_stdout.and raise_error(SystemExit)
      end

      it "利用可能なルールセットの一覧を表示する" do
        expect { begin; command.execute; rescue SystemExit; end }.to output(/利用可能なルールセット:/).to_stdout
        expect { begin; command.execute; rescue SystemExit; end }.to output(/default: デフォルトのルールセット/).to_stdout
        expect { begin; command.execute; rescue SystemExit; end }.to output(/custom: カスタムルールセット/).to_stdout
      end
    end
  end
end 