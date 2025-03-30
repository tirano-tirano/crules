# frozen_string_literal: true

require "spec_helper"

RSpec.describe Crules::Commands::RemoveCommand do
  describe "#execute" do
    let(:command) { described_class.new(rule_name) }
    let(:rule_name) { "test_rule" }
    let(:rules_dir) { File.join(Dir.pwd, "rules") }
    let(:rule_file) { File.join(rules_dir, "#{rule_name}.yml") }

    before do
      FileUtils.mkdir_p(rules_dir)
    end

    after do
      FileUtils.rm_rf(rules_dir)
    end

    context "指定したルールが存在する場合" do
      before do
        File.write(rule_file, "name: TestRule\n")
      end

      it "ルールを削除する" do
        expect { command.execute }.to output(/ルール 'test_rule' を削除しました/).to_stdout
        expect(File.exist?(rule_file)).to be false
      end
    end

    context "指定したルールが存在しない場合" do
      it "エラーメッセージを表示する" do
        expect { command.execute }.to output(/ルール 'test_rule' が見つかりません/).to_stdout
      end
    end

    context "ルールディレクトリが存在しない場合" do
      before do
        FileUtils.rm_rf(rules_dir)
      end

      it "エラーメッセージを表示する" do
        expect { command.execute }.to output(/ルールディレクトリが見つかりません/).to_stdout
      end
    end

    context "ルールの削除に失敗した場合" do
      before do
        File.write(rule_file, "name: TestRule\n")
        allow(File).to receive(:delete).with(rule_file).and_raise(Errno::EACCES)
      end

      it "エラーメッセージを表示する" do
        expect { command.execute }.to output(/ルール 'test_rule' の削除に失敗しました/).to_stdout
      end
    end
  end
end 