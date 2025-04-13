"""
crules - ユーティリティ関数
"""

import os
import yaml
import shutil
import click
import glob
import fnmatch
import re
from typing import Tuple, Dict, Any, Optional, List, Union
from pathlib import Path
from datetime import datetime
from .exceptions import (
    FileOperationError,
    ValidationError,
    TemplateError,
    YAMLError,
    MarkdownError,
    DeploymentError,
    ConflictError,
)


def log_error(message: str) -> None:
    """エラーメッセージをログに記録

    Args:
        message: エラーメッセージ
    """
    click.echo(f"エラー: {message}", err=True)


def ensure_directory(path: str) -> None:
    """ディレクトリが存在することを確認し、存在しない場合は作成

    Args:
        path: ディレクトリパス
    """
    if not os.path.exists(path):
        os.makedirs(path)


def copy_file(source: str, target: str, force: bool = False) -> bool:
    """ファイルをコピー

    Args:
        source: コピー元ファイルパス
        target: コピー先ファイルパス
        force: 既存のファイルを上書きするかどうか

    Returns:
        bool: コピーが成功したかどうか
    """
    try:
        # ターゲットディレクトリを作成
        target_dir = os.path.dirname(target)
        ensure_directory(target_dir)

        # ファイルが存在する場合は上書きするかどうかを確認
        if os.path.exists(target) and not force:
            return False

        # ファイルをコピー
        shutil.copy2(source, target)
        return True
    except Exception as e:
        log_error(f"ファイルのコピーに失敗しました: {e}")
        return False


def copy_files(source_dir: str, target_dir: str, force: bool = False) -> bool:
    """ディレクトリ内のファイルをコピー

    Args:
        source_dir: コピー元ディレクトリパス
        target_dir: コピー先ディレクトリパス
        force: 既存のファイルを上書きするかどうか

    Returns:
        bool: コピーが成功したかどうか
    """
    try:
        # ターゲットディレクトリを作成
        ensure_directory(target_dir)

        # ファイルをコピー
        for root, _, files in os.walk(source_dir):
            for file in files:
                source = os.path.join(root, file)
                rel_path = os.path.relpath(root, source_dir)
                target = os.path.join(target_dir, rel_path, file)
                if not copy_file(source, target, force):
                    return False
        return True
    except Exception as e:
        log_error(f"ファイルのコピーに失敗しました: {e}")
        return False


