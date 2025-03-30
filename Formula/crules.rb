class Crules < Formula
  desc "Cursor IDEのルールを効率的に管理するためのCLIツール"
  homepage "https://github.com/tirano-tirano/crules"
  url "https://github.com/tirano-tirano/crules/archive/refs/tags/v0.2.2.tar.gz"
  sha256 "6254ed22da8414bd101d3b5b7b4e3a94a45c18f2cd2c86e79935584445c4789b"

  depends_on "ruby"

  def install
    ENV["GEM_HOME"] = libexec
    ENV["GEM_PATH"] = libexec
    ENV["BUNDLE_GEMFILE"] = "#{buildpath}/Gemfile"
    ENV["BUNDLE_PATH"] = "#{libexec}/vendor/bundle"

    system "gem", "install", "bundler"
    system "bundle", "install"
    system "bundle", "exec", "gem", "build", "crules.gemspec"
    system "bundle", "exec", "gem", "install", "--ignore-dependencies", "--no-document", "--install-dir", libexec, "crules-#{version}.gem"

    (bin/"crules").write <<~EOS
      #!/bin/bash
      export GEM_HOME="#{libexec}"
      export GEM_PATH="#{libexec}"
      export BUNDLE_GEMFILE="#{prefix}/Gemfile"
      export BUNDLE_PATH="#{libexec}/vendor/bundle"
      exec "#{libexec}/bin/crules" "$@"
    EOS

    prefix.install "Gemfile", "Gemfile.lock"
  end

  test do
    system "#{bin}/crules", "version"
  end
end 