# 引き継ぎ資料（本編フレームワーク層・カタログ刷新・WF化）— 2026-08-28（続）

対象: The Academy コーススライド生成システム。土台は既存 `HANDOFF.md`／`HANDOFF_wireframes_2026-08-28.md`／
`CLAUDE.md` を参照。本書は **2026-08-28 の続き作業**（ディスパッチャ接続→content.txt→カタログ刷新→
本編フレームワーク層→WF化）に絞る。作業リポジトリ: `~/Downloads/academy_handoff_20260828/slide-generator-main`。

環境は従来どおり：`.venv`（Python3.12）＋`python-pptx==1.0.2`/`PyMuPDF`/`Pillow`/`requests`、
アイコン用に **`cairosvg` 追加導入済み**（soco-st イラストで使用）。LibreOffice で検査/PDF化。

---

## 0. このセッションでやったこと（全体像）

1. **wf50型 → pages ディスパッチャ接続**（`pages.py` に `W01…W50`/型名/wf関数名で引ける RENDERERS 拡張）
2. **content.txt → コース1本 生成**（`coursegen.py`：`【型キー】`＋`key: value` を parse → `pages.render`）
3. **グラフをブランド版へ刷新**（`slides.py` の bar/line/pie を「グラフ集」デザイン＝青みグレー＋アクセント・スリムに）
4. **2カタログを刷新（同URLへ再デプロイ）**
   - パターンライブラリ（グラフ28＋図解26＋自作拡張15）… `41ece272`
   - コース用テンプレ集（28型＋本編フレームワーク12）… `a8b42788`
5. **本編フレームワーク層**（`frameworks.py`＋`layouts.py`）：思考フローを1ブロックで章分展開、
   fan-out で長尺化、グラフ/表/図解連携、アイコン/イラスト（併用）、**レイアウト・ローテーション＋wf型接続**
6. **WF化チャート**（`wfcharts.py`）：グラフ集の各グラフを WF流儀（リード＋主ビジュアル＋示唆パネル＋出典）で構成
7. テストコース生成（AIプロンプト初級・全4章）

---

## 1. 新規モジュール（役割）

| ファイル | 役割 | 主API |
|---|---|---|
| `coursegen.py` | content.txt からコース1本を生成する薄いドライバ | `build_course(content, out)` / `parse(text)` |
| `frameworks.py` | 本編フレームワーク（思考フロー×スライド構成）を1ブロックで複数ページ展開 | `render(prs, key, fields)` / `FRAMEWORKS` / `teach_concept(...)` |
| `layouts.py` | 誌面的（非対称）本文レイアウト。ローテーションで「同じ型を続けない」 | `ROTATION` / `rotate(i)` / `lay_claim_evidence` 他 |
| `wfcharts.py` | グラフを WF流儀の誌面に構成（テキスト位置まで型化） | `frame(...)` / `wf_donut` `wf_hbar` `wf_vbar` `wf_line` `wf_stacked` `wf_waterfall` |

---

## 2. content.txt でコースを組む（coursegen）

```
【コース表紙】
title: …／subtitle: …／meta: …
【チャプター扉】
num: 01／course_name: …／goals: A｜B｜C／icon: ph:…
【W01】               ← 本編ワイヤー50型（W01..W50/型名/wf関数名）も同じ経路
title: …
【本編:概念習得】       ← フレームワーク（1ブロック→章扉＋本編を一括展開）
topic: …／details: …／why: … など
【修了】
message: …／cta: …／illust: …（soco-st検索語）
```
- 書式：`【型キー】`＝ページ、`key: value`＝フィールド、`｜`＝list、`=`＝pair、行頭`|`＝続き行、`#`＝コメント。
- `coursegen.build_course` が `frameworks.is_framework(key)` を先に見て、フレームワークなら複数ページ展開、
  それ以外は `pages.render` に渡す。末尾で検査ゲート（ERROR0でPASS）。
- 実装例：`projects/course_from_content/`（短）・`projects/course_ai_prompt/`（AIプロンプト全4章）。

---

## 3. 本編フレームワーク層（frameworks.py / layouts.py）

### 3.1 考え方
本編＝「思考の流れ」。フローを型化＝フレームワーク（＝スライドの見せ方）。カタログ `course-frameworks.html`
（`07e277f8`／`a8b42788` の C+節に統合済み）に **12フロー**（TF1課題解決〜TF12分類）を整理。
既存ページ型＋図解＋グラフ＋表を「並べるだけ」で本編が組める。

### 3.2 実装済み：TF2 概念習得型（What→Why→How）
`【本編:概念習得】` 1ブロック → 章扉＋本編を一括展開。**フィールドのあるページだけ描く**。

