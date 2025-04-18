"""
crules - コマンド実装
"""

import json
import os
from typing import Any, Dict, List, Optional, Tuple, Union
from pathlib import Path
import shutil
import logging
import argparse
import yaml

import click

from . import utils
from .utils import validate_file_content, ensure_directory
from .exceptions import FileOperationError, ValidationError

logger = logging.getLogger(__name__)


def init_command(
    project_dir: Union[str, Path],
    template_dir: Optional[Union[str, Path]] = None,
    force: bool = False,
) -> None:
    """
    プロジェクトを初期化します。

    Args:
        project_dir: プロジェクトディレクトリのパス
        template_dir: テンプレートディレクトリのパス（Noneの場合はデフォルトのテンプレートを使用）
        force: 強制的に上書きするかどうか

    Raises:
        FileOperationError: ファイル操作に失敗した場合
        ValidationError: 検証に失敗した場合
    """
    try:
        project_path = Path(project_dir)
        template_path = (
            Path(template_dir) if template_dir else get_default_template_dir()
        )

        # プロジェクトディレクトリの作成
        project_path.mkdir(parents=True, exist_ok=True)

        # テンプレートディレクトリの存在確認
        if not template_path.exists():
            error_msg = f"テンプレートディレクトリが存在しません: {template_path}"
            logger.error(error_msg)
            raise FileOperationError(error_msg)

        # テンプレートファイルのコピー
        for template_file in template_path.glob("**/*"):
            if template_file.is_file():
                # プロジェクト内の相対パスを計算
                relative_path = template_file.relative_to(template_path)
                target_path = project_path / relative_path

                # 親ディレクトリの作成
                target_path.parent.mkdir(parents=True, exist_ok=True)

                # ファイルのコピー
                if target_path.exists() and not force:
                    logger.warning(f"ファイルが既に存在します: {target_path}")
                    continue

                shutil.copy2(template_file, target_path)
                logger.info(f"ファイルをコピーしました: {target_path}")

        logger.info(f"プロジェクトを初期化しました: {project_path}")

    except FileOperationError:
        raise
    except Exception as e:
        error_msg = f"プロジェクトの初期化に失敗しました: {e}"
        logger.error(error_msg)
        raise ValidationError(error_msg)


def deploy_command(
    template_dir: str, target_dir: str = None, force: bool = False
) -> bool:
    """
    テンプレートをデプロイします。

    Args:
        template_dir (str): テンプレートディレクトリのパス
        target_dir (str, optional): デプロイ先のディレクトリ。指定されない場合はカレントディレクトリ
        force (bool, optional): 既存のファイルを強制的に上書きするかどうか

    Returns:
        bool: デプロイが成功した場合はTrue、失敗した場合はFalse

    Raises:
        FileOperationError: ファイル操作に失敗した場合
    """
    try:
        template_path = Path(template_dir)
        if not template_path.exists():
            raise FileOperationError(f"テンプレートディレクトリが存在しません: {template_dir}")

        target_path = Path(target_dir) if target_dir else Path.cwd()
        rules_dir = target_path / ".cursor" / "rules"
        notes_dir = target_path / "notes"

        # ディレクトリの作成
        ensure_directory(rules_dir)
        ensure_directory(notes_dir)

        # ルールファイルのコピー
        rules_source = template_path / "rules"
        if rules_source.exists():
            for rule_file in rules_source.glob("**/*.md"):
                relative_path = rule_file.relative_to(rules_source)
                target_file = rules_dir / relative_path.with_suffix(".mdc")
                ensure_directory(target_file.parent)
                if not target_file.exists() or force:
                    shutil.copy2(rule_file, target_file)
                    logger.info(f"ルールファイルをコピーしました: {target_file}")

        # ノートファイルのコピー
        notes_source = template_path / "notes"
        if notes_source.exists():
            for note_file in notes_source.glob("**/*.md"):
                relative_path = note_file.relative_to(notes_source)
                target_file = notes_dir / relative_path
                ensure_directory(target_file.parent)
                if not target_file.exists() or force:
                    shutil.copy2(note_file, target_file)
                    logger.info(f"ノートファイルをコピーしました: {target_file}")

        logger.info(f"テンプレートをデプロイしました: {template_path} -> {target_path}")
        return True
    except Exception as e:
        logger.error(f"テンプレートのデプロイに失敗しました: {e}")
        return False


