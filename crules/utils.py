"""
Utility functions for the crules package.
"""

import os
import yaml
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from .exceptions import ValidationError, FileOperationError

from .logger import get_logger

logger = get_logger(__name__)

def read_yaml_front_matter(content: Union[str, Path]) -> Optional[Dict[str, Any]]:
    """
    マークダウンファイルからYAML front matterを読み込みます。

    Args:
        content: マークダウンファイルの内容またはファイルパス

    Returns:
        Optional[Dict[str, Any]]: YAML front matterの内容。存在しない場合はNone
    """
    try:
        # ファイルパスが渡された場合は内容を読み込む
        if isinstance(content, Path):
            with open(content, 'r', encoding='utf-8') as f:
                content = f.read()

        # YAML front matterの開始と終了を検出
        if not content.startswith("---\n"):
            return None

        end_index = content.find("\n---\n")
        if end_index == -1:
            return None

        # YAML front matterを抽出
        yaml_content = content[4:end_index].strip()
        if not yaml_content:
            return None

        # YAMLをパース
        try:
            return yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            logger.warning(f"YAMLのパースに失敗しました: {str(e)}")
            return None

    except Exception as e:
        logger.warning(f"YAML front matterの読み込みに失敗しました: {str(e)}")
        return None

def validate_file_content(file_path: Union[str, Path], required_fields: Optional[List[str]] = None) -> List[str]:
    """
    ファイルの内容を検証します。

    Args:
        file_path: 検証するファイルのパス
        required_fields: 必須フィールドのリスト（オプショナル）

    Returns:
        List[str]: 不足している必須フィールドのリスト。空のリストは検証が成功したことを示します。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # YAMLフロントマターの検証
        if not content.startswith('---\n'):
            return required_fields or []

        # YAMLフロントマターの抽出
        front_matter = read_yaml_front_matter(content)
        if not front_matter:
            return required_fields or []

        # 必須フィールドの検証
        if required_fields:
            return [field for field in required_fields if field not in front_matter]

        return []
    except Exception:
        return required_fields or []

def ensure_directory(directory: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Directory path
        
    Returns:
        Path object for the directory
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_file_extension(file_path: Union[str, Path]) -> str:
    """
    Get the extension of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension without the dot
    """
    return Path(file_path).suffix.lstrip('.')

def is_valid_file(file_path: Union[str, Path], allowed_extensions: Optional[List[str]] = None) -> bool:
    """
    Check if a file is valid based on its extension.
    
    Args:
        file_path: Path to the file
        allowed_extensions: List of allowed file extensions
        
    Returns:
        True if the file is valid, False otherwise
    """
    if not allowed_extensions:
        return True
        
    extension = get_file_extension(file_path)
    return extension.lower() in [ext.lower() for ext in allowed_extensions]

def copy_file(src: Path, dst: Path) -> None:
    """
    ファイルをコピーします。

    Args:
        src (Path): コピー元のファイルパス
        dst (Path): コピー先のファイルパス

    Raises:
        FileOperationError: ファイルのコピーに失敗した場合
    """
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        log_error(f"ファイルのコピーに失敗しました: {src} -> {dst}, エラー: {e}")
        raise FileOperationError(f"ファイルのコピーに失敗しました: {src} -> {dst}") from e

def log_error(message: str) -> None:
    """
    エラーメッセージをログに出力します。

    Args:
        message (str): ログに出力するメッセージ
    """
    logger.error(message)

def list_files(directory: str, pattern: Optional[str] = None, recursive: bool = False) -> List[Path]:
    """
    指定されたディレクトリ内のファイルをリストアップします。
    
    Args:
        directory (str or Path): 検索対象のディレクトリ
        pattern (str, optional): ファイル名のパターン（glob形式）
        recursive (bool, optional): サブディレクトリも検索するかどうか
    
    Returns:
        list: ファイルパスのリスト
    """
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        return []
    
    if pattern:
        if recursive:
            return list(directory.glob(f"**/{pattern}"))
        else:
            return list(directory.glob(pattern))
    else:
        if recursive:
            return list(directory.glob("**/*"))
        else:
            return list(directory.glob("*"))

def read_file(file_path: str) -> str:
    """
    ファイルの内容を読み込みます。
    
    Args:
        file_path (str or Path): 読み込むファイルのパス
    
    Returns:
        str: ファイルの内容
    
    Raises:
        FileOperationError: ファイルが存在しない場合、または読み込みに失敗した場合
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileOperationError(f"ファイルが存在しません: {file_path}")
    
    try:
        return file_path.read_text(encoding='utf-8')
    except Exception as e:
        raise FileOperationError(f"ファイルの読み込みに失敗しました: {file_path}") from e 

