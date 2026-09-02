# 資料全体の統一感 — 統一する7項目と、内容ごとに変える10項目

同じ資料としての統一感は要る。ただし **全スライドを同じテンプレートにしてはいけない**。
この2つは矛盾しない。「揃えるもの」を**限定**し、それ以外は**内容に合わせて動かす**からだ。

本書はその線引きと、それをソース上で担保する仕組み（`editorial.py` / `spreads.py` /
`ediagrams.py` / `audit.py`）の使い方をまとめる。

---

## 1. 統一してよいもの（この7つだけ）

| 項目 | 定義元 | 実体 |
|---|---|---|
| 基本フォントの方向性 | `editorial.TYPE` | 和文＝`JP_FONT` ／ latin＝`FONT` ／ 装飾英字＝`JOSEFIN`。系統だけを揃え、級数・ウェイトはページごとに変える |
| 本文色 | `editorial.INK` / `INK_SUB` / `INK_REV` | 本文・補助・反転の3段。これ以外の文字色を使わない |
| アクセント色 | `editorial.ACCENT` | 1資料1色。面で塗らず、**焦点1〜2箇所**に置く |
| 余白の感覚 | `editorial.U` / `space()` / `GRID` / `baseline()` | 基本単位 0.42cm。横は12列グリッド、縦は基準線。余白は必ずこの倍数 |
| 罫線の太さ | `editorial.RULE` | `hair 0.5 / thin 0.75 / rule 1.0 / structure 1.5 / accent 2.25` pt の5値のみ |
| 注釈の扱い | `editorial.note()` / `mark()` | ヘアラインで切り、8.5pt・補助色。番号は ※1 ※2。位置は変えてよいが見え方は変えない |
| 編集トーン | `editorial.TONE` / `tone_lint()` | 寄り添い・後押し。脅し／プレッシャー／根拠なき約束／感嘆符の連打を機械で弾く |

この7つは `editorial.py` が唯一の定義元で、プリミティブ（`rule` `kicker` `heading`
`lead` `body` `caption` `figure` `note` `plane`）を通さないと描けない。
たとえば `rule(..., weight=3.0)` は例外で止まる。**揃うのではなく、揃うようにする**。

---

## 2. 内容に合わせて変えるもの（この10項目は統一しない）

見出しの位置／カラム数と幅／数値の見せ方／図解の有無／写真の有無／余白の位置／
本文の密度／要素の大きさ／情報の読み順／主役となる要素。

`spreads.py` が構成（スプレッド）として10型を持ち、上の10軸をそれぞれ違う値で組む。

| 構成 | 主役 | 段組み | 見出しの位置 | 余白の偏り |
|---|---|---|---|---|
| `statement` | 1文 | 9列1段 | 上・左 | 右下に大きく |
| `lead_and_void` | 本文 | 7＋4（右は空ける） | 左上 | 右 |
| `two_voices` | 本文 | 7＋4（縦罫で仕切る） | 左中 | 右下 |
| `figure_first` | 数値 | 4＋7 | 右上 | 左下 |
| `process_band` | 工程図 | 全幅＋下段4:7 | **下段左** | 右上 |
| `correspondence` | 対応表 | 8＋3（図が先） | 右上 | 右下 |
| `load_report` | 負荷図 | 8＋3（薄い面で仕切る） | 左上 | 下 |
| `change_note` | 変化図 | 4＋7 | 左上 | 左下 |
| `connection_map` | 接続図 | 全幅 | 左上 | 上・右 |
| `photo_frame` | 写真 | 7＋4（左右は内容で選ぶ） | 図の反対側 | 下 |

### 構成の選び方（順番で回さない）

`spreads.choose(content, history)` は **内容の形** から構成を決める。

```
steps  →  process_band     points →  change_note
pairs  →  correspondence   nodes  →  connection_map
load   →  load_report      value  →  figure_first
image / photo → photo_frame
（どれにも当てはまらない文章だけのページは、直近と最も違う構成を選ぶ）
```

順番のローテーションではないので、内容が変われば構成が変わり、内容が似ていても
直近3ページと軸が3つ未満しか違わない構成には罰点が付いて後ろへ回る。

```python
from spreads import render_all

render_all(prs, [
    {"section": "OVERVIEW ／ 全体像", "title": "…", "statement": "…",
     "note": ["対象：…"]},
    {"section": "PROCESS ／ 工程", "title": "…",
     "steps": [("企画", "範囲を決める"), ("設計", "前提の置き場所")],
     "accent_at": 1, "head": "…", "body": ["…"]},
])
```

`render_all` は描く前に全ページの文言を `tone_lint` にかけ、トーン違反があれば
例外で止める（トーンは統一項目なので、ページごとの判断に委ねない）。

---

## 3. 説明図（editorial line diagram）

