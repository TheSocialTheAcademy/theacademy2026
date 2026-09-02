# 引き継ぎ資料（本編スライド型・ワイヤーフレーム対応）— 2026-08-28

対象: The Academy コーススライド生成システム。土台の全体像は既存 `HANDOFF.md` と
`CLAUDE.md` を参照。本書は **2026-08-27〜28 に行った「ワイヤーフレーム準拠の本編
スライド型50 実装」と「既存図解の標準化」** に絞った引き継ぎ。

作業リポジトリ: `~/Downloads/slide-generator-main 3`（`.venv` は Python3.12）。

---

## 1. 何をしたか（ゴール）

ユーザー作成のワイヤーフレーム `~/Desktop/wireframe_master_050.pptx`（業務スライド
**全50型**）を、**構図まで完全一致**で The Academy ブランドに実装した。
色は **Primary Blue #0141D4** のみ、書体は **ヒラギノ角ゴ ProN＋Graphik**。狙いは
"AIっぽさ" の除去（デザイナー品質への引き上げ）。

### 仕上げ規定（AIっぽさ除去・厳守）★ユーザー確定
1. アイコン・装飾イラスト・写真は使わない。要点は文字と図形だけ
2. 土台は白／黒／グレー。色はメイン1色（accent＝Primary Blue）のみ
3. グラデ禁止・単色塗り。**角丸・影禁止**（直角フラット。データ点の円のみ可）
4. ベタ塗り見出し帯は使わない。区切りは細いヘアライン
5. **accent は各スライドの焦点1箇所**に限定。ほかの強調は黒の太字
6. 緑(SUCCESS)/オレンジ(DANGER)も既定では使わない

---

## 2. 成果物と場所

| 成果物 | 場所 |
|---|---|
| **本編スライド型 50 実装** | `wireframes.py`（リポジトリ直下・新設）`wf_01 … wf_50` |
| 動作確認ギャラリー（全50型） | `projects/wireframe_gallery/generate.py` → `output.pptx/.pdf`（検査PASS・52枚） |
| 図解ビルダー20型（標準化済み） | `diagrams.py` ＋ `projects/diagram_gallery/` |
| パターンライブラリ（94型・50型追加済み） | `docs/catalog/pattern-library.html` ／ Artifact https://claude.ai/code/artifact/41ece272-e0c3-4f01-a6c7-f8a17910193e |
| 型テンプレ集（フォント表記更新済み） | `docs/catalog/course-slide-templates.html` ／ Artifact https://claude.ai/code/artifact/a8b42788-686e-4a37-be64-15c995df95b0 |
| 納品 pptx/pdf | `TheAcademy_本編スライド型_全50型.pptx/.pdf`（別途送付） |

---

## 3. wireframes.py の構造（デザイン標準レイヤー）

本文ゾーン（`y≥3.0`）だけに描く。固定chrome（見出し帯・ページ番号・青枠）はテンプレ
継承のまま不変。各 `wf_*` は既定データ入りで、gallery が引数なしで全50型を描ける。

### 共通レイアウトの背骨
```
リード（上部1行 muted）＋ 主ビジュアル ＋ 下部示唆（右パネル or フル幅バー）
```

### 共通ヘルパー（これを組み合わせて各型を作る）
- `lead(slide, text)` — 本文ゾーン上部の1行リード
- `split(main_ratio / panel_w)` — 主矩形／右パネル矩形を返す
- `insight_panel(slide, x,y,w,h, blocks=[(見出し,本文),...])` — 右の淡主色示唆パネル
- `bottom_bar(slide, head, body, boxed=)` — 下部フル幅バー（左accent見出し＋縦罫＋本文）
- `label_rule / num_tab` — ラベル＋下線 ／「NN｜ラベル」ミニ見出し
- `kpi_number` — 大きな数値。`rule/vrule/dot(円)`
- チャート: `vbars`(1本強調)／`hbars`／`linechart`／`dual_line`(計画実績)／`data_table`(hi_col/row/cell・sub_headers)
- 定数: `X0/ZW/ZY/ZH/ZB/DY/DH/PANEL_W/BAR_Y/GREY/GREY_L/INK`、`DASH`(破線)

