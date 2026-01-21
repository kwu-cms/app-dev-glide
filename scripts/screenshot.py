#!/usr/bin/env python3
"""
Glideアプリのスクリーンショットを取得するスクリプト

使用方法:
    pip install playwright
    playwright install chromium
    python scripts/screenshot.py
"""

import os
import csv
import time
from pathlib import Path
from typing import List, Dict

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwrightがインストールされていません。'pip install playwright' を実行してください。")

# 設定
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_PATH = PROJECT_ROOT / 'data.csv'
SCREENSHOTS_DIR = PROJECT_ROOT / 'images' / 'screenshots'

# iPhone 16 Pro相当のビューポート
SCREENSHOT_WIDTH = 402
SCREENSHOT_HEIGHT = 874
DEVICE_SCALE_FACTOR = 3  # iPhone 16 Proのデバイススケールファクター

# ページ読み込み後の待機時間（秒）
WAIT_TIME = 15

# ページ読み込みのタイムアウト（ミリ秒）
TIMEOUT = 60000


def load_apps() -> List[Dict]:
    """CSVファイルからアプリデータを読み込む（列名で取得）"""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSVファイルが見つかりません: {CSV_PATH}")
    
    apps = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader):
            # アプリのURLがある行のみ処理
            url = row.get('アプリのURL', '').strip()
            if url:
                app_id = row.get('ID', '').strip() or str(index + 1)
                apps.append({
                    'id': app_id,
                    'uuid': row.get('UUID', '').strip(),
                    'url': url,
                    'description': row.get('アプリの説明', '').strip(),
                    'pdf': row.get('pdf', '').strip()
                })
    
    return apps


def take_screenshot(app: Dict) -> bool:
    """アプリのスクリーンショットを取得"""
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwrightが利用できません")
        return False
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                viewport={
                    'width': SCREENSHOT_WIDTH,
                    'height': SCREENSHOT_HEIGHT,
                    'device_scale_factor': DEVICE_SCALE_FACTOR
                }
            )
            
            url = app['url']
            app_id = app['id']
            
            print(f"📸 アプリ {app_id} のスクリーンショットを取得中: {url}")
            
            # ページに移動（networkidleを待たずに、loadイベントを待つ）
            try:
                page.goto(url, wait_until='load', timeout=TIMEOUT)
            except Exception as e:
                # loadがタイムアウトしても、domcontentloadedを試す
                print(f"  ⚠️ loadタイムアウト、domcontentloadedを試行中...")
                try:
                    page.goto(url, wait_until='domcontentloaded', timeout=TIMEOUT)
                except Exception:
                    # それでも失敗した場合は、とにかくページを開いて待機
                    print(f"  ⚠️ タイムアウトしましたが、ページを開いて待機します...")
                    page.goto(url, wait_until='commit', timeout=TIMEOUT)
            
            # Glideのページは読み込みに時間がかかるため、15秒待機
            print(f"⏳ ページの読み込み完了を待機中（{WAIT_TIME}秒）...")
            time.sleep(WAIT_TIME)
            
            # スクリーンショットを保存
            screenshot_path = SCREENSHOTS_DIR / f"app-{app_id}.png"
            page.screenshot(path=str(screenshot_path), full_page=False)
            
            browser.close()
            
            print(f"✅ 保存完了: {screenshot_path}")
            return True
            
    except Exception as e:
        print(f"❌ アプリ {app['id']} のスクリーンショット取得に失敗: {e}")
        return False


def main():
    """メイン処理"""
    print("=" * 60)
    print("Glideアプリ スクリーンショット生成ツール")
    print("=" * 60)
    print()
    
    # Playwrightが利用可能か確認
    if not PLAYWRIGHT_AVAILABLE:
        print("エラー: Playwrightがインストールされていません。")
        print("インストール方法:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return
    
    # ブラウザがインストールされているか確認
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
    except Exception as e:
        print(f"Playwrightのブラウザがインストールされていないようです。")
        print(f"自動インストールを試みます...")
        try:
            import subprocess
            result = subprocess.run(
                ['python3', '-m', 'playwright', 'install', 'chromium'],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print(f"✓ Playwrightのブラウザをインストールしました")
            else:
                print(f"✗ インストールに失敗しました: {result.stderr}")
                print(f"手動で実行してください: playwright install chromium")
                return
        except Exception as install_error:
            print(f"✗ 自動インストールに失敗しました: {install_error}")
            print(f"手動で実行してください: playwright install chromium")
            return
    
    # アプリデータを読み込む
    try:
        apps = load_apps()
        print(f"📱 {len(apps)}件のアプリデータを読み込みました\n")
    except Exception as e:
        print(f"❌ エラー: {e}")
        return
    
    # スクリーンショット保存先ディレクトリを作成
    SCREENSHOTS_DIR.mkdir(exist_ok=True, parents=True)
    
    print(f"出力ディレクトリ: {SCREENSHOTS_DIR.absolute()}")
    print(f"スクリーンショットサイズ: {SCREENSHOT_WIDTH}x{SCREENSHOT_HEIGHT}px")
    print(f"待機時間: {WAIT_TIME}秒\n")
    
    # 各アプリのスクリーンショットを取得
    success_count = 0
    error_count = 0
    
    for i, app in enumerate(apps, 1):
        print(f"\n[{i}/{len(apps)}]")
        success = take_screenshot(app)
        
        if success:
            success_count += 1
        else:
            error_count += 1
        
        # リクエスト間隔を空ける（最後のアプリ以外）
        if i < len(apps):
            print("⏸️  2秒待機中...")
            time.sleep(2)
    
    # 結果を表示
    print("\n" + "=" * 60)
    print("完了!")
    print(f"成功: {success_count}個")
    print(f"エラー: {error_count}個")
    print(f"出力ディレクトリ: {SCREENSHOTS_DIR.absolute()}")
    print("=" * 60)


if __name__ == '__main__':
    main()
