"""
list_commandの統合テスト

このテストでは以下の機能を検証します：
- テンプレートディレクトリからルールとノートの一覧を取得
- YAML front matterの抽出
- 存在しないディレクトリの処理
"""

import os
import shutil
from pathlib import Path
import pytest

from crules.commands import list_command


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


def test_list_command_success(template_project):
    """list_commandが正常に実行されることを確認"""
    result = list_command(str(template_project))
    
    # ルールとノートの一覧を確認
    assert len(result["rules"]) == 2
    assert len(result["notes"]) == 2
    
    # ルールの内容を確認
    rule1 = next(rule for rule in result["rules"] if rule["title"] == "ルール1")
    assert rule1["description"] == "ルール1の説明"
    assert rule1["globs"] == "src/**/*.ts"
    assert rule1["alwaysApply"] is True
    assert rule1["tags"] == ["typescript"]
    
    rule2 = next(rule for rule in result["rules"] if rule["title"] == "ルール2")
    assert rule2["description"] == "ルール2の説明"
    assert rule2["globs"] == "src/**/*.tsx"
    assert rule2["alwaysApply"] is False
    assert rule2["tags"] == ["react"]
    
    # ノートの内容を確認
    note1 = next(note for note in result["notes"] if note["title"] == "ノート1")
    assert note1["description"] == "ノート1の説明"
    assert note1["tags"] == ["documentation"]
    
    note2 = next(note for note in result["notes"] if note["title"] == "ノート2")
    assert note2["description"] == "ノート2の説明"
    assert note2["tags"] == ["guide"]


def test_list_command_missing_template(tmp_path):
    """テンプレートディレクトリが存在しない場合の処理を確認"""
    result = list_command(str(tmp_path / "non_existent_template"))
    
    # 空のリストが返されることを確認
    assert result["rules"] == []
    assert result["notes"] == []


def test_list_command_missing_directories(template_project):
    """ルールとノートのディレクトリが存在しない場合の処理を確認"""
    # ディレクトリを削除
    shutil.rmtree(template_project / "rules")
    shutil.rmtree(template_project / "notes")
    
    result = list_command(str(template_project))
    
    # 空のリストが返されることを確認
    assert result["rules"] == []
    assert result["notes"] == []


def test_list_command_invalid_files(template_project):
    """無効なファイルの処理を確認"""
    # 無効なルールファイルを作成
    invalid_rule = template_project / "rules" / "invalid_rule.md"
    invalid_rule.write_text("""---
title: "無効なルール"
description: "無効なルールの説明"
globs: invalid glob pattern
alwaysApply: true
tags: ["invalid"]
---
# 無効なルール
無効なルールの内容
""")
    
    # 無効なノートファイルを作成
    invalid_note = template_project / "notes" / "invalid_note.md"
    invalid_note.write_text("""---
title: "無効なノート"
description: "無効なノートの説明"
tags: ["invalid"]
---
# 無効なノート
無効なノートの内容
""")
    
    result = list_command(str(template_project))
    
    # 無効なファイルは除外されることを確認
    assert len(result["rules"]) == 2
    assert len(result["notes"]) == 2
    assert not any(rule["title"] == "無効なルール" for rule in result["rules"])
    assert not any(note["title"] == "無効なノート" for note in result["notes"])


def test_list_command_nested_directories(template_project):
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
    
    result = list_command(str(template_project))
    
    # ネストされたルールが含まれることを確認
    assert len(result["rules"]) == 3
    assert any(rule["title"] == "ネストされたルール" for rule in result["rules"]) 