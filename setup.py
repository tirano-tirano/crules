from setuptools import setup, find_packages
import os

# READMEファイルのパスを取得
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="crules",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.7",
        "pyyaml>=6.0.1",
        "markdown>=3.4.3",
    ],
    entry_points={
        "console_scripts": [
            "crules=crules.cli:cli",
        ],
    },
    author="John Smith",
    author_email="tirano.tirano@gmail.com",
    description="プロジェクトルール管理CLIツール",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tirano-tirano/crules",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
