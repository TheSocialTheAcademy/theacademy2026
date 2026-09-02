# 引き継ぎ資料 — The Academy コーススライド生成システム

最終更新: 2026-08-21 ／ 引き継ぎ先: Codex

このドキュメントだけ読めば作業を継続できるようにまとめてある。まず `## 1〜3` を読み、
コードを触る前に `## 8 落とし穴` に必ず目を通すこと。

---

## 1. これは何か（ゴール）

`slide-generator`（python-pptx ベースのスライド自動生成ツール）を土台に、
**The Academy**（The Social の子ブランド・オンライン学習）の**コーススライドを型に沿って自動生成**する仕組みを作っている。

大きな構想は制作フロー全体（企画→教材→**スライド**→レビュー→音声→動画→公開）。
**今のフォーカスはスライド**。中でも「型（テンプレート）を先に用意し、内容を流し込む」方式。

コース領域は **IT・ビジネス・語学** がメイン。

---

## 1.5 標準スライドフロー（コース構成の正）★ユーザー確定 2026-08-21

コース1本は必ずこの順で構成する（**ユーザー確定・最終版 2026-08-21**）。
**目次は置かない**。**学習目標は各チャプター扉に「学べること：」として内蔵**する。
**理解チェック/チェックリスト・次回予告/さらに学ぶ・全体のまとめ は全チャプター終了後にまとめ、全体のまとめは最後**に置く。

```
コース表紙
  └ ┌ チャプター扉（CHAPTER NN ＋「学べること：・○○ ・○○」）      ┐
    │  └ 教える内容 ×複数                                       │  ← チャプター数だけ
    │     （文字・画像・グラフ・図解を混在させ、飽きないレイアウト）  │     繰り返す
    │  └ （必要に応じて）事例                                    │     （枚数は内容量次第）
    │  └ チャプターまとめ（その章の要点）                        │
    └ └──────────────────────────────────────────────────────┘
  └ 理解チェック（クイズ）または チェックリスト   … 全チャプター終了後
  └ 次回予告・さらに学ぶ
  └ 全体のまとめ（コース通しの要点）             … 最後
  └ 裏表紙
```

- **目次ページは作らない**（コースは表紙→最初のチャプター扉へ）。
- **学習目標＝チャプター扉に内蔵**：扉に `学べること：・○○ ・○○ ・○○` を載せる。コース単位の独立目標ページは置かない。
- **教える内容**は本編パターン（概念/手順/具体例/比較/データ/構造/画像/コード/例文/会話…）から選び、**1チャプター内で文字・画像・グラフ・図解を混在**させて単調にしない（＝飽きないレイアウト）。必ず図・グラフ・図解のいずれかを伴わせ、文字だけの連続にしない。
- **事例**は必要な場合にチャプター内へ追加（走る事例を1つ決めて反復すると理解が繋がる）。
- **チャプターまとめ**は各チャプター末に置く。
- **理解チェックとチェックリスト**はどちらか（または両方）を全チャプター後に。**次回予告・さらに学ぶ**を続け、**全体のまとめを最後**に置く。
- **規模**: コース／チャプター数により総枚数は変わる（数十〜**~140枚**）。
- 実装リファレンス: `projects/academy_prompt_course/generate.py`（この最終フローを実装した実例）。

### 実コース観察（ユーザー既存作『マーケティング戦略基礎コース』全144枚）★流儀の正

ユーザーが実際に作るコースの構成。上のフローはこの実態に合わせて運用する。

- **学習目標は「チャプター扉」に内蔵**する（`Chapter NN で学べること：・○○ ・○○`）。コース単位の独立目標ページは置かない流儀。
- **走る事例を全編で反復**する（例のコースは「クッキー屋さん」を PEST/3C/SWOT/4P/ペルソナ/カスタマージャーニー…全フレームで一貫使用）。これが理解を繋ぐ背骨。**新規コースでも事例を1つ決めて通す**。
- **フレームワーク展開のミクロパターン**（各トピックでこの順を反復）:
  `「○○について詳しく知る」(小扉) → 「○○とは？」(定義) → 各要素を1枚ずつ → 重要ポイント → 事例に当てはめる`
