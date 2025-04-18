"""
deploy_commandの統合テスト

このテストでは以下の機能を検証します：
- テンプレートディレクトリからルールとノートのデプロイ
- ルールファイルの.mdc拡張子への変換
- 既存ファイルの保持
- ネストされたディレクトリの処理
"""

import os
import shutil
from pathlib import Path
import pytest

from crules.commands import deploy_command
from crules.exceptions import FileOperationError
from crules.utils import ensure_directory


@pytest.fixture
def template_project(tmp_path):
    """テンプレートプロジェクトの構造を作成"""
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    
    # ルールディレクトリ
    rules_dir = template_dir / "app" / "rules"
    rules_dir.mkdir(parents=True)
    
    # ルールファイル1
    rule1 = rules_dir / "rule1.md"
    rule1.write_text("""---
description: ルール1の説明
globs: []
alwaysApply: false
---
# ルール1
ルール1の内容
""")
    
    # ルールファイル2
    rule2 = rules_dir / "rule2.md"
    rule2.write_text("""---
description: ルール2の説明
globs: []
alwaysApply: false
---
# ルール2
ルール2の内容
""")
    
    # ネストされたルールディレクトリ
    nested_rules_dir = rules_dir / "nested"
    nested_rules_dir.mkdir(parents=True)
    
    # ネストされたルールファイル
    nested_rule = nested_rules_dir / "nested_rule.md"
    nested_rule.write_text("""---
description: ネストされたルールの説明
globs: []
alwaysApply: true
---
# ネストされたルール
ネストされたルールの内容
""")
    
    # ノートディレクトリ
    notes_dir = template_dir / "app" / "notes"
    notes_dir.mkdir(parents=True)
    
    # ノートファイル1
    note1 = notes_dir / "note1.md"
    note1.write_text("""---
description: ノート1の説明
---
# ノート1
ノート1の内容
""")
    
    # ノートファイル2
    note2 = notes_dir / "note2.md"
    note2.write_text("""---
description: ノート2の説明
---
# ノート2
ノート2の内容
""")
    
    return template_dir


@pytest.fixture
def target_project(tmp_path):
    """ターゲットプロジェクトの構造を作成"""
    target_dir = tmp_path / "target"
    target_dir.mkdir()
    
    # .cursorディレクトリ
    cursor_dir = target_dir / ".cursor"
    cursor_dir.mkdir()
    
    # rulesディレクトリ
    rules_dir = cursor_dir / "rules"
    rules_dir.mkdir()
    
    # 既存のルールファイル
    existing_rule = rules_dir / "existing_rule.mdc"
    existing_rule.write_text("""---
description: 既存のルールの説明
globs: []
alwaysApply: false
---
# 既存のルール
既存のルールの内容
""")
    
    # notesディレクトリ
    notes_dir = target_dir / "notes"
    notes_dir.mkdir()
    
    return target_dir


def test_deploy_command_success(template_project, target_project):
    """デプロイコマンドが正常に実行されることを確認"""
    result = deploy_command(str(template_project), str(target_project))
    assert result is True
    
    # ルールファイルが.mdc拡張子でコピーされていることを確認
    rules_dir = target_project / ".cursor" / "rules"
    assert (rules_dir / "rule1.mdc").exists()
    assert (rules_dir / "rule2.mdc").exists()
    
    # ネストされたルールファイルがコピーされていることを確認
    assert (rules_dir / "nested" / "nested_rule.mdc").exists()
    
    # ノートファイルがコピーされていることを確認
    notes_dir = target_project / "notes"
    assert (notes_dir / "note1.md").exists()
    assert (notes_dir / "note2.md").exists()


def test_deploy_command_missing_template(target_project):
    """テンプレートディレクトリが存在しない場合の処理を確認"""
    result = deploy_command("non_existent_template", str(target_project))
    assert result is False


def test_deploy_command_missing_target(template_project, tmp_path):
    """ターゲットディレクトリが存在しない場合の処理を確認"""
    result = deploy_command(str(template_project), str(tmp_path / "non_existent_target"))
    assert result is True
    
    # ターゲットディレクトリが作成されていることを確認
    target_dir = tmp_path / "non_existent_target"
    assert target_dir.exists()
    
    # ルールファイルが.mdc拡張子でコピーされていることを確認
    rules_dir = target_dir / ".cursor" / "rules"
    assert (rules_dir / "rule1.mdc").exists()
    assert (rules_dir / "rule2.mdc").exists()


def test_deploy_command_existing_files(template_project, target_project):
    """既存のファイルが保持されることを確認"""
    result = deploy_command(str(template_project), str(target_project))
    assert result is True
    
    # 既存のルールファイルが保持されていることを確認
    rules_dir = target_project / ".cursor" / "rules"
    assert (rules_dir / "existing_rule.mdc").exists()
    
    # 新しいルールファイルがコピーされていることを確認
    assert (rules_dir / "rule1.mdc").exists()
    assert (rules_dir / "rule2.mdc").exists()


def test_deploy_command_nested_rules(template_project, target_project):
    """ネストされたルールディレクトリが正しく処理されることを確認"""
    result = deploy_command(str(template_project), str(target_project))
    assert result is True
    
    # ネストされたルールファイルが正しいパスでコピーされていることを確認
    rules_dir = target_project / ".cursor" / "rules"
    nested_rule = rules_dir / "nested" / "nested_rule.mdc"
    assert nested_rule.exists()
    
    # ネストされたルールファイルの内容を確認
    content = nested_rule.read_text()
    assert "description: ネストされたルールの説明" in content
    assert "globs: []" in content
    assert "alwaysApply: true" in content 