def read_file(path: str) -> str:
    """
    ファイルを読み込みます。

    Args:
        path (str): 読み込むファイルのパス

    Returns:
        str: ファイルの内容

    Raises:
        FileOperationError: ファイルが見つからない場合やファイルの読み込みに失敗した場合
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileOperationError(f"ファイルが見つかりません: {path}")
    except Exception as e:
        raise FileOperationError(f"ファイルの読み込みに失敗しました: {e}")


def write_file(path: str, content: str) -> bool:
    """ファイルを書き込み

    Args:
        path: ファイルパス
        content: 書き込む内容

    Returns:
        bool: 書き込みが成功したかどうか
    """
    try:
        # ディレクトリを作成
        directory = os.path.dirname(path)
        ensure_directory(directory)

        # ファイルを書き込み
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        log_error(f"ファイルの書き込みに失敗しました: {e}")
        return False


def read_yaml_front_matter(file_path_or_content: str) -> Optional[Dict[str, Any]]:
    """YAMLフロントマターを読み込む

    Args:
        file_path_or_content (str): ファイルパスまたはコンテンツ文字列

    Returns:
        Optional[Dict[str, Any]]: YAMLフロントマターの内容。無効な場合はNone

    Raises:
        ValidationError: YAMLフロントマターが無効な場合
    """
    try:
        # ファイルパスの場合はファイルを読み込む
        if os.path.exists(file_path_or_content):
            with open(file_path_or_content, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = file_path_or_content

        # YAMLフロントマターを抽出
        pattern = r"^---\s*\n(.*?)\n---\s*\n"
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            raise ValidationError("YAMLフロントマターが見つかりません")

        # YAMLをパース
        try:
            front_matter = yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            raise ValidationError(f"YAMLフロントマターのパースに失敗しました: {str(e)}")

        if not isinstance(front_matter, dict):
            raise ValidationError("YAMLフロントマターは辞書形式である必要があります")

        return front_matter

    except OSError as e:
        raise ValidationError(f"ファイルの読み込みに失敗しました: {str(e)}")
    except Exception as e:
        raise ValidationError(f"YAMLフロントマターの読み込みに失敗しました: {str(e)}")


def get_yaml_front_matter(path: str) -> Dict[str, Any]:
    """ファイルからYAML front matterを取得

    Args:
        path: ファイルパス

    Returns:
        Dict[str, Any]: YAML front matter
    """
    return read_yaml_front_matter(path)


def validate_yaml_front_matter(front_matter: Dict[str, Any]) -> bool:
    """YAML front matterを検証

    Args:
        front_matter: YAML front matter

    Returns:
        bool: 検証が成功したかどうか
    """
    required_fields = ["description", "globs"]
    return all(field in front_matter for field in required_fields)


def list_files(directory: str) -> List[str]:
    """ディレクトリ内のファイルを一覧

    Args:
        directory: ディレクトリパス

    Returns:
        List[str]: ファイルパスのリスト

    Raises:
        FileOperationError: ディレクトリの操作に失敗した場合
    """
    try:
        if not os.path.exists(directory):
            error_msg = f"ディレクトリが存在しません: {directory}"
            log_error(error_msg)
            raise FileOperationError(error_msg)

        if not os.path.isdir(directory):
            error_msg = f"指定されたパスはディレクトリではありません: {directory}"
            log_error(error_msg)
            raise FileOperationError(error_msg)

        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files
    except FileOperationError as e:
        raise e
    except Exception as e:
        error_msg = f"ディレクトリの操作に失敗しました: {e}"
        log_error(error_msg)
        raise FileOperationError(error_msg)


def validate_file_format(
    file_path: str, allowed_extensions: List[str] = [".md", ".mdc"]
) -> bool:
    """ファイル形式を検証

    Args:
        file_path: ファイルパス
        allowed_extensions: 許可する拡張子のリスト

    Returns:
        bool: 検証が成功したかどうか
    """
    _, ext = os.path.splitext(file_path)
    return ext in allowed_extensions


def validate_file_size(file_path: str, max_size: int = 1024 * 1024) -> bool:
    """ファイルサイズを検証

    Args:
        file_path: ファイルパス
        max_size: 最大サイズ（バイト）

    Returns:
        bool: 検証が成功したかどうか
    """
    return os.path.getsize(file_path) <= max_size


def validate_file_content(
    file_path: str,
    required_fields: Optional[List[str]] = None,
    content: Optional[str] = None,
) -> bool:
    """ファイルの内容を検証

    Args:
        file_path: ファイルパス
        required_fields: 必須フィールドのリスト（Noneの場合はデフォルト値を使用）
        content: 検証する内容（Noneの場合はファイルから読み込み）

    Returns:
        bool: 検証が成功したかどうか
    """
    try:
        if content is None:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

        # 空のファイルは無効
        if not content:
            return False

        # YAML front matterを検証
        front_matter = read_yaml_front_matter(content)

        # 必須フィールドの検証
        if required_fields:
            if not all(field in front_matter for field in required_fields):
                return False
        elif not validate_yaml_front_matter(front_matter):
            return False

        return True
    except ValidationError:
        return False
    except Exception as e:
        log_error(f"ファイルの内容の検証に失敗しました: {e}")
        return False


def validate_file_structure(file_path: str) -> bool:
    """ファイルの構造を検証

    Args:
        file_path: ファイルパス

    Returns:
        bool: 検証が成功したかどうか
    """
    try:
        # ファイルを読み込み
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # ファイルが空でないことを確認
        if not content:
            log_error("ファイルが空です")
            return False

        # 改行コードを統一
        content = content.replace("\r\n", "\n")
        lines = content.split("\n")

        # YAML front matterの開始を確認
        if not lines or not lines[0].startswith("---"):
            log_error("YAMLフロントマターが見つかりません")
            return False

        # 2つ目の区切り文字を探す
        end_index = -1
        for i, line in enumerate(lines[1:], 1):
            if line == "---":
                end_index = i
                break

        if end_index == -1:
            log_error("YAMLフロントマターの終了マーカーが見つかりません")
            return False

        # YAML部分を抽出してパース
        yaml_content = "\n".join(lines[1:end_index])
        try:
            front_matter = yaml.safe_load(yaml_content)
            if not isinstance(front_matter, dict):
                log_error("YAMLフロントマターが辞書形式ではありません")
                return False

            # 必須フィールドの検証
            if not validate_yaml_front_matter(front_matter):
                log_error("必須フィールドが不足しています")
                return False
        except yaml.YAMLError as e:
            log_error(f"YAMLフロントマターの解析に失敗しました: {e}")
            return False

        # 本文が存在することを確認
        if len(lines) <= end_index + 1:
            log_error("本文が存在しません")
            return False

        # 本文が空でないことを確認
        body = "\n".join(lines[end_index + 1 :]).strip()
        if not body:
            log_error("本文が空です")
            return False

        return True
    except FileNotFoundError:
        log_error(f"ファイルが見つかりません: {file_path}")
        return False
    except Exception as e:
        log_error(f"ファイルの構造検証に失敗しました: {e}")
        return False


def resolve_conflict(source: str, target: str, force: bool = False) -> bool:
    """ファイルの競合を解決する

    Args:
        source: コピー元ファイルのパス
        target: コピー先ファイルのパス
        force: 強制上書きフラグ（デフォルトはFalse）

    Returns:
        bool: 競合が解決された場合はTrue、キャンセルされた場合はFalse

    Raises:
        FileOperationError: ファイル操作に失敗した場合
        ConflictError: 競合解決に失敗した場合
    """
    try:
        # ソースファイルの存在確認
        if not os.path.exists(source):
            error_msg = f"ソースファイルが存在しません: {source}"
            log_error(error_msg)
            raise FileOperationError(error_msg)

        # ターゲットファイルが存在しない場合は単純にコピー
        if not os.path.exists(target):
            shutil.copy2(source, target)
            return True

        # 強制上書きでない場合は内容を比較
        if not force:
            # 同一内容の場合はスキップ
            if is_same_file(source, target):
                log_info(f"ファイルの内容が同じため、上書きをスキップします: {target}")
                return True

            # ユーザーに上書き確認
            if not click.confirm(
                f"ファイル {target} は既に存在します。上書きしますか？", default=False
            ):
                log_info("ユーザーによってキャンセルされました")
                return False

        # バックアップの作成
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{target}.{timestamp}.bak"
        try:
            shutil.copy2(target, backup_path)
            log_info(f"バックアップを作成しました: {backup_path}")
        except Exception as e:
            error_msg = f"バックアップの作成に失敗しました: {e}"
            log_error(error_msg)
            raise ConflictError(error_msg)

        # ファイルのコピー
        shutil.copy2(source, target)
        log_info(f"ファイルを上書きしました: {target}")
        return True

    except Exception as e:
        error_msg = f"競合の解決に失敗しました: {e}"
        log_error(error_msg)
        raise ConflictError(error_msg)


def list_rules(template_dir: str) -> List[Dict[str, str]]:
    """ルールファイルの一覧を取得

    Args:
        template_dir: テンプレートディレクトリパス

    Returns:
        List[Dict[str, str]]: ルール情報のリスト

    Raises:
        FileOperationError: ディレクトリの操作に失敗した場合
    """
    try:
        rules = []
        for file_path in list_files(template_dir):
            if file_path.endswith((".md", ".mdc")):
                front_matter = read_yaml_front_matter(file_path)
                rules.append(
                    {
                        "path": file_path,
                        "title": os.path.splitext(os.path.basename(file_path))[0],
                        "description": front_matter.get("description", ""),
                        "globs": front_matter.get("globs", ""),
                        "alwaysApply": front_matter.get("alwaysApply", False),
                    }
                )
        return rules
    except Exception as e:
        error_msg = f"ルールファイルの一覧取得に失敗しました: {e}"
        log_error(error_msg)
        raise FileOperationError(error_msg)


def filter_rules(
    rules: List[Dict[str, str]], category: Optional[str] = None
) -> List[Dict[str, str]]:
    """ルールをフィルタリング

    Args:
        rules: ルール情報のリスト
        category: フィルタリングするカテゴリ

    Returns:
        List[Dict[str, str]]: フィルタリングされたルール情報のリスト
    """
    if category:
        return [rule for rule in rules if rule.get("category") == category]
    return rules


def sort_rules(rules: List[Dict[str, str]], key: str = "title") -> List[Dict[str, str]]:
    """ルールをソート

    Args:
        rules: ルール情報のリスト
        key: ソートキー

    Returns:
        List[Dict[str, str]]: ソートされたルール情報のリスト
    """
    return sorted(rules, key=lambda x: x.get(key, ""))


def display_status(message: str) -> None:
    """ステータスメッセージを表示

    Args:
        message: メッセージ
    """
    click.echo(message)


def display_progress(current: int, total: int, message: str) -> None:
    """進捗状況を表示

    Args:
        current: 現在の進捗
        total: 全体の数
        message: メッセージ
    """
    percentage = int((current / total) * 100)
    click.echo(f"\r{message}: {percentage}% ({current}/{total})", nl=False)
    if current == total:
        click.echo()


def display_completion(message: str) -> None:
    """完了メッセージを表示

    Args:
        message: メッセージ
    """
    click.echo(click.style(message, fg="green"))


def display_error(message: str) -> None:
    """エラーメッセージを表示

    Args:
        message: メッセージ
    """
    click.echo(click.style(message, fg="red"))


def log_info(message: str) -> None:
    """情報メッセージを記録

    Args:
        message: メッセージ
    """
    click.echo(message)


def log_warning(message: str) -> None:
    """警告メッセージを記録

    Args:
        message: メッセージ
    """
    click.echo(click.style(f"警告: {message}", fg="yellow"))


def validate_directory_hierarchy(directory: str) -> Tuple[bool, List[str]]:
    """ディレクトリ階層を検証

    Args:
        directory: ディレクトリパス

    Returns:
        Tuple[bool, List[str]]: 検証結果とエラーメッセージのリスト
    """
    errors = []

    # ディレクトリの存在を確認
    if not os.path.exists(directory):
        errors.append(f"ディレクトリが見つかりません: {directory}")
        return False, errors

    # ルールディレクトリの存在を確認
    rules_path = os.path.join(directory, "rules")
    if not os.path.exists(rules_path):
        errors.append(f"ルールディレクトリが見つかりません: {rules_path}")

    # ノートディレクトリの存在を確認
    notes_path = os.path.join(directory, "notes")
    if not os.path.exists(notes_path):
        errors.append(f"ノートディレクトリが見つかりません: {notes_path}")

    return len(errors) == 0, errors


def display_directory_hierarchy(directory: str, indent: int = 0) -> None:
    """ディレクトリ階層を表示

    Args:
        directory: ディレクトリパス
        indent: インデントレベル
    """
    # ディレクトリ名を表示
    if indent > 0:
        click.echo("  " * (indent - 1) + "└─ " + os.path.basename(directory))

    # サブディレクトリとファイルを表示
    try:
        items = os.listdir(directory)
        items.sort()
        for item in items:
            path = os.path.join(directory, item)
            if os.path.isdir(path):
                display_directory_hierarchy(path, indent + 1)
            else:
                click.echo("  " * indent + "└─ " + item)
    except Exception as e:
        log_error(f"ディレクトリの表示に失敗しました: {e}")


def is_same_file(file1: str, file2: str) -> bool:
    """2つのファイルの内容が同じかどうかを比較

    Args:
        file1: 比較対象ファイル1のパス
        file2: 比較対象ファイル2のパス

    Returns:
        bool: ファイルの内容が同じ場合はTrue、異なる場合はFalse

    Raises:
        FileOperationError: ファイルの読み込みに失敗した場合
    """
    try:
        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            # ファイルサイズを比較
            if os.path.getsize(file1) != os.path.getsize(file2):
                return False

            # チャンクサイズを設定（メモリ効率のため）
            CHUNK_SIZE = 8192

            while True:
                chunk1 = f1.read(CHUNK_SIZE)
                chunk2 = f2.read(CHUNK_SIZE)

                if chunk1 != chunk2:
                    return False

                if not chunk1:  # ファイルの終わりに達した
                    break

            return True

    except Exception as e:
        error_msg = f"ファイルの比較に失敗しました: {e}"
        log_error(error_msg)
        raise FileOperationError(error_msg)


def ensure_directory(path: str) -> bool:
    """ディレクトリが存在しない場合は作成

    Args:
        path: 作成するディレクトリのパス

    Returns:
        bool: ディレクトリが存在するか作成されたかどうか
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        click.echo(f"エラー: ディレクトリの作成に失敗しました: {e}")
        return False


