#!/bin/bash

# スクリプトのディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# gemファイルのパス
GEM_FILE="$SCRIPT_DIR/crules-0.1.1.gem"

# gemファイルが存在するか確認
if [ ! -f "$GEM_FILE" ]; then
    echo "Error: crules-0.1.1.gem not found"
    echo "Please build the gem first using: gem build crules.gemspec"
    exit 1
fi

# gemをインストール
echo "Installing crules..."
gem install --user-install "$GEM_FILE"

# インストール成功メッセージ
echo "Installation complete!"
echo "You can now use the 'crules' command" 