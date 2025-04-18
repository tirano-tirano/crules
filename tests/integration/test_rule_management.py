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


# ルールの配置テスト
def test_rule_placement(change_to_project_dir):
    """ルールの配置機能をテスト"""
    # ルールを配置
    source_file = "template/app/rules/test_rule.md"
    target_dir = ".cursor/rules"
    target_file = f"{target_dir}/test_rule.mdc"

    # ターゲットディレクトリを作成
    ensure_directory(target_dir)

    # ルールを配置
    resolve_conflict(source_file, target_file, force=True)

    # 配置されたファイルを確認
    assert os.path.exists(target_file)
    assert read_file(target_file) == read_file(source_file)


def test_rule_validation(change_to_project_dir):
    """ルールの検証機能をテスト"""
    # 有効なルールファイル
    valid_rule = "template/app/rules/test_rule.md"
    assert validate_file_format(valid_rule, [".md"])
    assert validate_file_size(valid_rule, 1024 * 1024)
    assert validate_file_content(valid_rule, ["description", "globs", "alwaysApply"])
    assert validate_file_structure(valid_rule)

    # 無効なルールファイルを作成
    invalid_rule = "template/app/rules/invalid_rule.md"
    with open(invalid_rule, "w") as f:
        f.write(
            """---
description: "Invalid rule"
globs: "src/**/*.ts"
alwaysApply: "not_boolean"
---

# Invalid Rule
Invalid alwaysApply value.
"""
        )

    # 無効なルールを検証
    assert not validate_file_content(
        invalid_rule, ["description", "globs", "alwaysApply"]
    )
    assert not validate_file_structure(invalid_rule)


def test_rule_listing(change_to_project_dir):
    """ルールの一覧表示機能をテスト"""
    # 複数のルールファイルを作成
    rules = [
        ("rule1.md", "Rule 1"),
        ("rule2.md", "Rule 2"),
        ("subdir/rule3.md", "Rule 3"),
    ]

    for filename, content in rules:
        filepath = f"template/app/rules/{filename}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write(
                f"""---
description: "{content}"
globs: "src/**/*.ts"
alwaysApply: false
---

# {content}
This is {content}.
"""
            )

    # ルールファイルを列挙
    rule_files = list_files("template/app/rules")
    assert len(rule_files) == 4  # test_rule.md + 3 new rules

    # サブディレクトリのルールも含まれていることを確認
    assert any(f.endswith("subdir/rule3.md") for f in rule_files)


def test_rule_update(change_to_project_dir):
    """ルールの更新機能をテスト"""
    # ルールを配置
    source_file = "template/app/rules/test_rule.md"
    target_dir = ".cursor/rules"
    target_file = f"{target_dir}/test_rule.mdc"
    ensure_directory(target_dir)
    resolve_conflict(source_file, target_file, force=True)

    # ルールを更新
    updated_content = """---
description: "Updated test rule"
globs: "src/**/*.ts"
alwaysApply: true
---

# Updated Test Rule
This is an updated test rule.
"""
    with open(source_file, "w") as f:
        f.write(updated_content)

    # 更新を適用
    resolve_conflict(source_file, target_file, force=True)

    # 更新された内容を確認
    assert read_file(target_file) == updated_content


def test_rule_deletion(change_to_project_dir):
    """ルールの削除機能をテスト"""
    # ルールを配置
    source_file = "template/app/rules/test_rule.md"
    target_dir = ".cursor/rules"
    target_file = f"{target_dir}/test_rule.mdc"
    ensure_directory(target_dir)
    resolve_conflict(source_file, target_file, force=True)

    # ルールを削除
    os.remove(target_file)

    # 削除されたことを確認
    assert not os.path.exists(target_file)

    # テンプレートのルールは残っていることを確認
    assert os.path.exists(source_file)