- **章の大きさは内容量で大きく変動**（実例は 3〜69枚/章）。1章＝1トピックの深掘り。
- **章末に「おさらい」**（章による・任意）。**コース末は「最後に＝動機づけ」**で締める（例：「楽しむ！」「基礎中の基礎」「無限大！」）。
- **理解チェック/クイズ/チェックリストは、実コースでは未使用**（講義型）。→ **任意要素**として扱う（入れる場合は §1.5 の通り全章終了後にまとめる）。The Academy 用に学習効果を上げたい場合は追加提案してよい。
- **規模の目安**: フル講座で **~130〜144枚**（末尾に補足・予備の空白ページを持つこともある）。
- 事例出典: `~/Desktop/デスクトップ - Mac/コース資料/マーケティング戦略基礎コース資料資料/マーケティング戦略基礎コース.pptx`。

---

## 2. いまの成果物（3つ＋サンプル）

| 成果物 | 形態 | 場所 / URL |
|---|---|---|
| コース用スライド型テンプレ集 v0.4（全28型） | 設計カタログ(HTML) | `docs/catalog/course-slide-templates.html` ／ https://claude.ai/code/artifact/a8b42788-686e-4a37-be64-15c995df95b0 |
| スライド・パターンライブラリ（グラフ10＋図解25＋追加5＝40型） | 設計カタログ(HTML) | `docs/catalog/pattern-library.html` ／ https://claude.ai/code/artifact/41ece272-e0c3-4f01-a6c7-f8a17910193e |
| サンプルコース LESSON03「プロンプト設計の基本」全9枚 | 実装(.pptx/.pdf) | `projects/academy_prompt_lesson/` |

- **型テンプレ集** = ページ単位の役割（コース表紙/学習目標/概念/…）の一覧。4フェーズ(A/B/C/D)・28型。
- **パターンライブラリ** = コンテンツゾーンに差し込む可視化（円グラフ/フロー/ピラミッド/…）40型。
- サンプルは両者を組み合わせて実際に生成し、検査ゲート **PASS** 済み。

---

## 3. 主要ファイルの地図

```
slide-generator-main/
├─ brand.py                     ★ ブランド定義（色/フォント/雛形名）。The Academy 化済み
├─ slides.py                    生成ヘルパー本体（textbox/card/callout/*_chart/validate 等）※編集不要
├─ templates/
│  ├─ スライド雛形.pptx          元の雛形（オレンジ・K.S.Rogersロゴ）※変更禁止・保険用
│  └─ スライド雛形_academy.pptx  ★ Academy版（ブルー化・CONFIDENTIAL除去・白ACADEMYロゴ）現行雛形
├─ projects/
│  └─ academy_prompt_lesson/    ★ サンプル。generate.py が実装の参考
│     ├─ generate.py            ← 型の実装例（表紙/目標/概念/例/データ/ピラミッド/演習/まとめ）
│     └─ output.pptx / .pdf     生成物
├─ docs/catalog/                ★ 設計カタログHTML（型テンプレ集・パターンライブラリ）
├─ .venv/                       ★ Python3.12 の venv（システム3.9では動かない。§8）
└─ HANDOFF.md                   このファイル
```

---

## 4. 環境（重要 — セットアップ済み）

- **Python**: `.venv` は **Python 3.12**（`/opt/homebrew/bin/python3.12` で作成）。
  システムPythonは3.9で **slides.py が動かない**（§8-1）。必ず `.venv/bin/python3` を使う。
- **依存**: `python-pptx==1.0.2` / `PyMuPDF 1.28.2` / `Pillow` / `requests`（`.venv` に導入済み）。
  さらに **`add_icon`（Iconifyアイコン）を使う場合は `cairosvg` が必要**（導入済み・system側は `brew install cairo`）。アイコン未使用なら不要。
- **アイコン**: リソース＝**Iconify**（15万種／https://icon-sets.iconify.design/ ）。**ハウスセット＝Phosphor（`ph:`）に確定**（`brand.py` の `ICON_SET="ph"`）。全スライドで `ph:` に統一し、色は1アイコン1色（白地＝PRIMARY）。`add_icon(slide, "ph:xxx", x, y, size, color="#0141D4")`。初回取得後 `~/.cache/ksr-slides/icons/` にキャッシュ。
- **soco-st 連携（公式イラスト・Phosphorと併用／都度判断）**: `soco.py` に実装済み。
  - `soco_search("キーワード")` → 候補アイコンIDのリスト（公式APIが無いため検索結果ページからID抽出）。
  - `soco_icon_fit(slide, "ID", x, y, box_w, box_h, variant="paint")` → soco-st の **カラー版（塗り＝paint）をそのまま配置**（フルカラーのイラスト。再着色しない・背景パネルは付けない）。`~/.cache/ksr-slides/soco/` にキャッシュ。線画が要る場合のみ `variant="line"`。（`color=` を渡した時だけ SVG から着色＝`cairosvg` はその時のみ必須）。
  - 使いどころ：**チャプター内スライド**と**「最後に」スライド**でイラストとして活用（実例＝`page_illustration()`／`page_complete()`）。**背景色は付けず、白地にそのまま置く**。
  - 役割分担：Phosphor（`ph:`）＝ブランド青の小アイコン（UI的）／soco-st（paint）＝フルカラーのイラスト（人物・シーン）。
  - 利用規約：soco-st は商用可・著作権は先方保持。素材の再配布・販売は不可。https://soco-st.com/guide を順守。
