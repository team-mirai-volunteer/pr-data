# PR Data Migration Scripts

このディレクトリには、PRデータの移行と管理のためのスクリプトが含まれています。

## migrate_data.py

このスクリプトは、team-mirai/random リポジトリの merged_prs_data.json から
team-mirai-volunteer/pr-data リポジトリのファイルごとのPRデータ形式に変換します。

### 使用方法

```bash
python migrate_data.py --input /path/to/merged_prs_data.json --output-dir /path/to/output/directory
```

### 引数

- `--input`: 入力JSONファイルのパス（必須）
- `--output-dir`: 出力ディレクトリのパス（デフォルト: カレントディレクトリ）

### 出力

スクリプトは以下のディレクトリ構造を作成します：

```
output-dir/
├── prs/
│   ├── 1.json     # PR #1のデータ
│   ├── 2.json     # PR #2のデータ
│   └── ...
├── indexes/
│   ├── by_label/
│   │   ├── education.json  # 教育ラベルのPR一覧
│   │   └── ...
│   └── by_section/
│       ├── section1.json   # セクション1のPR一覧
│       └── ...
```

## sample_data.json

テスト用のサンプルPRデータです。migrate_data.pyのテストに使用できます。

### テスト実行例

```bash
python migrate_data.py --input sample_data.json --output-dir ..
```
