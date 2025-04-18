"""
tree_commandの統合テスト

このテストでは以下の機能を検証します：
- テンプレートディレクトリの構造を表示
- ルールとノートの詳細情報を表示
- 存在しないディレクトリの処理
"""

import os
import shutil
from pathlib import Path
import pytest

from crules.commands import tree_command


@pytest.fixture
def template_project(tmp_path):
    """テンプレートプロジェクトの構造を作成"""
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    
    # ルールディレクトリ
    rules_dir = template_dir / "rules"
    rules_dir.mkdir()
    
    # ルールファイル1
    rule1 = rules_dir / "rule1.md"
    rule1.write_text("""---
title: "ルール1"
description: "ルール1の説明"
globs: src/**/*.ts
alwaysApply: true
tags: ["typescript"]
---
# ルール1
ルール1の内容
""")
    
    # ルールファイル2
    rule2 = rules_dir / "rule2.md"
    rule2.write_text("""---
title: "ルール2"
description: "ルール2の説明"
globs: src/**/*.tsx
alwaysApply: false
tags: ["react"]
---
# ルール2
ルール2の内容
""")
    
    # ノートディレクトリ
    notes_dir = template_dir / "notes"
    notes_dir.mkdir()
    
    # ノートファイル1
    note1 = notes_dir / "note1.md"
    note1.write_text("""---
title: "ノート1"
description: "ノート1の説明"
tags: ["documentation"]
---
# ノート1
ノート1の内容
""")
    
    # ノートファイル2
    note2 = notes_dir / "note2.md"
    note2.write_text("""---
title: "ノート2"
description: "ノート2の説明"
tags: ["guide"]
---
# ノート2
ノート2の内容
""")
    
    return template_dir


def test_tree_command_success(template_project):
    """tree_commandが正常に実行されることを確認"""
    result = tree_command(str(template_project))
    
    # テンプレートディレクトリの構造を確認
    assert "template" in result
    assert "rules" in result["template"]
    assert "notes" in result["template"]
    
    # ファイル名を確認
    assert "rule1.md" in result["template"]["rules"]
    assert "rule2.md" in result["template"]["rules"]
    assert "note1.md" in result["template"]["notes"]
    assert "note2.md" in result["template"]["notes"]
    
    # ルールとノートの詳細情報を確認
    assert result["template"]["rules"]["rule1.md"]["title"] == "ルール1"
    assert result["template"]["rules"]["rule1.md"]["description"] == "ルール1の説明"
    assert result["template"]["rules"]["rule1.md"]["globs"] == "src/**/*.ts"
    assert result["template"]["rules"]["rule1.md"]["alwaysApply"] is True
    assert result["template"]["rules"]["rule1.md"]["tags"] == ["typescript"]
    
    assert result["template"]["rules"]["rule2.md"]["title"] == "ルール2"
    assert result["template"]["rules"]["rule2.md"]["description"] == "ルール2の説明"
    assert result["template"]["rules"]["rule2.md"]["globs"] == "src/**/*.tsx"
    assert result["template"]["rules"]["rule2.md"]["alwaysApply"] is False
    assert result["template"]["rules"]["rule2.md"]["tags"] == ["react"]
    
    assert result["template"]["notes"]["note1.md"]["title"] == "ノート1"
    assert result["template"]["notes"]["note1.md"]["description"] == "ノート1の説明"
    assert result["template"]["notes"]["note1.md"]["tags"] == ["documentation"]
    
    assert result["template"]["notes"]["note2.md"]["title"] == "ノート2"
    assert result["template"]["notes"]["note2.md"]["description"] == "ノート2の説明"
    assert result["template"]["notes"]["note2.md"]["tags"] == ["guide"]


def test_tree_command_missing_template(tmp_path):
    """テンプレートディレクトリが存在しない場合の処理を確認"""
    result = tree_command(str(tmp_path / "non_existent_template"))
    
    # 空の結果が返されることを確認
    assert result == {}


def test_tree_command_empty_directories(template_project):
    """空のディレクトリの処理を確認"""
    # ディレクトリを削除
    shutil.rmtree(template_project / "rules")
    shutil.rmtree(template_project / "notes")
    
    # 空のディレクトリを作成
    (template_project / "rules").mkdir()
    (template_project / "notes").mkdir()
    
    result = tree_command(str(template_project))
    
    # 空のディレクトリが含まれることを確認
    assert "template" in result
    assert "rules" in result["template"]
    assert "notes" in result["template"]
    assert len(result["template"]["rules"]) == 0
    assert len(result["template"]["notes"]) == 0


def test_tree_command_nested_directories(template_project):
    """ネストされたディレクトリの処理を確認"""
    # ネストされたルールディレクトリを作成
    nested_rules_dir = template_project / "rules" / "nested"
    nested_rules_dir.mkdir()
    
    # ネストされたルールファイルを作成
    nested_rule = nested_rules_dir / "nested_rule.md"
    nested_rule.write_text("""---
title: "ネストされたルール"
description: "ネストされたルールの説明"
globs: src/**/*.ts
alwaysApply: true
tags: ["typescript"]
---
# ネストされたルール
ネストされたルールの内容
""")
    
    result = tree_command(str(template_project))
    
    # ネストされたルールが含まれることを確認
    assert "nested" in result["template"]["rules"]
    assert "nested_rule.md" in result["template"]["rules"]["nested"]
    assert result["template"]["rules"]["nested"]["nested_rule.md"]["title"] == "ネストされたルール"
    assert result["template"]["rules"]["nested"]["nested_rule.md"]["description"] == "ネストされたルールの説明"
    assert result["template"]["rules"]["nested"]["nested_rule.md"]["globs"] == "src/**/*.ts"
    assert result["template"]["rules"]["nested"]["nested_rule.md"]["alwaysApply"] is True
    assert result["template"]["rules"]["nested"]["nested_rule.md"]["tags"] == ["typescript"]


def test_tree_command_default_template(tmp_path):
    """デフォルトのテンプレートディレクトリの処理を確認"""
    # デフォルトのテンプレートディレクトリを作成
    default_template = tmp_path / ".crules" / "template"
    default_template.mkdir(parents=True)
    
    result = tree_command(str(tmp_path))
    
    # デフォルトのテンプレートディレクトリが含まれることを確認
    assert ".crules" in result
    assert "template" in result[".crules"]
    assert "rules" in result[".crules"]["template"]
    assert "notes" in result[".crules"]["template"]
    assert len(result[".crules"]["template"]["rules"]) == 0
    assert len(result[".crules"]["template"]["notes"]) == 0 