- **レイアウトパターン「soco-st イラスト＋解説」**: `projects/academy_prompt_course/generate.py` の `page_illustration(section_label, title, lead_text, icon_id, heading, bullets, side)` が実装例（片側にブランド色イラスト、反対側に見出し＋箇条書き）。他コースへ流用可。
- **画像素材**: `assets/academy_logo_white.png`（白ロゴ/ダーク背景用）・`assets/academy_logo_blue.png`（青ロゴ/白背景用）＝The Academy 公式ロゴ。チャプター扉デザインで使用。
- **チャプター扉デザイン（マーケコース準拠・確定）**: 全面ブルー地に、左＝ロゴ／コース名（`COURSE_NAME`）＋"COURSE"／`Chapter NN` ピル／「学べること：」＋箇条書き、右＝**コースに合った“薄い”トピックアイコン**（`add_icon(..., color="#3A66DE")` の淡い青、`COURSE_ICON` で指定。AI系=`mdi:robot-outline` 等）。実装は `projects/academy_prompt_course/generate.py` の `chapter()`。**コースごとに `COURSE_NAME`／`COURSE_ICON` を差し替える**。
- **LibreOffice**: `/Applications/LibreOffice.app/Contents/MacOS/soffice`（導入済み）。
  検査ゲートのレンダ照合(`validate_render`)・PDF/PNGプレビューに必須。実行時 PATH に追加する。

### 生成コマンド（サンプルを回す）
```bash
cd projects/academy_prompt_lesson
PATH="/Applications/LibreOffice.app/Contents/MacOS:$PATH" \
  ../../.venv/bin/python3 generate.py
# 末尾の validate() が検査ゲート。ERROR があると exit 1。PASS になるまで直す。
```

### 目視プレビュー（PNG化して確認）
`Read` ツールでの PDF 直読は poppler 未導入で不可。**PyMuPDF で PNG 化**して見る:
```bash
cd projects/academy_prompt_lesson
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir . output.pptx
../../.venv/bin/python3 -c "import pymupdf,os;d=pymupdf.open('output.pdf');[p.get_pixmap(dpi=110).save(f'prev_{i+1:02d}.png') for i,p in enumerate(d)]"
```

---

## 5. ブランド仕様（The Academy / 出典: `~/Desktop/【2026年版】The Socialガイドライン.pptx`）

### 色（`brand.py` に反映済み・役割名は据え置き値のみ差し替え）
| 定数 | HEX | 役割 |
|---|---|---|
| PRIMARY | #0141D4 | 主色・見出し・章扉・CTA。面積で優位に |
| PRIMARY_LIGHT | #EEF2FD | 淡い青の面 |
| SECONDARY | #005BA3（濃紺は#012270も可） | 構造・区切り |
| HIGHLIGHT | #3E78FE | 学習アクセント・強調 |
| SUCCESS | #27AE60 | 正解・完了 |
| DANGER | #F76B38 | 注意・CTA（**赤は不使用**。「悪い例」はTEXT_MUTEDで表す） |
| TEXT / TEXT_MUTED | #222222 / #676688 | 本文 / 補助 |
| BORDER / SURFACE | #E6E6EA / #F4F6FC | 罫線 / 面 |

**禁止**: 赤の新規追加、オレンジ/イエロー面に白文字、アクセントを1画面3色以上、装飾目的の色。

### フォント（`brand.py`）
- `JP_FONT="Hiragino Kaku Gothic ProN"`（**ヒラギノ優先**・macOS標準。見出しW6=bold・本文W3）。
  配布時に非搭載環境では **Noto Sans JP**（W700=W6/W400=W3）へフォールバック。
