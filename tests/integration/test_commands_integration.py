import os
import shutil
from pathlib import Path

import pytest

from crules.commands import (
    deploy_command,
    init_command,
    list_command,
    tree_command,
    validate_command,
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

    # ノートディレクトリを作成
    notes_dir = app_template / "notes"
    notes_dir.mkdir()

    # サンプルノートファイルを作成
    note_content = """---
description: "Test note"
category: "development"
---

# Test Note
This is a test note.
"""
    (notes_dir / "test_note.md").write_text(note_content)

    # ターゲットディレクトリを作成
    target_dir = project_dir / ".cursor" / "rules"
    target_dir.mkdir(parents=True)

    notes_target_dir = project_dir / ".notes"
    notes_target_dir.mkdir()

    return project_dir


@pytest.fixture
def change_to_project_dir(temp_project):
    """プロジェクトディレクトリに移動するフィクスチャ"""
    original_dir = os.getcwd()
    os.chdir(temp_project)
    yield
    os.chdir(original_dir)


# 統合テスト
def test_init_and_deploy_workflow(change_to_project_dir):
    """initコマンドとdeployコマンドの連携をテスト"""
    # initコマンドを実行
    result = init_command("app", force=True)
    assert result is True

    # ルールファイルが配置されたことを確認
    rule_file = Path(".cursor/rules/test_rule.mdc")
    assert rule_file.exists()

    # ノートファイルが配置されたことを確認
    note_file = Path(".notes/test_note.md")
    assert note_file.exists()

    # テンプレートファイルを編集
    template_rule = Path("template/app/rules/test_rule.md")
    edited_content = """---
description: "Updated test rule"
globs: "src/**/*.ts"
alwaysApply: true
---

# Updated Test Rule
This is an updated test rule.
"""
    template_rule.write_text(edited_content)

    # deployコマンドを実行
    result = deploy_command("app", force=True)
    assert result is True

    # 更新されたルールファイルが配置されたことを確認
    updated_rule_content = rule_file.read_text()
    assert "Updated test rule" in updated_rule_content
    assert "This is an updated test rule" in updated_rule_content


def test_validate_and_list_workflow(change_to_project_dir):
    """validateコマンドとlistコマンドの連携をテスト"""
    # validateコマンドを実行
    result = validate_command("app")
    assert result == 0  # 成功

    # listコマンドを実行
    result = list_command("app", "text")
    assert result == 0  # 成功

    # 無効なテンプレートを作成
    invalid_template = Path("template/app/rules/invalid.md")
    invalid_content = """---
title: Invalid Rule
description: Invalid Rule Description
tags: [invalid]
---

# Invalid Rule
No YAML front matter
"""
    invalid_template.write_text(invalid_content)

    # validateコマンドを実行（エラーが発生するはず）
    result = validate_command("app")
    assert result == 1  # エラー


def test_tree_and_list_workflow(change_to_project_dir):
    """treeコマンドとlistコマンドの連携をテスト"""
    # 階層構造を持つルールを作成
    nested_rules_dir = Path("template/app/rules/nested")
    nested_rules_dir.mkdir()

    nested_rule_content = """---
description: "Nested test rule"
globs: "src/**/*.ts"
alwaysApply: false
---

# Nested Test Rule
This is a nested test rule.
"""
    (nested_rules_dir / "nested_rule.md").write_text(nested_rule_content)

    # treeコマンドを実行
    result = tree_command("app")
    assert result is True

    # listコマンドを実行
    result = list_command("app", "json")
    assert result is True


def test_init_with_multiple_templates(change_to_project_dir):
    """複数のテンプレートを持つinitコマンドをテスト"""
    # Flutterテンプレートを作成
    flutter_template = Path("template/flutter")
    flutter_template.mkdir()

    flutter_rules_dir = flutter_template / "rules"
    flutter_rules_dir.mkdir()

    flutter_rule_content = """---
description: "Flutter test rule"
globs: "lib/**/*.dart"
alwaysApply: false
---

# Flutter Test Rule
This is a Flutter test rule.
"""
    (flutter_rules_dir / "flutter_rule.md").write_text(flutter_rule_content)

    # アプリケーションテンプレートを初期化
    result = init_command("app", force=True)
    assert result is True

    # Flutterテンプレートを初期化
    result = init_command("flutter", force=True)
    assert result is True

    # 両方のルールファイルが配置されたことを確認
    app_rule_file = Path(".cursor/rules/test_rule.mdc")
    flutter_rule_file = Path(".cursor/rules/flutter_rule.mdc")
    assert app_rule_file.exists()
    assert flutter_rule_file.exists()
