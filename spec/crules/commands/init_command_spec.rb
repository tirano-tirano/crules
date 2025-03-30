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
    allow(rule_set_finder).to receive(:copy_rule_set).with(any_args)
  end

  describe "#execute" do
    let(:command) { described_class.new }
    let(:rules_dir) { File.join(Dir.pwd, "rules") }

    before do
      FileUtils.rm_rf(rules_dir) if Dir.exist?(rules_dir)
    end

    after do
      FileUtils.rm_rf(rules_dir)
    end

    context "ルールディレクトリが存在しない場合" do
      it "ルールディレクトリを作成する" do
        expect { command.execute }.to output(/ルールセット 'default' の初期化が完了しました/).to_stdout
      end

      it "デフォルトのルールをコピーする" do
        expect(rule_set_finder).to receive(:copy_rule_set).with("default", false)
        command.execute
      end
    end

    context "ルールディレクトリが既に存在する場合" do
      before do
        FileUtils.mkdir_p(rules_dir)
      end

      it "エラーメッセージを表示する" do
        expect(rule_set_finder).to receive(:copy_rule_set).with("default", false)
        expect { command.execute }.to output(/ルールセット 'default' の初期化が完了しました/).to_stdout
      end

      it "既存のルールディレクトリを変更しない" do
        original_files = Dir.glob(File.join(rules_dir, "*"))
        expect(rule_set_finder).to receive(:copy_rule_set).with("default", false)
        command.execute
        expect(Dir.glob(File.join(rules_dir, "*"))).to match_array(original_files)
      end
    end

    context "ルールディレクトリの作成に失敗した場合" do
      before do
        allow(rule_set_finder).to receive(:copy_rule_set).with("default", false).and_raise(Errno::EACCES)
      end

      it "エラーメッセージを表示する" do
        expect { command.execute }.to output(/ルールディレクトリの作成に失敗しました/).to_stdout
      end
    end

    context "デフォルトルールのコピーに失敗した場合" do
      before do
        allow(rule_set_finder).to receive(:copy_rule_set).with("default", false).and_raise(StandardError)
      end

      it "エラーメッセージを表示する" do
        expect { command.execute }.to output(/デフォルトルールのコピーに失敗しました/).to_stdout
      end
    end

    context "デフォルトのルールセットを指定した場合" do
      let(:command) { described_class.new([], { rule_set: "default" }) }

      it "デフォルトのルールセットをコピーする" do
        expect(rule_set_finder).to receive(:copy_rule_set).with("default", false)
        command.execute
      end
    end

    context "存在するカスタムルールセットを指定した場合" do
      let(:command) { described_class.new([], { rule_set: "custom" }) }

      it "指定したルールセットをコピーする" do
        expect(rule_set_finder).to receive(:copy_rule_set).with("custom", false)
        command.execute
      end
    end

    context "forceオプションを指定した場合" do
      let(:command) { described_class.new([], { rule_set: "default", force: true }) }

      it "強制上書きオプション付きでルールセットをコピーする" do
        expect(rule_set_finder).to receive(:copy_rule_set).with("default", true)
        command.execute
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