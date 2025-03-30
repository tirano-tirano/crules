# frozen_string_literal: true

require "spec_helper"

RSpec.describe Crules::Commands::ListCommand do
  describe "#execute" do
    let(:command) { described_class.new }
    let(:rules_dir) { File.join(Dir.pwd, "rules") }

    before do
      FileUtils.mkdir_p(rules_dir)
    end

    after do
      FileUtils.rm_rf(rules_dir)
    end

    context "ルールが存在する場合" do
      before do
        File.write(File.join(rules_dir, "ruby.yml"), "name: Ruby\n")
        File.write(File.join(rules_dir, "python.yml"), "name: Python\n")
      end

      it "ルール一覧を表示する" do
        expect { command.execute }.to output(/Ruby/).to_stdout
        expect { command.execute }.to output(/Python/).to_stdout
      end

      it "ルールの総数を表示する" do
        expect { command.execute }.to output(/合計: 2件/).to_stdout
      end
    end

    context "ルールが存在しない場合" do
      it "ルールが存在しない旨を表示する" do
        expect { command.execute }.to output(/ルールが存在しません/).to_stdout
      end

      it "ルールの総数を0件と表示する" do
        expect { command.execute }.to output(/合計: 0件/).to_stdout
      end
    end

    context "ルールディレクトリが存在しない場合" do
      before do
        FileUtils.rm_rf(rules_dir)
      end

      it "ルールが存在しない旨を表示する" do
        expect { command.execute }.to output(/ルールが存在しません/).to_stdout
      end

      it "ルールの総数を0件と表示する" do
        expect { command.execute }.to output(/合計: 0件/).to_stdout
      end
    end
  end
end 