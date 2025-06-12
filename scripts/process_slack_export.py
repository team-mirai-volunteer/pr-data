#!/usr/bin/env python3
"""
Slackエクスポートデータ処理スクリプト

Slackエクスポートデータを読み込み、チャンネル別・日付別の
Markdownレポートを生成します。
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import zipfile
import tempfile


def extract_slack_export(zip_path, extract_dir):
    """Slackエクスポートのzipファイルを展開する"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"Slackエクスポートを展開しました: {extract_dir}")
        return True
    except Exception as e:
        print(f"zipファイルの展開中にエラーが発生しました: {e}")
        return False


def load_channels_info(export_dir):
    """チャンネル情報を読み込む"""
    channels_file = Path(export_dir) / "channels.json"
    if not channels_file.exists():
        print("channels.jsonが見つかりません")
        return {}
    
    try:
        with open(channels_file, encoding="utf-8") as f:
            channels_data = json.load(f)
        
        channels_info = {}
        for channel in channels_data:
            channels_info[channel["id"]] = {
                "name": channel["name"],
                "purpose": channel.get("purpose", {}).get("value", ""),
                "topic": channel.get("topic", {}).get("value", "")
            }
        return channels_info
    except Exception as e:
        print(f"チャンネル情報の読み込み中にエラーが発生しました: {e}")
        return {}


def load_users_info(export_dir):
    """ユーザー情報を読み込む"""
    users_file = Path(export_dir) / "users.json"
    if not users_file.exists():
        print("users.jsonが見つかりません")
        return {}
    
    try:
        with open(users_file, encoding="utf-8") as f:
            users_data = json.load(f)
        
        users_info = {}
        for user in users_data:
            users_info[user["id"]] = {
                "name": user.get("name", "unknown"),
                "real_name": user.get("real_name", ""),
                "display_name": user.get("profile", {}).get("display_name", "")
            }
        return users_info
    except Exception as e:
        print(f"ユーザー情報の読み込み中にエラーが発生しました: {e}")
        return {}


def format_timestamp(ts):
    """タイムスタンプを日付文字列に変換する"""
    try:
        timestamp = float(ts)
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")
    except:
        return "unknown-date", "unknown-time"


def format_user_name(user_id, users_info):
    """ユーザーIDから表示名を取得する"""
    if user_id in users_info:
        user = users_info[user_id]
        display_name = user.get("display_name") or user.get("real_name") or user.get("name")
        return display_name
    return f"User-{user_id}"


def process_message_text(text, users_info):
    """メッセージテキストを処理する（ユーザーメンション等を変換）"""
    if not text:
        return ""
    
    import re
    def replace_user_mention(match):
        user_id = match.group(1)
        user_name = format_user_name(user_id, users_info)
        return f"@{user_name}"
    
    text = re.sub(r'<@([A-Z0-9]+)>', replace_user_mention, text)
    
    text = re.sub(r'<#[A-Z0-9]+\|([^>]+)>', r'#\1', text)
    
    text = re.sub(r'<(https?://[^|>]+)\|([^>]+)>', r'[\2](\1)', text)
    text = re.sub(r'<(https?://[^>]+)>', r'\1', text)
    
    return text


def load_channel_messages(export_dir, channel_name):
    """特定チャンネルのメッセージを読み込む"""
    channel_dir = Path(export_dir) / channel_name
    if not channel_dir.exists():
        return {}
    
    messages_by_date = defaultdict(list)
    
    for json_file in channel_dir.glob("*.json"):
        try:
            with open(json_file, encoding="utf-8") as f:
                messages = json.load(f)
            
            for message in messages:
                if message.get("type") == "message" and message.get("text"):
                    date, time = format_timestamp(message.get("ts", "0"))
                    messages_by_date[date].append({
                        "time": time,
                        "user": message.get("user", "unknown"),
                        "text": message.get("text", ""),
                        "ts": message.get("ts", "0")
                    })
        except Exception as e:
            print(f"メッセージファイル {json_file} の読み込み中にエラーが発生しました: {e}")
    
    for date in messages_by_date:
        messages_by_date[date].sort(key=lambda x: float(x["ts"]))
    
    return dict(messages_by_date)