- `FONT="Arial"`（latin・検査ゲートの幅計測用の安定値。正式は Graphik / 代替 Inter）。
- 行間 1.6〜1.8。W6は1ページ2〜3箇所まで。

### トーン
寄り添い・後押し。脅し/プレッシャー/専門用語/根拠なき約束は使わない。
スローガンは英語のまま完全形 "Creating an Opportunity To Take Action"。

### ロゴ・その他
- 公式 The Academy ロゴを使用（**自作・改変しない**）。ガイドライン内の白版=`image7` を使用済み。
- **CONFIDENTIAL はコースで非表示**（提案書専用だった）。
- 章扉（チャプター扉）の全面色 = **Primary Blue #0141D4**（決定）。

---

## 6. 雛形リブランドで実施したこと（再現手順のメモ）

`templates/スライド雛形_academy.pptx` は元雛形から以下を機械変換して作成:
1. 全XMLでオレンジ hex（`EE613D` `EC6739` `EA633A` `FF644E`）→ `0141D4` に置換。
2. `<p:sp>` に含まれる「CONFIDENTIAL」テキスト図形を全削除（layout1/layout3/slide1）。
3. body用 `slideLayout3.xml` に残った**空の青ピル** roundRect（`name="Google Shape;34;p5"`）を削除。
4. ロゴ画像 `ppt/media/image1.png`（元は K.S.Rogers）を、ガイドラインの**白 THE ACADEMY ロゴ**を
   400×100透過キャンバスにアスペクト維持で左寄せ合成したものに差し替え（枠は4:1で歪みなし）。
- **サイズ・レイアウト・ゾーン・見出し構造は一切変更していない（色と書体・ロゴのみ）**。
- 元の `スライド雛形.pptx` は保険として温存。雛形を作り直す場合は上記1〜4を再実行すること。

---

## 7. スライド生成の仕組み（slides.py の使い方）

`generate.py` の骨格（`projects/academy_prompt_lesson/generate.py` が実例）:
```python
prs = load_template()                              # スライド雛形_academy.pptx を読む
update_cover(prs.slides[0], lines=[...])           # 表紙（既存slide0を書換。add_slideで作らない）
reset_to_cover_only(prs)                            # サンプルの扉/本文/裏紙を削除
# 本文: s = prs.slides.add_slide(prs.slide_layouts[L_BODY]); configure_body(s, section_label=, title=)
#   → その後 y=3.0〜12.8 / x=1.07〜24.33 の範囲だけに自由描画
# 章扉: add_slide(L_CHAPTER) + configure_chapter(chapter_num=, title=, subtitle=)
add_back_cover(prs); finalize_page_numbers(prs, skip_first=True)
prs.save(OUT); validate(prs, OUT, render=True)      # 検査ゲート（PASSまで直す）
```
使えるヘルパー: `textbox / shape_box / card / callout / connector / picture /
bar_chart / line_chart / pie_chart / configure_body / configure_chapter / update_cover / validate`。
座標は cm。色は `RGBColor`（`add_icon` の color のみ hex 文字列）。複数行はリストで渡す（`\n`は改行にならない）。

固定ルール（触らない）: 見出し領域 y=0〜3.0 は描かない（テンプレが描く）。見出し帯・ページ番号
サークル・表紙/裏表紙はレイアウト継承で自動保持。AIが差し替えるのはテキストと y≥3.0 のコンテンツのみ。

---

## 8. 落とし穴（着手前に必読）

1. **slides.py は Python 3.10+ 必須**。`str | None` 構文を使うためシステム3.9では import 時に TypeError。
   必ず `.venv/bin/python3`（3.12）を使う。
2. **PDF直読不可**: `Read` ツールは poppler 未導入で pptx/pdf を画像化できない。§4のPyMuPDF手順でPNG化。
3. **検査ゲート**: `validate()` は ERROR で exit 1。よく出るやつと対処:
   - `WRAP`（1行想定の枠が2行に）→ 例: カードchipに "01" は折返す。**1文字**"1"にする。
   - `OVERFLOW_V`（縦あふれ）→ カード高さを上げる or タイトル/本文を短く。
   - 設計基準 `need_h ≤ 0.85 × box_h`（PowerPointの行送り差の安全マージン）。