### 50型 → 関数（idx｜型名｜関数）
```
01 データ＋示唆        wf_data_insight       26 カスタマージャーニー wf_journey
02 左右比較           wf_compare_lr         27 計画対実績          wf_plan_actual
03 結論＋3つの根拠     wf_conclusion_reasons 28 ギャップ分析        wf_gap
04 課題・原因・解決    wf_problem_cause_solution 29 表＋示唆        wf_table_insight
05 プロセス・手順      wf_process_steps      30 リスク＋対策        wf_risk_action
06 重要数値＋推移      wf_kpi_trend          31 優先順位            wf_priority
07 全体数値＋内訳      wf_total_breakdown    32 まとめ＋次アクション wf_summary_actions
08 マトリクス          wf_matrix             33 並列グラフ比較      wf_dual_charts
09 時系列・変化        wf_timeline_change    34 重点方針＋実行構造  wf_policy_execution
10 全体像・構造分解    wf_structure_decompose 35 ロジックツリー     wf_logic_tree
11 事例・成果          wf_case_result        36 KPIドライバー       wf_kpi_driver
12 問い＋回答          wf_question_answer    37 戦略カスケード      wf_strategy_cascade
13 1メッセージ         wf_one_message        38 同心円・対象範囲    wf_concentric_scope
14 重要数値単独        wf_kpi_single         39 ベン図・重なり      wf_venn
15 Before／After       wf_before_after       40 レイヤー・基盤構造  wf_layers
16 メリット・デメリット wf_pros_cons          41 スイムレーン        wf_swimlane
17 選択肢比較表        wf_options_table      42 RACI・役割分担      wf_raci
18 ランキング          wf_ranking            43 加重評価スコア      wf_weighted_score
19 ファネル            wf_funnel             44 シナリオ比較        wf_scenarios
20 ピラミッド・階層    wf_pyramid_levels     45 仮説検証            wf_hypothesis
21 循環・サイクル      wf_cycle              46 ウォーターフォール  wf_waterfall
22 ロードマップ        wf_roadmap            47 構成比変化          wf_composition_change
23 判断フロー          wf_decision_flow      48 ヒートマップ        wf_heatmap
24 因果関係            wf_causality          49 顧客の声→論点→施策 wf_voice_to_action
25 相関・関係図        wf_relation           50 KPIダッシュボード   wf_kpi_dashboard
```

---

## 4. 既存図解の標準化（diagrams.py / チャート）

ワイヤー標準へ寄せて以下を変更（検査PASS済み）:
- **角丸→フラット**: サイクル節点＝白丸OVAL＋主色線 ／ ランキング順位バッジ＝直角
  （首位のみ主色ベタ・他は白地に主色文字）／ 会話吹き出し＝直角
- **表ヘッダのベタ塗り廃止**: `diagram_table` ヘッダ＝淡グレー(SURFACE)地＋黒文字＋細罫線
- **グループ見出し帯廃止**: `diagram_group` ＝白箱＋淡グレーヘッダ＋主色見出し（細罫線）
- **チャート配色**: `CHART_PALETTE` を **主色青＋無彩グレー主体**に変更（緑/オレンジを既定から除外。
  必要時のみ `colors=` で SUCCESS/DANGER を明示）

---

## 5. 生成・確認コマンド

```bash
cd projects/wireframe_gallery
PATH="/Applications/LibreOffice.app/Contents/MacOS:$PATH" ../../.venv/bin/python3 generate.py
# 末尾 validate() が検査ゲート。ERROR 0 で PASS。
# 目視: soffice で output.pptx→pdf、PyMuPDF で PNG 化して確認
```
落とし穴は既存 `CLAUDE.md`／`HANDOFF.md §8` を参照（Python3.12必須・PDF直読不可・
`need_h ≤ 0.85×box_h` の余白・`validate` は再レンダ時 output.pdf を消してから実行が確実）。

---

## 6. 次のタスク（未着手・優先順）

1. **50型を pages.py へ組み込み**、`content.txt`／型指定から実コースを1本通しで生成する
   （＝本来のゴール。`wireframes.py` の各 `wf_*` を pages のディスパッチャに接続）。
2. 実コース（例: マーケ基礎/AI活用）の**通し生成→検査→PDF納品**。
3. 図解の残り（pyramid/matrix/steps/before_after/flow 等）で accent 過多が残る箇所の微調整。
4. カタログの本編50型に**ミニプレビュー画像**を付ける（現状は番号＋名称＋関数のリファレンス）。

---

## 7. ユーザー方針（守ること）
- スピード重視。個人情報・機密以外は許可を求めず進めてよい。
- 色（青）と書体（ヒラギノ／Graphik）は不変。仕上げ規定（§1）を全生成で厳守。
- 呼び名は「チャプター」。配布は PDF で字形固定（ヒラギノ/Graphik 非搭載PC対策）。
