import pytest
from crules.reporter import create_validation_report

def test_create_validation_report_success():
    """検証成功時のレポート生成テスト"""
    rule = {
        "name": "コミットメッセージのフォーマット",
        "pattern": "^(feat|fix|docs|style|refactor|test|chore):.+$",
        "message": "コミットメッセージは 'type: description' の形式である必要があります"
    }
    result = True
    
    report = create_validation_report(rule, result)
    assert "✅" in report
    assert rule["name"] in report
    assert "検証成功" in report

def test_create_validation_report_failure():
    """検証失敗時のレポート生成テスト"""
    rule = {
        "name": "コミットメッセージのフォーマット",
        "pattern": "^(feat|fix|docs|style|refactor|test|chore):.+$",
        "message": "コミットメッセージは 'type: description' の形式である必要があります"
    }
    result = False
    
    report = create_validation_report(rule, result)
    assert "❌" in report
    assert rule["name"] in report
    assert rule["message"] in report
    assert "検証失敗" in report 