4. **フォント配布**: ヒラギノ非搭載PCで開くと崩れる。**顧客配布はPDF**が安全（サンプルもPDF併置）。
5. **雛形を作り直すと** CONFIDENTIAL除去・ロゴ差し替えが消える。§6を再実行すること。
6. **soffice を PATH に入れ忘れる**と `validate(render=True)` のレンダ照合が動かない。

---

## 9. 次のタスク（優先順）

### タスクA: 図解ビルダーの実装（本命の次工程）★2026-08-26 完了
パターンライブラリ40型のうち**新規ビルダーが要る図解**を、再利用関数として実装した。
- 置き場所: **`diagrams.py`（リポジトリ直下・新設済み）**。共通ヘルパー `_tint`（白へ寄せた淡色）
  `_on`（塗り上の可読文字色）`_lab_sub`（(label,sub) 正規化）を内蔵。
- API規約: `def diagram_xxx(slide, x, y, w, h, *, データ, accent=PRIMARY): ...`。
  内部は `shape_box`/`textbox`/`connector` 経由で描く（→ `validate()` に自動登録される）。色はブランド定数のみ。
- 角丸ルール: 表・帯・入れ子・直列は直角(`RECTANGLE`)、単独の浮くノード（サイクル節点・順位/ステップ
  のバッジ）のみ角丸(`ROUNDED_RECTANGLE`)。
- **実装済み優先11型**: `diagram_flow_h`(横フロー) / `diagram_flow_v`(縦フロー) /
  `diagram_pyramid` / `diagram_before_after` / `diagram_matrix`(2×2) / `diagram_steps`(階段) /
  `diagram_cycle` / `diagram_timeline` / `diagram_ranking`(値バー付) / `diagram_formula`(＋/＝) /
  `diagram_group`。各データ契約は `diagrams.py` のdocstring参照。
- **動作確認＆カタログ**: `projects/diagram_gallery/generate.py`（全11型を1枚ずつ描画）。
  検査ゲート **PASS**（`PATH="…/soffice:$PATH" ../../.venv/bin/python3 generate.py`）。出力＝同フォルダの `output.pptx/.pdf`。
- 手書き実装だった `academy_prompt_course/generate.py` の `flow_row`/`page_stepwise` は将来
  `diagram_flow_h`/`diagram_steps` に置換して重複解消できる（未着手・任意）。

### タスクB: 本編Cの新型に必要なビルダー ★2026-08-26 完了
`diagrams.py` に本編C専用の5ビルダーを追加（合計16ビルダー）。動作確認は `projects/diagram_gallery/`（全型・検査ゲートPASS）。
- **`diagram_table`**（C4比較/C14語彙/C15書式を兼用）: 罫線グリッド・ヘッダ帯・ゼブラ・列幅比。
- **`diagram_code`**（C10）: 暗色コードブロック＋行番号＋行ハイライト＋右側注釈（`MONO`=Courier New）。
- **`diagram_conversation`**（C12）: 左右吹き出し＋話者バッジ（角丸・side指定）。
- **`diagram_image_explain`**（C8）: 画像/プレースホルダ＋見出し＋箇条書きの2カラム。
- **`diagram_ui_steps`**（C9）: スクショ/プレースホルダ＋番号ピン＋手順リスト。
- 文法(C13)は `diagram_formula`（タスクA）を流用。

### タスクC: 28型のページ関数化 ★2026-08-26 完了
型テンプレ集 v0.4 の全28型を **`pages.py`（リポジトリ直下）** に関数化。1型＝1関数で、
`slides.py`＋`diagrams.py` を使いブランド準拠・ゾーン内に収まる。
- 関数名: `course_cover/curriculum/chapter_cover/lesson_cover/objectives/motivation/prerequisites/
  concept/steps_page/example/comparison/data/structure/pitfalls/image_explain/ui_guide/code_explain/
  parallel_text/dialog/grammar/vocabulary/format_template/exercise/quiz/checklist/summary/next_up/complete`。
- `RENDERERS` 辞書で **idx（A1..D6）と和名（コース表紙/コード解説…）の双方**から関数を引ける。
  `pages.render(prs, key, fields)` が薄いディスパッチャ。フィールドは `_list`（`｜`区切り）・`_pairs`（`=`）で正規化。
- **slides-gen スキルの判定表を更新済み**（SKILL.md §3.2 に idx→和名→関数→主フィールドの28行表）。
  `【型名】` があるページは pages.py 関数で、無いページは従来の自由設計。**型テンプレ使用でも §5 検査ゲート＋design-guide 監査は免除されない**。