図解は「入れること」を目的にしない。**工程・接続・負荷・変化・対応関係**という
関係を説明する必要があるときだけ、`ediagrams.py` の5型を使う。

| 関数 | 示すもの | 構図 |
|---|---|---|
| `edia_process` | 工程 | 横一本の背骨線に節点。上にラベル、下に補足。矢じりは終端に1つ |
| `edia_connection` | 接続 | 中心の系と周辺要素を細線で結び、**各線の上**に関係ラベル |
| `edia_load` | 負荷 | 細いトラック＋実測バー。上限は縦線で示し、超過分は線の外へ伸ばす |
| `edia_change` | 変化 | 細い折れ線。始点・終点・差分だけを注記 |
| `edia_correspondence` | 対応関係 | 左右2列を細線で結ぶ。焦点の1組だけアクセント |

画風は全型共通で固定する。

- 細い線と最小限の面（線幅は `RULE` の5値のみ）
- 色は本文色＋アクセントの**2色以内**
- 影なし／3Dなし／光沢なし／キャラクター表現なし／円形アイコン背景なし
- 角丸を使わない。ベタ塗りの帯・カードを作らない
- ラベルは必ず対応する線・節点の直近に置く（`_label` の `middle_at` / `bottom_at`
  で線に合わせる。固定オフセットで「だいたい」の位置に置かない）

各ビルダーは描画前に `editorial.figure_area()` で自分の矩形を申告する。図の内部は
段組みの起点や基準線に乗らないのが正しいので、`audit` の余白検査はこの範囲を除く。

---

## 4. 検査（統一と変化の両方を機械で見る）

`slides.validate()` は「収まっているか」の検査ゲート。`audit.py` はその上に載る
**編集の検査**で、生成した pptx を実測する。宣言ではなく描かれた結果を測るので、
「宣言だけ変えて中身は同じ」を見逃さない。

```python
from audit import audit
audit(prs)          # ERROR があれば SystemExit(1)
```

### 統一の検査

| コード | 重さ | 内容 |
|---|---|---|
| `INK` | ERROR | 本文色・アクセント色の外の文字色 |
| `FONT` | WARN | 規定外の書体 |
| `RULE_W` | WARN | `RULE` の5値以外の線幅 |
| `NOTE_STYLE` | WARN | 注釈級数の文字が補助色でない |
| `ACCENT_MANY` | WARN | 1画面のアクセントが3箇所を超える |
| `GRID_X` / `GRID_Y` | WARN | 段組みの起点・基準線から外れたブロック（図版内部と注釈、中央/右揃えのテキストは対象外） |

### 変化の検査

10軸を pptx から再計測して比べる。

| コード | 重さ | 内容 |
|---|---|---|
| `SAME_SPREAD` | ERROR | 直前ページと10軸すべて一致 |
| `NEAR_SPREAD` | WARN | 直前ページと軸が3つ未満しか違わない |
| `SYMMETRY` | WARN | 左右対称・等幅・同サイズだけで組まれた誌面 |
| `VARIETY_LOW` | WARN | 相異なる構成が全体の6割未満 |

実測した10軸はレポートの前に一覧で出るので、「どのページが何を主役にしているか」を
表で見比べられる。

```
P 2 見出し=left-top   段=1:L 数値=hero   図=− 写真=− 余白=top-right   密度=sparse 主役=number  読順=tb  大小=contrast
P 5 見出し=left-mid   段=2:C 数値=inline 図=○ 写真=− 余白=bottom-left 密度=sparse 主役=diagram 読順=tb  大小=even
```

許容値を変えたいときは `Policy` を渡す（`audit(prs, policy=Policy(accent_max=2))`）。

---

## 5. 実例

`projects/editorial_consistency/generate.py`。本文10枚が同じトークンを共有しながら
1枚も同じ構成にならない。検査ゲート・編集検査ともに PASS。

```bash
cd projects/editorial_consistency
PATH="/Applications/LibreOffice.app/Contents/MacOS:$PATH" ../../.venv/bin/python3 generate.py
```

---

## 6. 何を作るかではなく、何を編集したか

- 装飾部品を組み合わせた結果としてレイアウトを作らない。**情報を編集した結果**として
  レイアウトを作る。1ページに置く要素は、そのページの結論を支えるものだけにする。
- 情報を分けるときは、囲みや色面より先に **余白・段組み・細い罫線・行と列・番号・
  見出しの位置・インデント・基準線・薄い背景面・文字サイズの差**を使う。
- すべてを左右対称・等間隔・同じ大きさにしない。非対称の段組みと、大きく残した
  余白を積極的に使う（`SYMMETRY` はそれを外したときに鳴る）。
- 既存の `pages.py` / `wireframes.py` / `diagrams.py` はそのまま使える。本レイヤーは
  それらを置き換えるものではなく、**誌面として編集する**ときの語彙と検査を足すもの。
