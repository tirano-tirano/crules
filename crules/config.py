"""
設定管理モジュール

このモジュールは環境変数の読み込みと設定の管理を行います。
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# .envファイルの読み込み
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# デフォルト設定
DEFAULT_CONFIG = {
    "APP_ENV": "development",
    "DEBUG": True,
    "LOG_LEVEL": "INFO",
    "LOG_FILE": "crules.log",
    "TEST_COVERAGE_THRESHOLD": 80,
    "SECRET_KEY": "default-secret-key",
}


def get_env(key: str, default: Any = None) -> Any:
    """
    環境変数を取得します。

    Args:
        key: 環境変数のキー
        default: デフォルト値

    Returns:
        環境変数の値
    """
    return os.getenv(key, default)


def get_config(key: str, default: Any = None) -> Any:
    """
    設定値を取得します。

    Args:
        key: 設定のキー
        default: デフォルト値

    Returns:
        設定値
    """
    # 環境変数から取得を試みる
    value = get_env(key)
    if value is not None:
        return value

    # デフォルト設定から取得
    return DEFAULT_CONFIG.get(key, default)


def get_all_config() -> Dict[str, Any]:
    """
    すべての設定を取得します。

    Returns:
        すべての設定を含む辞書
    """
    config = DEFAULT_CONFIG.copy()

    # 環境変数で上書き
    for key in config:
        value = get_env(key)
        if value is not None:
            config[key] = value

    return config