def generate_channel_markdown(channel_name, channel_info, messages_by_date, users_info, output_dir):
    """チャンネルのMarkdownレポートを生成する"""
    channel_output_dir = Path(output_dir) / "slack_reports" / channel_name
    os.makedirs(channel_output_dir, exist_ok=True)
    
    overview_file = channel_output_dir / "README.md"
    with open(overview_file, "w", encoding="utf-8") as f:
        f.write(f"# #{channel_name}\n\n")
        if channel_info.get("purpose"):
            f.write(f"**目的**: {channel_info['purpose']}\n\n")
        if channel_info.get("topic"):
            f.write(f"**トピック**: {channel_info['topic']}\n\n")
        
        f.write("## 日別会話ログ\n\n")
        sorted_dates = sorted(messages_by_date.keys())
        for date in sorted_dates:
            f.write(f"- [{date}](./{date}.md)\n")
    
    for date, messages in messages_by_date.items():
        date_file = channel_output_dir / f"{date}.md"
        with open(date_file, "w", encoding="utf-8") as f:
            f.write(f"# #{channel_name} - {date}\n\n")
            f.write(f"**メッセージ数**: {len(messages)}\n\n")
            
            f.write("## 会話ログ\n\n")
            
            current_user = None
            for message in messages:
                user_name = format_user_name(message["user"], users_info)
                message_text = process_message_text(message["text"], users_info)
                
                if current_user != user_name:
                    if current_user is not None:
                        f.write("\n")
                    f.write(f"### {user_name} ({message['time']})\n\n")
                    current_user = user_name
                else:
                    f.write(f"**{message['time']}**\n\n")
                
                f.write(f"{message_text}\n\n")
    
    print(f"チャンネル #{channel_name} のレポートを生成しました: {channel_output_dir}")


def process_slack_export(export_path, output_dir):
    """Slackエクスポートデータを処理する"""
    if export_path.endswith('.zip'):
        with tempfile.TemporaryDirectory() as temp_dir:
            if not extract_slack_export(export_path, temp_dir):
                return False
            export_dir = temp_dir
            return process_extracted_export(export_dir, output_dir)
    else:
        return process_extracted_export(export_path, output_dir)


def process_extracted_export(export_dir, output_dir):
    """展開済みのSlackエクスポートデータを処理する"""
    export_path = Path(export_dir)
    
    channels_info = load_channels_info(export_path)
    users_info = load_users_info(export_path)
    
    print(f"チャンネル数: {len(channels_info)}")
    print(f"ユーザー数: {len(users_info)}")
    
    processed_channels = 0
    for channel_id, channel_info in channels_info.items():
        channel_name = channel_info["name"]
        
        channel_dir = export_path / channel_name
        if not channel_dir.exists():
            print(f"チャンネル #{channel_name} のデータが見つかりません")
            continue
        
        messages_by_date = load_channel_messages(export_path, channel_name)
        
        if not messages_by_date:
            print(f"チャンネル #{channel_name} にメッセージがありません")
            continue
        
        generate_channel_markdown(channel_name, channel_info, messages_by_date, users_info, output_dir)
        processed_channels += 1
    
    summary_file = Path(output_dir) / "slack_reports" / "README.md"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("# Slack活動レポート\n\n")
        f.write(f"**処理日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**処理チャンネル数**: {processed_channels}\n")
        f.write(f"**総ユーザー数**: {len(users_info)}\n\n")
        
        f.write("## チャンネル一覧\n\n")
        for channel_id, channel_info in channels_info.items():
            channel_name = channel_info["name"]
            channel_dir = Path(output_dir) / "slack_reports" / channel_name
            if channel_dir.exists():
                f.write(f"- [#{channel_name}](./{channel_name}/README.md)")
                if channel_info.get("purpose"):
                    f.write(f" - {channel_info['purpose']}")
                f.write("\n")
    
    print(f"\n処理完了: {processed_channels}チャンネルのレポートを生成しました")
    print(f"出力ディレクトリ: {Path(output_dir) / 'slack_reports'}")
    
    return True


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="Slackエクスポートデータを処理してMarkdownレポートを生成します")
    parser.add_argument("--input", required=True, help="Slackエクスポートファイル（.zip）またはディレクトリのパス")
    parser.add_argument("--output-dir", default=".", help="出力ディレクトリのパス")
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"入力ファイル/ディレクトリ {args.input} が見つかりません")
        return 1
    
    if process_slack_export(args.input, args.output_dir):
        print("Slackデータ処理が完了しました")
        return 0
    else:
        print("Slackデータ処理に失敗しました")
        return 1


if __name__ == "__main__":
    sys.exit(main())
