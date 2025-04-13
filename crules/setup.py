from setuptools import setup, find_packages

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
    author_email="john.smith@example.com",
    description="プロジェクトルール管理CLIツール",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/johnsmith/crules",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 