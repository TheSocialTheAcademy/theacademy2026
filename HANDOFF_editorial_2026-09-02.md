# 引き継ぎ資料（編集レイヤー：資料全体の統一感）— 2026-09-02

対象: The Academy コーススライド生成システム。土台は `HANDOFF.md` ／
`HANDOFF_wireframes_2026-08-28.md` ／ `HANDOFF_frameworks_2026-08-28.md` ／ `CLAUDE.md`。
本書は **「同じ資料に見せながら、全スライドを同じテンプレートにしない」ための層** に絞る。

仕様の正は `docs/EDITORIAL.md`。本書は経緯・判断・残件を書く。

---

## 1. 何を解いたか

要求は2つで、放っておくと衝突する。

1. 各スライドに最低限の統一感を持たせる
2. ただし全スライドを同じテンプレートにしない

解き方は **「揃えてよいもの」を7項目に限定して1箇所で定義し、それ以外の10項目は
内容ごとに変える**。そのうえで、両方を機械で検査できるようにした（守れているかを
目視の感想に委ねない）。

- 統一する7項目：基本フォントの方向性／本文色／アクセント色／余白の感覚／
  罫線の太さ／注釈の扱い／編集トーン
- 変える10項目：見出しの位置／カラム数と幅／数値の見せ方／図解の有無／写真の有無／
  余白の位置／本文の密度／要素の大きさ／情報の読み順／主役となる要素

---

## 2. 追加したモジュール

| ファイル | 役割 | 主API |
|---|---|---|
| `editorial.py` | 統一7項目の唯一の定義元＋プリミティブ | `TYPE/INK/ACCENT/U/GRID/baseline/RULE/note/tone_lint`、`fit_h`、`after`、`Signature`、`figure_area` |
| `spreads.py` | 誌面構成10型と、内容の形からの選択 | `SPREADS` / `choose()` / `render()` / `render_all()` |
| `ediagrams.py` | 説明図5型（工程・接続・負荷・変化・対応関係） | `edia_process/connection/load/change/correspondence` |
| `audit.py` | 生成物を実測する編集検査 | `audit()` / `audit_violations()` / `measure_signature()` / `Policy` |

実例: `projects/editorial_consistency/generate.py`（本文10枚）。
テスト: `tests/test_editorial_tokens.py`（統一トークン）／`tests/test_editorial_variety.py`
（構成の選択・反復の検出・統一の逸脱）。全 73 件 PASS。

### 設計上の判断（あとから変えるとき用）

- **プリミティブを通さないと描けない形にした**。`rule(weight=3.0)` は例外で止まる。
  「揃える」ではなく「揃うようにする」ため。
- **文字の高さは実測する**。`fit_h` は `slides._wrap_lines`（検査ゲートと同じ計測）で
  必要行数を出し、設計基準 `need_h ≤ 0.85×box_h` の余裕を含めて高さを返す。
  各プリミティブは**下端 y を返す**ので、`after()` で次の基準線に送って流し込める。
  固定高さのベタ置きをやめたことで、`CLIP`／`OVERFLOW_V` が構造的に出なくなった。
- **`body(fit_to=)` は密度を1段ずつ落として収める**。それでも収まらなければ例外。
  黙って字を切らない・勝手に 8pt 未満へ縮めない。
- **構成は順番で回さない**。`choose()` は内容の形（`steps`/`pairs`/`load`/`points`/
  `nodes`/`value`/`image`）で決め、直近3ページと軸が3つ未満しか違わない候補に罰点を付ける。
  `layouts.py` の `rotate(i)`（index ローテーション）とはここが違う。
- **検査は宣言ではなく実測**。`spreads` が返す `Signature` は書き手の意図で、`audit` は
  同じ10軸を pptx から測り直す。宣言だけ変えて中身が同じ、を防ぐため。
- **図版の領域は描いた側が申告する**（`editorial.figure_area`）。図の内部はラベルを線に
  合わせるのが正しく、段組みの起点や基準線に乗らない。形からの推測だと本文まで
  巻き込むので、申告があるデッキでは申告を正とする。記録はパッケージの弱参照で
  持つので、同一プロセスで作り直しても前のランの記録は混ざらない。

