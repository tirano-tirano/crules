"""
テスト用の設定ファイル

このモジュールはテスト実行に必要な設定を提供します。
"""

import os
import sys
from pathlib import Path

import pytest
import shutil

# プロジェクトのルートディレクトリをPYTHONPATHに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# テスト用の環境変数を設定
os.environ["CRULES_TEMPLATE_DIR"] = str(project_root / "template")
os.environ["CRULES_TARGET_DIR"] = str(project_root / "target")


# テスト用のフィクスチャを定義
@pytest.fixture(scope="session")
def project_root():
    """プロジェクトのルートディレクトリを返すフィクスチャ"""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def template_dir(project_root):
    """テンプレートディレクトリのパスを返すフィクスチャ"""
    return project_root / "template"


@pytest.fixture(scope="session")
def target_dir(project_root):
    """ターゲットディレクトリのパスを返すフィクスチャ"""
    return project_root / "target"

@pytest.fixture
def temp_dir(tmp_path):
    """
    一時ディレクトリを提供するフィクスチャ
    """
    return tmp_path

@pytest.fixture
def sample_config_file(temp_dir):
    """
    サンプルの設定ファイルを提供するフィクスチャ
    """
    config_file = temp_dir / "config.yaml"
    config_file.write_text("""
# サンプル設定ファイル
LOG_LEVEL: INFO
LOG_FILE: test.log
TEST_COVERAGE_THRESHOLD: 80.0
""")
    return config_file

@pytest.fixture
def sample_log_file(temp_dir):
    """
    サンプルのログファイルを提供するフィクスチャ
    """
    log_file = temp_dir / "test.log"
    log_file.write_text("""
2024-03-20 10:00:00,000 - INFO - テストログメッセージ1
2024-03-20 10:00:01,000 - WARNING - テストログメッセージ2
2024-03-20 10:00:02,000 - ERROR - テストログメッセージ3
""")
    return log_file

@pytest.fixture
def test_env(tmp_path):
    """テスト環境を準備するフィクスチャ"""
    # テンプレートディレクトリを作成
    template_dir = tmp_path / "template"
    rules_dir = template_dir / "app" / "rules"
    notes_dir = template_dir / "app" / "notes"
    rules_dir.mkdir(parents=True)
    notes_dir.mkdir(parents=True)

    # 配置先ディレクトリを作成
    cursor_dir = tmp_path / ".cursor"
    notes_dir = tmp_path / ".notes"
    cursor_dir.mkdir(parents=True)
    notes_dir.mkdir(parents=True)

    yield {
        "template_dir": template_dir,
        "rules_dir": rules_dir,
        "notes_dir": notes_dir,
        "cursor_dir": cursor_dir,
        "notes_dir": notes_dir,
    }

    # クリーンアップ
    shutil.rmtree(template_dir)
    shutil.rmtree(cursor_dir)
    shutil.rmtree(notes_dir)


@pytest.fixture
def test_case(test_env):
    """テストケースごとに独立した環境を用意するフィクスチャ"""
    # テストケースごとに独立したディレクトリを作成
    case_dir = test_env["template_dir"] / "test_case"
    case_dir.mkdir(parents=True)

    yield case_dir

    # クリーンアップ
    shutil.rmtree(case_dir)


@pytest.fixture
def test_data(test_env):
    """テストデータを自動的に生成するフィクスチャ"""
    # テストデータを生成
    rule_data = {
        "title": "Test Rule",
        "description": "Test Description",
        "tags": ["test", "example"],
    }
    note_data = {
        "title": "Test Note",
        "content": "Test Content",
    }

    yield {
        "rule": rule_data,
        "note": note_data,
    }
