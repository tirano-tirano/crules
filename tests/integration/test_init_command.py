"""
Integration tests for the init command.

This module tests the functionality of the init command, which:
- Creates a new project directory
- Copies template files to the project directory
- Handles force flag for overwriting existing files
"""

import os
import shutil
from pathlib import Path
import pytest
from crules.commands import init_command
from crules.exceptions import FileOperationError, ValidationError

@pytest.fixture
def template_project(tmp_path):
    """Create a template project structure."""
    template_dir = tmp_path / "template"
    
    # Create template structure
    app_dir = template_dir / "app"
    rules_dir = app_dir / "rules"
    notes_dir = app_dir / "notes"
    
    # Create directories
    for directory in [template_dir, app_dir, rules_dir, notes_dir]:
        directory.mkdir(parents=True)
    
    # Create rule files
    rule_files = [
        ("rule1.md", """---
description: "ルール1の説明"
globs: "src/**/*.ts, src/**/*.tsx"
alwaysApply: true
---
# ルール1
ルール1の内容
"""),
        
        ("rule2.md", """---
description: "ルール2の説明"
globs: "src/**/*.ts, src/**/*.tsx"
alwaysApply: false
---
# ルール2
ルール2の内容
""")
    ]
    
    # Create note files
    note_files = [
        ("note1.md", """---
description: "ノート1の説明"
---
# ノート1
ノート1の内容
"""),
        
        ("note2.md", """---
description: "ノート2の説明"
---
# ノート2
ノート2の内容
""")
    ]
    
    # Write rule files
    for filename, content in rule_files:
        file_path = rules_dir / filename
        file_path.write_text(content)
    
    # Write note files
    for filename, content in note_files:
        file_path = notes_dir / filename
        file_path.write_text(content)
    
    return template_dir

def test_init_command_success(template_project, tmp_path):
    """Test successful project initialization."""
    project_dir = tmp_path / "new_project"
    
    # Execute init command
    init_command(project_dir, template_project)
    
    # Check if project directory was created
    assert project_dir.exists()
    
    # Check if template files were copied
    app_dir = project_dir / "app"
    rules_dir = app_dir / "rules"
    notes_dir = app_dir / "notes"
    
    assert app_dir.exists()
    assert rules_dir.exists()
    assert notes_dir.exists()
    
    # Check rule files
    rule_files = list(rules_dir.glob("*.md"))
    assert len(rule_files) == 2
    
    # Check specific rule files
    rule1_path = rules_dir / "rule1.md"
    rule2_path = rules_dir / "rule2.md"
    assert rule1_path.exists()
    assert rule2_path.exists()
    
    # Check rule content
    rule1_content = rule1_path.read_text()
    assert 'description: "ルール1の説明"' in rule1_content
    assert "globs: src/**/*.ts, src/**/*.tsx" in rule1_content
    assert "alwaysApply: true" in rule1_content
    
    rule2_content = rule2_path.read_text()
    assert 'description: "ルール2の説明"' in rule2_content
    assert "globs: src/**/*.ts, src/**/*.tsx" in rule2_content
    assert "alwaysApply: false" in rule2_content
    
    # Check note files
    note_files = list(notes_dir.glob("*.md"))
    assert len(note_files) == 2
    
    # Check specific note files
    note1_path = notes_dir / "note1.md"
    note2_path = notes_dir / "note2.md"
    assert note1_path.exists()
    assert note2_path.exists()
    
    # Check note content
    note1_content = note1_path.read_text()
    assert 'description: "ノート1の説明"' in note1_content
    assert "alwaysApply: false" in note1_content
    
    note2_content = note2_path.read_text()
    assert 'description: "ノート2の説明"' in note2_content
    assert "alwaysApply: true" in note2_content

def test_init_command_missing_template(template_project, tmp_path):
    """Test initialization with missing template directory."""
    project_dir = tmp_path / "new_project"
    non_existent_dir = tmp_path / "non_existent"
    
    # Execute init command with non-existent template
    with pytest.raises(FileOperationError) as excinfo:
        init_command(project_dir, non_existent_dir)
    
    assert "テンプレートディレクトリが存在しません" in str(excinfo.value)
    
    # Check that project directory was not created
    assert not project_dir.exists()

def test_init_command_existing_project(template_project, tmp_path):
    """Test initialization with existing project directory."""
    project_dir = tmp_path / "existing_project"
    project_dir.mkdir()
    
    # Create a file in the project directory
    existing_file = project_dir / "existing_file.txt"
    existing_file.write_text("既存のファイル")
    
    # Execute init command without force flag
    init_command(project_dir, template_project)
    
    # Check that existing file was preserved
    assert existing_file.exists()
    assert existing_file.read_text() == "既存のファイル"
    
    # Check that template files were copied
    app_dir = project_dir / "app"
    assert app_dir.exists()
    
    # Execute init command with force flag
    init_command(project_dir, template_project, force=True)
    
    # Check that template files were copied again
    rules_dir = app_dir / "rules"
    notes_dir = app_dir / "notes"
    
    assert rules_dir.exists()
    assert notes_dir.exists()
    
    # Check rule files
    rule_files = list(rules_dir.glob("*.md"))
    assert len(rule_files) == 2
    
    # Check note files
    note_files = list(notes_dir.glob("*.md"))
    assert len(note_files) == 2

def test_init_command_nested_directories(template_project, tmp_path):
    """Test initialization with nested directories in template."""
    project_dir = tmp_path / "nested_project"
    
    # Create nested directory in template
    nested_dir = template_project / "app" / "rules" / "nested"
    nested_dir.mkdir(parents=True)
    
    # Create nested rule file
    nested_rule = nested_dir / "nested_rule.md"
    nested_rule.write_text("""---
description: "ネストされたルールの説明"
globs: "src/**/*.ts"
alwaysApply: true
---
# ネストされたルール
ネストされたルールの内容
""")
    
    # Execute init command
    init_command(project_dir, template_project)
    
    # Check if nested directory was created
    target_nested_dir = project_dir / "app" / "rules" / "nested"
    assert target_nested_dir.exists()
    
    # Check if nested rule file was copied
    target_nested_rule = target_nested_dir / "nested_rule.md"
    assert target_nested_rule.exists()
    
    # Check nested rule content
    nested_rule_content = target_nested_rule.read_text()
    assert 'description: "ネストされたルールの説明"' in nested_rule_content
    assert "globs: src/**/*.ts" in nested_rule_content
    assert "alwaysApply: true" in nested_rule_content
    
    # Cleanup
    shutil.rmtree(nested_dir) 