---

## 3. 検査の読み方

```bash
cd projects/editorial_consistency
PATH="/Applications/LibreOffice.app/Contents/MacOS:$PATH" ../../.venv/bin/python3 generate.py
```

`validate()`（収まっているか）→ `audit()`（統一と変化）の順に出る。`audit` はレポートの前に
実測した10軸を一覧表示するので、「どのページが何を主役にしているか」を並べて確認できる。

- ERROR: `INK`（本文色・アクセント色の外の文字色）／`SAME_SPREAD`（直前と10軸すべて一致）
- WARN: `FONT` `RULE_W` `NOTE_STYLE` `ACCENT_MANY` `GRID_X` `GRID_Y` `NEAR_SPREAD`
  `SYMMETRY` `VARIETY_LOW`

許容値は `Policy` で変えられる（`audit(prs, policy=Policy(accent_max=2))`）。

---

## 4. 既存モジュールとの関係

置き換えではない。`pages.py`（28型）・`wireframes.py`（wf50型）・`diagrams.py`・
`wfcharts.py` はそのまま使える。本レイヤーは、それらを**誌面として編集する**ときの
語彙（グリッド・基準線・罫線・注釈・数値）と検査を足すもの。

- `audit` は `ediagrams` を使っていないデッキでも動く（図版の申告が無ければ、細い要素の
  密集から図解領域を推定する）。既存型にかけた実測は次のとおり。
  - `concept` / `comparison`：違反なし。ただし等幅カードの横並びは `SYMMETRY`（WARN）で
    鳴る＝「すべてを同じ大きさにしない」に照らして正しい指摘。
  - `code_explain`：独自の暗色パレット（`CODE_TX` `CODE_LN`）が `INK`（ERROR）、行番号の
    罫が `RULE_W`（WARN）。`data`（グラフ）はグラフ内部の文字を読まないので静か。
  → 既存型を本レイヤーの下に寄せるか、型ごとに `Policy` を緩めるかは未決（§6-1）。

---

## 5. このセッションで直した既存の不具合

- 雛形ファイル名が **NFD**（macOS 由来）で、Linux では `brand.TEMPLATE`（NFC）から
  解決できず `load_template()` が `PackageNotFoundError` で落ちていた。NFC に正規化した。
  以後、雛形を macOS から持ち込むときは正規化を確認すること。

---

## 6. 次のタスク（未着手・優先順）

1. **実コースへの適用**：`projects/course_ai_prompt` などを本レイヤーで組み直し、
   audit を通す。`pages.py` の型を使う場合はトークンの差分をどう扱うか（Policy を
   緩めるか、型側を寄せるか）をここで決める。
2. **説明図の追加**：現在は5型（工程・接続・負荷・変化・対応関係）。分岐・入れ子・
   比率の3つは需要が見えたら足す。**画風は増やさない**（細い線と最小限の面・2色以内）。
3. **構成の追加**：10型のうち写真は枠のみの実装。実写が入る運用が決まったら
   `sp_photo_frame` のトリミング規則（裁ち落とし・キャプションの位置）を決める。
4. **`choose()` の精度**：いまは内容の形＋直近ペナルティ。章のなかでの位置（扉直後・
   まとめ前）も見て選べるとより誌面らしくなる。
5. **`layouts.py` の統合**：`rotate(i)` の3型は本レイヤーの構成と役割が重なる。
   `spreads` に寄せて廃止するか、`frameworks.py` からの参照を差し替えるかを決める。

---

## 7. 方針（守ること）

- 統一するのは7項目だけ。増やさない（増やすほどページは似てくる）。
- 図解を入れること自体を目的にしない。関係の説明が要るときだけ描く。
- すべてを左右対称・等間隔・同じ大きさにしない。非対称と大きな余白を使う。
- 装飾部品の組み合わせでレイアウトを作らない。情報を編集した結果として作る。
- 完了条件は `validate()` PASS **かつ** `audit()` ERROR 0。
