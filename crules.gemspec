# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "crules"
  spec.version       = Crules::VERSION
  spec.authors       = ["Your Name"]
  spec.email         = ["your.email@example.com"]

  spec.summary       = "CLI tool for generating Cursor rules for Flutter projects"
  spec.description   = "A command-line tool that generates and manages Cursor rules (.mdc files) for Flutter projects"
  spec.homepage      = "https://github.com/yourusername/crules"
  spec.license       = "MIT"
  spec.required_ruby_version = ">= 2.6.0"

  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = spec.homepage
  spec.metadata["changelog_uri"] = "#{spec.homepage}/blob/main/CHANGELOG.md"

  spec.files = Dir.glob("{bin,lib}/**/*")
  spec.bindir        = "bin"
  spec.executables   = ["crules"]
  spec.require_paths = ["lib"]

  spec.add_dependency "thor", "~> 1.3"
  spec.add_dependency "activesupport", "~> 7.1"
  spec.add_dependency "colorize", "~> 1.1"
  spec.add_dependency "fileutils", "~> 1.7"
  spec.add_dependency "json", "~> 2.6"

  spec.add_development_dependency "rake", "~> 13.0"
  spec.add_development_dependency "rspec", "~> 3.12"
  spec.add_development_dependency "rubocop", "~> 1.60"
  spec.add_development_dependency "rubocop-rspec", "~> 2.26"
end 