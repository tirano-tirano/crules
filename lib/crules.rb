# frozen_string_literal: true

require "thor"
require "fileutils"
require "json"

require_relative "crules/version"
require_relative "crules/cli"
require_relative "crules/commands/base_command"
require_relative "crules/commands/init_command"
require_relative "crules/commands/list_command"
require_relative "crules/commands/remove_command"
require_relative "crules/utils/rule_set_finder"

module Crules
  class Error < StandardError; end
end

Crules::CLI.start(ARGV) if $PROGRAM_NAME == __FILE__ 