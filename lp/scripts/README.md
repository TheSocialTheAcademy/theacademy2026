# lp/scripts

サイト（`lp/`）の各ページを作るスクリプトです。

## 使い方

```bash
bash lp/scripts/build.sh
```

- **トップページ `lp/lp-design.html` は手で編集します。** ヘッダー・フッター・共通の CSS はトップから取り出して、ほかの全ページに使います。そのため、トップを直したら `build.sh` を実行して全ページを作り直してください。
- 必要なのは Python 3 だけです（追加のライブラリは不要）。どのフォルダから実行しても動きます。

## ファイルと作るページ

| スクリプト | 作るページ |
|---|---|
| `gen_courses.py` | コースを探す（courses.html）。ほかのスクリプトが共通部品を取り出すときにも使う |
| `gen_howto.py` | 学び方・受講成果（how-to-learn.html） |
| `gen_portfolio.py` | ポートフォリオ（portfolio.html） |
| `gen_blog.py` | 学びのヒント（blog.html） |
| `gen_beginners.py` | はじめての方へ（beginners.html） |
| `gen_extra.py` ＋ `k2block.py`・`k2.css` | 無料相談・資料請求（contact.html）、よくある質問（faq.html）、記事の見本（article.html）、コース詳細13ページ（course-*.html） |
| `gen_resources.py` | お役立ち資料（resources.html） |
| `gen_evidence.py` | 数字の根拠（evidence.html）。受講生の声のアイコンは `lp/assets/avatars/` |
| `gen_legal.py` | 特定商取引法に基づく表記・プライバシーポリシー・利用規約（`LEGAL_SITE=1` のときだけ書き出す） |
| `gen_replace_list.py` | 差し替え箇所の一覧（lp/docs/replace-list.html・.csv） |
| `gen_legal_review.py` | 法務ページの文面レビュー用ページ（一時フォルダに legal-draft.html を書き出す） |
| `slim_zips.py` | `downloads/` の素材 ZIP を、中身を変えずに軽くする（`pip install pyoxipng` が必要） |

## コースのサムネイル（カテゴリの単色グラデーション＋形6種類＋つくるもの）

`lp/assets/thumbs/<slug>.webp`（1280×800）は、コース一覧のデータ（gen_courses.py の C）から作っています。コースを足したら、gen_courses.py の DELIV（成果物の名前）と gen_thumbs.py の ICON に1行ずつ足して、次を実行します（Node と Playwright が必要）。

```bash
python3 lp/scripts/gen_thumbs.py && NODE_PATH=$(npm root -g) node lp/scripts/gen_thumbs.js && python3 lp/scripts/thumbs_webp.py
```

## ダイジェスト動画の表紙

コース詳細のダイジェスト動画（今のサイトと同じ Vimeo）は、押すまで読み込まない作りです。表紙はサムネイルと同じ背景から文字を抜いたもの（`lp/assets/digest/<slug>.webp`）。

```bash
TA_THUMBS_BARE=1 TA_THUMBS_DIR=lp/assets/digest python3 lp/scripts/gen_thumbs.py && NODE_PATH=$(npm root -g) node lp/scripts/gen_thumbs.js && python3 lp/scripts/thumbs_webp.py
```

動画の URL と長さは `course_data.json` の `digest`。イベントデザイン・インスタグラムの動画は、Vimeo の設定で theacademyjapan.org 以外では再生できない（本番の Wix では再生できる）。