- **長尺化（fan-out）**：`details=（要素=箇条書き｜…）` `examples=` `applications=` は **項目数だけ1枚ずつ**展開。
  間に小扉も入る。要素・事例を増やすほど厚くなり **1ブロック15枚規模**まで伸びる（実コース＝Chapter10×15枚想定）。
  `=` の右は `・`／`／` で箇条書き（例 `指示=動詞で始める・対象を名詞で`）。
- **ライブラリ紐付け**：`data=（ラベル=値）`→グラフ、`table=（h1,h2｜a,b）`→表（`,`でセル・`｜`で行）、
  図解（概念フロー/構造ピラミッド/よくある失敗=Before-After）は常時。
- **wf型接続**：`wf=（W10=タイトル｜…）` で本編ワイヤー50型を差し込み（本文はwf既定を作り手が差し替え）。
- **アイコン/イラスト（併用・方針）**：アイコンは**強調文の横**（`why_icons`＝動機づけカード見出し左に Phosphor 1色）。
  イラストは `illust`＝**修了などの主役**に soco-st カラー（**章扉には使わない**）。
- **レイアウト・ローテーション**：詳細スライドは `layouts.rotate(i)` で構図を回す（大きな主張＋根拠／罫線なし段組み／
  上結論・下詳細）。連続で同じ型を出さない＝機械的配置（3等分/全中央/全部囲う）を回避。

### 3.3 フィールド早見（teach_concept 主なもの）
`topic, num, course_name, icon, goals, illust,`
`concept_lead, parts, concept_conclusion,`
`details, details_door, why, why_lead, why_icons, why_conclusion,`
`elements(構造ピラミッド), data, data_chart, table, wf,`
`examples, examples_door, misconceptions, corrections, applications,`
`summary_points, summary_takeaway, rotate_layouts(既定True)`

### 3.4 未実装フロー
TF1/3/4/5/6/7〜12 は未実装。**同じ作り**（ページ関数を順に呼ぶ展開関数を1つ書く）で追加できる。
TF1 課題解決は「ロジックツリー／なぜなぜ分析図」の専用ビルダーが要る（ツリーは diagrams、なぜなぜは派生で作れる）。

---

## 4. WF化チャート（wfcharts.py）

「グラフ集」の各グラフを WF流儀の誌面に構成する。**周辺テキストの位置まで型で用意**：
```
番号｜型名 → 大タイトル → リード1行
┌ 主ビジュアル（左・枠付き＋グラフ見出し）┐  ┌ 示唆パネル（右）┐
└─────────────────────┘  └────────┘
出典・注釈（小・下）
```
- `frame(prs, kicker, title, lead, insight=[(見出し,本文)], footnote=, chart_title=)` が外枠を敷き、主ビジュアル域を返す。
- チャート本体は `wireframes.py`（`vbars`/`hbars`/`linechart`/`data_table`）＋`slides.py`（`pie_chart`/`bar_chart`）を再利用。
- 実装済み型：`wf_donut`(C1) `wf_hbar`(B1) `wf_vbar`(V1) `wf_line`(T1) `wf_stacked`(S2) `wf_waterfall`(W1)。
- ギャラリー：`projects/wf_chart_gallery/`（6族・検査PASS）。
- **次工程（b）**：フレームワークの `data`/`table` スロットを wfcharts に差し替え＋ローテーションへ織り込む（未着手）。
- 既知の小調整：横棒(B1)の左ラベル折返し／W1のグラフ見出しが先頭バーと軽く重なる。

---

## 5. ビルダー更新（既存ファイル）

### slides.py（グラフ＝「グラフ集」デザイン＝青みハーモナイズ＋スリム）
- **チャートトークン**：`CHART_INK #4A5A8C`／`CHART_GREY #8C97BC`／`CHART_GREY_L #DCE1F0`（Primary Blueに調和する“青みグレー”）
  ＋`CHART_ACCENT`=PRIMARY／`CHART_GRID`/`CHART_AXIS`。`CHART_PALETTE`＝青＋グレー濃→淡。
- `_style_plot_area()`＝縦グリッド無し・枠なし・目盛なし・横罫線最薄。
- `bar_chart`：`highlight`（点強調）/`stacked`/`reverse_order`（降順を上から）/`gap_width=150`（細め）/値ラベル外側。
- `line_chart`：`line_width=1.75`・角マーカー・単系列は濃青みグレー。
- `pie_chart`：既定ドーナツ＋`hole_size=78`（細リング・中央数字用）／`highlight`／凡例なし既定／`_set_doughnut_hole`。
- **リブランド後の値の履歴**：濃色は当初 `#3C3C3C`(純グレー)→`#363E5C`→**`#4A5A8C`**（青寄り・軽く）。細リング化・凡例整列も実施。

### pages.py
- **W01..W50 ディスパッチャ**：`RENDERERS` を wf50型（idx/型名/wf関数名）へ拡張（`_make_wf_page` ラッパ）。
- `data`：円を**ドーナツ（hole52）＋右に凡例**（数字を右揃え）に。素の中央円をやめ文字とのバランス改善。
- `motivation`：`icons=` で各カード見出し横に Phosphor（強調文の横）。
- `chapter_cover`：`illust=`（soco-st）対応＋従来の淡いphアイコン。`complete`：`illust=` 対応。
- `quiz`/`checklist`：正解・チェックの緑(SUCCESS)→**アクセント青**に統一。