- 動作確認＆実装例: `projects/pages_demo/generate.py`（標準フロー §1.5 で主要型を通しで生成・検査ゲートPASS・17枚）。
- カタログHTML `docs/catalog/course-slide-templates.html`（28型）と `pattern-library.html`（図解）は「実装済み（●青）」表示に更新済み・公開Artifactへ再デプロイ済み。

### 未決定（ユーザー確認待ち）
- 型テンプレ集で「28型に足す候補」: 引用・専門家の声／Q&A・FAQ／事例インタビュー／料金・プラン／
  リスニング(音声スクリプト)。IT: アーキテクチャ図/エラー対処。ビジネス: KPIダッシュボード。
- 実装の着手順（まとめて or 2〜3型ずつ）。

---

## 10. ユーザーの方針（守ること）

- **スピード重視**。個人情報・機密情報以外は許可を求めず進めてよい。
- 固定仕様（サイズ/ゾーン/見出しレイアウト）は変えない。**色と書体のみ**ブランド適用。
- 呼び名は「チャプター」（モジュールではない）。
- 書体はヒラギノ優先、章扉はPrimaryBlueでOK。
```

---

## 11. 参考取り込みワークフロー（refs/）★2026-08-26 着手

Slideland（https://www.slideland.tech/ ）のような**参考ギャラリーを自分の生成パイプラインに接続**する仕組み。
パターン整備を「3層」で捉える：**①参考ギャラリー（refs/）→ ②実装ライブラリ（diagrams.py/pages.py）→ ③テーマ層（brand.py テーマ辞書化・今後）**。

- **`refs/README.md`** に運用ルール（4ステップ・タグ語彙・蒸留チェックリスト・著作権の線引き）。
- 流れ：`inbox/` にスクショ → `refs.json` に1件追記（種類/業種/配色/テイスト/要素タグ）→ `.venv/bin/python3 refs/build_board.py` で **タグ絞り込みボード `refs/board.html`** 再生成 → 良い参考は `theme-preset.template.md` を複製して `presets/<名>.md` に**配色・書体・余白・モチーフだけ蒸留**。
- ⚠️ **`board.html`・`inbox/` は社内閲覧専用＝公開/Artifact化しない**（他社資料の再配布防止）。取り込むのは一般原則のみ、ロゴ/写真/丸ごと再現はNG。出典URLは refs.json に必ず残す。
- **次の接続先**：presets/ が溜まったら ③ `brand.py` をテーマ辞書化（`THEMES["saas-trust-blue"]=…`）して、既存の diagrams/pages 全型を再配色可能にする。さらに全ビルダー×テーマを一括レンダした**タグ付き実装ギャラリー**を作ると、Slideland の閲覧体験を自作出力で再現できる（②側にも同じタグ語彙を付与）。
- ⚠️ 他社サイト（Slideland等）の**自動スクレイプ／特定スライドの再現はしない**（ToS・著作権）。参考は手で少量集め、**原則だけ**拝借する。

---

## 12. 方針（2026-08-26 更新）

- **汎用レイアウト・アーカイタイプ集の拡張は取りやめ**。`layouts.py` は削除済み（`projects/marketing_course` は自ファイル内にローカル定義して自己完結・依存なし）。
- 今後は **実コースをデザイナー品質に引き上げる**ことに集中。叩き台＝`projects/marketing_course`（21枚）。
- 参考の取り込みは **Slideland等の更新スライドを手で観察→スクショを `refs/inbox/` に蓄積→原則を抽出**し、**スライド・パターンライブラリ**（`docs/catalog/pattern-library.html`）と**コース用スライド型テンプレ**（`docs/catalog/course-slide-templates.html`）を自作オリジナルとして磨く。観察の観点＝`refs/README.md`（レイアウト構成・配色バランス・アイコン/写真の置き方・文字の位置と大きさ・余白）。
- 引き上げの要点（AI生成っぽさを消す）：①同一カードの横並び反復を避ける ②中央寄せ一辺倒をやめ非対称グリッド ③主色ドミナンス＋余白を広く、アクセントは1画面1〜2箇所 ④アイコン(Iconify `ph:`)・図・グラフ・写真で質感 ⑤モチーフを1つ反復 ⑥装飾のためだけの線を引かない。
- リデザイン実例（ビフォー/アフター）：導入ヒーロー・3C を高craft化して検証済み（scratchpad）。次は他の型も同トーンで整え、方向確定後に全体展開。
