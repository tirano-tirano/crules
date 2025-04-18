class ValidationError(Exception):
    """バリデーションエラーを表す例外クラス"""
    pass

def validate_rule_file(file_path: str) -> None:
    """
    ルールファイルを検証します。

    Args:
        file_path (str): 検証するルールファイルのパス

    Raises:
        ValidationError: バリデーションエラーが発生した場合
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # YAMLフロントマターの検証
    if not content.startswith('---\n'):
        raise ValidationError("YAMLフロントマターがありません")

    try:
        # YAMLフロントマターを抽出
        _, yaml_content, _ = content.split('---\n', 2)
        yaml.safe_load(yaml_content)
    except (ValueError, yaml.YAMLError) as e:
        raise ValidationError(f"YAMLフロントマターの形式が不正です: {str(e)}")

def validate_note_file(file_path: str) -> None:
    """
    ノートファイルを検証します。

    Args:
        file_path (str): 検証するノートファイルのパス

    Raises:
        ValidationError: バリデーションエラーが発生した場合
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # YAMLフロントマターの検証
    if not content.startswith('---\n'):
        raise ValidationError("YAMLフロントマターがありません")

    try:
        # YAMLフロントマターを抽出
        _, yaml_content, _ = content.split('---\n', 2)
        yaml.safe_load(yaml_content)
    except (ValueError, yaml.YAMLError) as e:
        raise ValidationError(f"YAMLフロントマターの形式が不正です: {str(e)}") 