# frozen_string_literal: true

require "thor"
require "fileutils"
require "colorize"
require "json"

require_relative "crules/version"
require_relative "crules/cli"

module Crules
  class Error < StandardError; end
end

Crules::CLI.start(ARGV) if $PROGRAM_NAME == __FILE__ 