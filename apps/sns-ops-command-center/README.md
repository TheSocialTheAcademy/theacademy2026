# SNS Ops Command Center

SNS運用（投稿戦略・投稿管理・カレンダー・分析・競合分析・キャンペーン・コメント管理・チーム/アカウント管理）を1画面で扱うブラウザアプリ。ビルド不要の素の HTML/CSS/JS で、データはブラウザの localStorage に保存し、任意で Google Sheets（Apps Script）経由でチーム同期する。

## 構成

| パス | 役割 |
|---|---|
| `sns-strategy-app/` | **編集対象のソース**（`index.html` / `styles.css` / `app.js` / `data.js` / `social-icons.js`） |
| `sns-strategy-app/Code.gs` | チーム同期用 Apps Script（手順は `SETUP_GUIDE.md`） |
| `build.js` | ソースを1ファイルに結合し `dist/index.html` 等を生成 |
| `dist/index.html` | 生成物（静的ホスティングの公開ディレクトリ。`.openai/hosting.json` 参照） |

## 開発フロー

1. `sns-strategy-app/` を編集する（`dist/` は直接編集しない）
2. `node build.js` で `dist/index.html` と単一HTML（`sns-ops-command-center-single*.html`、git 管理外）を再生成
3. `dist/index.html` をブラウザで開いて確認（`--sync` で `~/Downloads` にもコピー）

ソースと `dist/index.html` は必ず同じコミットで更新する。
