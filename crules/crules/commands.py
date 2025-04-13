"""
crules - コマンド実装
"""

import os
import json
import click
from typing import Optional, List, Dict, Any, Tuple
from . import utils


def init_command(template_dir: Optional[str] = None, force: bool = False) -> bool:
    """テンプレートからプロジェクトルールとノートを配置
    
    Args:
        template_dir: テンプレートディレクトリ名
        force: 既存のファイルを上書きするかどうか
        
    Returns:
        bool: 処理が成功したかどうか
    """
    # テンプレートディレクトリのパスを取得
    if template_dir:
        template_path = os.path.join('template', template_dir)
        if not os.path.exists(template_path):
            utils.log_error(f"テンプレートディレクトリ '{template_dir}' が見つかりません")
            return False
    else:
        template_path = 'template'
        if not os.path.exists(template_path):
            utils.log_error("テンプレートディレクトリが見つかりません")
            return False

    # テンプレートディレクトリの構造を検証
    is_valid, errors = utils.validate_directory_hierarchy(template_path)
    if not is_valid:
        for error in errors:
            utils.log_error(error)
        return False

    # ディレクトリ階層を解析
    hierarchy = utils.analyze_directory_hierarchy(template_path)
    utils.display_status("ディレクトリ階層を解析しています...")
    utils.display_directory_hierarchy(template_path)

    # ルールの配置
    rules_path = os.path.join(template_path, 'rules')
    if os.path.exists(rules_path):
        utils.display_status("ルールを配置しています...")
        success = True
        total_files = len(utils.list_files(rules_path))
        processed_files = 0
        
        for root, _, files in os.walk(rules_path):
            for file in files:
                if file.endswith('.md'):  # .mdファイルを処理
                    source = os.path.join(root, file)
                    rel_path = os.path.relpath(root, rules_path)
                    # 拡張子を.mdcに変更
                    target_file = os.path.splitext(file)[0] + '.mdc'
                    target = os.path.join('.cursor/rules', rel_path, target_file)
                    
                    # ファイル形式を検証
                    if not utils.validate_file_format(source, ['.md']):
                        utils.log_error(f"無効なファイル形式です: {source}")
                        success = False
                        continue
                    
                    # ファイルサイズを検証
                    if not utils.validate_file_size(source, 1024 * 1024):  # 1MB
                        utils.log_error(f"ファイルサイズが大きすぎます: {source}")
                        success = False
                        continue
                    
                    # ファイル内容を検証
                    missing_fields = utils.validate_file_content(source, ['description'])
                    if missing_fields:
                        utils.log_error(f"必須フィールドがありません: {', '.join(missing_fields)} in {source}")
                        success = False
                        continue
                    
                    # ファイル構造を検証
                    structure_errors = utils.validate_file_structure(source)
                    if structure_errors:
                        for error in structure_errors:
                            utils.log_error(f"{error} in {source}")
                        success = False
                        continue
                    
                    # 競合を解決
                    if utils.resolve_conflict(source, target, force):
                        utils.log_info(f"ルールを配置しました: {source} -> {target}")
                    else:
                        success = False
                    
                    processed_files += 1
                    utils.display_progress(processed_files, total_files, "ルールの配置")
        
        if success:
            utils.display_completion("ルールの配置が完了しました")
        else:
            utils.display_error("ルールの配置中にエラーが発生しました")
    else:
        utils.log_warning(f"ルールディレクトリが見つかりません: {rules_path}")

    # ノートの配置
    notes_path = os.path.join(template_path, 'notes')
    if os.path.exists(notes_path):
        utils.display_status("ノートを配置しています...")
        success = True
        total_files = len(utils.list_files(notes_path))
        processed_files = 0
        
        for root, _, files in os.walk(notes_path):
            for file in files:
                if file.endswith('.md'):
                    source = os.path.join(root, file)
                    rel_path = os.path.relpath(root, notes_path)
                    target = os.path.join('.notes', rel_path, file)
                    
                    # ファイル形式を検証
                    if not utils.validate_file_format(source, ['.md']):
                        utils.log_error(f"無効なファイル形式です: {source}")
                        success = False
                        continue
                    
                    # ファイルサイズを検証
                    if not utils.validate_file_size(source, 1024 * 1024):  # 1MB
                        utils.log_error(f"ファイルサイズが大きすぎます: {source}")
                        success = False
                        continue
                    
                    # ファイル内容を検証
                    missing_fields = utils.validate_file_content(source, ['description'])
                    if missing_fields:
                        utils.log_error(f"必須フィールドがありません: {', '.join(missing_fields)} in {source}")
                        success = False
                        continue
                    
                    # ファイル構造を検証
                    structure_errors = utils.validate_file_structure(source)
                    if structure_errors:
                        for error in structure_errors:
                            utils.log_error(f"{error} in {source}")
                        success = False
                        continue
                    
                    # 競合を解決
                    if utils.resolve_conflict(source, target, force):
                        utils.log_info(f"ノートを配置しました: {source} -> {target}")
                    else:
                        success = False
                    
                    processed_files += 1
                    utils.display_progress(processed_files, total_files, "ノートの配置")
        
        if success:
            utils.display_completion("ノートの配置が完了しました")
        else:
            utils.display_error("ノートの配置中にエラーが発生しました")
    else:
        utils.log_warning(f"ノートディレクトリが見つかりません: {notes_path}")
        
    return True


