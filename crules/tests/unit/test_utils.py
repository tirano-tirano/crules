"""
Tests for the utils module.
"""

import os
from pathlib import Path
import pytest
import yaml
from crules.utils import read_yaml_front_matter, validate_file_content

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
def invalid_yaml_file(temp_dir):
    """Create a file with invalid YAML front matter."""
    file_path = temp_dir / "invalid.md"
    content = """---
title: Invalid File
description: [Missing bracket
tags: [test
---

This is an invalid file.
"""
    file_path.write_text(content)
    return file_path

@pytest.fixture
def no_front_matter_file(temp_dir):
    """Create a file without front matter."""
    file_path = temp_dir / "no_front_matter.md"
    content = "This is a file without front matter."
    file_path.write_text(content)
    return file_path

@pytest.fixture
def empty_front_matter_file(temp_dir):
    """Create a file with empty front matter."""
    file_path = temp_dir / "empty_front_matter.md"
    content = """---
---

This file has empty front matter.
"""
    file_path.write_text(content)
    return file_path

@pytest.fixture
def unreadable_file(temp_dir):
    """Create a file that cannot be read."""
    file_path = temp_dir / "unreadable.md"
    file_path.write_text("Some content")
    os.chmod(file_path, 0o000)
    return file_path

def test_read_yaml_front_matter_valid(sample_file):
    """Test reading valid YAML front matter."""
    front_matter = read_yaml_front_matter(sample_file)
    assert front_matter == {
        "title": "Test File",
        "description": "A test file",
        "tags": ["test", "sample"]
    }

def test_read_yaml_front_matter_invalid(invalid_yaml_file):
    """Test reading invalid YAML front matter."""
    with pytest.raises(yaml.YAMLError):
        read_yaml_front_matter(invalid_yaml_file)

def test_read_yaml_front_matter_no_front_matter(no_front_matter_file):
    """Test reading a file without front matter."""
    front_matter = read_yaml_front_matter(no_front_matter_file)
    assert front_matter == {}

def test_read_yaml_front_matter_empty(empty_front_matter_file):
    """Test reading empty front matter."""
    front_matter = read_yaml_front_matter(empty_front_matter_file)
    assert front_matter == {}

def test_read_yaml_front_matter_unreadable(unreadable_file):
    """Test reading an unreadable file."""
    with pytest.raises(OSError):
        read_yaml_front_matter(unreadable_file)

def test_validate_file_content_valid(sample_file):
    """Test validating a file with valid content."""
    required_fields = ["title", "description", "tags"]
    missing_fields = validate_file_content(sample_file, required_fields)
    assert not missing_fields

def test_validate_file_content_missing_fields(sample_file):
    """Test validating a file with missing required fields."""
    required_fields = ["title", "description", "tags", "author", "date"]
    missing_fields = validate_file_content(sample_file, required_fields)
    assert "author" in missing_fields
    assert "date" in missing_fields
    assert "title" not in missing_fields
    assert "description" not in missing_fields
    assert "tags" not in missing_fields

def test_validate_file_content_no_front_matter(no_front_matter_file):
    """Test validating a file without front matter."""
    required_fields = ["title", "description"]
    missing_fields = validate_file_content(no_front_matter_file, required_fields)
    assert set(missing_fields) == set(required_fields)

def test_validate_file_content_empty_front_matter(empty_front_matter_file):
    """Test validating a file with empty front matter."""
    required_fields = ["title", "description"]
    missing_fields = validate_file_content(empty_front_matter_file, required_fields)
    assert set(missing_fields) == set(required_fields)

def test_validate_file_content_unreadable(unreadable_file):
    """Test validating an unreadable file."""
    required_fields = ["title", "description"]
    missing_fields = validate_file_content(unreadable_file, required_fields)
    assert set(missing_fields) == set(required_fields)

def test_validate_file_content_nonexistent(temp_dir):
    """Test validating a nonexistent file."""
    nonexistent_file = temp_dir / "nonexistent.md"
    required_fields = ["title", "description"]
    missing_fields = validate_file_content(nonexistent_file, required_fields)
    assert set(missing_fields) == set(required_fields)

def test_validate_file_content_with_unicode(temp_dir):
    """Test validating a file with Unicode content."""
    file_path = temp_dir / "unicode.md"
    content = """---
title: 日本語のタイトル
description: 説明文も日本語です
tags: [テスト, サンプル]
---

Unicode content in the body: 🌟🌍🌈
"""
    file_path.write_text(content, encoding="utf-8")
    
    required_fields = ["title", "description", "tags"]
    missing_fields = validate_file_content(file_path, required_fields)
    assert not missing_fields

def test_validate_file_content_with_large_front_matter(temp_dir):
    """Test validating a file with large front matter."""
    file_path = temp_dir / "large.md"
    # Create a large list of tags
    tags = [f"tag{i}" for i in range(1000)]
    content = f"""---
title: Large Front Matter
description: A file with large front matter
tags: {tags}
---

Regular content
"""
    file_path.write_text(content)
    
    required_fields = ["title", "description", "tags"]
    missing_fields = validate_file_content(file_path, required_fields)
    assert not missing_fields 