"""
テストモジュールのテスト

このモジュールは crules.testing モジュールのテストを提供します。
"""

import os
import sys
from pathlib import Path
import pytest
from crules.testing import run_tests, run_coverage_report

def test_run_tests_basic(tmp_path):
    """基本的なテスト実行のテスト"""
    test_file = tmp_path / "test_sample.py"
    test_file.write_text("""
def test_sample():
    assert True
""")

    exit_code = run_tests(test_file, verbose=2)
    assert exit_code == 0

def test_run_tests_with_coverage(tmp_path):
    """カバレッジ付きのテスト実行のテスト"""
    test_file = tmp_path / "test_sample2.py"
    test_file.write_text("""
def test_sample():
    assert True
""")

    exit_code = run_tests(
        test_file,
        coverage=True,
        coverage_report=True,
        coverage_html=True,
        coverage_xml=True,
        coverage_terminal=True,
        verbose=2
    )
    assert exit_code == 0

    # カバレッジレポートファイルの存在を確認
    assert (Path.cwd() / "htmlcov").exists()
    assert (Path.cwd() / "coverage.xml").exists()

def test_run_coverage_report(tmp_path):
    """カバレッジレポート生成のテスト"""
    test_file = tmp_path / "test_sample3.py"
    test_file.write_text("""
def test_sample():
    assert True
""")

    exit_code = run_coverage_report(
        test_file,
        coverage_html=True,
        coverage_xml=True,
        coverage_terminal=True,
        verbose=2
    )
    assert exit_code == 0

    # カバレッジレポートファイルの存在を確認
    assert (Path.cwd() / "htmlcov").exists()
    assert (Path.cwd() / "coverage.xml").exists() 