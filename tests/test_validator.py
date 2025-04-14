import pytest
from crules.validator import validate_rule

def test_validate_rule_basic():
    """基本的なルール検証のテスト"""
    valid_rule = {
        "name": "コミットメッセージのフォーマット",
        "pattern": "^(feat|fix|docs|style|refactor|test|chore):.+$",
        "message": "コミットメッセージは 'type: description' の形式である必要があります"
    }
    
    assert validate_rule(valid_rule) == True

def test_validate_rule_missing_required():
    """必須フィールドが欠けている場合のテスト"""
    invalid_rule = {
        "name": "コミットメッセージのフォーマット",
        "pattern": "^(feat|fix|docs|style|refactor|test|chore):.+$"
        # messageフィールドが欠けている
    }
    
    with pytest.raises(ValueError):
        validate_rule(invalid_rule)

def test_validate_rule_invalid_pattern():
    """無効な正規表現パターンの場合のテスト"""
    invalid_rule = {
        "name": "コミットメッセージのフォーマット",
        "pattern": "[",  # 無効な正規表現
        "message": "コミットメッセージは 'type: description' の形式である必要があります"
    }
    
    with pytest.raises(ValueError):
        validate_rule(invalid_rule) 