def copy_files(source_dir: str, target_dir: str, force: bool = False) -> bool:
    """ディレクトリ内のファイルをコピー

    Args:
        source_dir: コピー元のディレクトリパス
        target_dir: コピー先のディレクトリパス
        force: 既存のファイルを上書きするかどうか

    Returns:
        bool: すべてのファイルのコピーが成功したかどうか
    """
    try:
        source_path = Path(source_dir)
        target_path = Path(target_dir)

        if not source_path.exists():
            raise FileOperationError(
                f"コピー元のディレクトリが存在しません: {source_dir}"
            )

        target_path.mkdir(parents=True, exist_ok=True)

        success = True
        for src_file in source_path.rglob("*"):
            if src_file.is_file():
                rel_path = src_file.relative_to(source_path)
                dst_file = target_path / rel_path

                if dst_file.exists() and not force:
                    click.echo(f"警告: ファイルが既に存在します: {dst_file}")
                    success = False
                    continue

                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)

        return success
    except Exception as e:
        click.echo(f"エラー: ファイルのコピーに失敗しました: {e}")
        return False


def read_file(file_path: str) -> Tuple[bool, str]:
    """ファイルを読み込む

    Args:
        file_path: 読み込むファイルのパス

    Returns:
        Tuple[bool, str]: (成功したかどうか, ファイルの内容)
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileOperationError(f"ファイルが存在しません: {file_path}")

        return True, path.read_text(encoding="utf-8")
    except Exception as e:
        click.echo(f"エラー: ファイルの読み込みに失敗しました: {e}")
        return False, ""


def write_file(file_path: str, content: str) -> bool:
    """ファイルに書き込む

    Args:
        file_path: 書き込むファイルのパス
        content: 書き込む内容

    Returns:
        bool: 書き込みが成功したかどうか
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        click.echo(f"エラー: ファイルの書き込みに失敗しました: {e}")
        return False


