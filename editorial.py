"""editorial.py — 資料全体の「統一してよいもの」だけを一元化する編集レイヤー。

## なぜこのモジュールがあるか

同じ資料としての統一感は必要だが、**全スライドを同じテンプレートにしてはいけない**。
そこで「統一するもの」と「内容ごとに変えるもの」を**ソースの上で分離**する。

- 統一してよいもの（＝このモジュールが唯一の定義元。全ページで同じ値を使う）
    1. 基本フォントの方向性 …… `TYPE`
    2. 本文色                 …… `INK` / `INK_SUB` / `INK_REV`
    3. アクセント色           …… `ACCENT`（1資料1色。淡面は `ACCENT_PALE`）
    4. 余白の感覚             …… `U` / `space()` / `GRID` / `baseline()`
    5. 罫線の太さ             …… `RULE`（この5値以外を引かない）
    6. 注釈の扱い             …… `note()` / `mark()` / `NOTE_*`
    7. 編集トーン             …… `TONE` / `tone_lint()`

- 内容に合わせて変えるもの（＝**統一しない**。`spreads.py` が構成ごとに選び分ける）
    見出しの位置／カラム数と幅／数値の見せ方／図解の有無／写真の有無／
    余白の位置／本文の密度／要素の大きさ／情報の読み順／主役となる要素
    → 何を変えたかは `Signature` に記録し、`audit.py` が「変わっているか」を検査する。

## 使い方（骨子）

    from editorial import GRID, baseline, rule, kicker, heading, body, note

    x, w = GRID.span(0, 7)             # 12列グリッドの 0列目から7列ぶん
    kicker(s, x, baseline(0), w, "OVERVIEW")
    heading(s, x, baseline(1), w, "運用は3つの工程に分かれる")
    rule(s, x, baseline(4), w, weight="structure")
    body(s, x, baseline(5), w, ["…", "…"], density="sparse")
    note(s, *GRID.span(8, 4), y=baseline(18), items=["出典：社内実績値"])

装飾部品を並べるためのモジュールではない。**情報を編集した結果としての誌面**を
組むための語彙（グリッド・基準線・罫線・注釈・数値の扱い）を提供する。
"""
from __future__ import annotations

from dataclasses import dataclass, field as _dc_field
import re

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

import slides as _sl
from slides import (
    PRIMARY, PRIMARY_LIGHT, TEXT, TEXT_MUTED, BORDER, SURFACE, WHITE,
    FONT, JP_FONT, JOSEFIN,
    RGBColor, textbox, shape_box, connector,
)

__all__ = [
    # 統一トークン
    "TYPE", "INK", "INK_SUB", "INK_REV", "ACCENT", "ACCENT_PALE", "HAIR",
    "U", "space", "GRID", "Grid", "FIELD", "BASE", "baseline", "baselines",
    "RULE", "NOTE_SIZE", "NOTE_COLOR", "NOTE_MARK", "TONE", "SCALE", "DENSITY",
    # プリミティブ
    "rule", "vrule", "kicker", "heading", "lead", "body", "figure",
    "note", "mark", "plane", "caption", "fit_h", "after",
    # 検査・記録
    "tone_lint", "Signature", "figure_area", "figure_areas",
]


# ============================================================================
# 1. 統一してよいもの（この節の値は資料全体で共有する）
# ============================================================================

# ---------------------------------------------------------------- 基本フォントの方向性
# 「方向性」だけを統一する＝和文ゴシック1本／latin グロテスク1本／装飾英字1本。
# サイズ・ウェイトはページごとに変えてよい（統一するのは書体の系統のみ）。
TYPE = {
    "jp": JP_FONT,          # 和文（ea/cs）
    "latin": FONT,          # 英数字
    "display": JOSEFIN,     # 章番号・数字ラベルなどの装飾英字
}

# ---------------------------------------------------------------- 本文色
INK = TEXT              # 本文・主見出し
INK_SUB = TEXT_MUTED    # 補助・注釈・キャプション
INK_REV = WHITE         # 濃色面の上の反転文字
HAIR = BORDER           # 罫線色（構造線。文字には使わない）

