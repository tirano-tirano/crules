---
description: "High-level architecture and design principles"
globs: 
alwaysApply: false
---

# アーキテクチャ設計ガイドライン

## 大原則
- **このルールズの意義**: このプルジェクトルールズは、単にAIへの指示という意味だけでなく、開発を進める上で今までの開発内容を確認するためのドキュメントという意味合いをもっています。

## システム構成
Ruby製のCLIツールとして実装。
指定されたルールセットと同名のtemplatesフォルダ内のファイルを拡張子を変更して、.cursor/rulesにコピーする。
ルールセットが指定されなかった時は、templatesフォルダ内のdefaultフォルダ内のファイルを拡張子を変更して、.cursor/rulesにコピーする。



RubyGemsにはアップロードしないが、bundlerを利用しgemとしてインストールできるようにする。
また、homebrewの公式にはプルリクエストを送らないが、　tapして、インストールできるようにする。

プログラム本体のリポジトリは下記のとおりです。
https://github.com/tirano-tirano/crules

フォーミュラのリポジトリは、下記のとおりです。
https://github.com/tirano-tirano/homebrew-crules

## ルールの変更に関するガイド
- **ルール更新提案**: 開発を進めていく中で、ルールに反するような開発をおこなう可能性がでてきた場合は、および、ルールに新たな内容を付け加える必要がでてきた場合は、そのまま開発を進めないでください。この場合、ユーザーの合意を得てルールを変更してください。 