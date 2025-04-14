def create_validation_report(rule: dict, result: bool) -> str:
    """
    ルール検証の結果をレポート形式で生成する

    Args:
        rule (dict): 検証したルール
        result (bool): 検証結果

    Returns:
        str: レポート文字列
    """
    if result:
        return f"✅ {rule['name']}\n検証成功"
    else:
        return f"❌ {rule['name']}\n検証失敗\n{rule['message']}"