# ---------------------------------------------------------------- アクセント色
# 1資料1色。面で使わず、**焦点1〜2箇所**（見出しの罫・主役の数値・図解の主線）に置く。
ACCENT = PRIMARY
ACCENT_PALE = PRIMARY_LIGHT   # 薄い背景面（情報の区切りに使う。装飾に使わない）
PLANE = SURFACE               # 無彩に近い薄面（区切り用）

# ---------------------------------------------------------------- 余白の感覚
# すべての余白は基本単位 U の倍数で取る。「なんとなくの余白」を作らないための単位。
U = 0.42        # cm（≒12pt）

# 誌面（本文コンテンツの有効矩形）。テンプレ固定の見出し帯 y<3.0 には描かない。
FIELD = {"x": 1.07, "y": 3.15, "w": 23.26, "h": 9.45}
FIELD_R = FIELD["x"] + FIELD["w"]     # 右端 24.33
FIELD_B = FIELD["y"] + FIELD["h"]     # 下端 12.60

BASE = U        # 基準線（ベースライン）の間隔


def space(n: float) -> float:
    """余白 n 単位（cm）。0.5 単位まで許容し、それ未満の端数は作らない。"""
    return round(U * n, 4)


def baseline(n: int) -> float:
    """誌面上端から n 本目の基準線の y（cm）。要素の上端はここに揃える。"""
    return round(FIELD["y"] + BASE * n, 4)