def list_command(template_dir: str) -> Dict[str, List[Dict[str, Any]]]:
    """テンプレートディレクトリ内のルールとノートを一覧表示する

    Args:
        template_dir (str): テンプレートディレクトリのパス

    Returns:
        Dict[str, List[Dict[str, Any]]]: ルールとノートの一覧
    """
    try:
        # テンプレートディレクトリの存在確認
        if not os.path.exists(template_dir):
            utils.log_error(f"テンプレートディレクトリが存在しません: {template_dir}")
            return {"rules": [], "notes": []}

        # ルールとノートのディレクトリパス
        rules_path = os.path.join(template_dir, "rules")
        notes_path = os.path.join(template_dir, "notes")

        # ルールとノートの一覧を取得
        rules = []
        notes = []

        # ルールファイルの一覧を取得
        if os.path.exists(rules_path):
            for file in os.listdir(rules_path):
                if file.endswith(".md"):
                    file_path = os.path.join(rules_path, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    front_matter = utils.read_yaml_front_matter(content)
                    if front_matter:
                        rules.append(front_matter)

        # ノートファイルの一覧を取得
        if os.path.exists(notes_path):
            for file in os.listdir(notes_path):
                if file.endswith(".md"):
                    file_path = os.path.join(notes_path, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    front_matter = utils.read_yaml_front_matter(content)
                    if front_matter:
                        notes.append(front_matter)

        return {"rules": rules, "notes": notes}

    except Exception as e:
        utils.log_error(f"一覧表示中にエラーが発生しました: {str(e)}")
        return {"rules": [], "notes": []}


def tree_command(template_dir: Optional[str] = None) -> str:
    """テンプレートディレクトリの階層構造を表示

    Args:
        template_dir: テンプレートディレクトリのパス

    Returns:
        str: ディレクトリ構造を表す文字列
    """
    # テンプレートディレクトリのパスを取得
    if not template_dir:
        template_dir = "template"

    if not os.path.exists(template_dir):
        utils.log_error(f"テンプレートディレクトリが見つかりません: {template_dir}")
        return ""

    # ディレクトリ階層を解析
    hierarchy = utils.analyze_directory_hierarchy(template_dir)

    # 結果を格納する文字列
    result = []

    # ディレクトリ階層を表示
    result.append(f"テンプレートディレクトリ: {template_dir}")
    result.append(utils.get_directory_hierarchy_string(template_dir))

    # 詳細情報を表示
    result.append("\n詳細情報:")
    rules_path = os.path.join(template_dir, "rules")
    notes_path = os.path.join(template_dir, "notes")
    rules_count = len(utils.list_files(rules_path)) if os.path.exists(rules_path) else 0
    notes_count = len(utils.list_files(notes_path)) if os.path.exists(notes_path) else 0
    result.append(f"ルールファイル数: {rules_count}")
    result.append(f"ノートファイル数: {notes_count}")

    # 結果を表示
    output = "\n".join(result)
    click.echo(output)

    return output


class ValidationError(Exception):
    """ファイル検証時のエラーを表すクラス"""

    pass


def validate_rule_file(file_path: Path) -> None:
    """ルールファイルを検証します。

    Args:
        file_path: 検証するファイルのパス

    Raises:
        ValidationError: 検証に失敗した場合
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        if not content.startswith("---"):
            raise ValidationError(f"{file_path}: YAMLフロントマターがありません")

        # YAMLフロントマターを抽出
        _, yaml_content, _ = content.split("---", 2)
        front_matter = yaml.safe_load(yaml_content)

        # 必須フィールドの確認
        required_fields = ["description", "globs", "alwaysApply"]
        for field in required_fields:
            if field not in front_matter:
                raise ValidationError(f"{file_path}: 必須フィールド '{field}' がありません")

    except yaml.YAMLError as e:
        raise ValidationError(f"{file_path}: YAMLの解析に失敗しました: {e}")
    except ValueError:
        raise ValidationError(f"{file_path}: YAMLフロントマターの形式が不正です")


def validate_note_file(file_path: Path) -> bool:
    """ノートファイルのバリデーションを行う

    Args:
        file_path (Path): バリデーション対象のファイルパス

    Returns:
        bool: バリデーションが成功した場合はTrue、失敗した場合はFalse
    """
    try:
        content = file_path.read_text()
        if not content.strip():
            logger.error(f"{file_path}: ファイルが空です")
            return False
        return True
    except Exception as e:
        logger.error(f"{file_path}: {str(e)}")
        return False


def validate_command(path: str) -> bool:
    """
    指定されたパスのルールとノートを検証します。

    Args:
        path: 検証するプロジェクトのパス

    Returns:
        bool: 検証が成功した場合はTrue、失敗した場合はFalse
    """
    from pathlib import Path
    import logging

    project_path = Path(path)
    rules_dir = project_path / "rules"
    notes_dir = project_path / "notes"
    has_errors = False

    # rulesディレクトリの検証
    if not rules_dir.exists():
        logging.error("rulesディレクトリが存在しません")
        return False

    # ルールファイルの検証
    rule_files = list(rules_dir.glob("*.md")) + list(rules_dir.glob("*.mdc"))
    if not rule_files:
        logging.error("ルールファイルが存在しません")
        return False

    for rule_file in rule_files:
        try:
            content = rule_file.read_text(encoding="utf-8")
            if not content.strip():
                logging.error(f"{rule_file.name}: ファイルが空です")
                has_errors = True
                continue

            # YAMLフロントマターの検証
            if "---" not in content:
                logging.error(f"{rule_file.name}: YAMLフロントマターがありません")
                has_errors = True
            else:
                # YAMLフロントマターを抽出して検証
                _, yaml_content, _ = content.split("---", 2)
                front_matter = yaml.safe_load(yaml_content)
                
                # 必須フィールドの確認
                required_fields = ["description", "globs", "alwaysApply"]
                for field in required_fields:
                    if field not in front_matter:
                        logging.error(f"{rule_file.name}: 必須フィールド '{field}' がありません")
                        has_errors = True

        except Exception as e:
            logging.error(f"{rule_file.name}: ファイルの読み込みに失敗しました - {str(e)}")
            has_errors = True

    # notesディレクトリの検証
    if not notes_dir.exists():
        logging.error("notesディレクトリが存在しません")
        has_errors = True
    else:
        note_files = list(notes_dir.glob("*.md"))
        if not note_files:
            logging.error("ノートファイルが存在しません")
            has_errors = True
        else:
            for note_file in note_files:
                try:
                    content = note_file.read_text(encoding="utf-8")
                    if not content.strip():
                        logging.error(f"{note_file.name}: ファイルが空です")
                        has_errors = True

                except Exception as e:
                    logging.error(f"{note_file.name}: ファイルの読み込みに失敗しました - {str(e)}")
                    has_errors = True

    return not has_errors


def get_default_template_dir() -> Path:
    """
    デフォルトのテンプレートディレクトリのパスを取得します。

    Returns:
        Path: デフォルトのテンプレートディレクトリのパス
    """
    return Path.home() / ".cursor" / "templates"


def validate_file_content(file_path: Path, required_fields: List[str] = None) -> List[str]:
    """
    ファイルの内容を検証します。

    Args:
        file_path: 検証するファイルのパス
        required_fields: 必須フィールドのリスト（Noneの場合はデフォルト値を使用）

    Returns:
        List[str]: エラーメッセージのリスト
    """
    errors = []
    try:
        # ファイル名の検証
        if " " in file_path.name:
            errors.append("ファイル名にスペースが含まれています")
        if any(c in file_path.name for c in "@#$%^&*"):
            errors.append("ファイル名に特殊文字が含まれています")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # ルールファイルの場合のみYAMLフロントマターを検証
        if file_path.suffix == ".mdc":
            front_matter = utils.read_yaml_front_matter(content)
            if not front_matter:
                errors.append("YAML front matterが見つかりません")
                return errors

            # 必須フィールドの検証（デフォルト値を使用）
            if required_fields is None:
                required_fields = ["description", "globs", "alwaysApply"]
            
            missing_fields = [
                field for field in required_fields if field not in front_matter
            ]
            if missing_fields:
                errors.append(f"必須フィールドが欠けています: {', '.join(missing_fields)}")

            # 説明文の長さチェック
            if "description" in front_matter and len(front_matter["description"]) > 100:
                errors.append("説明文が長すぎます（100文字以内にしてください）")

            # globsフィールドの検証（ルールファイルの場合）
            if "globs" in front_matter:
                if not isinstance(front_matter["globs"], list):
                    errors.append("globsフィールドは配列である必要があります")
                elif not front_matter["globs"]:
                    errors.append("globsフィールドは空の配列にできません")

    except Exception as e:
        errors.append(f"ファイルの検証中にエラーが発生しました: {str(e)}")

    return errors