### diagrams.py
- `diagram_table`：淡ヘッダ＋ゼブラ → **濃い青みスレート(CHART_INK)ヘッダ＋白文字＋ゼブラ無し**（集D1準拠）。
- 中立グレー `#9A9AA6` → `NEUTRAL`（=CHART_GREY 青みグレー）に統一。connector 線幅も細線化。

---

## 6. カタログ（2つとも同URLへ再デプロイ済み）

| カタログ | URL | 内容 |
|---|---|---|
| スライド・パターンライブラリ | https://claude.ai/code/artifact/41ece272-e0c3-4f01-a6c7-f8a17910193e | グラフ28型（『グラフ集』準拠）＋表・図解26型（『表・図解デザイン集』準拠）＋自作拡張15。**青みグレー＋アクセント・シャープ&スリム**で統一 |
| コース用スライド型テンプレ集 | https://claude.ai/code/artifact/a8b42788-686e-4a37-be64-15c995df95b0 | 28型（コース全体/導入/本編/定着締め）＋**本編フレームワーク12（C+節）**。全体を青みハーモナイズ、緑/オレンジ装飾を青へ |
| 本編フレームワーク集（単独・任意） | https://claude.ai/code/artifact/07e277f8-6393-4594-be19-6ec50a991da1 | 12フローを思考フロー×スライド構成で。上のC+節と同内容 |

- ローカル実体：`docs/catalog/pattern-library.html` / `course-slide-templates.html` / `course-frameworks.html`。
- 再デプロイは Artifact ツールに **`url`＋`force:true`** を渡す（先に WebFetch で現行版を確認済み）。ソースはDOCTYPE/head無しでArtifact形式。

---

## 7. projects（このセッションの成果物/検証）

| project | 内容 |
|---|---|
| `course_via_dispatcher` | wf50型を pages.render 経由で通し生成（接続実証） |
| `course_from_content` | content.txt→coursegen の最小例 |
| `chart_rebrand_check` | グラフ集ブランド版の再現（C1/B1/V1/V2/B3/T1） |
| `course_ai_prompt` | テストコース「AIプロンプト初級」全4章（25枚・PASS） |
| `framework_concept_demo` | TF2概念習得の長尺・紐付け・アイコン・ローテーション・wf接続の総合デモ |
| `layout_prototype` | 機械的→誌面的レイアウトのBefore/After比較 |
| `wf_style_prototype` | グラフ/表のWF化 Before/After |
| `wf_chart_gallery` | グラフ集6族のWF化ギャラリー |

生成コマンド（例）：
```bash
cd projects/framework_concept_demo
PATH="/Applications/LibreOffice.app/Contents/MacOS:$PATH" ../../.venv/bin/python3 generate.py
```

---

## 8. デザイン方針（守ること）

- **配色**：Primary Blue #0141D4 を主役に、無強調は**青みグレー3段**（#4A5A8C/#8C97BC/#DCE1F0）。緑/オレンジは
  装飾に使わない（正解ハイライト等も青）。ブランド説明のスウォッチ・状態ドット凡例のみ緑を残置。
- **スリム/シャープ**：細リング・細棒・細線・小さめ角丸・行数に応じた高さ。間延びさせない。
- **脱・機械配置**：3等分/全中央/全部囲う/同サイズ/同余白を避け、非対称・強弱・余白の注釈を使う（`layouts.py`）。
- **WF流儀**：グラフ/表は「リード＋主ビジュアル＋示唆パネル＋出典」で構成（`wfcharts.py`）。
- **アイコン/イラスト**：アイコン＝強調文の横（ph:1色）／イラスト＝修了などの主役（soco-st）。章扉にイラストは置かない。
- スピード重視・個人情報以外は許可不要・呼び名は「チャプター」・配布はPDF（字形固定）。

---

## 9. 次のタスク（優先順・未着手）

1. **(b) WF化をフレームワークへ本組み込み**：teach_concept の `data`/`table` を wfcharts へ、layouts.ROTATION にWF流儀ビジュアルを織り込む。
2. **他フローの実装**：TF3手順／TF6データ示唆（既存型だけで組める）→ TF1課題解決（なぜなぜ図が要る）。
3. **WF化チャートの残り型**：散布図(X)・面(A)・アイコンチャート(I)・円ゲージ(C2)・数字カード＋縦棒(V3)。
4. 小調整：横棒ラベル折返し／W1見出し重なり。
5. （任意）レイアウトパターン集（「使用してよい例」12種の単独カタログ）。
6. レイアウト選択を「順番」から「内容に応じた最適」判定へ発展。