def baselines() -> int:
    """誌面に収まる基準線の本数。"""
    return int(FIELD["h"] // BASE)


@dataclass(frozen=True)
class Grid:
    """段組みの基準となる列グリッド。

    列数は固定（12）だが、**使い方は固定しない**。`span()` で任意の列数を
    つないで 1段／非対称2段／3段…を作る。カラム数と幅は内容ごとに変える。
    """
    x: float = FIELD["x"]
    w: float = FIELD["w"]
    n: int = 12
    gutter: float = U

    @property
    def col(self) -> float:
        """1列の幅（cm）。"""
        return (self.w - self.gutter * (self.n - 1)) / self.n

    def span(self, start: int, cols: int) -> tuple[float, float]:
        """start 列目（0起点）から cols 列ぶんの (x, w) を返す。"""
        if start < 0 or cols < 1 or start + cols > self.n:
            raise ValueError(f"span 範囲外: start={start} cols={cols} n={self.n}")
        x = self.x + start * (self.col + self.gutter)
        w = self.col * cols + self.gutter * (cols - 1)
        return round(x, 4), round(w, 4)

    def split(self, *ratios: int, gap: int = 1) -> list[tuple[float, float]]:
        """列数の比で段を割る。例 `split(7, 5)` → 7列＋5列（非対称2段）。

        gap は段と段のあいだに空ける列数（既定1列＝溝も情報の区切りに使う）。
        """
        total = sum(ratios) + gap * (len(ratios) - 1)
        if total > self.n:
            raise ValueError(f"列が足りない: 要求{total} > {self.n}")
        out, cur = [], 0
        for r in ratios:
            out.append(self.span(cur, r))
            cur += r + gap
        return out


GRID = Grid()

# ---------------------------------------------------------------- 罫線の太さ
# 引いてよい線幅はこの5値だけ。太さで意味を分ける（装飾の線は引かない）。
RULE = {
    "hair": 0.5,        # 情報の区切り（最も弱い。注釈の上・行間の仕切り）
    "thin": 0.75,       # 表・図解の内部罫
    "rule": 1.0,        # 節の区切り
    "structure": 1.5,   # 見出しと本文の境／段の境
    "accent": 2.25,     # アクセント色で引く焦点の線（1画面1本まで）
}

# ---------------------------------------------------------------- 文字サイズの段
# 「差」を作るための段。すべて使う必要はなく、1ページで使うのは3〜4段まで。
SCALE = {
    "hero": 40.0,       # 主役の数値・1メッセージ
    "display": 26.0,    # 大きな主張
    "head": 15.0,       # 節見出し
    "lead": 12.5,       # リード文
    "body": 11.0,       # 本文
    "small": 9.5,       # 補助
    "note": 8.5,        # 注釈
    "kicker": 9.0,      # ラベル（英字・小）
}

# 本文の密度（内容量に応じて変える。統一しない）
DENSITY = {
    "sparse": (13.0, 1.95),
    "normal": (11.0, 1.75),
    "dense": (9.75, 1.55),
}

# ---------------------------------------------------------------- 注釈の扱い
# 注釈は「本文の下に小さく・muted・ヘアラインで切る」で全ページ統一。
# 位置（どの段の下に置くか）はページごとに変えてよいが、見え方は変えない。
NOTE_SIZE = SCALE["note"]
NOTE_COLOR = INK_SUB
NOTE_MARK = "※"

# ---------------------------------------------------------------- 編集トーン
# 寄り添い・後押し。脅し／プレッシャー／根拠なき約束／過剰な強調記号を使わない。
TONE = {
    "voice": "寄り添い・後押し（読み手を急かさない）",
    "sentence": "結論を先に書き、体言止めと文末を混在させない",
    "forbid": "脅し・プレッシャー・根拠なき約束・感嘆符の多用・専門用語の素置き",
}

# tone_lint が拾う表現（部分一致）。過検出を避けるため強い表現に絞る。
_TONE_NG = [
    (r"[!！]{2,}", "感嘆符の連打（トーン：落ち着いた編集調にする）"),
    (r"(絶対に|必ず)(儲か|成功|成果が出)", "根拠なき約束"),
    (r"(手遅れ|取り残され|今すぐ買わ|やらないと損)", "脅し・プレッシャー"),
    (r"(誰でも|たった)\s*\d+\s*(日|分|時間)で", "誇大な即効性の訴求"),
    (r"[〜～]し(なければならない|なくてはならない)", "強制的な言い回し（提案形にする）"),
]


def tone_lint(*texts) -> list[str]:
    """編集トーンの機械チェック。引っかかった表現を理由つきで返す（空＝合格）。

    文字列・文字列リスト・ネストしたリストを混ぜて渡せる。
    """
    flat: list[str] = []

    def _walk(v):
        if v is None:
            return
        if isinstance(v, (list, tuple)):
            for i in v:
                _walk(i)
        else:
            flat.append(str(v))

    _walk(list(texts))
    out = []
    for t in flat:
        for pat, why in _TONE_NG:
            if re.search(pat, t):
                out.append(f"{why}: 「{t[:40]}」")
    return out


# ============================================================================
# 2. プリミティブ（統一トークンを必ず通す描画）
#    ここを経由して描けば、色・線幅・注釈の見え方は自動的に揃う。
#    そのうえで「どこに・どれだけの大きさで置くか」は呼び出し側が変える。
# ============================================================================

def _weight(w) -> float:
    """線幅の指定（キー名 or 数値）を pt に解決する。未登録の太さは弾く。"""
    if isinstance(w, str):
        if w not in RULE:
            raise ValueError(f"罫線の太さは {sorted(RULE)} のみ: {w!r}")
        return RULE[w]
    if not any(abs(float(w) - v) < 1e-6 for v in RULE.values()):
        raise ValueError(f"罫線の太さは {sorted(set(RULE.values()))} pt のみ: {w}")
    return float(w)


def fit_h(lines, w, size, *, ls=1.0, font=None, bold=False):
    """その幅・その級数で本当に必要な高さ（cm）を返す。

    `slides` の折返し計測（検査ゲートと同じ実装）を使うので、ここで決めた高さは
    そのまま検査を通る。設計基準 `need_h ≤ 0.85 × box_h` の余裕を含める。
    """
    lines = [lines] if isinstance(lines, str) else [str(t) for t in lines if str(t)]
    if not lines:
        return 0.0
    ml = mr = 0.1
    mt = mb = 0.05
    eff_w_pt = max(1.0, (w - ml - mr) * _sl.PT_PER_CM)
    n = 0
    for para in lines:
        wrapped, _ = _sl._wrap_lines(para, eff_w_pt, size, bold, font or TYPE["latin"])
        n += len(wrapped)
    need = n * size * _sl.LINE_H_FACTOR * ls / _sl.PT_PER_CM + mt + mb
    return round(need / 0.85, 4)


def after(y: float, *, gap: int = 1) -> float:
    """y の下で最初に来る基準線（gap 本ぶん空ける）。段落送りを基準線に乗せる。"""
    n = (y - FIELD["y"]) / BASE
    import math
    return round(baseline(int(math.ceil(n - 1e-6)) + max(gap - 1, 0)), 4)


def rule(slide, x, y, w, *, weight="hair", color=None):
    """水平の罫線。太さは RULE の5値のみ、色は既定でヘアライン色。"""
    return connector(slide, x, y, x + w, y,
                     color=color or (ACCENT if weight == "accent" else HAIR),
                     width=_weight(weight))


def vrule(slide, x, y, h, *, weight="hair", color=None):
    """垂直の罫線（段の境・数値の仕切り）。"""
    return connector(slide, x, y, x, y + h,
                     color=color or (ACCENT if weight == "accent" else HAIR),
                     width=_weight(weight))


def plane(slide, x, y, w, h, *, tone="pale"):
    """薄い背景面（情報を分けるための面。装飾では使わない）。

    tone: "pale"=淡いアクセント面 / "plain"=無彩に近い面。枠線は引かない。
    """
    return shape_box(slide, MSO_SHAPE.RECTANGLE, x, y, w, h,
                     fill=ACCENT_PALE if tone == "pale" else PLANE, line=None)


def _text(slide, x, y, w, lines, *, size, ls, color, bold=False,
          align=PP_ALIGN.LEFT, font=None):
    """内部共通。必要な高さを実測して置き、**下端の y** を返す。"""
    lines = [lines] if isinstance(lines, str) else [str(t) for t in lines if str(t)]
    if not lines:
        return y
    h = fit_h(lines, w, size, ls=ls, font=font, bold=bold)
    textbox(slide, x, y, w, h, lines, size=size, bold=bold, color=color,
            align=align, line_spacing=ls, font=font or TYPE["latin"])
    return round(y + h, 4)


def kicker(slide, x, y, w, text, *, accent=True, size=None):
    """小ラベル（節の名前・番号）。下端の y を返す。"""
    if not text:
        return y
    return _text(slide, x, y, w, [text], size=size or SCALE["kicker"], ls=1.2,
                 color=ACCENT if accent else INK_SUB, bold=True)


def heading(slide, x, y, w, text, *, size=None, lines=None, color=None):
    """見出し。**位置と大きさは呼び出し側が決める**（統一するのは書体と色だけ）。"""
    body_lines = lines if lines is not None else [text]
    return _text(slide, x, y, w, body_lines, size=size or SCALE["head"], ls=1.35,
                 color=color or INK, bold=True)


def lead(slide, x, y, w, text, *, size=None):
    """リード文（そのページで読ませる1〜2行）。本文色で置く。"""
    return _text(slide, x, y, w, [text] if isinstance(text, str) else text,
                 size=size or SCALE["lead"], ls=1.6, color=INK)


_DENSITY_ORDER = ("sparse", "normal", "dense")


def body(slide, x, y, w, lines, *, density="normal", color=None, fit_to=None):
    """本文。density で文字量に応じた密度を選ぶ（ページごとに変えてよい）。

    fit_to（使える高さ cm）を渡すと、収まる密度まで自動で1段ずつ詰める。
    最も詰めても収まらないときは例外で止める（黙って字を切らない）。
    """
    lines = [lines] if isinstance(lines, str) else [str(t) for t in lines if str(t)]
    if not lines:
        return y
    order = list(_DENSITY_ORDER[_DENSITY_ORDER.index(density):])
    size, ls = DENSITY[order[0]]
    if fit_to is not None:
        for d in order:
            size, ls = DENSITY[d]
            if fit_h(lines, w, size, ls=ls) <= fit_to:
                break
        else:
            need = fit_h(lines, w, size, ls=ls)
            raise ValueError(
                f"本文が誌面に収まらない（必要 {need:.2f}cm > 使える {fit_to:.2f}cm）。"
                f"文章を短くするか、段を広げること。")
    return _text(slide, x, y, w, lines, size=size, ls=ls, color=color or INK)


def caption(slide, x, y, w, text, *, align=PP_ALIGN.LEFT):
    """図版・数値に添える短い説明。注釈より一段強い補助テキスト。"""
    return _text(slide, x, y, w, [text] if isinstance(text, str) else text,
                 size=SCALE["small"], ls=1.45, color=INK_SUB, align=align)


def figure(slide, x, y, w, value, *, unit="", label="", size=None,
           accent=True, align=PP_ALIGN.LEFT):
    """数値。**見せ方（大きさ・単位の添え方・ラベルの上下）は場面ごとに変える**。

    ここが統一するのは色（アクセント or 本文色）と書体だけ。
    """
    size = size or SCALE["hero"]
    top = y
    if label:
        top = after(_text(slide, x, top, w, [label], size=SCALE["kicker"], ls=1.2,
                          color=INK_SUB, align=align), gap=1)
    val = f"{value}{unit}" if unit else str(value)
    return _text(slide, x, top, w, [val], size=size, ls=1.05, color=ACCENT if accent else INK,
                 bold=True, align=align, font=TYPE["latin"])


# ---------------------------------------------------------------- 図版の領域
# 説明図は「線に合わせて」ラベルを置くのが正しく、段組みの起点や基準線には乗らない。
# どこが図版かは形から推測しきれないので、描いた側が領域を申告する（記録のみ・描画しない）。
FIGURE_REGISTRY: list = []


def figure_area(slide, x, y, w, h):
    """説明図が占める矩形を記録する。`audit` の余白検査がこの範囲を除外する。"""
    FIGURE_REGISTRY.append({"slide_id": slide.slide_id,
                            "x": float(x), "y": float(y),
                            "w": float(w), "h": float(h)})


def figure_areas(slide):
    """そのスライドに記録された図版領域 [(x0, y0, x1, y1), ...]。"""
    return [(r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"])
            for r in FIGURE_REGISTRY if r["slide_id"] == slide.slide_id]


def mark(n: int) -> str:
    """本文中に置く注釈マーカー（※1）。本文末尾に連結して使う。"""
    return f"{NOTE_MARK}{n}"


def note(slide, x, y, w, items, *, rule_above=True, align=PP_ALIGN.LEFT):
    """注釈。ヘアラインで本文と切り、muted の小文字で置く（全ページ共通）。

    items: 文字列リスト。番号は自動で ※1 ※2 … を振る（1件なら番号なし）。
    """
    items = [items] if isinstance(items, str) else [i for i in (items or []) if i]
    if not items:
        return y
    if rule_above:
        rule(slide, x, y, w, weight="hair")
        y += space(0.45)
    lines = ([f"{mark(i + 1)} {t}" for i, t in enumerate(items)]
             if len(items) > 1 else [f"{NOTE_MARK} {items[0]}"])
    return _text(slide, x, y, w, lines, size=NOTE_SIZE, ls=1.4,
                 color=NOTE_COLOR, align=align)


# ============================================================================
# 3. 変えたことの記録（Signature）
#    「内容ごとに変える」と口で言っても検査できないので、10軸を値にして残す。
#    audit.py はこの宣言ではなく **実際の pptx** から同じ10軸を再計測し、
#    宣言と実物の双方で「同じ誌面の反復」になっていないかを見る。
# ============================================================================

@dataclass
class Signature:
    """1ページの構成を10軸で表したもの（同じ値が続く＝テンプレ化のサイン）。"""
    head_pos: str = "left-top"      # 見出しの位置
    columns: str = "1"              # カラム数と幅（例 "7:5"）
    number: str = "none"            # 数値の見せ方 none/inline/hero/table/chart
    diagram: bool = False           # 図解の有無
    photo: bool = False             # 写真の有無
    void: str = "right"             # 余白の位置（大きく空ける側）
    density: str = "normal"         # 本文の密度
    hero: str = "text"              # 主役となる要素
    order: str = "lr"               # 情報の読み順 lr/tb/zig/radial
    scale: str = "even"             # 要素の大きさの差 even/contrast

    def key(self) -> tuple:
        return (self.head_pos, self.columns, self.number, self.diagram,
                self.photo, self.void, self.density, self.hero, self.order,
                self.scale)

    def distance(self, other: "Signature") -> int:
        """異なっている軸の数。3未満なら「ほぼ同じ誌面」とみなす。"""
        return sum(1 for a, b in zip(self.key(), other.key()) if a != b)
