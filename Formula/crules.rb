class Crules < Formula
  desc "Cursor IDEのルールを効率的に管理するためのCLIツール"
  homepage "https://github.com/tirano-tirano/crules"
  url "https://github.com/tirano-tirano/crules/archive/refs/tags/v0.2.2.tar.gz"
  sha256 "6254ed22da8414bd101d3b5b7b4e3a94a45c18f2cd2c86e79935584445c4789b"

  depends_on "ruby"

  def install
    ENV["GEM_HOME"] = libexec
    ENV["GEM_PATH"] = libexec

    system "gem", "install", "bundler"
    system "bundle", "install"
    system "gem", "build", "crules.gemspec"
    system "gem", "install", "--local", "crules-#{version}.gem"

    bin.install Dir["#{libexec}/bin/*"]
    bin.env_script_all_files(libexec/"bin", GEM_HOME: ENV["GEM_HOME"], GEM_PATH: ENV["GEM_PATH"])
  end

  test do
    system "#{bin}/crules", "version"
  end
end 