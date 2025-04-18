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


def create_test_file(path: Path, content: str):
    """テストファイルを作成するヘルパー関数"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def create_test_structure(tmp_path: Path, rule_content: str = None, note_content: str = None):
    """テストディレクトリ構造を作成するヘルパー関数"""
    if rule_content:
        create_test_file(tmp_path / "rules" / "test_rule.md", rule_content)
    if note_content:
        create_test_file(tmp_path / "notes" / "test_note.md", note_content)


@pytest.fixture(autouse=True)
def cleanup_test_dirs(tmp_path):
    """テスト実行後のクリーンアップを行うフィクスチャ"""
    yield
    # テスト実行後に一時ディレクトリを強制的に削除
    if tmp_path.exists():
        for item in tmp_path.glob("**/*"):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
        shutil.rmtree(tmp_path, ignore_errors=True)


def test_validate_command_success(tmp_path):
    """正常なルールとノートファイルの検証"""
    rule_content = """---
title: テストルール
description: これはテストです
---
ルールの内容"""
    note_content = "これはテストノートです"
    create_test_structure(tmp_path, rule_content, note_content)

    result = validate_command(str(tmp_path))
    assert result == 0


def test_validate_command_empty_directories(tmp_path):
    """空のディレクトリ構造の検証"""
    create_test_structure(tmp_path)
    result = validate_command(str(tmp_path))
    assert result == 1  # rulesディレクトリが存在しないためエラー


def test_validate_command_with_rules_only(tmp_path):
    """rulesディレクトリのみ存在する場合の検証"""
    rule_content = """---
title: テストルール
description: これはテストです
---
ルールの内容"""
    create_test_structure(tmp_path, rule_content)

    result = validate_command(str(tmp_path))
    assert result == 1  # notesディレクトリが存在しないためエラー


def test_validate_command_with_invalid_rule(tmp_path):
    """無効なルールファイルの検証"""
    invalid_content = "これは無効なルールファイルです"
    create_test_structure(tmp_path, invalid_content)

    result = validate_command(str(tmp_path))
    assert result == 1  # YAMLフロントマターがないためエラー


def test_validate_command_with_empty_rule(tmp_path):
    """空のルールファイルの検証"""
    create_test_structure(tmp_path, "")
    
    result = validate_command(str(tmp_path))
    assert result == 1  # 空のファイルはエラー


def test_validate_command_with_empty_note(tmp_path):
    """空のノートファイルの検証"""
    rule_content = """---
title: テストルール
description: これはテストです
---
ルールの内容"""
    create_test_structure(tmp_path, rule_content, "")
    
    result = validate_command(str(tmp_path))
    assert result == 1  # 空のノートファイルはエラー