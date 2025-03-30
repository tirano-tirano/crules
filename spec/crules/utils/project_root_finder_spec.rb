# frozen_string_literal: true

require "spec_helper"
require "fileutils"
require "tmpdir"

RSpec.describe Crules::Utils::ProjectRootFinder do
  let(:finder) { described_class.new }

  describe "#find" do
    around do |example|
      Dir.mktmpdir do |dir|
        Dir.chdir(dir) do
          example.run
        end
      end
    end

    context "プロジェクトルートが見つかる場合" do
      before do
        FileUtils.mkdir_p(".git")
      end

      it "プロジェクトルートのパスを返す" do
        expect(finder.find).to eq(Dir.pwd)
      end
    end

    context "プロジェクトルートが見つからない場合" do
      it "現在のディレクトリを返す" do
        expect(finder.find).to eq(Dir.pwd)
      end
    end

    context "親ディレクトリにプロジェクトルートがある場合" do
      before do
        FileUtils.mkdir_p("subdir")
        FileUtils.mkdir_p(".git")
        Dir.chdir("subdir")
      end

      it "親ディレクトリのパスを返す" do
        expect(finder.find).to eq(File.dirname(Dir.pwd))
      end
    end
  end
end 