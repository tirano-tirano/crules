---
description: "Functional and system specifications for the app"
globs: 
alwaysApply: false
---

# 仕様書ガイドライン

## 大原則
- **このルールズの意義**: このプルジェクトルールズは、単にAIへの指示という意味だけでなく、開発を進める上で今までの開発内容を確認するためのドキュメントという意味合いをもっています。

## 画面仕様

### 認証系画面
- **ログイン画面**
  - ユーザー名/メールアドレス入力フィールド
  - パスワード入力フィールド（マスク表示）
  - ログインボタン
  - パスワードリセットリンク
  - 新規登録リンク
  - ソーシャルログインボタン（Google, Apple）
  - エラーメッセージ表示エリア（赤字）

- **新規登録画面**
  - メールアドレス入力フィールド
  - パスワード入力フィールド（マスク表示）
  - パスワード確認入力フィールド
  - 利用規約同意チェックボックス
  - 登録ボタン
  - エラーメッセージ表示エリア

### メイン機能画面
- **ホーム画面**
  - ユーザー情報表示エリア
  - 〇〇情報のリスト表示
  - プルダウンによる再読込機能
  - 各項目タップ時の詳細画面遷移
  - 新規作成ボタン

- **詳細画面**
  - 〇〇情報の詳細表示
  - 編集ボタン
  - 削除ボタン
  - 関連情報の表示

## データ仕様

### データモデル
- **ユーザー情報**
  ```dart
  class User {
    final String id;
    final String email;
    final String name;
    final String? profileImageUrl;
    final DateTime createdAt;
    final DateTime updatedAt;
    final Map<String, dynamic> preferences;
  }
  ```

- **〇〇エンティティ**
  ```dart
  class Item {
    final String id;
    final String title;
    final String description;
    final DateTime createdAt;
    final String createdBy;
    final List<String> tags;
  }
  ```

### API仕様
- **認証系API**
  - `POST /api/v1/auth/login`
    - リクエスト: `{ email: string, password: string }`
    - レスポンス: `{ token: string, user: User }`
  
  - `POST /api/v1/auth/register`
    - リクエスト: `{ email: string, password: string, name: string }`
    - レスポンス: `{ token: string, user: User }`

- **データ操作API**
  - `GET /api/v1/items`
    - クエリパラメータ: `page`, `limit`, `sort`
    - レスポンス: `{ items: Item[], total: number }`
  
  - `POST /api/v1/items`
    - リクエスト: `{ title: string, description: string, tags: string[] }`
    - レスポンス: `Item`

## 振る舞いとビジネスロジック

### 認証フロー
1. ユーザーがログイン画面で認証情報を入力
2. 入力値のバリデーション
3. APIリクエスト送信
4. レスポンスに基づく処理
   - 成功: トークン保存とホーム画面遷移
   - 失敗: エラーメッセージ表示

### データ同期フロー
1. アプリ起動時にローカルDBの状態確認
2. サーバーとの最終同期時刻比較
3. 必要に応じてバックグラウンドでデータ更新
4. UIの更新通知

### エラーハンドリング
- **ネットワークエラー**
  - オフライン時のローカルデータ表示
  - 再接続時の自動同期
  - ユーザーへの通知

- **バリデーションエラー**
  - フィールドごとのエラーメッセージ表示
  - フォーム全体のエラー状態管理

- **サーバーエラー**
  - リトライロジックの実装
  - ユーザーフレンドリーなエラーメッセージ
  - エラーログの記録

## ルールの変更に関するガイド
- **ルール更新提案**: 開発を進めていく中で、ルールに反するような開発をおこなう可能性がでてきた場合は、および、ルールに新たな内容を付け加える必要がでてきた場合は、そのまま開発を進めないでください。この場合、ユーザーの合意を得てルールを変更してください。 