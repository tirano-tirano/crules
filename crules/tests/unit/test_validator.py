"""
Tests for the validator module.
"""

import os
from pathlib import Path
import pytest
from crules.validator import FileValidator


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for test files."""
    return tmp_path


@pytest.fixture
def sample_file(temp_dir):
    """Create a sample file with valid front matter."""
    file_path = temp_dir / "sample.md"
    content = """---
title: Test File
description: A test file
tags: [test, sample]
---

This is a test file.
"""
    file_path.write_text(content)
    return file_path


@pytest.fixture
def invalid_file(temp_dir):
    """Create a sample file with invalid front matter."""
    file_path = temp_dir / "invalid.md"
    content = """---
title: Invalid File
---

This is an invalid file.
"""
    file_path.write_text(content)
    return file_path


@pytest.fixture
def empty_file(temp_dir):
    """Create an empty file."""
    file_path = temp_dir / "empty.md"
    file_path.write_text("")
    return file_path


@pytest.fixture
def complex_directory(temp_dir):
    """Create a complex directory structure with multiple files."""
    # Create subdirectories
    (temp_dir / "dir1" / "subdir1").mkdir(parents=True)
    (temp_dir / "dir1" / "subdir2").mkdir()
    (temp_dir / "dir2").mkdir()

    # Create valid files
    valid_files = [
        (
            "dir1/file1.md",
            """---
title: File 1
description: First file
tags: [test]
---
Content 1""",
        ),
        (
            "dir1/subdir1/file2.md",
            """---
title: File 2
description: Second file
tags: [test, nested]
---
Content 2""",
        ),
    ]

    # Create invalid files
    invalid_files = [
        (
            "dir1/subdir2/invalid1.md",
            """---
title: Invalid 1
---
Missing fields""",
        ),
        (
            "dir2/invalid2.md",
            """---
description: Invalid 2
tags: [test]
---
Missing title""",
        ),
    ]

    # Write all files
    for path, content in valid_files + invalid_files:
        file_path = temp_dir / path
        file_path.write_text(content)

    return temp_dir


@pytest.fixture
def malformed_file(temp_dir):
    """Create a file with malformed front matter."""
    file_path = temp_dir / "malformed.md"
    content = """---
