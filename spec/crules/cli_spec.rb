# frozen_string_literal: true

require "spec_helper"
require "crules/cli"
require "crules/version"
require "fileutils"

RSpec.describe Crules::CLI do
  let(:cli) { described_class.new }

  describe "#version" do
    it "displays the version number" do
      expect { cli.version }.to output("crules v#{Crules::VERSION}\n").to_stdout
    end
  end

  describe "#init" do
    let(:rules_dir) { File.join(Dir.pwd, ".cursor", "rules") }
    let(:errors_dir) { File.join(rules_dir, "errors") }

    before do
      FileUtils.rm_rf(rules_dir) if Dir.exist?(rules_dir)
    end

    after do
      FileUtils.rm_rf(rules_dir) if Dir.exist?(rules_dir)
    end

    context "with default framework" do
      it "creates necessary directories" do
        cli.options = { "framework" => "default" }
        cli.init
        expect(Dir.exist?(rules_dir)).to be true
        expect(Dir.exist?(errors_dir)).to be true
      end

      it "copies template files" do
        cli.options = { "framework" => "default" }
        cli.init
        expect(File.exist?(File.join(rules_dir, "rule_template.mdc"))).to be true
      end
    end

    context "with flutter framework" do
      it "creates necessary directories" do
        cli.options = { "framework" => "flutter" }
        cli.init
        expect(Dir.exist?(rules_dir)).to be true
        expect(Dir.exist?(errors_dir)).to be true
      end

      it "copies template files" do
        cli.options = { "framework" => "flutter" }
        cli.init
        expect(File.exist?(File.join(rules_dir, "rule_template.mdc"))).to be true
      end
    end

    context "with invalid framework" do
      it "displays error message" do
        cli.options = { "framework" => "invalid" }
        expect { cli.init }.to output(/無効なフレームワークです/).to_stdout
      end
    end
  end

  describe "#add" do
    let(:rules_dir) { File.join(Dir.pwd, ".cursor", "rules") }
    let(:rule_name) { "test_rule" }
    let(:rule_path) { File.join(rules_dir, "#{rule_name}.mdc") }

    before do
      FileUtils.mkdir_p(rules_dir)
    end

    after do
      FileUtils.rm_rf(rules_dir)
    end

    it "creates a new rule file" do
      cli.options = { "framework" => "default" }
      cli.add(rule_name)
      expect(File.exist?(rule_path)).to be true
    end

    context "when file already exists" do
      before do
        File.write(rule_path, "existing content")
      end

      it "does not overwrite without force option" do
        cli.options = { "framework" => "default" }
        cli.add(rule_name)
        expect(File.read(rule_path)).to eq("existing content")
      end

      it "overwrites with force option" do
        cli.options = { "framework" => "default", "force" => true }
        cli.add(rule_name)
        expect(File.read(rule_path)).not_to eq("existing content")
      end
    end

    context "with invalid framework" do
      it "displays error message" do
        cli.options = { "framework" => "invalid" }
        expect { cli.add(rule_name) }.to output(/無効なフレームワークです/).to_stdout
      end
    end
  end
end 