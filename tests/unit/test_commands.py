import os
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
def temp_dir(tmp_path):
    """一時ディレクトリを作成するフィクスチャ"""
    return tmp_path


@pytest.fixture
def template_dir(temp_dir):
    """テンプレートディレクトリを作成するフィクスチャ"""
    template_path = temp_dir / "template"
    template_path.mkdir()

    # ルールディレクトリを作成
    rules_path = template_path / "app" / "rules"
    rules_path.mkdir(parents=True)

    # サンプルルールファイルを作成
    rule_content = """---
description: "Test rule"
globs: "src/**/*.ts"
alwaysApply: false
---

# Test Rule
This is a test rule.
"""
    (rules_path / "test_rule.md").write_text(rule_content)

    # ノートディレクトリを作成
    notes_path = template_path / "app" / "notes"
    notes_path.mkdir(parents=True)

    # サンプルノートファイルを作成
    note_content = """---
description: "Test note"
category: "development"
---

# Test Note
This is a test note.
"""
    (notes_path / "test_note.md").write_text(note_content)

    return template_path


@pytest.fixture
def target_dir(temp_dir):
    """ターゲットディレクトリを作成するフィクスチャ"""
    target_path = temp_dir / "target"
    target_path.mkdir()
    return target_path


# 初期化コマンドのテスト
def test_init_command(template_dir, target_dir):
    """init_command関数のテスト"""
    result = init_command(str(target_dir))
    assert result is True

    # デプロイされたファイルの確認
    deployed_rules = target_dir / "app" / "rules"
    assert deployed_rules.exists()
    assert (deployed_rules / "test_rule.mdc").exists()

    deployed_notes = target_dir / "app" / "notes"
    assert deployed_notes.exists()
    assert (deployed_notes / "test_note.md").exists()


def test_init_command_with_existing_files(template_dir, target_dir):
    """既存のファイルがある場合のinit_command関数のテスト"""
    # 既存のファイルを作成
    existing_file = target_dir / "app" / "rules" / "test_rule.mdc"
    existing_file.parent.mkdir(parents=True)
    existing_file.write_text("Existing content")

    result = init_command(str(target_dir))
    assert result is True

    # バックアップが作成されていることを確認
    backup_file = target_dir / "app" / "rules" / "test_rule.mdc.bak"
    assert backup_file.exists()


# デプロイコマンドのテスト
def test_deploy_command(template_dir, target_dir):
    """deploy_command関数のテスト"""
    result = deploy_command(str(template_dir), str(target_dir))
    assert result is True

    # デプロイされたファイルの確認
    deployed_rules = target_dir / "app" / "rules"
    assert deployed_rules.exists()
    assert (deployed_rules / "test_rule.mdc").exists()

    deployed_notes = target_dir / "app" / "notes"
    assert deployed_notes.exists()
    assert (deployed_notes / "test_note.md").exists()


# リストコマンドのテスト
def test_list_command(template_dir):
    """list_command関数のテスト"""
    result = list_command(str(template_dir))
    assert isinstance(result, dict)
    assert "rules" in result
    assert "notes" in result
    assert len(result["rules"]) == 1
    assert len(result["notes"]) == 1


# ツリーコマンドのテスト
def test_tree_command(template_dir):
    """tree_command関数のテスト"""
    result = tree_command(str(template_dir))
    assert isinstance(result, str)
    assert "template" in result
    assert "app" in result
    assert "rules" in result
    assert "notes" in result


# バリデーションコマンドのテスト
def test_validate_command_valid(template_dir):
    """有効なテンプレートディレクトリのvalidate_command関数のテスト"""
    result = validate_command(str(template_dir))
    assert result is True


def test_validate_command_invalid(temp_dir):
    """無効なテンプレートディレクトリのvalidate_command関数のテスト"""
    result = validate_command(str(temp_dir))
    assert result is False
