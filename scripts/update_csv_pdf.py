#!/usr/bin/env python3
"""
CSVファイルの発表資料列を「pdf」に変更し、IDに対応するPDFファイルのパスを追記するスクリプト

使用方法:
    python3 scripts/update_csv_pdf.py
"""

import csv
from pathlib import Path

# 設定
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_PATH = PROJECT_ROOT / 'data.csv'

# PDFファイルを探すディレクトリ（複数の場所をチェック）
PDF_SEARCH_DIRS = [
    PROJECT_ROOT,
    PROJECT_ROOT / 'pdf',
    PROJECT_ROOT / 'pdfs',
    PROJECT_ROOT / 'files',
    PROJECT_ROOT / 'documents'
]


def find_pdf_file(app_id: str) -> str:
    """IDに対応するPDFファイルを探す"""
    # 複数のパターンで検索
    patterns = [
        f"{app_id}.pdf",
        f"app-{app_id}.pdf",
        f"{app_id}_*.pdf",
        f"*{app_id}*.pdf"
    ]
    
    for search_dir in PDF_SEARCH_DIRS:
        if not search_dir.exists():
            continue
        
        # まず正確なファイル名で検索
        pdf_path = search_dir / f"{app_id}.pdf"
        if pdf_path.exists():
            # プロジェクトルートからの相対パスを返す
            return str(pdf_path.relative_to(PROJECT_ROOT))
        
        # パターンマッチで検索
        for pattern in patterns[1:]:  # 最初のパターンは既にチェック済み
            for pdf_file in search_dir.glob(pattern):
                return str(pdf_file.relative_to(PROJECT_ROOT))
    
    return ''


def main():
    """メイン処理"""
    print("=" * 60)
    print("CSVファイル更新ツール（PDF列更新）")
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
    
    # 長い列名を「pdf」に変更
    old_column_name = '発表資料（PowerPointやWord）などのファイルがある場合は提出してください。口頭での発表の場合はなくても構いません。'
    
    if old_column_name in fieldnames:
        # 列名を「pdf」に変更
        index = fieldnames.index(old_column_name)
        fieldnames[index] = 'pdf'
        print(f"✅ 列名を変更: '{old_column_name}' → 'pdf'")
    elif 'pdf' not in fieldnames:
        # pdf列が存在しない場合は追加（最後に追加）
        fieldnames.append('pdf')
        print("✅ 'pdf'列を追加")
    
    # 各行のPDFファイルを確認
    print(f"\n📄 PDFファイルを検索中...")
    print(f"検索ディレクトリ: {', '.join([str(d) for d in PDF_SEARCH_DIRS if d.exists()])}")
    print()
    
    pdf_found_count = 0
    
    for row in rows:
        app_id = row.get('ID', '').strip()
        if not app_id:
            row['pdf'] = ''
            continue
        
        # PDFファイルを探す
        pdf_path = find_pdf_file(app_id)
        
        if pdf_path:
            row['pdf'] = pdf_path
            pdf_found_count += 1
            print(f"  ✅ ID {app_id}: {pdf_path}")
        else:
            row['pdf'] = ''
            print(f"  ⚪ ID {app_id}: PDFファイルが見つかりません")
        
        # 古い列名のデータがあれば削除
        if old_column_name in row:
            del row[old_column_name]
    
    # CSVファイルを更新
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n✅ CSVファイルを更新しました: {CSV_PATH}")
    print(f"📋 新しい列: {', '.join(fieldnames)}")
    print(f"📊 更新された行数: {len(rows)}行")
    print(f"📄 PDFファイルが見つかった数: {pdf_found_count}個")
    print("=" * 60)


if __name__ == '__main__':
    main()
