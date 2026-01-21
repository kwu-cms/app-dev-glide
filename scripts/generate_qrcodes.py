#!/usr/bin/env python3
"""
CSVファイルのアプリのURLからQRコードを生成するスクリプト

使用方法:
    pip install qrcode[pil]
    python3 scripts/generate_qrcodes.py
"""

import csv
import os
from pathlib import Path

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    print("qrcodeがインストールされていません。'pip install qrcode[pil]' を実行してください。")

# 設定
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_PATH = PROJECT_ROOT / 'data.csv'
QRCODES_DIR = PROJECT_ROOT / 'images' / 'qrcodes'

# QRコードの設定
QR_CODE_SIZE = 10  # QRコードのボックスサイズ
QR_CODE_BORDER = 4  # ボーダーサイズ


def generate_qrcode(url: str, output_path: Path, app_name: str = '') -> bool:
    """URLからQRコードを生成して保存"""
    if not QRCODE_AVAILABLE:
        print("❌ qrcodeライブラリが利用できません")
        return False
    
    try:
        # QRコードを生成
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=QR_CODE_SIZE,
            border=QR_CODE_BORDER,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # 画像を作成
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 画像を保存
        img.save(output_path)
        
        print(f"✅ QRコード生成完了: {output_path.name} ({app_name})")
        return True
        
    except Exception as e:
        print(f"❌ QRコード生成に失敗 ({app_name}): {e}")
        return False


def main():
    """メイン処理"""
    print("=" * 60)
    print("QRコード生成ツール")
    print("=" * 60)
    print()
    
    # qrcodeライブラリが利用可能か確認
    if not QRCODE_AVAILABLE:
        print("エラー: qrcodeライブラリがインストールされていません。")
        print("インストール方法:")
        print("  pip install qrcode[pil]")
        return
    
    # CSVファイルが存在するか確認
    if not CSV_PATH.exists():
        print(f"❌ エラー: CSVファイルが見つかりません: {CSV_PATH}")
        return
    
    # QRコード保存先ディレクトリを作成
    QRCODES_DIR.mkdir(exist_ok=True, parents=True)
    
    print(f"CSVファイル: {CSV_PATH}")
    print(f"出力ディレクトリ: {QRCODES_DIR.absolute()}")
    print()
    
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
    
    # QRコード列が存在しない場合は追加
    if 'QRコード' not in fieldnames:
        # ID列の後にQRコード列を追加
        if 'ID' in fieldnames:
            id_index = fieldnames.index('ID')
            fieldnames.insert(id_index + 1, 'QRコード')
        else:
            fieldnames.insert(0, 'QRコード')  # 最初の列に追加
    
    print(f"📱 {len(rows)}件のアプリのQRコードを生成します...\n")
    
    # 各アプリのQRコードを生成
    success_count = 0
    error_count = 0
    
    for i, row in enumerate(rows, 1):
        url = row.get('アプリのURL', '').strip()
        if not url:
            # URLがない行はスキップ（QRコード列は空のまま）
            continue
        
        app_id = row.get('ID', '').strip() or str(i)
        
        print(f"[{i}/{len(rows)}] アプリ {app_id}")
        output_path = QRCODES_DIR / f"qrcode-{app_id}.png"
        qrcode_path = f"images/qrcodes/qrcode-{app_id}.png"
        
        success = generate_qrcode(url, output_path, f'アプリ {app_id}')
        
        if success:
            # QRコード列にパスを追記
            row['QRコード'] = qrcode_path
            success_count += 1
        else:
            # エラーでも空文字を設定（既存の値があれば保持）
            if 'QRコード' not in row or not row.get('QRコード', '').strip():
                row['QRコード'] = ''
            error_count += 1
    
    # CSVファイルを更新（QRコード列の値を書き込み）
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n✅ CSVファイルを更新しました: {CSV_PATH}")
    
    # 結果を表示
    print("\n" + "=" * 60)
    print("完了!")
    print(f"成功: {success_count}個")
    print(f"エラー: {error_count}個")
    print(f"出力ディレクトリ: {QRCODES_DIR.absolute()}")
    print("=" * 60)


if __name__ == '__main__':
    main()
