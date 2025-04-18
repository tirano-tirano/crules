import os
import shutil
from pathlib import Path

import pytest

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


# ファイル操作の統合テスト
def test_file_read_write_operations(change_to_project_dir):
    """ファイルの読み書き操作をテスト"""
    # ファイルを読み込む
    file_path = "template/app/rules/test_rule.md"
    content = read_file(file_path)
    assert content is not None
    assert "Test Rule" in content

    # 新しいファイルを作成
    new_file_path = "template/app/rules/new_rule.md"
    new_content = """---
description: "New test rule"
globs: "src/**/*.ts"
alwaysApply: true
---

# New Test Rule
This is a new test rule.
"""
    write_file(new_file_path, new_content)

    # 作成したファイルを読み込む
    read_content = read_file(new_file_path)
    assert read_content is not None
    assert "New Test Rule" in read_content


def test_directory_operations(change_to_project_dir):
    """ディレクトリ操作をテスト"""
    # 新しいディレクトリを作成
    new_dir = "template/app/rules/new_dir"
    ensure_directory(new_dir)
    assert os.path.exists(new_dir)

    # ディレクトリ内のファイルを列挙
    files = list_files("template/app/rules")
    assert len(files) > 0
    assert "test_rule.md" in [os.path.basename(f) for f in files]


def test_file_validation_operations(change_to_project_dir):
    """ファイル検証操作をテスト"""
    # ファイル形式を検証
    file_path = "template/app/rules/test_rule.md"
    assert validate_file_format(file_path, [".md"]) is True

    # ファイルサイズを検証
    assert validate_file_size(file_path, 1024 * 1024) is True

    # ファイル内容を検証
    missing_fields = validate_file_content(file_path, ["description"])
    assert missing_fields == []

    # ファイル構造を検証
    structure_errors = validate_file_structure(file_path)
    assert structure_errors == []

    # YAML front matterを読み込む
    yaml_data = read_yaml_front_matter(file_path)
    assert yaml_data is not None
    assert yaml_data.get("description") == "Test rule"


def test_conflict_resolution(change_to_project_dir):
    """競合解決をテスト"""
    # ターゲットディレクトリを作成
    target_dir = ".cursor/rules"
    ensure_directory(target_dir)

    # ターゲットファイルを作成
    target_file = f"{target_dir}/test_rule.mdc"
    with open(target_file, "w") as f:
        f.write("Existing content")

    # 競合を解決
    source_file = "template/app/rules/test_rule.md"
    assert resolve_conflict(source_file, target_file, force=True) is True

    # ファイルが上書きされたことを確認
    with open(target_file, "r") as f:
        content = f.read()
        assert "Test Rule" in content


def test_error_handling(change_to_project_dir):
    """エラーハンドリングをテスト"""
    # 存在しないファイルを読み込む
    with pytest.raises(Exception):
        read_file("non_existent_file.md")

    # 無効なファイル形式を検証
    assert validate_file_format("template/app/rules/test_rule.md", [".txt"]) is False

    # 無効なファイル内容を検証
    invalid_file = "template/app/rules/invalid.md"
    with open(invalid_file, "w") as f:
        f.write("# Invalid file without YAML front matter")

    with pytest.raises(Exception):
        read_yaml_front_matter(invalid_file)
