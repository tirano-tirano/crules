"""
crules - コマンド実装
"""

import os
import json
import click
from typing import Optional, List, Dict, Any, Tuple
from . import utils


def init_command(target_dir: str = ".") -> bool:
    """プロジェクトを初期化する

    Args:
        target_dir (str): 初期化対象のディレクトリパス

    Returns:
        bool: 初期化が成功したかどうか
    """
    try:
        # ターゲットディレクトリの存在確認
        if not os.path.exists(target_dir):
            utils.log_error(f"ターゲットディレクトリが存在しません: {target_dir}")
            return False

        # appディレクトリを作成
        app_dir = os.path.join(target_dir, "app")
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)

        # rulesディレクトリを作成
        rules_dir = os.path.join(app_dir, "rules")
        if not os.path.exists(rules_dir):
            os.makedirs(rules_dir)

        # notesディレクトリを作成
        notes_dir = os.path.join(app_dir, "notes")
        if not os.path.exists(notes_dir):
            os.makedirs(notes_dir)

        # サンプルルールファイルを作成
        sample_rule = """---
description: "サンプルルール"
globs: "src/**/*.ts"
alwaysApply: false
---

# サンプルルール
これはサンプルルールです。
"""
        rule_path = os.path.join(rules_dir, "test_rule.mdc")
        if os.path.exists(rule_path):
            # 既存のファイルをバックアップ
            backup_path = rule_path + ".bak"
            os.rename(rule_path, backup_path)
        with open(rule_path, "w", encoding="utf-8") as f:
            f.write(sample_rule)

        # サンプルノートファイルを作成
        sample_note = """---
description: "サンプルノート"
category: "development"
---

# サンプルノート
これはサンプルノートです。
"""
        note_path = os.path.join(notes_dir, "test_note.md")
        if os.path.exists(note_path):
            # 既存のファイルをバックアップ
            backup_path = note_path + ".bak"
            os.rename(note_path, backup_path)
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(sample_note)

        print("完了: プロジェクトの初期化が完了しました")
        return True

    except Exception as e:
        utils.log_error(f"初期化中にエラーが発生しました: {str(e)}")
        return False


def deploy_command(template_dir: str, target_dir: str) -> bool:
    """テンプレートをデプロイする

    Args:
        template_dir (str): テンプレートディレクトリのパス
        target_dir (str): デプロイ先のディレクトリパス

    Returns:
        bool: デプロイが成功したかどうか
    """
    try:
        # テンプレートディレクトリの存在確認
        if not os.path.exists(template_dir):
            utils.log_error(f"テンプレートディレクトリが存在しません: {template_dir}")
            return False

        # ターゲットディレクトリの存在確認
        if not os.path.exists(target_dir):
            utils.log_error(f"ターゲットディレクトリが存在しません: {target_dir}")
            return False

        # appディレクトリを作成
        target_app_dir = os.path.join(target_dir, "app")
        if not os.path.exists(target_app_dir):
            os.makedirs(target_app_dir)

        # rulesディレクトリを作成
        target_rules_path = os.path.join(target_app_dir, "rules")
        if not os.path.exists(target_rules_path):
            os.makedirs(target_rules_path)

        # notesディレクトリを作成
        target_notes_path = os.path.join(target_app_dir, "notes")
        if not os.path.exists(target_notes_path):
            os.makedirs(target_notes_path)

        # ルールファイルをコピー
        template_rules_path = os.path.join(template_dir, "app", "rules")
        if os.path.exists(template_rules_path):
            for file in os.listdir(template_rules_path):
                if file.endswith(".md"):
                    source = os.path.join(template_rules_path, file)
                    target = os.path.join(target_rules_path, file.replace(".md", ".mdc"))
                    utils.copy_file(source, target)

        # ノートファイルをコピー
        template_notes_path = os.path.join(template_dir, "app", "notes")
        if os.path.exists(template_notes_path):
            for file in os.listdir(template_notes_path):
                if file.endswith(".md"):
                    source = os.path.join(template_notes_path, file)
                    target = os.path.join(target_notes_path, file)
                    utils.copy_file(source, target)

        print("完了: テンプレートのデプロイが完了しました")
        return True

    except Exception as e:
        utils.log_error(f"デプロイ中にエラーが発生しました: {str(e)}")
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
        rules_path = os.path.join(template_dir, "app", "rules")
        notes_path = os.path.join(template_dir, "app", "notes")

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
    rules_path = os.path.join(template_dir, "app", "rules")
    notes_path = os.path.join(template_dir, "app", "notes")
    rules_count = len(utils.list_files(rules_path)) if os.path.exists(rules_path) else 0
    notes_count = len(utils.list_files(notes_path)) if os.path.exists(notes_path) else 0
    result.append(f"ルールファイル数: {rules_count}")
    result.append(f"ノートファイル数: {notes_count}")

    # 結果を表示
    output = "\n".join(result)
    click.echo(output)

    return output


def validate_command(template_dir: str) -> bool:
    """テンプレートディレクトリの構造を検証する

    Args:
        template_dir (str): テンプレートディレクトリのパス

    Returns:
        bool: 検証が成功したかどうか
    """
    try:
        # テンプレートディレクトリの存在確認
        if not os.path.exists(template_dir):
            utils.log_error(f"テンプレートディレクトリが存在しません: {template_dir}")
            return False

        # appディレクトリの存在確認
        app_dir = os.path.join(template_dir, "app")
        if not os.path.exists(app_dir):
            utils.log_error(f"appディレクトリが見つかりません: {app_dir}")
            return False

        # ルールとノートのディレクトリの存在確認
        rules_path = os.path.join(app_dir, "rules")
        notes_path = os.path.join(app_dir, "notes")

        if not os.path.exists(rules_path):
            utils.log_error(f"ルールディレクトリが見つかりません: {rules_path}")
            return False

        if not os.path.exists(notes_path):
            utils.log_error(f"ノートディレクトリが見つかりません: {notes_path}")
            return False

        # ルールファイルの検証
        for file in os.listdir(rules_path):
            if file.endswith(".md"):
                file_path = os.path.join(rules_path, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                front_matter = utils.read_yaml_front_matter(content)
                if not front_matter:
                    utils.log_error(f"ルールファイルのフロントマターが無効です: {file_path}")
                    return False

        # ノートファイルの検証
        for file in os.listdir(notes_path):
            if file.endswith(".md"):
                file_path = os.path.join(notes_path, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                front_matter = utils.read_yaml_front_matter(content)
                if not front_matter:
                    utils.log_error(f"ノートファイルのフロントマターが無効です: {file_path}")
                    return False

        return True

    except Exception as e:
        utils.log_error(f"検証中にエラーが発生しました: {str(e)}")
        return False