title: Malformed File
description: This file has malformed front matter
tags: [test
---

Invalid YAML in front matter.
"""
    file_path.write_text(content)
    return file_path


@pytest.fixture
def unreadable_file(temp_dir):
    """Create a file that cannot be read."""
    file_path = temp_dir / "unreadable.md"
    file_path.write_text("Some content")
    # Make the file unreadable
    os.chmod(file_path, 0o000)
    return file_path


@pytest.fixture
def validator():
    """Create a FileValidator instance."""
    return FileValidator(required_fields=["title", "description", "tags"])


def test_validate_file_valid(validator, sample_file):
    """Test validating a file with all required fields."""
    missing_fields = validator.validate_file(sample_file)
    assert not missing_fields


def test_validate_file_invalid(validator, invalid_file):
    """Test validating a file with missing required fields."""
    missing_fields = validator.validate_file(invalid_file)
    assert "description" in missing_fields
    assert "tags" in missing_fields
    assert "title" not in missing_fields


def test_validate_file_empty(validator, empty_file):
    """Test validating an empty file."""
    missing_fields = validator.validate_file(empty_file)
    assert all(field in missing_fields for field in ["title", "description", "tags"])


def test_validate_directory(validator, temp_dir, sample_file, invalid_file):
    """Test validating all files in a directory."""
    results = validator.validate_directory(temp_dir)
    assert len(results) == 1
    assert invalid_file in results
    assert "description" in results[invalid_file]
    assert "tags" in results[invalid_file]


def test_validate_files(validator, sample_file, invalid_file):
    """Test validating a list of files."""
    results = validator.validate_files([sample_file, invalid_file])
    assert len(results) == 1
    assert invalid_file in results
    assert "description" in results[invalid_file]
    assert "tags" in results[invalid_file]


def test_validate_nonexistent_file(validator, temp_dir):
    """Test validating a nonexistent file."""
    nonexistent_file = temp_dir / "nonexistent.md"
    missing_fields = validator.validate_file(nonexistent_file)
    assert all(field in missing_fields for field in ["title", "description", "tags"])


def test_validate_directory_nonexistent(validator, temp_dir):
    """Test validating a nonexistent directory."""
    nonexistent_dir = temp_dir / "nonexistent"
    results = validator.validate_directory(nonexistent_dir)
    assert not results


def test_validate_complex_directory(validator, complex_directory):
    """Test validating a complex directory structure."""
    results = validator.validate_directory(complex_directory)

    # Should find 2 invalid files
    assert len(results) == 2

    # Check invalid files in dir1/subdir2
    invalid1 = complex_directory / "dir1" / "subdir2" / "invalid1.md"
    assert invalid1 in results
    assert "description" in results[invalid1]
    assert "tags" in results[invalid1]

    # Check invalid files in dir2
    invalid2 = complex_directory / "dir2" / "invalid2.md"
    assert invalid2 in results
    assert "title" in results[invalid2]


def test_validate_malformed_file(validator, malformed_file):
    """Test validating a file with malformed front matter."""
    missing_fields = validator.validate_file(malformed_file)
    assert all(field in missing_fields for field in ["title", "description", "tags"])


def test_validate_files_with_duplicates(validator, invalid_file):
    """Test validating a list of files with duplicates."""
    results = validator.validate_files([invalid_file, invalid_file])
    assert len(results) == 1
    assert invalid_file in results


def test_validate_files_empty_list(validator):
    """Test validating an empty list of files."""
    results = validator.validate_files([])
    assert not results


def test_validate_directory_with_symlinks(validator, temp_dir, sample_file):
    """Test validating a directory containing symlinks."""
    # Create a symlink to the sample file
    symlink_path = temp_dir / "symlink.md"
    os.symlink(sample_file, symlink_path)

    results = validator.validate_directory(temp_dir)
    assert not results  # Symlink should point to valid file


def test_validate_directory_with_hidden_files(validator, temp_dir):
    """Test validating a directory with hidden files."""
    # Create a hidden file
    hidden_file = temp_dir / ".hidden.md"
    hidden_file.write_text(
        """---
title: Hidden File
---
"""
    )

    results = validator.validate_directory(temp_dir)
    assert hidden_file in results
    assert "description" in results[hidden_file]
    assert "tags" in results[hidden_file]


def test_validate_unreadable_file(validator, unreadable_file):
    """Test validating a file that cannot be read."""
    missing_fields = validator.validate_file(unreadable_file)
    assert all(field in missing_fields for field in ["title", "description", "tags"])


def test_validate_directory_with_unreadable_files(validator, temp_dir, unreadable_file):
    """Test validating a directory containing unreadable files."""
    results = validator.validate_directory(temp_dir)
    assert unreadable_file in results
    assert all(
        field in results[unreadable_file] for field in ["title", "description", "tags"]
    )


def test_validate_file_with_binary_content(temp_dir):
    """Test validating a file with binary content."""
    file_path = temp_dir / "binary.md"
    # Create a file with binary content
    with open(file_path, "wb") as f:
        f.write(bytes([0x00, 0x01, 0x02, 0x03]))

    validator = FileValidator(required_fields=["title", "description", "tags"])
    missing_fields = validator.validate_file(file_path)
    assert all(field in missing_fields for field in ["title", "description", "tags"])


def test_validate_file_with_large_content(temp_dir):
    """Test validating a file with large content."""
    file_path = temp_dir / "large.md"
    # Create a file with large content (1MB)
    content = "---\ntitle: Large File\ndescription: A large file\ntags: [test]\n---\n\n"
    content += "x" * (1024 * 1024)  # 1MB of content
    file_path.write_text(content)

    validator = FileValidator(required_fields=["title", "description", "tags"])
    missing_fields = validator.validate_file(file_path)
    assert not missing_fields


def test_validate_file_with_special_characters(temp_dir):
    """Test validating a file with special characters in front matter."""
    file_path = temp_dir / "special.md"
    content = """---
title: "Special: !@#$%^&*()"
description: "Description with special chars: 日本語"
tags: ["tag:1", "tag:2", "tag:3"]
---

Content with special characters.
"""
    file_path.write_text(content)

    validator = FileValidator(required_fields=["title", "description", "tags"])
    missing_fields = validator.validate_file(file_path)
    assert not missing_fields
