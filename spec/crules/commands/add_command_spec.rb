# frozen_string_literal: true

require "spec_helper"

RSpec.describe Crules::Commands::AddCommand do
  let(:template_dir) { File.join(File.dirname(__FILE__), "..", "..", "..", "lib", "crules", "templates") }
  let(:template_path) { File.join(template_dir, "rule-template.md") }
  let(:rules_dir) { File.join(".cursor", "rules") }

  before do
    # テンプレートディレクトリとファイルを作成
    FileUtils.mkdir_p(template_dir)
    File.write(template_path, "# テンプレート内容")

    # ルールディレクトリを作成
    FileUtils.mkdir_p(rules_dir)
  end

  after do
    # テストで作成したファイルを削除
    FileUtils.rm_f(template_path)
    FileUtils.rm_rf(rules_dir)
  end

  describe "#execute" do
    context "新規ルールを追加する場合" do
      let(:command) { described_class.new(["new-rule"]) }
      let(:target_path) { File.join(rules_dir, "new-rule.mdc") }

      it "ルールファイルを作成する" do
        command.execute
        expect(File).to exist(target_path)
      end

      it "成功メッセージを表示する" do
        expect { command.execute }.to output(/ルールファイルを作成しました: #{Regexp.escape(target_path)}/).to_stdout
      end
    end

    context "既存のルールを上書きする場合" do
      let(:command) { described_class.new(["existing-rule"], { force: true }) }
      let(:target_path) { File.join(rules_dir, "existing-rule.mdc") }

      before do
        # 既存のルールファイルを作成
        File.write(target_path, "既存のルール内容")
      end

      it "ルールファイルを上書きする" do
        command.execute
        expect(File.read(target_path)).to eq("# テンプレート内容")
      end

      it "成功メッセージを表示する" do
        expect { command.execute }.to output(/ルールファイルを作成しました: #{Regexp.escape(target_path)}/).to_stdout
      end
    end

    context "既存のルールをforceオプションなしで上書きしようとする場合" do
      let(:command) { described_class.new(["existing-rule"]) }
      let(:target_path) { File.join(rules_dir, "existing-rule.mdc") }

      before do
        # 既存のルールファイルを作成
        File.write(target_path, "既存のルール内容")
      end

      it "エラーメッセージを表示して終了する" do
        expect { command.execute }.to output(/エラー: ファイルが既に存在します/).to_stdout.and raise_error(SystemExit)
      end

      it "--forceオプションの使用を促すメッセージを表示する" do
        expect { begin; command.execute; rescue SystemExit; end }
          .to output(/上書きするには --force オプションを使用してください/).to_stdout
      end

      it "既存のファイルを変更しない" do
        begin; command.execute; rescue SystemExit; end
        expect(File.read(target_path)).to eq("既存のルール内容")
      end
    end

    context "テンプレートファイルが存在しない場合" do
      let(:command) { described_class.new(["new-rule"]) }

      before do
        # テンプレートファイルを削除
        FileUtils.rm_f(template_path)
      end

      it "エラーメッセージを表示して終了する" do
        expect { command.execute }.to output(/エラー: テンプレートファイルが見つかりません/).to_stdout.and raise_error(SystemExit)
      end
    end
  end
end 