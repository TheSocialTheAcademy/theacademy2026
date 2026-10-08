# 画像パターンの見本（2026-10-08）

コースのサムネイル・成果物画像・記事のアイキャッチ・トップのメイン画像の「型」を比べる見本ボードを作るスクリプトです。

| スクリプト | 出力 | 中身 |
|---|---|---|
| b_thumb.py | thumb.html | コースのサムネイル T-A〜T-D |
| b_deliv.py | deliv.html | 成果物の画像 D-A〜D-D（D-B は全13コース分） |
| b_eye.py | eye.html | 記事のアイキャッチ E-A〜E-D |
| b_eye4.py | eye4.html | 記事のアイキャッチ N-1〜N-4（1枚で表す表紙：大見出し・要点・蛍光ペン）。N-1・N-2 は b_eye3.py と同じ写真を使う |
| b_eye3.py | eye3.html | 記事のアイキャッチ P-1〜P-3（CC0 の写真＋カード＋アイコン）。写真は未採用のため ph/ に置いて実行（出典は下） |
| b_eye2.py | eye2.html | 記事のアイキャッチ（考え直し）EA〜ED。コースのサムネイルと見分けられるか |
| b_hero.py | hero.html | トップのメイン画像 H-A〜H-D |
| b_cover2.py | cover2.html | C-4 の背景の上に入れるもの X-1〜X-4（アイコン／つくるもの／学習の目安／成果物の模型） |
| b_bg.py | bg.html | サムネイルの背景 B-1〜B-4（道のり／放射線／光の筋 濃紺・明るい地）。中身は X-2 |
| b_cover.py | cover.html | コースの表紙 C-1〜C-5（参考画像の表現を、カテゴリ色で作り直したもの） |

- `common.py` … カテゴリ色・線アイコン・コース一覧（成果物名と中身の見出し）。コースを足すときはここに1行足す
- `mock.py` … 成果物の模型5種類（doc／phone／sheet／chat／slide）

```bash
cd lp/scripts/patterns && python3 b_thumb.py && NODE_PATH=$(npm root -g) node shot.js file://$PWD/thumb.html thumb.png 1440
```

### b_eye3.py で使った写真（CC0・Openverse 経由。採用時に assets/photos/CREDITS.md へ）

| 記事 | ファイル | 出典 |
|---|---|---|
| 週2時間 | weekly.jpg | rawpixel「Free open notebook study table」 |
| ChatGPT | chatgpt.jpg | rawpixel「Free laptop coffee shop photo」 |
| SNS | sns.jpg | rawpixel「Man holding a smartphone」 |
| 英語 | english.jpg | rawpixel「Free business meeting cafe coffee」 |
| ポートフォリオ | portfolio.jpg | rawpixel「Leather chair laptop table」 |
| 進行表 | event.jpg | rawpixel「Free sticky notes office board」 |