def deploy_command(template_dir: Optional[str] = None, force: bool = False) -> bool:
    """編集済みファイルの配置
    
    Args:
        template_dir: テンプレートディレクトリ名
        force: 既存のファイルを上書きするかどうか
        
    Returns:
        bool: 処理が成功したかどうか
    """
    # テンプレートディレクトリのパスを取得
    if template_dir:
        template_path = os.path.join('template', template_dir)
        if not os.path.exists(template_path):
            utils.log_error(f"テンプレートディレクトリ '{template_dir}' が見つかりません")
            return False
    else:
        template_path = 'template'
        if not os.path.exists(template_path):
            utils.log_error("テンプレートディレクトリが見つかりません")
            return False

    # テンプレートディレクトリの構造を検証
    is_valid, errors = utils.validate_directory_hierarchy(template_path)
    if not is_valid:
        for error in errors:
            utils.log_error(error)
        return False

    # ディレクトリ階層を解析
    hierarchy = utils.analyze_directory_hierarchy(template_path)
    utils.display_status("ディレクトリ階層を解析しています...")
    utils.display_directory_hierarchy(template_path)

    # ルールの配置
    rules_path = os.path.join(template_path, 'rules')
    if os.path.exists(rules_path):
        utils.display_status("編集済みルールを配置しています...")
        success = True
        total_files = len(utils.list_files(rules_path))
        processed_files = 0
        
        for root, _, files in os.walk(rules_path):
            for file in files:
                if file.endswith('.md'):  # .mdファイルを処理
                    source = os.path.join(root, file)
                    rel_path = os.path.relpath(root, rules_path)
                    # 拡張子を.mdcに変更
                    target_file = os.path.splitext(file)[0] + '.mdc'
                    target = os.path.join('.cursor/rules', rel_path, target_file)
                    
                    # ファイル形式を検証
                    if not utils.validate_file_format(source, ['.md']):
                        utils.log_error(f"無効なファイル形式です: {source}")
                        success = False
                        continue
                    
                    # ファイルサイズを検証
                    if not utils.validate_file_size(source, 1024 * 1024):  # 1MB
                        utils.log_error(f"ファイルサイズが大きすぎます: {source}")
                        success = False
                        continue
                    
                    # ファイル内容を検証
                    missing_fields = utils.validate_file_content(source, ['description'])
                    if missing_fields:
                        utils.log_error(f"必須フィールドがありません: {', '.join(missing_fields)} in {source}")
                        success = False
                        continue
                    
                    # ファイル構造を検証
                    structure_errors = utils.validate_file_structure(source)
                    if structure_errors:
                        for error in structure_errors:
                            utils.log_error(f"{error} in {source}")
                        success = False
                        continue
                    
                    # 競合を解決
                    if utils.resolve_conflict(source, target, force):
                        utils.log_info(f"編集済みルールを配置しました: {source} -> {target}")
                    else:
                        success = False
                    
                    processed_files += 1
                    utils.display_progress(processed_files, total_files, "編集済みルールの配置")
        
        if success:
            utils.display_completion("編集済みルールの配置が完了しました")
        else:
            utils.display_error("編集済みルールの配置中にエラーが発生しました")
        return success
    else:
        utils.log_warning(f"ルールディレクトリが見つかりません: {rules_path}")
        return False


