import pytest
from pathlib import Path

from crules.validator import FileValidator


def test_validate_file_basic(tmp_path):
    """基本的なファイル検証のテスト"""
    # テスト用のファイルを作成
    file_path = tmp_path / "test.md"
    content = """---
title: "Test Rule"
description: "This is a test rule"
globs: ["src/**/*.ts"]
---
"""
    file_path.write_text(content)
    
    validator = FileValidator(["title", "description", "globs"])
    errors = validator.validate_file(file_path)
    assert not errors

def test_validate_file_missing_required(tmp_path):
    """必須フィールドが欠けている場合のテスト"""
    # テスト用のファイルを作成
    file_path = tmp_path / "test.md"
    content = """---
title: "Test Rule"
# descriptionフィールドが欠けている
globs: ["src/**/*.ts"]
---
"""
    file_path.write_text(content)
    
    validator = FileValidator(["title", "description", "globs"])
    errors = validator.validate_file(file_path)
    assert "description" in errors

def test_validate_file_invalid_yaml(tmp_path):
    """無効なYAMLの場合のテスト"""
    # テスト用のファイルを作成
    file_path = tmp_path / "test.md"
    content = """---
title: "Test Rule"
description: "This is a test rule"
globs: [invalid yaml
---
"""
    file_path.write_text(content)
    
    validator = FileValidator(["title", "description", "globs"])
    errors = validator.validate_file(file_path)
    assert errors  # YAMLのパースエラーが発生するため、エラーが返される 