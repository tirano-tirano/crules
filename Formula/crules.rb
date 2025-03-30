class Crules < Formula
  desc "Cursor IDEのルールを効率的に管理するためのCLIツール"
  homepage "https://github.com/tirano-tirano/crules"
  url "https://github.com/tirano-tirano/crules/archive/refs/tags/v0.2.2.tar.gz"
  sha256 "8ed66d63db90152e4e4fb4aee627ef50a8708bdeab2a507ed145ea92de793188"

  depends_on "ruby"

  def install
    ENV["GEM_HOME"] = libexec
    system "gem", "build", "crules.gemspec"
    system "gem", "install", "crules-0.2.2.gem", "--install-dir", libexec
    bin.install libexec/"bin/crules"
    bin.env_script_all_files(libexec/"bin", GEM_HOME: ENV["GEM_HOME"])
  end

  test do
    system "#{bin}/crules", "version"
  end
end 