import re


def validate_rule(rule: dict) -> bool:
    """
    ルールの検証を行う

    Args:
        rule (dict): 検証するルール

    Returns:
        bool: ルールが有効な場合はTrue

    Raises:
        ValueError: ルールが無効な場合
    """
    # 必須フィールドの確認
    required_fields = ["name", "pattern", "message"]
    for field in required_fields:
        if field not in rule:
            raise ValueError(f"必須フィールド '{field}' が欠けています")

    # 正規表現パターンの検証
    try:
        re.compile(rule["pattern"])
    except re.error:
        raise ValueError("無効な正規表現パターンです")

    return True
