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

    # ノートディレクトリを作成
    notes_dir = app_template / "notes"
    notes_dir.mkdir()

    # サンプルノートファイルを作成
    note_content = """---
description: "Test note"
globs: "src/**/*.ts"
alwaysApply: false
---

# Test Note
This is a test note.
"""
    (notes_dir / "test_note.md").write_text(note_content)

    return project_dir


@pytest.fixture
def change_to_project_dir(temp_project):
    """プロジェクトディレクトリに移動するフィクスチャ"""
    original_dir = os.getcwd()
    os.chdir(temp_project)
    yield
    os.chdir(original_dir)


# ノートの配置テスト
def test_note_placement(change_to_project_dir):
    """ノートの配置機能をテスト"""
    # ノートを配置
    source_file = "template/app/notes/test_note.md"
    target_dir = ".cursor/notes"
    target_file = f"{target_dir}/test_note.mdc"

    # ターゲットディレクトリを作成
    ensure_directory(target_dir)

    # ノートを配置
    resolve_conflict(source_file, target_file, force=True)

    # 配置されたファイルを確認
    assert os.path.exists(target_file)
    assert read_file(target_file) == read_file(source_file)


def test_note_validation(change_to_project_dir):
    """ノートの検証機能をテスト"""
    # 有効なノートファイル
    valid_note = "template/app/notes/test_note.md"
    assert validate_file_format(valid_note, [".md"])
    assert validate_file_size(valid_note, 1024 * 1024)
    assert validate_file_content(valid_note, ["description", "globs", "alwaysApply"])
    assert validate_file_structure(valid_note)

    # 無効なノートファイルを作成
    invalid_note = "template/app/notes/invalid_note.md"
    with open(invalid_note, "w") as f:
        f.write(
            """---
description: "Invalid note"
globs: "src/**/*.ts"
alwaysApply: "not_boolean"
---

# Invalid Note
Invalid alwaysApply value.
"""
        )

    # 無効なノートを検証
    assert not validate_file_content(
        invalid_note, ["description", "globs", "alwaysApply"]
    )
    assert not validate_file_structure(invalid_note)


def test_note_listing(change_to_project_dir):
    """ノートの一覧表示機能をテスト"""
    # 複数のノートファイルを作成
    notes = [
        ("note1.md", "Note 1"),
        ("note2.md", "Note 2"),
        ("subdir/note3.md", "Note 3"),
    ]

    for filename, content in notes:
        filepath = f"template/app/notes/{filename}"
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

    # ノートファイルを列挙
    note_files = list_files("template/app/notes")
    assert len(note_files) == 4  # test_note.md + 3 new notes

    # サブディレクトリのノートも含まれていることを確認
    assert any(f.endswith("subdir/note3.md") for f in note_files)


def test_note_update(change_to_project_dir):
    """ノートの更新機能をテスト"""
    # ノートを配置
    source_file = "template/app/notes/test_note.md"
    target_dir = ".cursor/notes"
    target_file = f"{target_dir}/test_note.mdc"
    ensure_directory(target_dir)
    resolve_conflict(source_file, target_file, force=True)

    # ノートを更新
    updated_content = """---
description: "Updated test note"
globs: "src/**/*.ts"
alwaysApply: true
---

# Updated Test Note
This is an updated test note.
"""
    with open(source_file, "w") as f:
        f.write(updated_content)

    # 更新を適用
    resolve_conflict(source_file, target_file, force=True)

    # 更新された内容を確認
    assert read_file(target_file) == updated_content


def test_note_deletion(change_to_project_dir):
    """ノートの削除機能をテスト"""
    # ノートを配置
    source_file = "template/app/notes/test_note.md"
    target_dir = ".cursor/notes"
    target_file = f"{target_dir}/test_note.mdc"
    ensure_directory(target_dir)
    resolve_conflict(source_file, target_file, force=True)

    # ノートを削除
    os.remove(target_file)

    # 削除されたことを確認
    assert not os.path.exists(target_file)

    # テンプレートのノートは残っていることを確認
    assert os.path.exists(source_file)
