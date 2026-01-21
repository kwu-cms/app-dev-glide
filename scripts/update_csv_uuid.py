#!/usr/bin/env python3
"""
CSVファイルからメールと名前列を削除し、UUID列を追加するスクリプト

使用方法:
    python3 scripts/update_csv_uuid.py
"""

import csv
import uuid
from pathlib import Path

# 設定
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_PATH = PROJECT_ROOT / 'data.csv'


def main():
    """メイン処理"""
    print("=" * 60)
    print("CSVファイル更新ツール（UUID追加）")
    print("=" * 60)
    print()
    
    # CSVファイルが存在するか確認
    if not CSV_PATH.exists():
        print(f"❌ エラー: CSVファイルが見つかりません: {CSV_PATH}")
        return
    
    # CSVファイルを読み込む
    rows = []
    fieldnames = None
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    
    if not rows:
        print("❌ CSVファイルにデータが見つかりませんでした")
        return
    
    print(f"📋 現在の列: {', '.join(fieldnames)}")
    print()
    
    # メールと名前列を削除
    if 'メール' in fieldnames:
        fieldnames.remove('メール')
    if '名前' in fieldnames:
        fieldnames.remove('名前')
    
    # UUID列を追加（ID列の後）
    if 'UUID' not in fieldnames:
        if 'ID' in fieldnames:
            id_index = fieldnames.index('ID')
            fieldnames.insert(id_index + 1, 'UUID')
        else:
            fieldnames.insert(1, 'UUID')
    
    # 各行にUUIDを生成（既にUUIDがある場合は保持）
    for row in rows:
        if 'UUID' not in row or not row.get('UUID', '').strip():
            row['UUID'] = str(uuid.uuid4())
        # メールと名前列を削除
        if 'メール' in row:
            del row['メール']
        if '名前' in row:
            del row['名前']
    
    # CSVファイルを更新
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ CSVファイルを更新しました: {CSV_PATH}")
    print(f"📋 新しい列: {', '.join(fieldnames)}")
    print(f"📊 更新された行数: {len(rows)}行")
    print("=" * 60)


if __name__ == '__main__':
    main()
