# frozen_string_literal: true

require_relative "lib/crules/version"

Gem::Specification.new do |spec|
  spec.name          = "crules"
  spec.version       = Crules::VERSION
  spec.authors       = ["tirano-tirano"]
  spec.email         = ["tirano.tirano@gmail.com"]

  spec.summary       = "A command-line tool to generate and manage Cursor rules (.mdc files) for various frameworks"
  spec.description   = "A command-line tool to generate and manage Cursor rules (.mdc files) for various frameworks"
  spec.homepage      = "https://github.com/tirano-tirano/crules"
  spec.license       = "MIT"
  spec.required_ruby_version = ">= 2.6.0"

  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = spec.homepage
  spec.metadata["changelog_uri"] = "#{spec.homepage}/blob/main/CHANGELOG.md"

  spec.files = Dir.glob("{bin,lib}/**/*")
  spec.bindir        = "bin"
  spec.executables   = ["crules"]
  spec.require_paths = ["lib"]

  # Dependencies
  spec.add_dependency "thor", "~> 1.0"
  spec.add_dependency "pastel", "~> 0.8"

  # Development dependencies
  spec.add_development_dependency "rake", "~> 13.0"
  spec.add_development_dependency "rspec", "~> 3.0"
  spec.add_development_dependency "rubocop", "~> 1.21"
end 