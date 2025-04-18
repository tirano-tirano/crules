import os
import shutil
from pathlib import Path

import pytest

from crules.exceptions import ConfigurationError, FileOperationError, ValidationError
from crules.utils import (
    ensure_directory,
    list_files,
    read_file,
    read_yaml_front_matter,
    resolve_conflict,
    validate_file_content,
    validate_file_format,
    validate_file_size,
    validate_file_structure,
    write_file,
)


# テスト用のフィクスチャ
@pytest.fixture
def temp_project(tmp_path):
    """一時的なプロジェクトディレクトリを作成するフィクスチャ"""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()

    # テンプレートディレクトリを作成
    template_dir = project_dir / "template"
    template_dir.mkdir()

    # アプリケーションテンプレートを作成
    app_template = template_dir / "app"
    app_template.mkdir()

    # ルールディレクトリを作成
    rules_dir = app_template / "rules"
    rules_dir.mkdir()

    # サンプルルールファイルを作成
    rule_content = """---
description: "Test rule"
globs: "src/**/*.ts"
alwaysApply: false
---

# Test Rule
This is a test rule.
"""
    (rules_dir / "test_rule.md").write_text(rule_content)

    return project_dir


@pytest.fixture
def change_to_project_dir(temp_project):
    """プロジェクトディレクトリに移動するフィクスチャ"""
    original_dir = os.getcwd()
    os.chdir(temp_project)
    yield
    os.chdir(original_dir)


# ファイル操作のエラーハンドリング
def test_file_read_errors(change_to_project_dir):
    """ファイル読み込みのエラーハンドリングをテスト"""
    # 存在しないファイルを読み込む
    with pytest.raises(FileOperationError):
        read_file("non_existent_file.md")

    # 読み取り権限のないファイルを作成
    restricted_file = "template/app/rules/restricted.md"
    with open(restricted_file, "w") as f:
        f.write("Restricted content")
    os.chmod(restricted_file, 0o000)

    with pytest.raises(FileOperationError):
        read_file(restricted_file)

    # 権限を元に戻す
    os.chmod(restricted_file, 0o644)


def test_file_write_errors(change_to_project_dir):
    """ファイル書き込みのエラーハンドリングをテスト"""
    # 書き込み権限のないディレクトリを作成
    restricted_dir = "template/app/rules/restricted"
    os.makedirs(restricted_dir)
    os.chmod(restricted_dir, 0o000)

    with pytest.raises(FileOperationError):
        write_file(f"{restricted_dir}/test.md", "Test content")

    # 権限を元に戻す
    os.chmod(restricted_dir, 0o755)


def test_validation_errors(change_to_project_dir):
    """検証のエラーハンドリングをテスト"""
    # 無効なファイル形式
    assert validate_file_format("template/app/rules/test_rule.md", [".txt"]) is False

    # サイズ制限を超えるファイルを作成
    large_file = "template/app/rules/large.md"
    with open(large_file, "w") as f:
        f.write("x" * (1024 * 1024 + 1))  # 1MB + 1バイト
    assert validate_file_size(large_file, 1024 * 1024) is False

    # 必須フィールドが欠けているファイルを作成
    invalid_content_file = "template/app/rules/invalid_content.md"
    with open(invalid_content_file, "w") as f:
        f.write(
            """---
globs: "src/**/*.ts"
alwaysApply: false
---

# Invalid Content
Missing description field.
"""
        )
    missing_fields = validate_file_content(invalid_content_file, ["description"])
    assert "description" in missing_fields

    # YAML front matterが無効なファイルを作成
    invalid_yaml_file = "template/app/rules/invalid_yaml.md"
    with open(invalid_yaml_file, "w") as f:
        f.write(
            """---
description: "Invalid YAML
globs: "src/**/*.ts"
alwaysApply: false
---

# Invalid YAML
Invalid YAML front matter.
"""
        )
    with pytest.raises(ValidationError):
        read_yaml_front_matter(invalid_yaml_file)


def test_conflict_resolution_errors(change_to_project_dir):
    """競合解決のエラーハンドリングをテスト"""
    # ソースファイルが存在しない場合
    with pytest.raises(FileOperationError):
        resolve_conflict("non_existent.md", "target.md", force=True)

    # ターゲットディレクトリが存在しない場合
    with pytest.raises(FileOperationError):
        resolve_conflict(
            "template/app/rules/test_rule.md", "non_existent/target.md", force=True
        )

    # ターゲットファイルが読み取り専用の場合
    target_dir = ".cursor/rules"
    ensure_directory(target_dir)
    target_file = f"{target_dir}/readonly.mdc"
    with open(target_file, "w") as f:
        f.write("Read-only content")
    os.chmod(target_file, 0o444)

    with pytest.raises(FileOperationError):
        resolve_conflict("template/app/rules/test_rule.md", target_file, force=True)

    # 権限を元に戻す
    os.chmod(target_file, 0o644)


def test_directory_operation_errors(change_to_project_dir):
    """ディレクトリ操作のエラーハンドリングをテスト"""
    # 存在しないディレクトリのファイルを列挙
    with pytest.raises(FileOperationError):
        list_files("non_existent_dir")

    # 権限のないディレクトリを作成
    restricted_parent = "template/app/rules/restricted_parent"
    os.makedirs(restricted_parent)
    os.chmod(restricted_parent, 0o000)

    with pytest.raises(FileOperationError):
        ensure_directory(f"{restricted_parent}/new_dir")

    # 権限を元に戻す
    os.chmod(restricted_parent, 0o755)
