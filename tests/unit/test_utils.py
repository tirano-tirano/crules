import os
from pathlib import Path

import pytest

from crules.exceptions import ConflictError, ValidationError
from crules.utils import (
    ensure_directory,
    read_yaml_front_matter,
    validate_file_content,
    validate_file_format,
    validate_file_size,
    validate_file_structure,
    validate_yaml_front_matter,
)


# テスト用のフィクスチャ
@pytest.fixture
def temp_dir(tmp_path):
    """一時ディレクトリを作成するフィクスチャ"""
    return tmp_path


@pytest.fixture
def valid_md_file(temp_dir):
    """有効なマークダウンファイルを作成するフィクスチャ"""
    content = """---
description: "Test description"
globs: "src/**/*.ts"
alwaysApply: false
---

# Test Content
This is a test file.
"""
    file_path = temp_dir / "test.md"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def invalid_md_file(temp_dir):
    """無効なマークダウンファイルを作成するフィクスチャ"""
    content = """# Invalid File
No YAML front matter
"""
    file_path = temp_dir / "invalid.md"
    file_path.write_text(content)
    return file_path


# ディレクトリ関連のテスト
def test_ensure_directory(temp_dir):
    """ensure_directory関数のテスト"""
    test_dir = temp_dir / "test_dir"
    ensure_directory(test_dir)
    assert test_dir.exists()
    assert test_dir.is_dir()


# YAMLフロントマター関連のテスト
def test_read_yaml_front_matter_valid(tmp_path):
    """有効なYAML front matterの読み込みテスト"""
    file_path = tmp_path / "test.md"
    with open(file_path, "w") as f:
        f.write(
            """---
description: Test description
globs: ["*.md"]
---
Content"""
        )

    front_matter = read_yaml_front_matter(str(file_path))
    assert isinstance(front_matter, dict)
    assert front_matter["description"] == "Test description"
    assert front_matter["globs"] == ["*.md"]


def test_read_yaml_front_matter_invalid(tmp_path):
    """無効なYAML front matterの読み込みテスト"""
    file_path = tmp_path / "test.md"
    with open(file_path, "w") as f:
        f.write("Content without front matter")

    with pytest.raises(ValidationError):
        read_yaml_front_matter(str(file_path))


def test_validate_yaml_front_matter_valid():
    """有効なYAML front matterの検証テスト"""
    front_matter = {"description": "Test description", "globs": ["*.md"]}
    assert validate_yaml_front_matter(front_matter) is True


def test_validate_yaml_front_matter_invalid():
    """無効なYAML front matterの検証テスト"""
    front_matter = {"description": "Test description"}
    assert validate_yaml_front_matter(front_matter) is False


# ファイル検証関連のテスト
def test_validate_file_format_valid(tmp_path):
    """有効なファイル形式の検証テスト"""
    file_path = tmp_path / "test.md"
    file_path.touch()
    assert validate_file_format(str(file_path)) is True


def test_validate_file_format_invalid(tmp_path):
    """無効なファイル形式の検証テスト"""
    file_path = tmp_path / "test.txt"
    file_path.touch()
    assert validate_file_format(str(file_path)) is False


def test_validate_file_size_valid(tmp_path):
    """有効なファイルサイズの検証テスト"""
    file_path = tmp_path / "test.md"
    with open(file_path, "w") as f:
        f.write("Small content")
    assert validate_file_size(str(file_path)) is True


def test_validate_file_size_invalid(tmp_path):
    """無効なファイルサイズの検証テスト"""
    file_path = tmp_path / "test.md"
    with open(file_path, "w") as f:
        f.write("x" * (1024 * 1024 + 1))  # 1MB + 1 byte
    assert validate_file_size(str(file_path)) is False


def test_validate_file_content_valid(tmp_path):
    """有効なファイル内容の検証テスト"""
    file_path = tmp_path / "test.md"
    with open(file_path, "w") as f:
        f.write(
            """---
description: Test description
globs: ["*.md"]
---
Content"""
        )
    assert validate_file_content(str(file_path)) is True


def test_validate_file_content_invalid(tmp_path):
    """無効なファイル内容の検証テスト"""
    file_path = tmp_path / "test.md"
    with open(file_path, "w") as f:
        f.write("Content without front matter")
    assert validate_file_content(str(file_path)) is False


def test_validate_file_structure_valid(tmp_path):
    """有効なファイル構造の検証テスト"""
    file_path = tmp_path / "test.md"
    with open(file_path, "w") as f:
        f.write(
            """---
description: Test description
globs: ["*.md"]
---
Content"""
        )
    assert validate_file_structure(str(file_path)) is True


def test_validate_file_structure_invalid(tmp_path):
    """無効なファイル構造の検証テスト"""
    file_path = tmp_path / "test.md"
    with open(file_path, "w") as f:
        f.write("Content without front matter")
    assert validate_file_structure(str(file_path)) is False
