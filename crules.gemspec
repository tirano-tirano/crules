# frozen_string_literal: true

require_relative "lib/crules/version"

Gem::Specification.new do |spec|
  spec.name          = "crules"
  spec.version       = Crules::VERSION
  spec.authors       = ["John Smith"]
  spec.email         = ["john.smith@example.com"]

  spec.summary       = "Cursorルールを管理するためのCLIツール"
  spec.description   = "プロジェクトタイプに応じたルールセットを管理するためのコマンドラインツール。Flutterプロジェクトを含む、様々なプロジェクトタイプに対応。"
  spec.homepage      = "https://github.com/johnsmith/crules"
  spec.license       = "MIT"
  spec.required_ruby_version = ">= 2.6.0"

  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = spec.homepage
  spec.metadata["changelog_uri"] = "#{spec.homepage}/blob/main/CHANGELOG.md"

  spec.files = Dir.glob("{bin,lib}/**/*")
  spec.bindir        = "bin"
  spec.executables   = spec.files.grep(%r{^bin/}) { |f| File.basename(f) }
  spec.require_paths = ["lib"]

  spec.add_dependency "thor", "~> 1.0"
  spec.add_dependency "pastel", "~> 0.8.0"

  spec.add_development_dependency "rspec", "~> 3.0"
  spec.add_development_dependency "rubocop", "~> 1.0"
end 