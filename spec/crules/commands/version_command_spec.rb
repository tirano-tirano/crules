# frozen_string_literal: true

require "spec_helper"

RSpec.describe Crules::Commands::VersionCommand do
  describe "#execute" do
    let(:command) { described_class.new }

    it "バージョン情報を表示する" do
      expect { command.execute }.to output(/crules #{Crules::VERSION}/).to_stdout
    end

    it "Rubyのバージョン情報を表示する" do
      expect { command.execute }.to output(/Ruby #{RUBY_VERSION}/).to_stdout
    end

    it "実行環境の情報を表示する" do
      expect { command.execute }.to output(/実行環境: #{RUBY_PLATFORM}/).to_stdout
    end
  end
end 