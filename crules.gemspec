# frozen_string_literal: true

require_relative "lib/crules/version"

Gem::Specification.new do |spec|
  spec.name = "crules"
  spec.version = Crules::VERSION
  spec.authors = ["Your Name"]
  spec.email = ["your.email@example.com"]

  spec.summary = "Generate Cursor rule files for Flutter projects"
  spec.description = "A command-line tool to generate and manage Cursor rule files (.mdc) for Flutter projects"
  spec.homepage = "https://github.com/yourusername/crules"
  spec.license = "MIT"
  spec.required_ruby_version = ">= 2.6.0"

  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = "https://github.com/yourusername/crules"

  # Specify which files should be added to the gem when it is released.
  spec.files = Dir.glob(%w[
    lib/**/*.rb
    lib/**/*.md
    bin/*
    LICENSE.txt
    README.md
  ])
  spec.bindir = "bin"
  spec.executables = ["crules"]
  spec.require_paths = ["lib"]

  # Dependencies
  spec.add_dependency "thor", "~> 1.3"
  spec.add_dependency "colorize", "~> 1.1"

  # Development dependencies
  spec.add_development_dependency "rake", "~> 13.0"
  spec.add_development_dependency "rspec", "~> 3.0"
  spec.add_development_dependency "rubocop", "~> 1.21"
end 