def list_command(template_dir: Optional[str] = None, format: str = 'text') -> bool:
    """利用可能なルールの一覧表示
    
    Args:
        template_dir: テンプレートディレクトリ名
        format: 出力形式（text/json）
        
    Returns:
        bool: 処理が成功したかどうか
    """
    # テンプレートディレクトリのパスを取得
    if template_dir:
        template_path = os.path.join('template', template_dir)
        if not os.path.exists(template_path):
            utils.log_error(f"テンプレートディレクトリ '{template_dir}' が見つかりません")
            return False
    else:
        template_path = 'template'
        if not os.path.exists(template_path):
            utils.log_error("テンプレートディレクトリが見つかりません")
            return False

    # ディレクトリ階層を解析
    hierarchy = utils.analyze_directory_hierarchy(template_path)

    # ルールの一覧を取得
    rules = utils.list_rules(template_path)
    
    # カテゴリでフィルタリング
    rules = utils.filter_rules(rules)
    
    # タイトルでソート
    rules = utils.sort_rules(rules)
    
    # 出力形式に応じて表示
    if format == 'json':
        result = {
            'hierarchy': hierarchy,
            'rules': rules
        }
        click.echo(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # ディレクトリ階層を表示
        utils.display_status("\nディレクトリ階層:")
        utils.display_directory_hierarchy(template_path)
        
        # ルール一覧を表示
        utils.display_status("\n利用可能なルール:")
        if not rules:
            utils.log_info("利用可能なルールはありません")
            return False
        for rule in rules:
            click.echo(f"\nファイル: {rule['file']}")
            click.echo(f"タイトル: {rule['title']}")
            click.echo(f"説明: {rule['description']}")
            if rule.get('category'):
                click.echo(f"カテゴリ: {rule['category']}")
            
    return True


def tree_command(template_dir: Optional[str] = None) -> bool:
    """テンプレートディレクトリの階層構造を表示
    
    Args:
        template_dir: テンプレートディレクトリ名
        
    Returns:
        bool: 処理が成功したかどうか
    """
    # テンプレートディレクトリのパスを取得
    if template_dir:
        template_path = os.path.join('template', template_dir)
        if not os.path.exists(template_path):
            utils.log_error(f"テンプレートディレクトリ '{template_dir}' が見つかりません")
            return False
    else:
        template_path = 'template'
        if not os.path.exists(template_path):
            utils.log_error("テンプレートディレクトリが見つかりません")
            return False

    # ディレクトリ階層を解析
    hierarchy = utils.analyze_directory_hierarchy(template_path)

    # ディレクトリ階層を表示
    utils.display_status(f"テンプレートディレクトリ: {template_path}")
    utils.display_directory_hierarchy(template_path)

    # 詳細情報を表示
    utils.display_status("\n詳細情報:")
    rules_count = len(utils.list_files(os.path.join(template_path, 'rules')))
    notes_count = len(utils.list_files(os.path.join(template_path, 'notes')))
    click.echo(f"ルールファイル数: {rules_count}")
    click.echo(f"ノートファイル数: {notes_count}")
    
    return True


def validate_command(template_dir: Optional[str] = None) -> bool:
    """テンプレートディレクトリの構造を検証
    
    Args:
        template_dir: テンプレートディレクトリ名
        
    Returns:
        bool: 処理が成功したかどうか
    """
    # テンプレートディレクトリのパスを取得
    if template_dir:
        template_path = os.path.join('template', template_dir)
        if not os.path.exists(template_path):
            utils.log_error(f"テンプレートディレクトリ '{template_dir}' が見つかりません")
            return False
    else:
        template_path = 'template'
        if not os.path.exists(template_path):
            utils.log_error("テンプレートディレクトリが見つかりません")
            return False

    # テンプレートディレクトリの構造を検証
    is_valid, errors = utils.validate_directory_hierarchy(template_path)
    if not is_valid:
        utils.display_error("テンプレートディレクトリの構造に問題があります:")
        for error in errors:
            utils.log_error(error)
        return False

    # ディレクトリ階層を解析
    hierarchy = utils.analyze_directory_hierarchy(template_path)

    # ファイルの検証
    utils.display_status("\nファイルの検証を実行しています...")
    success = True
    
    # ルールファイルの検証
    rules_path = os.path.join(template_path, 'rules')
    if os.path.exists(rules_path):
        for root, _, files in os.walk(rules_path):
            for file in files:
                if file.endswith('.md'):  # .mdファイルを検証
                    source = os.path.join(root, file)
                    
                    # ファイル形式を検証
                    if not utils.validate_file_format(source, ['.md']):
                        utils.log_error(f"無効なファイル形式です: {source}")
                        success = False
                        continue
                    
                    # ファイルサイズを検証
                    if not utils.validate_file_size(source, 1024 * 1024):  # 1MB
                        utils.log_error(f"ファイルサイズが大きすぎます: {source}")
                        success = False
                        continue
                    
                    # ファイル内容を検証
                    missing_fields = utils.validate_file_content(source, ['description'])
                    if missing_fields:
                        utils.log_error(f"必須フィールドがありません: {', '.join(missing_fields)} in {source}")
                        success = False
                        continue
                    
                    # ファイル構造を検証
                    structure_errors = utils.validate_file_structure(source)
                    if structure_errors:
                        for error in structure_errors:
                            utils.log_error(f"{error} in {source}")
                        success = False
                        continue
    
    # ノートファイルの検証
    notes_path = os.path.join(template_path, 'notes')
    if os.path.exists(notes_path):
        for root, _, files in os.walk(notes_path):
            for file in files:
                if file.endswith('.md'):
                    source = os.path.join(root, file)
                    
                    # ファイル形式を検証
                    if not utils.validate_file_format(source, ['.md']):
                        utils.log_error(f"無効なファイル形式です: {source}")
                        success = False
                        continue
                    
                    # ファイルサイズを検証
                    if not utils.validate_file_size(source, 1024 * 1024):  # 1MB
                        utils.log_error(f"ファイルサイズが大きすぎます: {source}")
                        success = False
                        continue
                    
                    # ファイル内容を検証
                    missing_fields = utils.validate_file_content(source, ['description'])
                    if missing_fields:
                        utils.log_error(f"必須フィールドがありません: {', '.join(missing_fields)} in {source}")
                        success = False
                        continue
                    
                    # ファイル構造を検証
                    structure_errors = utils.validate_file_structure(source)
                    if structure_errors:
                        for error in structure_errors:
                            utils.log_error(f"{error} in {source}")
                        success = False
                        continue
    
    if success:
        utils.display_completion("テンプレートディレクトリの検証が完了しました")
        return True
    else:
        utils.display_error("テンプレートディレクトリの検証中にエラーが発生しました")
        return False 