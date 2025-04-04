# Changelog

## [0.1.5] - 2024-03-30

### Added

- ルールセットの動的検出機能
  - `templates/templates/`配下のディレクトリから自動的にルールセットを検出
  - 各ルールセットの説明を README.md から読み取る機能を追加

### Changed

- ルールセットの追加方法を改善
  - コードの変更なしで新しいルールセットを追加可能に
  - README.md によるルールセットの説明管理

## [0.1.4] - 2024-03-30

### Changed

- テンプレートディレクトリ構造を改善
  - `templates/templates/`配下にルールセットを配置
  - ルールテンプレートを`templates/`直下に移動
- "フレームワーク"の概念を"ルールセット"に変更
  - `--framework`オプションを`--rule-set`に変更
  - `AVAILABLE_FRAMEWORKS`を`AVAILABLE_RULE_SETS`に変更
- ファイル名の命名規則を統一
  - アンダースコアをハイフンに変更（例：`01_ai_behavior.mdc` → `01-ai-behavior.mdc`）

## [0.1.3] - 2024-03-27

### Changed

- デフォルトのルールテンプレートに Frontmatter を追加
  - `description`: ルールの説明
  - `globs`: 適用対象のファイルパターン
  - `alwaysApply`: 常に適用するかどうか

## [0.1.2] - 2024-03-27

### Changed

- `add`コマンドの仕様を変更
  - フレームワークオプションを削除
  - 常にデフォルトテンプレートを使用するように変更
- テンプレートの使用方針を明確化
  - `init`: フレームワーク固有のテンプレートを使用
  - `add`: デフォルトテンプレートを使用

### Removed

- フレームワークディレクトリから`rule_template.md`を削除

## [0.1.1] - 2024-03-27

### Added

- Flutter プロジェクト用のテンプレートを追加
- フレームワーク固有のルールテンプレートをサポート

### Changed

- `init`コマンドにフレームワークオプションを追加
- テンプレートのディレクトリ構造を整理

## [0.1.0] - 2024-03-27

### Added

- 初期リリース
- 基本的な CLI コマンド
  - `init`: Cursor ルールの初期化
  - `add`: 新規ルールの追加
  - `version`: バージョン表示
- デフォルトのルールテンプレート

## [0.2.1] - 2024-03-30

### 追加

- Homebrew でのインストールに対応