def parse_yaml_front_matter(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """YAML front matterを解析する

    Args:
        content: 解析するファイルの内容

    Returns:
        Tuple[Optional[Dict[str, Any]], str]: (YAML front matter, ファイルの内容)
    """
    if not content.startswith("---"):
        return None, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content

    try:
        front_matter = yaml.safe_load(parts[1])
        return front_matter, parts[2].strip()
    except yaml.YAMLError as e:
        raise YAMLError(f"YAML front matterの解析に失敗しました: {e}")


def generate_yaml_front_matter(data: Dict[str, Any]) -> str:
    """YAML front matterを生成する

    Args:
        data: YAML front matterのデータ

    Returns:
        str: 生成されたYAML front matter
    """
    try:
        yaml_content = yaml.dump(data, allow_unicode=True, sort_keys=False)
        return f"---\n{yaml_content}---\n"
    except yaml.YAMLError as e:
        raise YAMLError(f"YAML front matterの生成に失敗しました: {e}")


def update_yaml_front_matter(file_path: str, data: Dict[str, Any]) -> bool:
    """YAML front matterを更新する

    Args:
        file_path: 更新するファイルのパス
        data: 更新するデータ

    Returns:
        bool: 更新が成功したかどうか
    """
    try:
        success, content = read_file(file_path)
        if not success:
            return False

        front_matter, body = parse_yaml_front_matter(content)
        if front_matter is None:
            return False

        # 既存のデータを更新
        front_matter.update(data)

        # 新しいYAML front matterを生成
        new_front_matter = generate_yaml_front_matter(front_matter)

        # ファイルに書き込む
        new_content = f"{new_front_matter}{body}"
        return write_file(file_path, new_content)
    except Exception as e:
        click.echo(f"エラー: YAML front matterの更新に失敗しました: {e}")
        return False


def validate_yaml_structure(
    data: Dict[str, Any], required_fields: List[str]
) -> Tuple[bool, List[str]]:
    """YAMLデータの構造を検証する

    Args:
        data: 検証するYAMLデータ
        required_fields: 必須フィールドのリスト

    Returns:
        Tuple[bool, List[str]]: (検証が成功したかどうか, 不足しているフィールドのリスト)
    """
    missing_fields = [field for field in required_fields if field not in data]
    return len(missing_fields) == 0, missing_fields


def process_mdc_file(file_path: str) -> Tuple[bool, Dict[str, Any]]:
    """MDCファイルを処理する

    Args:
        file_path: 処理するファイルのパス

    Returns:
        Tuple[bool, Dict[str, Any]]: (処理が成功したかどうか, 処理結果)
    """
    try:
        front_matter, content = read_yaml_front_matter(file_path)
        if not front_matter:
            raise MarkdownError(f"YAML front matterが見つかりません: {file_path}")

        # 必須フィールドの検証
        required_fields = ["title", "description"]
        is_valid, missing_fields = validate_yaml_structure(
            front_matter, required_fields
        )
        if not is_valid:
            raise MarkdownError(
                f"必須フィールドが不足しています: {', '.join(missing_fields)}"
            )

        # ファイルサイズの検証
        file_size = get_file_size(file_path)
        if file_size > 10000:  # 10KB以上のファイルは警告
            click.echo(
                f"警告: ファイルサイズが大きすぎます: {file_path} ({file_size} bytes)"
            )

        return True, {
            "front_matter": front_matter,
            "content": content,
            "file_size": file_size,
        }
    except Exception as e:
        click.echo(f"エラー: MDCファイルの処理に失敗しました: {e}")
        return False, {}


def process_md_file(file_path: str) -> Tuple[bool, Dict[str, Any]]:
    """MDファイルを処理する

    Args:
        file_path: 処理するファイルのパス

    Returns:
        Tuple[bool, Dict[str, Any]]: (処理が成功したかどうか, 処理結果)
    """
    try:
        front_matter, content = read_yaml_front_matter(file_path)
        if not front_matter:
            raise MarkdownError(f"YAML front matterが見つかりません: {file_path}")

        # 必須フィールドの検証
        required_fields = ["title", "description"]
        is_valid, missing_fields = validate_yaml_structure(
            front_matter, required_fields
        )
        if not is_valid:
            raise MarkdownError(
                f"必須フィールドが不足しています: {', '.join(missing_fields)}"
            )

        # ファイルサイズの検証
        file_size = get_file_size(file_path)
        if file_size > 10000:  # 10KB以上のファイルは警告
            click.echo(
                f"警告: ファイルサイズが大きすぎます: {file_path} ({file_size} bytes)"
            )

        return True, {
            "front_matter": front_matter,
            "content": content,
            "file_size": file_size,
        }
    except Exception as e:
        click.echo(f"エラー: MDファイルの処理に失敗しました: {e}")
        return False, {}


def parse_markdown(content: str) -> Dict[str, Any]:
    """マークダウンを解析する

    Args:
        content: 解析するマークダウンの内容

    Returns:
        Dict[str, Any]: 解析結果
    """
    try:
        # 見出しの抽出
        headings = re.findall(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE)

        # リンクの抽出
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

        # コードブロックの抽出
        code_blocks = re.findall(r"```([^`]*?)```", content, re.DOTALL)

        return {
            "headings": [{"level": len(h[0]), "text": h[1]} for h in headings],
            "links": [{"text": l[0], "url": l[1]} for l in links],
            "code_blocks": code_blocks,
        }
    except Exception as e:
        raise MarkdownError(f"マークダウンの解析に失敗しました: {e}")


def validate_markdown(content: str) -> Tuple[bool, List[str]]:
    """マークダウンを検証する

    Args:
        content: 検証するマークダウンの内容

    Returns:
        Tuple[bool, List[str]]: (検証が成功したかどうか, エラーメッセージのリスト)
    """
    errors = []

    # 見出しの検証
    headings = re.findall(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE)
    if not headings:
        errors.append("見出しが見つかりません")

    # リンクの検証
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
    for link in links:
        if not link[1].startswith(("http://", "https://", "#", "/")):
            errors.append(f"無効なリンク: {link[0]} -> {link[1]}")

    # コードブロックの検証
    code_blocks = re.findall(r"```([^`]*?)```", content, re.DOTALL)
    for i, block in enumerate(code_blocks):
        if not block.strip():
            errors.append(f"空のコードブロック: #{i+1}")

    return len(errors) == 0, errors


def list_files(directory: str, pattern: Optional[str] = None) -> List[str]:
    """ディレクトリ内のファイルを列挙する

    Args:
        directory: 列挙するディレクトリのパス
        pattern: ファイル名のパターン（例: *.md）

    Returns:
        List[str]: ファイルのパスのリスト
    """
    try:
        path = Path(directory)
        if not path.exists():
            return []

        if pattern:
            return [str(f) for f in path.rglob(pattern)]
        else:
            return [str(f) for f in path.rglob("*") if f.is_file()]
    except Exception as e:
        click.echo(f"エラー: ファイルの列挙に失敗しました: {e}")
        return []


def find_files(directory: str, pattern: str) -> List[str]:
    """指定したパターンに一致するファイルを検索する

    Args:
        directory: 検索するディレクトリのパス
        pattern: 検索パターン（例: **/*.md）

    Returns:
        List[str]: 一致するファイルのパスのリスト
    """
    try:
        path = Path(directory)
        if not path.exists():
            return []

        return [str(f) for f in path.glob(pattern)]
    except Exception as e:
        click.echo(f"エラー: ファイルの検索に失敗しました: {e}")
        return []


def is_file_empty(file_path: str) -> bool:
    """ファイルが空かどうかを確認する

    Args:
        file_path: 確認するファイルのパス

    Returns:
        bool: ファイルが空かどうか
    """
    try:
        path = Path(file_path)
        return not path.exists() or path.stat().st_size == 0
    except Exception as e:
        click.echo(f"エラー: ファイルの確認に失敗しました: {e}")
        return True


def get_file_size(file_path: str) -> int:
    """ファイルのサイズを取得する

    Args:
        file_path: サイズを取得するファイルのパス

    Returns:
        int: ファイルのサイズ（バイト）
    """
    try:
        path = Path(file_path)
        return path.stat().st_size if path.exists() else 0
    except Exception as e:
        click.echo(f"エラー: ファイルサイズの取得に失敗しました: {e}")
        return 0


def get_file_extension(file_path: str) -> str:
    """ファイルの拡張子を取得する

    Args:
        file_path: 拡張子を取得するファイルのパス

    Returns:
        str: ファイルの拡張子（例: .md）
    """
    return Path(file_path).suffix


def is_same_file(file1: str, file2: str) -> bool:
    """2つのファイルが同じかどうかを確認する

    Args:
        file1: 1つ目のファイルのパス
        file2: 2つ目のファイルのパス

    Returns:
        bool: 2つのファイルが同じかどうか
    """
    try:
        path1 = Path(file1)
        path2 = Path(file2)
        return path1.exists() and path2.exists() and path1.samefile(path2)
    except Exception as e:
        click.echo(f"エラー: ファイルの比較に失敗しました: {e}")
        return False


def validate_template_directory(template_dir: str) -> bool:
    """テンプレートディレクトリの構造を検証する

    Args:
        template_dir: テンプレートディレクトリのパス

    Returns:
        bool: テンプレートディレクトリの構造が有効かどうか
    """
    try:
        path = Path(template_dir)
        if not path.exists():
            raise TemplateError(
                f"テンプレートディレクトリが存在しません: {template_dir}"
            )

        # 必須ディレクトリの確認
        rules_dir = path / "rules"
        notes_dir = path / "notes"

        if not rules_dir.exists():
            click.echo(f"警告: ルールディレクトリが見つかりません: {rules_dir}")
            return False

        if not notes_dir.exists():
            click.echo(f"警告: ノートディレクトリが見つかりません: {notes_dir}")
            return False

        return True
    except Exception as e:
        click.echo(f"エラー: テンプレートディレクトリの検証に失敗しました: {e}")
        return False


def check_template_files(template_dir: str) -> Tuple[bool, List[str]]:
    """テンプレートファイルの存在を確認する

    Args:
        template_dir: テンプレートディレクトリのパス

    Returns:
        Tuple[bool, List[str]]: (すべてのファイルが存在するかどうか, 存在しないファイルのリスト)
    """
    try:
        path = Path(template_dir)
        if not path.exists():
            raise TemplateError(
                f"テンプレートディレクトリが存在しません: {template_dir}"
            )

        missing_files = []

        # ルールファイルの確認
        rules_dir = path / "rules"
        if rules_dir.exists():
            rule_files = list(rules_dir.glob("*.mdc"))
            if not rule_files:
                missing_files.append(f"{rules_dir}/*.mdc")
        else:
            missing_files.append(str(rules_dir))

        # ノートファイルの確認
        notes_dir = path / "notes"
        if notes_dir.exists():
            note_files = list(notes_dir.glob("*.md"))
            if not note_files:
                missing_files.append(f"{notes_dir}/*.md")
        else:
            missing_files.append(str(notes_dir))

        return len(missing_files) == 0, missing_files
    except Exception as e:
        click.echo(f"エラー: テンプレートファイルの確認に失敗しました: {e}")
        return False, [str(e)]


def load_template_directory(template_dir: str) -> Dict[str, List[str]]:
    """テンプレートディレクトリを読み込む

    Args:
        template_dir: テンプレートディレクトリのパス

    Returns:
        Dict[str, List[str]]: テンプレートファイルのリスト
    """
    try:
        path = Path(template_dir)
        if not path.exists():
            raise TemplateError(
                f"テンプレートディレクトリが存在しません: {template_dir}"
            )

        result = {"rules": [], "notes": []}

        # ルールファイルの読み込み
        rules_dir = path / "rules"
        if rules_dir.exists():
            result["rules"] = [str(f) for f in rules_dir.glob("*.mdc")]

        # ノートファイルの読み込み
        notes_dir = path / "notes"
        if notes_dir.exists():
            result["notes"] = [str(f) for f in notes_dir.glob("*.md")]

        return result
    except Exception as e:
        click.echo(f"エラー: テンプレートディレクトリの読み込みに失敗しました: {e}")
        return {"rules": [], "notes": []}


def list_template_directories(base_dir: str = "template") -> List[str]:
    """テンプレートディレクトリを列挙する

    Args:
        base_dir: ベースディレクトリのパス

    Returns:
        List[str]: テンプレートディレクトリのリスト
    """
    try:
        path = Path(base_dir)
        if not path.exists():
            return []

        return [d.name for d in path.iterdir() if d.is_dir()]
    except Exception as e:
        click.echo(f"エラー: テンプレートディレクトリの列挙に失敗しました: {e}")
        return []


def deploy_file(source: str, target: str, force: bool = False) -> bool:
    """ファイルを配置する

    Args:
        source: 配置元のファイルパス
        target: 配置先のファイルパス
        force: 既存のファイルを上書きするかどうか

    Returns:
        bool: 配置が成功したかどうか
    """
    try:
        source_path = Path(source)
        target_path = Path(target)

        if not source_path.exists():
            raise DeploymentError(f"配置元のファイルが存在しません: {source}")

        # 配置先のディレクトリを作成
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # 既存のファイルをチェック
        if target_path.exists() and not force:
            click.echo(f"警告: ファイルが既に存在します: {target}")
            return False

        # ファイルをコピー
        shutil.copy2(source_path, target_path)
        click.echo(f"ファイルを配置しました: {target}")
        return True
    except Exception as e:
        click.echo(f"エラー: ファイルの配置に失敗しました: {e}")
        return False


def deploy_directory(source_dir: str, target_dir: str, force: bool = False) -> bool:
    """ディレクトリ内のファイルを配置する

    Args:
        source_dir: 配置元のディレクトリパス
        target_dir: 配置先のディレクトリパス
        force: 既存のファイルを上書きするかどうか

    Returns:
        bool: すべてのファイルの配置が成功したかどうか
    """
    try:
        source_path = Path(source_dir)
        target_path = Path(target_dir)

        if not source_path.exists():
            raise DeploymentError(f"配置元のディレクトリが存在しません: {source_dir}")

        # 配置先のディレクトリを作成
        target_path.mkdir(parents=True, exist_ok=True)

        success = True
        for src_file in source_path.rglob("*"):
            if src_file.is_file():
                rel_path = src_file.relative_to(source_path)
                dst_file = target_path / rel_path

                # 既存のファイルをチェック
                if dst_file.exists() and not force:
                    click.echo(f"警告: ファイルが既に存在します: {dst_file}")
                    success = False
                    continue

                # 配置先のディレクトリを作成
                dst_file.parent.mkdir(parents=True, exist_ok=True)

                # ファイルをコピー
                shutil.copy2(src_file, dst_file)
                click.echo(f"ファイルを配置しました: {dst_file}")

        return success
    except Exception as e:
        click.echo(f"エラー: ディレクトリの配置に失敗しました: {e}")
        return False


def move_file(source: str, target: str, force: bool = False) -> bool:
    """ファイルを移動する

    Args:
        source: 移動元のファイルパス
        target: 移動先のファイルパス
        force: 既存のファイルを上書きするかどうか

    Returns:
        bool: 移動が成功したかどうか
    """
    try:
        source_path = Path(source)
        target_path = Path(target)

        if not source_path.exists():
            raise DeploymentError(f"移動元のファイルが存在しません: {source}")

        # 移動先のディレクトリを作成
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # 既存のファイルをチェック
        if target_path.exists() and not force:
            click.echo(f"警告: ファイルが既に存在します: {target}")
            return False

        # ファイルを移動
        shutil.move(source_path, target_path)
        click.echo(f"ファイルを移動しました: {target}")
        return True
    except Exception as e:
        click.echo(f"エラー: ファイルの移動に失敗しました: {e}")
        return False


def analyze_directory_hierarchy(directory: str) -> Dict[str, Any]:
    """ディレクトリ階層を解析する

    Args:
        directory: 解析するディレクトリのパス

    Returns:
        Dict[str, Any]: ディレクトリ階層の解析結果
    """
    try:
        path = Path(directory)
        if not path.exists():
            raise FileOperationError(f"ディレクトリが存在しません: {directory}")

        result = {
            "name": path.name,
            "path": str(path),
            "is_dir": path.is_dir(),
            "children": [],
        }

        if path.is_dir():
            for item in path.iterdir():
                if item.is_dir():
                    result["children"].append(analyze_directory_hierarchy(str(item)))
                else:
                    result["children"].append(
                        {
                            "name": item.name,
                            "path": str(item),
                            "is_dir": False,
                            "extension": item.suffix,
                        }
                    )

        return result
    except Exception as e:
        click.echo(f"エラー: ディレクトリ階層の解析に失敗しました: {e}")
        return {"name": path.name, "path": str(path), "is_dir": False, "children": []}


def create_directory_hierarchy(base_dir: str, structure: Dict[str, Any]) -> bool:
    """ディレクトリ階層を作成する

    Args:
        base_dir: ベースディレクトリのパス
        structure: 作成するディレクトリ階層の構造

    Returns:
        bool: ディレクトリ階層の作成が成功したかどうか
    """
    try:
        base_path = Path(base_dir)
        base_path.mkdir(parents=True, exist_ok=True)

        for item in structure:
            item_path = base_path / item["name"]

            if item["is_dir"]:
                item_path.mkdir(parents=True, exist_ok=True)
                if "children" in item and item["children"]:
                    create_directory_hierarchy(str(item_path), item["children"])
            else:
                # 空のファイルを作成
                item_path.touch()

        return True
    except Exception as e:
        click.echo(f"エラー: ディレクトリ階層の作成に失敗しました: {e}")
        return False


def display_directory_hierarchy(directory: str, indent: int = 0) -> None:
    """ディレクトリ階層を表示する

    Args:
        directory: 表示するディレクトリのパス
        indent: インデントの深さ
    """
    try:
        path = Path(directory)
        if not path.exists():
            click.echo(f"ディレクトリが存在しません: {directory}")
            return

        # ディレクトリ名を表示
        prefix = "  " * indent
        click.echo(f"{prefix}{'📁' if path.is_dir() else '📄'} {path.name}")

        # 子要素を表示
        if path.is_dir():
            for item in sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name)):
                display_directory_hierarchy(str(item), indent + 1)
    except Exception as e:
        click.echo(f"エラー: ディレクトリ階層の表示に失敗しました: {e}")


