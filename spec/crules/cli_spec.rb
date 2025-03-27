# frozen_string_literal: true

require "spec_helper"
require "crules/cli"
require "crules/version"
require "fileutils"

RSpec.describe Crules::CLI do
  let(:cli) { described_class.new }
  let(:templates_dir) { File.join(File.dirname(__FILE__), "..", "..", "lib", "crules", "templates") }
  let(:rules_dir) { File.join(Dir.pwd, ".cursor", "rules") }

  before do
    FileUtils.rm_rf(rules_dir) if Dir.exist?(rules_dir)
  end

  describe "#version" do
    it "displays the version number" do
      expect { cli.version }.to output(/crules v#{Crules::VERSION}/).to_stdout
    end
  end

  describe "#init" do
    context "デフォルトフレームワークの場合" do
      it "デフォルトテンプレートをコピーする" do
        cli.init
        expect(Dir.exist?(rules_dir)).to be true
        expect(File.exist?(File.join(rules_dir, "rule_template.mdc"))).to be true
      end
    end

    context "Flutterフレームワークの場合" do
      it "Flutterテンプレートをコピーする" do
        cli.options = { framework: "flutter" }
        cli.init
        expect(Dir.exist?(rules_dir)).to be true
        expect(File.exist?(File.join(rules_dir, "01_ai_behavior.mdc"))).to be true
        expect(File.exist?(File.join(rules_dir, "errors", "error_logging_guide.mdc"))).to be true
      end

      it "ディレクトリ構造を保持する" do
        cli.options = { framework: "flutter" }
        cli.init
        expect(Dir.exist?(File.join(rules_dir, "errors"))).to be true
      end
    end

    context "無効なフレームワークの場合" do
      it "エラーメッセージを表示して終了する" do
        cli.options = { framework: "invalid" }
        expect { cli.init }.to raise_error(SystemExit)
      end
    end

    context "既存のファイルがある場合" do
      before do
        FileUtils.mkdir_p(rules_dir)
        FileUtils.touch(File.join(rules_dir, "01_ai_behavior.mdc"))
      end

      it "エラーメッセージを表示する" do
        cli.options = { framework: "flutter" }
        expect { cli.init }.to output(/既に存在します/).to_stdout
      end

      it "--forceオプションで上書きする" do
        cli.options = { framework: "flutter", force: true }
        cli.init
        expect(File.exist?(File.join(rules_dir, "01_ai_behavior.mdc"))).to be true
      end
    end
  end

  describe "#add" do
    before do
      FileUtils.mkdir_p(rules_dir)
    end

    it "デフォルトテンプレートから新しいルールを作成する" do
      cli.add("my_rule")
      expect(File.exist?(File.join(rules_dir, "my_rule.mdc"))).to be true
    end

    context "既存のファイルがある場合" do
      before do
        FileUtils.touch(File.join(rules_dir, "my_rule.mdc"))
      end

      it "エラーメッセージを表示する" do
        expect { cli.add("my_rule") }.to raise_error(SystemExit)
      end

      it "--forceオプションで上書きする" do
        cli.options = { force: true }
        cli.add("my_rule")
        expect(File.exist?(File.join(rules_dir, "my_rule.mdc"))).to be true
      end
    end
  end
end 