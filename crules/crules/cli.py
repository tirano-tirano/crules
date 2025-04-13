"""
crules - コマンドラインインターフェース
"""

import click
from typing import Optional
from . import commands


@click.group()
@click.version_option(version="0.1.0", prog_name="crules")
def cli():
    """プロジェクトルール管理CLIツール

    このツールは、プロジェクトごとに異なるルールとノートを効率的に管理・配置するためのCLIツールです。
    """
    pass


@cli.command()
@click.argument("template-dir", required=False)
@click.option("--force", "-f", is_flag=True, help="既存のファイルを上書きします")
def init(template_dir: Optional[str], force: bool):
    """テンプレートからプロジェクトルールとノートを配置します"""
    commands.init_command(template_dir, force)


@cli.command()
@click.argument("template-dir", required=False)
@click.option("--force", "-f", is_flag=True, help="既存のファイルを上書きします")
def deploy(template_dir: Optional[str], force: bool):
    """編集済みファイルを配置します"""
    commands.deploy_command(template_dir, force)


@cli.command()
@click.argument("template-dir", required=False)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["text", "json"]),
    default="text",
    help="出力形式を指定します",
)
def list(template_dir: Optional[str], format: str):
    """利用可能なルールの一覧を表示します"""
    commands.list_command(template_dir, format)


@cli.command()
@click.argument("template-dir", required=False)
def tree(template_dir: Optional[str]):
    """テンプレートディレクトリの階層構造を表示します"""
    commands.tree_command(template_dir)


@cli.command()
@click.argument("template-dir", required=False)
def validate(template_dir: Optional[str]):
    """テンプレートディレクトリの構造を検証します"""
    commands.validate_command(template_dir)


if __name__ == "__main__":
    cli()
    cli()