def resolve_conflict(source_path: str, target_path: str, force: bool = False) -> bool:
    """
    ファイルの競合を解決します。
    
    Args:
        source_path (str or Path): ソースファイルのパス
        target_path (str or Path): ターゲットファイルのパス
        force (bool, optional): 強制上書きするかどうか
    
    Returns:
        bool: 競合が解決されたかどうか
    
    Raises:
        FileOperationError: ファイルの操作に失敗した場合
    """
    source_path = Path(source_path)
    target_path = Path(target_path)
    
    if not source_path.exists():
        raise FileOperationError(f"ソースファイルが存在しません: {source_path}")
    
    if target_path.exists():
        if force:
            try:
                target_path.unlink()
                return True
            except Exception as e:
                raise FileOperationError(f"ファイルの削除に失敗しました: {target_path}") from e
        else:
            return False
    
    return True 

def validate_file_format(file_path: str, required_fields: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    ファイルのフォーマットを検証し、YAMLフロントマターを抽出します。
    
    Args:
        file_path (str or Path): 検証するファイルのパス
        required_fields (list, optional): 必須フィールドのリスト
    
    Returns:
        dict: 抽出されたYAMLフロントマター
    
    Raises:
        ValidationError: ファイルのフォーマットが無効な場合
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except OSError as e:
        raise ValidationError(f"ファイルを読み込めません: {file_path}") from e
    
    # YAMLフロントマターを抽出
    if not content.startswith('---\n'):
        raise ValidationError(f"YAMLフロントマターが見つかりません: {file_path}")
    
    try:
        # YAMLフロントマターを解析
        front_matter_end = content.find('\n---\n', 4)
        if front_matter_end == -1:
            raise ValidationError(f"YAMLフロントマターの終端が見つかりません: {file_path}")
        
        front_matter = yaml.safe_load(content[4:front_matter_end])
        if not isinstance(front_matter, dict):
            raise ValidationError(f"無効なYAMLフロントマター: {file_path}")
        
        # 必須フィールドの検証
        if required_fields:
            missing_fields = [field for field in required_fields if field not in front_matter]
            if missing_fields:
                raise ValidationError(f"必須フィールドが欠けています: {', '.join(missing_fields)}")
        
        return front_matter
    except yaml.YAMLError as e:
        raise ValidationError(f"YAMLフロントマターの解析に失敗しました: {file_path}") from e

def validate_file_size(file_path: str, max_size: int = 1024 * 1024) -> bool:
    """
    ファイルサイズを検証します。
    
    Args:
        file_path (str or Path): 検証するファイルのパス
        max_size (int, optional): 最大ファイルサイズ（バイト）
    
    Returns:
        bool: ファイルサイズが制限内の場合はTrue
    
    Raises:
        ValidationError: ファイルサイズが制限を超えている場合
        FileOperationError: ファイルが存在しない場合
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileOperationError(f"ファイルが存在しません: {file_path}")
    
    file_size = file_path.stat().st_size
    if file_size > max_size:
        raise ValidationError(
            f"ファイルサイズが制限を超えています: {file_size} bytes "
            f"(最大: {max_size} bytes)"
        )
    
    return True 

def validate_file_structure(file_path: str, required_sections: Optional[List[str]] = None) -> bool:
    """
    ファイルの構造を検証します。
    
    Args:
        file_path (str or Path): 検証するファイルのパス
        required_sections (list, optional): 必須セクションのリスト
    
    Returns:
        bool: ファイル構造が有効な場合はTrue
    
    Raises:
        ValidationError: ファイル構造が無効な場合
        FileOperationError: ファイルが存在しない場合
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except OSError as e:
        raise FileOperationError(f"ファイルを読み込めません: {file_path}") from e
    
    # YAMLフロントマターの検証
    if not content.startswith('---\n'):
        raise ValidationError(f"YAMLフロントマターが見つかりません: {file_path}")
    
    front_matter_end = content.find('\n---\n', 4)
    if front_matter_end == -1:
        raise ValidationError(f"YAMLフロントマターの終端が見つかりません: {file_path}")
    
    # Markdownコンテンツの検証
    markdown_content = content[front_matter_end + 5:]
    if not markdown_content.strip():
        raise ValidationError(f"Markdownコンテンツが空です: {file_path}")
    
    # 必須セクションの検証
    if required_sections:
        sections = [line.strip('# \n') for line in markdown_content.split('\n')
                   if line.startswith('# ') or line.startswith('## ')]
        missing_sections = [section for section in required_sections
                          if section not in sections]
        if missing_sections:
            raise ValidationError(
                f"必須セクションが欠けています: {', '.join(missing_sections)}"
            )
    
    return True 

def write_file(file_path: str, content: str, force: bool = False) -> bool:
    """
    ファイルに内容を書き込みます。
    
    Args:
        file_path (str or Path): 書き込み先のファイルパス
        content (str): 書き込む内容
        force (bool, optional): 既存ファイルを上書きするかどうか
    
    Returns:
        bool: 書き込みが成功した場合はTrue
    
    Raises:
        FileOperationError: ファイルの書き込みに失敗した場合
    """
    file_path = Path(file_path)
    
    # ディレクトリが存在しない場合は作成
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # ファイルが存在し、forceがFalseの場合はエラー
    if file_path.exists() and not force:
        raise FileOperationError(f"ファイルが既に存在します: {file_path}")
    
    try:
        file_path.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        raise FileOperationError(f"ファイルの書き込みに失敗しました: {file_path}") from e 

def analyze_directory_hierarchy(directory: str) -> Dict[str, Any]:
    """
    ディレクトリの階層構造を解析します。
    
    Args:
        directory (str or Path): 解析するディレクトリのパス
    
    Returns:
        dict: ディレクトリ構造の情報
        {
            'name': ディレクトリ名,
            'path': ディレクトリのパス,
            'rules': ルールファイルのリスト,
            'notes': ノートファイルのリスト,
            'subdirs': サブディレクトリのリスト
        }
    
    Raises:
        FileOperationError: ディレクトリが存在しない場合
    """
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        raise FileOperationError(f"ディレクトリが存在しません: {directory}")
    
    result = {
        'name': directory.name,
        'path': str(directory),
        'rules': [],
        'notes': [],
        'subdirs': []
    }
    
    try:
        # ファイルとディレクトリを列挙
        for item in directory.iterdir():
            if item.is_file():
                if item.suffix == '.md':
                    if 'rules' in str(item):
                        result['rules'].append(str(item))
                    elif 'notes' in str(item):
                        result['notes'].append(str(item))
            elif item.is_dir():
                # サブディレクトリを再帰的に解析
                subdir_info = analyze_directory_hierarchy(item)
                result['subdirs'].append(subdir_info)
                # サブディレクトリのルールとノートを集計
                result['rules'].extend(subdir_info['rules'])
                result['notes'].extend(subdir_info['notes'])
    except Exception as e:
        raise FileOperationError(f"ディレクトリの解析に失敗しました: {directory}") from e
    
    return result 

def get_directory_hierarchy_string(directory: Union[str, Path], prefix: str = "", is_last: bool = True) -> str:
    """
    ディレクトリ階層を文字列として表示します。

    Args:
        directory: ディレクトリのパス
        prefix: 現在の階層を表示するためのプレフィックス
        is_last: 現在のディレクトリが最後の要素かどうか

    Returns:
        str: ディレクトリ階層を表す文字列
    """
    directory = Path(directory)
    if not directory.exists():
        return ""

    result = []
    current_prefix = "└── " if is_last else "├── "
    result.append(f"{prefix}{current_prefix}{directory.name}")

    items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    for i, item in enumerate(items):
        next_prefix = prefix + ("    " if is_last else "│   ")
        if item.is_dir():
            result.append(get_directory_hierarchy_string(item, next_prefix, i == len(items) - 1))
        else:
            item_prefix = "└── " if i == len(items) - 1 else "├── "
            result.append(f"{next_prefix}{item_prefix}{item.name}")

    return "\n".join(result) 

def ensure_dir(path: Path) -> None:
    """
    ディレクトリが存在することを確認し、存在しない場合は作成します。

    Args:
        path (Path): 確認または作成するディレクトリのパス

    Raises:
        FileOperationError: ディレクトリの作成に失敗した場合
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        log_error(f"ディレクトリの作成に失敗しました: {path}, エラー: {e}")
        raise FileOperationError(f"ディレクトリの作成に失敗しました: {path}") from e 

def validate_yaml_front_matter(content: Union[str, Path], required_fields: Optional[List[str]] = None) -> bool:
    """
    YAML front matterを検証します。

    Args:
        content: マークダウンファイルの内容またはファイルパス
        required_fields: 必須フィールドのリスト

    Returns:
        bool: 検証が成功した場合はTrue、失敗した場合はFalse

    Raises:
        ValidationError: 検証に失敗した場合
    """
    try:
        front_matter = read_yaml_front_matter(content)
        if not front_matter:
            return False

        if required_fields:
            missing_fields = [field for field in required_fields if field not in front_matter]
            if missing_fields:
                return False

        return True
    except Exception:
        return False 