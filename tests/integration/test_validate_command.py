"""
validate_commandの統合テスト

このテストでは以下の機能を検証します：
- ルールとノートのYAML front matterの検証
- ファイルの存在確認
- 無効なファイルの処理
"""

import os
import pytest
import shutil
import tempfile
from pathlib import Path
from crules.commands import validate_command


def create_test_file(path: Path, content: str = "") -> None:
    """テストファイルを作成するヘルパー関数"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def create_test_structure(tmp_path: Path, rule_content: str = "", note_content: str = "") -> None:
    """テスト用のディレクトリ構造を作成するヘルパー関数"""
    if rule_content:
        create_test_file(tmp_path / "rules" / "test_rule.mdc", rule_content)
    if note_content:
        create_test_file(tmp_path / "notes" / "test_note.md", note_content)


@pytest.fixture(scope="function")
def temp_dir():
    """一時ディレクトリを作成し、テスト終了後に確実に削除するフィクスチャ"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception as e:
        print(f"Warning: Failed to cleanup temporary directory: {e}")


@pytest.fixture(autouse=True)
def cleanup_test_dirs(temp_dir):
    """テスト終了後に一時ディレクトリを確実に削除するフィクスチャ"""
    yield
    try:
        if temp_dir.exists():
            for item in temp_dir.glob('**/*'):
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
            shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception as e:
        print(f"Warning: Failed to cleanup temporary directory: {e}")


def test_validate_command_success(temp_dir):
    """正常なルールとノートファイルが存在する場合のテスト"""
    create_test_structure(
        temp_dir,
        rule_content="---\ntitle: Test Rule\n---\nTest content",
        note_content="---\ntitle: Test Note\n---\nTest content"
    )
    result = validate_command(temp_dir)
    assert result == 0


def test_validate_command_empty_directories(temp_dir):
    """空のディレクトリ構造の場合のテスト"""
    result = validate_command(temp_dir)
    assert result == 1


def test_validate_command_with_rules_only(temp_dir):
    """ルールディレクトリのみが存在する場合のテスト"""
    create_test_structure(temp_dir, rule_content="---\ntitle: Test Rule\n---\nTest content")
    result = validate_command(temp_dir)
    assert result == 1


def test_validate_command_with_invalid_rule(temp_dir):
    """無効なルールファイルが存在する場合のテスト"""
    create_test_structure(
        temp_dir,
        rule_content="Invalid content without YAML front matter",
        note_content="---\ntitle: Test Note\n---\nTest content"
    )
    result = validate_command(temp_dir)
    assert result == 1


def test_validate_command_with_empty_rule(temp_dir):
    """空のルールファイルが存在する場合のテスト"""
    create_test_structure(temp_dir, rule_content="", note_content="---\ntitle: Test Note\n---\nTest content")
    result = validate_command(temp_dir)
    assert result == 1


def test_validate_command_with_empty_note(temp_dir):
    """空のノートファイルが存在する場合のテスト"""
    create_test_structure(temp_dir, rule_content="---\ntitle: Test Rule\n---\nTest content", note_content="")
    result = validate_command(temp_dir)
    assert result == 1