def validate_file_format(
    file_path: str, allowed_extensions: List[str] = [".md", ".mdc"]
) -> bool:
    """ファイル形式を検証

    Args:
        file_path: ファイルパス
        allowed_extensions: 許可する拡張子のリスト

    Returns:
        bool: 検証が成功したかどうか
    """
    _, ext = os.path.splitext(file_path)
    return ext in allowed_extensions


def validate_file_size(file_path: str, max_size: int = 1024 * 1024) -> bool:
    """ファイルサイズを検証

    Args:
        file_path: ファイルパス
        max_size: 最大サイズ（バイト）

    Returns:
        bool: 検証が成功したかどうか
    """
    return os.path.getsize(file_path) <= max_size


def detect_existing_file(target: str) -> bool:
    """既存のファイルを検出する

    Args:
        target: 検出するファイルパス

    Returns:
        bool: 既存のファイルが存在するかどうか
    """
    return os.path.exists(target)


def confirm_overwrite(target: str) -> bool:
    """上書きを確認する

    Args:
        target: 上書きするファイルパス

    Returns:
        bool: 上書きするかどうか
    """
    response = input(f"既存のファイルを上書きしますか？ ({target}) [y/N]: ")
    return response.lower() == "y"


def backup_file(file_path: str) -> Optional[str]:
    """ファイルをバックアップする

    Args:
        file_path: バックアップするファイルパス

    Returns:
        Optional[str]: バックアップファイルパス、失敗した場合はNone
    """
    try:
        backup_path = f"{file_path}.bak"
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        click.echo(f"ファイルのバックアップに失敗しました: {e}")
        return None


