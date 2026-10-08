# 画像パターンの見本（2026-10-08）

コースのサムネイル・成果物画像・記事のアイキャッチ・トップのメイン画像の「型」を比べる見本ボードを作るスクリプトです。

| スクリプト | 出力 | 中身 |
|---|---|---|
| b_thumb.py | thumb.html | コースのサムネイル T-A〜T-D |
| b_deliv.py | deliv.html | 成果物の画像 D-A〜D-D（D-B は全13コース分） |
| b_eye.py | eye.html | 記事のアイキャッチ E-A〜E-D |
| b_hero.py | hero.html | トップのメイン画像 H-A〜H-D |
| b_cover.py | cover.html | コースの表紙 C-1〜C-5（参考画像の表現を、カテゴリ色で作り直したもの） |

- `common.py` … カテゴリ色・線アイコン・コース一覧（成果物名と中身の見出し）。コースを足すときはここに1行足す
- `mock.py` … 成果物の模型5種類（doc／phone／sheet／chat／slide）

```bash
cd lp/scripts/patterns && python3 b_thumb.py && NODE_PATH=$(npm root -g) node shot.js file://$PWD/thumb.html thumb.png 1440
```
