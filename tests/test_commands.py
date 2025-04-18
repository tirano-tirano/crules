import pytest
from pathlib import Path
from crules.commands import validate_command
from crules.exceptions import ValidationError, FileOperationError

def test_validate_command_success(test_env, test_case, test_data):
    """validate_command関数の正常系テスト"""
    # テスト用のファイルを作成
    test_file = test_case / "test.md"
    test_content = f"""---
title: {test_data["rule"]["title"]}
description: {test_data["rule"]["description"]}
tags: {test_data["rule"]["tags"]}
---

Test content
"""
    test_file.write_text(test_content)

    # 検証を実行
    result = validate_command(test_file)
    assert result == 0  # 成功

def test_validate_command_missing_fields(test_env, test_case, test_data):
    """validate_command関数の必須フィールド不足テスト"""
    # テスト用のファイルを作成（必須フィールドが不足）
    test_file = test_case / "test.md"
    test_content = f"""---
title: {test_data["rule"]["title"]}
---

Test content
"""
    test_file.write_text(test_content)

    # 検証を実行
    result = validate_command(test_file)
    assert result == 1  # エラー

def test_validate_command_custom_fields(tmp_path):
    """validate_command関数のカスタムフィールドテスト"""
    # テスト用のファイルを作成
    test_file = tmp_path / "test.md"
    test_content = """---
title: Test Title
author: Test Author
date: 2024-01-01
---

Test content
"""
    test_file.write_text(test_content)

    # カスタムフィールドで検証を実行
    validate_command(test_file, required_fields=["title", "author", "date"])
    # 例外が発生しなければ成功

def test_validate_command_nonexistent_file(test_env, test_case):
    """validate_command関数の存在しないファイルテスト"""
    # 存在しないファイルで検証を実行
    result = validate_command(test_case / "nonexistent.md")
    assert result == 1  # エラー

def test_validate_command_invalid_front_matter(test_env, test_case, test_data):
    """validate_command関数の不正なフロントマター形式テスト"""
    # テスト用のファイルを作成（不正なYAML形式）
    test_file = test_case / "test.md"
    test_content = f"""---
title: {test_data["rule"]["title"]}
description: "Unclosed quote
tags: {test_data["rule"]["tags"]}
---

Test content
"""
    test_file.write_text(test_content)

    # 検証を実行
    result = validate_command(test_file)
    assert result == 1  # エラー

def test_validate_command_empty_file(test_env, test_case):
    """validate_command関数の空ファイルテスト"""
    # 空のファイルを作成
    test_file = test_case / "test.md"
    test_file.write_text("")

    # 検証を実行
    result = validate_command(test_file)
    assert result == 1  # エラー

def test_validate_command_no_front_matter(test_env, test_case, test_data):
    """validate_command関数のフロントマターなしテスト"""
    # フロントマターなしのファイルを作成
    test_file = test_case / "test.md"
    test_content = f"""# {test_data["rule"]["title"]}

Test content
"""
    test_file.write_text(test_content)

    # 検証を実行
    result = validate_command(test_file)
    assert result == 1  # エラー

def test_validate_command_empty_front_matter(test_env, test_case):
    """validate_command関数の空のフロントマターテスト"""
    # 空のフロントマターを持つファイルを作成
    test_file = test_case / "test.md"
    test_content = """---
---

Test content
"""
    test_file.write_text(test_content)

    # 検証を実行
    result = validate_command(test_file)
    assert result == 1  # エラー 