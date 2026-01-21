# Glideアプリ制作物展示サイト

7名の学生が作成したGlideアプリを紹介する静的ウェブサイトです。

## 機能

- CSVファイルからアプリ情報を自動読み込み（PapaParse使用）
- 各アプリのスクリーンショットを自動取得（Python + Playwright使用）
- スマートフォンモックアップでカルーセル表示（Slick.js使用）
- レスポンシブデザイン対応
- タッチスワイプ対応

## セットアップ

### 1. PythonとPlaywrightのインストール（スクリーンショット取得用）

```bash
pip install -r requirements.txt
playwright install chromium
```

または

```bash
pip install playwright
playwright install chromium
```

### 2. スクリーンショットを取得

```bash
python3 scripts/screenshot.py
```

### 3. QRコードを生成

```bash
python3 scripts/generate_qrcodes.py
```

## ファイル構造

```
/
├── index.html              # メインHTMLファイル
├── styles/
│   └── main.css           # スタイルシート
├── js/
│   └── app.js             # JavaScript機能
├── images/
│   ├── screenshots/       # スクリーンショット画像
│   └── qrcodes/          # QRコード画像
├── scripts/
│   ├── screenshot.py      # スクリーンショット取得スクリプト（Python + Playwright）
│   └── generate_qrcodes.py  # QRコード生成スクリプト（Python）
├── data.csv                # CSVデータ
└── requirements.txt        # Python依存関係
```

## 使い方

1. スクリーンショットを取得する場合: `python3 scripts/screenshot.py` を実行
2. QRコードを生成する場合: `python3 scripts/generate_qrcodes.py` を実行
3. `index.html` をブラウザで開く
4. CSVファイルから自動的にアプリデータが読み込まれます
5. アプリカードをクリックするとモーダルが開き、スマホモックアップでカルーセル表示されます

## 技術スタック

- HTML5/CSS3/JavaScript
- PapaParse（CSVパース）
- jQuery + Slick.js（カルーセル）
- Python + Playwright（スクリーンショット取得）
- Python + qrcode（QRコード生成）

## ブラウザ対応

- Chrome（推奨）
- Firefox
- Safari
- Edge

## ライセンス

MIT
