# frozen_string_literal: true

require_relative "../version"

module Crules
  module Commands
    class VersionCommand < Thor::Group
      include Thor::Actions

      def execute
        puts "crules #{Crules::VERSION}"
      end
    end
  end
end 