"""
Validation utilities for the crules package.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional

from .logger import get_logger
from .utils import read_yaml_front_matter, validate_file_content

logger = get_logger(__name__)


class FileValidator:
    """Validator for files in the crules package."""

    def __init__(self, required_fields: List[str]):
        """
        Initialize the validator.

        Args:
            required_fields: List of required fields in the front matter
        """
        self.required_fields = required_fields

    def validate_file(self, file_path: Path) -> List[str]:
        """
        Validate a file.

        Args:
            file_path: Path to the file to validate

        Returns:
            List of missing required fields
        """
        try:
            return validate_file_content(file_path, self.required_fields)
        except Exception as e:
            logger.error(f"Error validating file {file_path}: {e}")
            return self.required_fields

    def validate_directory(self, directory: Path) -> Dict[Path, List[str]]:
        """
        Validate all files in a directory.

        Args:
            directory: Path to the directory to validate

        Returns:
            Dictionary mapping file paths to lists of missing required fields
        """
        results = {}

        try:
            for file_path in directory.glob("**/*"):
                if file_path.is_file():
                    missing_fields = self.validate_file(file_path)
                    if missing_fields:
                        results[file_path] = missing_fields

            return results

        except Exception as e:
            logger.error(f"Error validating directory {directory}: {e}")
            return {}

    def validate_files(self, files: List[Path]) -> Dict[Path, List[str]]:
        """
        Validate a list of files.

        Args:
            files: List of file paths to validate

        Returns:
            Dictionary mapping file paths to lists of missing required fields
        """
        results = {}

        for file_path in files:
            missing_fields = self.validate_file(file_path)
            if missing_fields:
                results[file_path] = missing_fields

        return results
