"""
crulesパッケージの例外クラスを定義するモジュール
"""

class CrulesError(Exception):
    """crulesの基本例外クラス"""
    pass

class FileOperationError(CrulesError):
    """ファイル操作に関する例外"""
    pass

class ValidationError(CrulesError):
    """検証に関する例外"""
    pass

class ConfigurationError(CrulesError):
    """設定に関する例外"""
    pass

class TemplateError(CrulesError):
    """テンプレートに関する例外"""
    pass

class CommandError(CrulesError):
    """コマンド実行に関する例外"""
    pass

class YAMLError(CrulesError):
    """YAML解析に関する例外"""
    pass

class MarkdownError(CrulesError):
    """マークダウン解析に関する例外"""
    pass

class DeploymentError(CrulesError):
    """デプロイに関する例外"""
    pass

class ConflictError(CrulesError):
    """競合解決に関する例外"""
    pass 