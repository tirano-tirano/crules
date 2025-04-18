"""
Integration tests for the validation workflow.

This module tests the interaction between different components
of the validation system, including:
- File validation
- Directory validation
- Configuration handling
- Error reporting
"""

import os
import shutil
from pathlib import Path
import pytest
from crules.validator import FileValidator
from crules.utils import read_yaml_front_matter, validate_file_content, ensure_directory

@pytest.fixture
def test_project(tmp_path):
    """Create a test project structure."""
    project_dir = tmp_path / "test_project"
    
    # Create project structure
    template_dir = project_dir / "template"
    app_dir = template_dir / "app"
    rules_dir = app_dir / "rules"
    
    # Create directories
    for directory in [template_dir, app_dir, rules_dir]:
        directory.mkdir(parents=True)
    
    # Create valid rule files
    valid_rules = [
        ("basic_rule.md", """---
title: Basic Rule
description: A basic validation rule
tags: [validation, basic]
severity: error
---
This is a basic validation rule."""),
        
        ("complex_rule.md", """---
title: Complex Rule
description: A complex validation rule with multiple tags
tags: [validation, complex, multiple]
severity: warning
examples:
  - description: "Example 1"
    code: |
      function example1() {
        // Code here
      }
  - description: "Example 2"
    code: |
      function example2() {
        // More code
      }
---
This is a complex validation rule with examples.""")
    ]
    
    # Create invalid rule files
    invalid_rules = [
        ("missing_fields.md", """---
title: Missing Fields Rule
---
This rule is missing required fields."""),
        
        ("invalid_yaml.md", """---
title: Invalid YAML
description: [Missing bracket
tags: [test
severity: error
---
This file has invalid YAML front matter."""),
        
        ("no_front_matter.md", """
This file has no front matter at all.""")
    ]
    
    # Write all files
    for filename, content in valid_rules + invalid_rules:
        file_path = rules_dir / filename
        file_path.write_text(content)
    
    return project_dir

@pytest.fixture
def validator():
    """Create a validator with standard rule requirements."""
    return FileValidator(required_fields=["title", "description", "tags", "severity"])

def test_validate_rule_files(test_project, validator):
    """Test validating all rule files in a project."""
    rules_dir = test_project / "template" / "app" / "rules"
    results = validator.validate_directory(rules_dir)
    
    # Should find 3 invalid files
    assert len(results) == 3
    
    # Check missing_fields.md
    missing_fields_path = rules_dir / "missing_fields.md"
    assert missing_fields_path in results
    assert "description" in results[missing_fields_path]
    assert "tags" in results[missing_fields_path]
    assert "severity" in results[missing_fields_path]
    
    # Check invalid_yaml.md
    invalid_yaml_path = rules_dir / "invalid_yaml.md"
    assert invalid_yaml_path in results
    assert set(results[invalid_yaml_path]) == {"title", "description", "tags", "severity"}
    
    # Check no_front_matter.md
    no_front_matter_path = rules_dir / "no_front_matter.md"
    assert no_front_matter_path in results
    assert set(results[no_front_matter_path]) == {"title", "description", "tags", "severity"}

def test_validate_rule_content(test_project):
    """Test validating the content of specific rule files."""
    rules_dir = test_project / "template" / "app" / "rules"
    
    # Test valid rule
    basic_rule_path = rules_dir / "basic_rule.md"
    front_matter = read_yaml_front_matter(basic_rule_path)
    assert front_matter["title"] == "Basic Rule"
    assert front_matter["description"] == "A basic validation rule"
    assert front_matter["tags"] == ["validation", "basic"]
    assert front_matter["severity"] == "error"
    
    # Test complex rule
    complex_rule_path = rules_dir / "complex_rule.md"
    front_matter = read_yaml_front_matter(complex_rule_path)
    assert front_matter["title"] == "Complex Rule"
    assert len(front_matter["examples"]) == 2
    assert front_matter["examples"][0]["description"] == "Example 1"
    assert "function example1()" in front_matter["examples"][0]["code"]

def test_project_structure(test_project):
    """Test the overall project structure and file organization."""
    # Check directory structure
    assert (test_project / "template").is_dir()
    assert (test_project / "template" / "app").is_dir()
    assert (test_project / "template" / "app" / "rules").is_dir()
    
    # Check file existence
    rules_dir = test_project / "template" / "app" / "rules"
    expected_files = {
        "basic_rule.md",
        "complex_rule.md",
        "missing_fields.md",
        "invalid_yaml.md",
        "no_front_matter.md"
    }
    actual_files = {f.name for f in rules_dir.iterdir()}
    assert expected_files == actual_files

def test_error_handling(test_project, validator):
    """Test error handling in the validation workflow."""
    rules_dir = test_project / "template" / "app" / "rules"
    
    # Test handling of unreadable file
    unreadable_file = rules_dir / "unreadable.md"
    unreadable_file.write_text("Some content")
    os.chmod(unreadable_file, 0o000)
    
    results = validator.validate_file(unreadable_file)
    assert set(results) == {"title", "description", "tags", "severity"}
    
    # Test handling of nonexistent file
    nonexistent_file = rules_dir / "nonexistent.md"
    results = validator.validate_file(nonexistent_file)
    assert set(results) == {"title", "description", "tags", "severity"}
    
    # Cleanup
    os.chmod(unreadable_file, 0o666)
    unreadable_file.unlink()

def test_directory_operations(test_project, validator):
    """Test directory-related operations in the validation workflow."""
    rules_dir = test_project / "template" / "app" / "rules"
    
    # Test nested directory validation
    nested_dir = rules_dir / "nested"
    nested_dir.mkdir()
    
    nested_file = nested_dir / "nested_rule.md"
    nested_file.write_text("""---
title: Nested Rule
description: A rule in a nested directory
tags: [nested]
severity: warning
---
This is a nested rule.""")
    
    results = validator.validate_directory(rules_dir)
    assert len(results) == 3  # Original 3 invalid files
    assert nested_file not in results  # Nested file is valid
    
    # Test symlink handling
    symlink_file = rules_dir / "symlink_rule.md"
    os.symlink(nested_file, symlink_file)
    
    results = validator.validate_directory(rules_dir)
    assert len(results) == 3  # Symlink to valid file should not affect count
    assert symlink_file not in results
    
    # Cleanup
    symlink_file.unlink()
    shutil.rmtree(nested_dir)

def test_bulk_validation(test_project, validator):
    """Test bulk validation of multiple files."""
    rules_dir = test_project / "template" / "app" / "rules"
    
    # Get all markdown files
    rule_files = list(rules_dir.glob("*.md"))
    assert len(rule_files) == 5  # Total number of test files
    
    # Validate all files at once
    results = validator.validate_files(rule_files)
    assert len(results) == 3  # Number of invalid files
    
    # Check that valid files are not in results
    valid_files = ["basic_rule.md", "complex_rule.md"]
    for filename in valid_files:
        assert rules_dir / filename not in results 