def list_templates(template_dir: str) -> List[Dict[str, Any]]:
    """テンプレート一覧を取得する

    Args:
        template_dir: テンプレートディレクトリパス

    Returns:
        List[Dict[str, Any]]: テンプレート一覧
    """
    templates = []

    if not os.path.exists(template_dir):
        return templates

    for item in os.listdir(template_dir):
        item_path = os.path.join(template_dir, item)
        if os.path.isdir(item_path):
            templates.append(
                {
                    "name": item,
                    "path": item_path,
                    "rules_count": len(list_rules(item_path)),
                }
            )

    return templates


def log_debug(message: str) -> None:
    """デバッグ情報をログに記録する

    Args:
        message: デバッグメッセージ
    """
    click.echo(f"デバッグ: {message}")


def display_progress(current: int, total: int, message: str = "") -> None:
    """進捗を表示する

    Args:
        current: 現在の進捗
        total: 合計
        message: メッセージ
    """
    percentage = int(current / total * 100) if total > 0 else 0
    click.echo(f"進捗: {percentage}% ({current}/{total}) {message}")


def display_status(message: str) -> None:
    """ステータスを表示する

    Args:
        message: ステータスメッセージ
    """
    click.echo(f"ステータス: {message}")


def display_completion(message: str) -> None:
    """完了を表示する

    Args:
        message: 完了メッセージ
    """
    click.echo(f"完了: {message}")


def display_error(message: str) -> None:
    """エラーを表示する

    Args:
        message: エラーメッセージ
    """
    click.echo(f"エラー: {message}")


def get_directory_hierarchy_string(path: str) -> str:
    """ディレクトリ階層を文字列として取得

    Args:
        path: ディレクトリパス

    Returns:
        str: ディレクトリ階層を表す文字列
    """
    result = []
    base_name = os.path.basename(path)
    result.append(f"📁 {base_name}")

    for root, dirs, files in os.walk(path):
        level = root[len(path):].count(os.sep)
        indent = "  " * (level + 1)
        rel_path = os.path.relpath(root, path)

        if rel_path != ".":
            result.append(f"{indent}📁 {os.path.basename(root)}")

        for file in files:
            result.append(f"{indent}  📄 {file}")

    return "\n".join(result)
