import os
import sys
import pytest
from pathlib import Path

# プロジェクトのルートディレクトリをPythonパスに追加
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
