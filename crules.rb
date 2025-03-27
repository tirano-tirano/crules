# frozen_string_literal: true

class Crules < Formula
  desc "Flutterプロジェクト用のCursorルール（.mdcファイル）を生成・管理するためのコマンドラインツール"
  homepage "https://github.com/tirano-tirano/crules"
  url "https://github.com/tirano-tirano/crules/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "YOUR_SHA256_HASH" # リリース時に更新が必要

  depends_on "ruby"

  def install
    ENV["GEM_HOME"] = libexec
    system "gem", "build", "crules.gemspec"
    system "gem", "install", "crules-#{version}.gem", "--install-dir", libexec
    bin.install libexec/"bin/crules"
    bin.env_script_all_files(libexec/"bin", GEM_HOME: ENV["GEM_HOME"])
  end

  test do
    system "#{bin}/crules", "--version"
  end
end 