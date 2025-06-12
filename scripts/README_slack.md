# Slackエクスポートデータ処理スクリプト

## 概要

`process_slack_export.py` は、Slackのエクスポートデータを処理して、チャンネル別・日付別のMarkdownレポートを生成するスクリプトです。

## 機能

- Slackエクスポートzipファイルまたは展開済みディレクトリの処理
- チャンネル別・日付別の会話ログ整理
- ユーザーメンション、チャンネルメンション、URLの適切な変換
- AI処理に適したMarkdown形式での出力
- 日本語での活動紹介作成に最適化

## 使用方法

### 基本的な使用方法

```bash
# zipファイルから処理
python scripts/process_slack_export.py --input /path/to/slack_export.zip --output-dir .

# 展開済みディレクトリから処理
python scripts/process_slack_export.py --input /path/to/slack_export_dir --output-dir .
```

### 出力構造

```
slack_reports/
├── README.md                    # 全体サマリー
├── general/                     # #generalチャンネル
│   ├── README.md               # チャンネル概要
│   ├── 2024-01-01.md          # 日別会話ログ
│   ├── 2024-01-02.md
│   └── ...
├── random/                      # #randomチャンネル
│   ├── README.md
│   ├── 2024-01-01.md
│   └── ...
└── ...
```

## 出力形式

### チャンネル概要ファイル (README.md)
- チャンネル名、目的、トピック
- 日別会話ログへのリンク一覧

### 日別会話ログファイル (YYYY-MM-DD.md)
- 日付とメッセージ数
- 時系列順の会話ログ
- ユーザー名と投稿時刻
- メンションやURLの適切な変換

## 処理される要素

- **ユーザーメンション**: `<@U1234567>` → `@username`
- **チャンネルメンション**: `<#C1234567|channel-name>` → `#channel-name`
- **URL**: `<http://example.com|example.com>` → `[example.com](http://example.com)`
- **タイムスタンプ**: Unix timestamp → `YYYY-MM-DD HH:MM:SS`

## 必要なファイル

Slackエクスポートには以下のファイルが含まれている必要があります：

- `channels.json` - チャンネル情報
- `users.json` - ユーザー情報
- `{channel_name}/` - 各チャンネルのメッセージファイル
  - `YYYY-MM-DD.json` - 日別メッセージデータ

## エラーハンドリング

- 不正なJSONファイルはスキップ
- 存在しないチャンネルディレクトリは警告表示
- ユーザー情報が見つからない場合はUser-IDで表示

## AI処理への最適化

生成されるMarkdownは以下の特徴を持ち、AI処理に適しています：

- 構造化された階層（チャンネル → 日付 → 会話）
- 一貫したフォーマット
- メタデータの明確な分離
- 日本語での自然な表現

## 使用例

```bash
# Slackエクスポートを処理
python scripts/process_slack_export.py --input ~/Downloads/slack_export.zip

# 結果確認
ls slack_reports/
cat slack_reports/README.md
```

## 注意事項

- 大きなエクスポートファイルの処理には時間がかかる場合があります
- プライベートチャンネルやDMは、エクスポートに含まれている場合のみ処理されます
- 添付ファイルやリアクションは現在サポートされていません
