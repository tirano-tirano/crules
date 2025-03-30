# frozen_string_literal: true

require "spec_helper"
require "fileutils"
require "tmpdir"

RSpec.describe Crules::Utils::RuleSetFinder do
  let(:finder) { described_class.new }

  describe "#find_available_rule_sets" do
    let(:templates_dir) { File.join(File.dirname(__FILE__), "..", "..", "..", "lib", "crules", "templates", "templates") }

    before do
      FileUtils.mkdir_p(templates_dir)
    end

    after do
      FileUtils.rm_rf(templates_dir)
    end

    context "ルールセットが存在する場合" do
      before do
        FileUtils.mkdir_p(File.join(templates_dir, "test_set"))
        File.write(File.join(templates_dir, "test_set", "README.md"), "# Test Rule Set\n")
      end

      it "利用可能なルールセットを返す" do
        rule_sets = finder.find_available_rule_sets
        expect(rule_sets).to include("test_set" => "Test Rule Set")
      end
    end

    context "READMEがない場合" do
      before do
        FileUtils.mkdir_p(File.join(templates_dir, "no_readme_set"))
      end

      it "ディレクトリ名をそのまま説明として使用" do
        rule_sets = finder.find_available_rule_sets
        expect(rule_sets).to include("no_readme_set" => "no_readme_set")
      end
    end
  end

  describe "#copy_rule_set" do
    around do |example|
      Dir.mktmpdir do |dir|
        Dir.chdir(dir) do
          example.run
        end
      end
    end

    let(:source_dir) { File.join(Dir.pwd, "templates") }
    let(:target_dir) { File.join(Dir.pwd, ".cursor", "rules") }

    before do
      FileUtils.mkdir_p(File.join(source_dir, "test_set"))
      File.write(File.join(source_dir, "test_set", "test.md"), "test content")
    end

    context "正常系" do
      it "ルールセットをコピーする" do
        finder.copy_rule_set("test_set")
        expect(File.exist?(File.join(target_dir, "test.mdc"))).to be true
      end
    end

    context "ファイルが既に存在する場合" do
      before do
        FileUtils.mkdir_p(target_dir)
        File.write(File.join(target_dir, "test.mdc"), "existing content")
      end

      it "forceオプションなしではスキップする" do
        finder.copy_rule_set("test_set")
        expect(File.read(File.join(target_dir, "test.mdc"))).to eq("existing content")
      end

      it "forceオプションありでは上書きする" do
        finder.copy_rule_set("test_set", true)
        expect(File.read(File.join(target_dir, "test.mdc"))).to eq("test content")
      end
    end
  end
end 