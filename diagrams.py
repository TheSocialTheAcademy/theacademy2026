"""図解ビルダー（パターンライブラリの型化）。

HANDOFF.md §9 タスクA。パターンライブラリ40型のうち「新規ビルダーが要る図解」を
再利用関数として実装する。slides.py を肥大化させないため独立モジュールにする。

API 規約:
    def diagram_xxx(slide, x, y, w, h, *, データ, accent=PRIMARY): ...
- 描画は必ず slides.py のビルダー（shape_box / textbox / connector）経由。
  これにより validate() の検知レジストリへ自動登録される。
- 色はブランド定数（brand.py 由来）のみ。accent で主役色を差し替え可能。
- 角丸ルール（design-guide）: 表・帯・入れ子・直列に並ぶ要素は直角 RECTANGLE、
  単独で浮くノード（サイクル節点など）のみ角丸 ROUNDED_RECTANGLE。
- x, y, w, h は cm。与えられた矩形の内側だけに描く（本文ゾーン逸脱を出さない）。

実装済み（優先11型）:
    diagram_flow_h      横フロー（→ / ＋ でつなぐ。最後を結果として強調）
    diagram_flow_v      縦フロー（下向き矢印で縦に連結）
    diagram_pyramid     ピラミッド（上ほど濃く・幅で階層を表現）
    diagram_before_after ビフォーアフター（左=現状/右=改善、中央に矢印）
    diagram_matrix      2×2 マトリクス（縦横軸ラベル＋4象限）
    diagram_steps       階段/ステップ（右肩上がりのブロックで段階的成長）
    diagram_cycle       サイクル（節点を円環に並べ矢印で循環）
    diagram_timeline    タイムライン（横線＋節点、上下交互ラベル）
    diagram_ranking     ランキング（順位バッジ＋ラベル＋値バー）
    diagram_formula     数式（部品ボックスを ＋ / ＝ でつなぐ）
    diagram_group       グループ図（見出し付きコンテナに要素を束ねる）
"""
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from slides import (
    PRIMARY, PRIMARY_LIGHT, SECONDARY, SUCCESS, DANGER, HIGHLIGHT,
    TEXT, TEXT_MUTED, BORDER, SURFACE, WHITE,
    CHART_INK, CHART_GREY, CHART_GREY_L,
    RGBColor, textbox, shape_box, connector, picture,
)

# 無強調の中立色は Primary Blue に調和する青みグレーで統一（グラフ節と同じ考え）。
NEUTRAL = CHART_GREY   # 旧 RGBColor(0x9A,0x9A,0xA6) の置き換え（青みグレー）

# コード解説用の暗色パレット（ブランド濃紺ベース）
MONO = "Courier New"                       # 等幅（配布先で安定して存在する latin 等幅）
CODE_BG = RGBColor(0x0E, 0x1A, 0x3A)       # 暗い紺の地
CODE_HI = RGBColor(0x1C, 0x2F, 0x60)       # ハイライト行の帯
CODE_TX = RGBColor(0xE9, 0xEC, 0xF7)       # 明るい本文
CODE_LN = RGBColor(0x6C, 0x7A, 0xB0)       # 行番号（控えめ）

__all__ = [
    # タスクA: 図解
    "diagram_flow_h", "diagram_flow_v", "diagram_pyramid",
    "diagram_before_after", "diagram_matrix", "diagram_steps",
    "diagram_cycle", "diagram_timeline", "diagram_ranking",
    "diagram_formula", "diagram_group",
    # タスクB: 本編C専用ビルダー
    "diagram_table", "diagram_code", "diagram_conversation",
    "diagram_image_explain", "diagram_ui_steps",
    # タスクD: 事業紹介デッキ参考の型（refs 蒸留・色は青へ置換）
    "diagram_nested_circles", "diagram_numbered_list",
    "diagram_split_hero", "diagram_stat_annot",
]


# ---------------------------------------------------------------- 共通ヘルパー
def _tint(color, t):
    """color を白へ t（0..1）だけ寄せた淡色を返す。t=0 で原色、t=1 で白。"""
    r, g, b = color[0], color[1], color[2]
    return RGBColor(int(r + (255 - r) * t), int(g + (255 - g) * t),
                    int(b + (255 - b) * t))


def _on(fill):
    """塗り色 fill の上で可読な文字色（明るければ TEXT、暗ければ WHITE）。"""
    r, g, b = fill[0], fill[1], fill[2]
    return TEXT if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else WHITE


def _lab_sub(item):
    """(label, sub) / (label,) / "label" を (label, sub) に正規化。"""
    if isinstance(item, (list, tuple)):
        return item[0], (item[1] if len(item) > 1 else "")
    return item, ""


import math


# ---------------------------------------------------------------- 1. 横フロー
def diagram_flow_h(slide, x, y, w, h, *, steps, accent=PRIMARY, connect="arrow"):
    """横フロー。steps=[(label, sub?), ...]。最後の要素を結果として accent 強調。

    connect="arrow"（矢印）/ "＋" などの記号 / None（連結なし）。
    """
    n = len(steps)
    steps = [_lab_sub(s) for s in steps]
    has_sub = any(sub for _, sub in steps)
    sub_h = 0.55 if has_sub else 0.0
    box_h = h - sub_h
    gap = 1.1
    box_w = (w - gap * (n - 1)) / n
    xs = [x + i * (box_w + gap) for i in range(n)]
    midy = y + box_h / 2
    for i, (lab, sub) in enumerate(steps):
        last = i == n - 1
        fill = _tint(accent, 0.86) if last else SURFACE
        line = accent if last else BORDER
        col = accent if last else TEXT
        shape_box(slide, MSO_SHAPE.RECTANGLE, xs[i], y, box_w, box_h, text=[lab],
                  fill=fill, line=line, line_w=0.75, size=13, bold=True, color=col)
        if sub:
            textbox(slide, xs[i], y + box_h + 0.1, box_w, sub_h, [sub],
                    size=9, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    for i in range(n - 1):
        cx = xs[i] + box_w + gap / 2
        if connect == "arrow":
            connector(slide, xs[i] + box_w + 0.12, midy, xs[i + 1] - 0.12, midy,
                      color=accent, width=1.0, end_arrow=True)
        elif connect:
            textbox(slide, cx - 0.45, midy - 0.5, 0.9, 1.0, [connect], size=18,
                    bold=True, color=accent, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE)


# ---------------------------------------------------------------- 2. 縦フロー
def diagram_flow_v(slide, x, y, w, h, *, steps, accent=PRIMARY):
    """縦フロー。steps=[(label, sub?), ...]。下向き矢印で縦に連結。最後を強調。"""
    n = len(steps)
    steps = [_lab_sub(s) for s in steps]
    gap = 0.85
    box_h = (h - gap * (n - 1)) / n
    bw = w * 0.72
    bx = x + (w - bw) / 2
    cx = x + w / 2
    ys = [y + i * (box_h + gap) for i in range(n)]
    for i, (lab, sub) in enumerate(steps):
        last = i == n - 1
        fill = _tint(accent, 0.86) if last else SURFACE
        line = accent if last else BORDER
        col = accent if last else TEXT
        txt = [lab] + ([sub] if sub else [])
        shape_box(slide, MSO_SHAPE.RECTANGLE, bx, ys[i], bw, box_h, text=txt,
                  fill=fill, line=line, line_w=0.75, size=12, bold=True, color=col)
    for i in range(n - 1):
        connector(slide, cx, ys[i] + box_h + 0.08, cx, ys[i + 1] - 0.08,
                  color=accent, width=1.0, end_arrow=True)


# ---------------------------------------------------------------- 3. ピラミッド
def diagram_pyramid(slide, x, y, w, h, *, levels, accent=PRIMARY):
    """ピラミッド。levels は上→下の順 [(label, sub?), ...]。上ほど濃色・狭幅。"""
    n = len(levels)
    levels = [_lab_sub(v) for v in levels]
    gap = 0.16
    lh = (h - gap * (n - 1)) / n
    for i, (lab, sub) in enumerate(levels):
        frac = 0.42 + 0.58 * (i / (n - 1) if n > 1 else 1.0)
        lw = w * frac
        lx = x + (w - lw) / 2
        ly = y + i * (lh + gap)
        t = (i / (n - 1)) * 0.72 if n > 1 else 0.0  # 上（i=0）が最も濃い
        fill = _tint(accent, t)
        col = _on(fill)
        txt = [lab] + ([sub] if (sub and frac > 0.7) else [])
        shape_box(slide, MSO_SHAPE.RECTANGLE, lx, ly, lw, lh, text=txt,
                  fill=fill, line=WHITE, line_w=1.5, size=13, bold=True, color=col)


# ---------------------------------------------------------- 4. ビフォーアフター
def diagram_before_after(slide, x, y, w, h, *, before, after, accent=PRIMARY):
    """ビフォーアフター。before/after={"title":..., "items":[...]}。

    左=現状（無彩色・TEXT_MUTED）、右=改善（accent）。中央に→。赤は使わない。
    """
    arrow_w = 1.6
    pw = (w - arrow_w) / 2
    head_h = 0.95
    lx, rx = x, x + pw + arrow_w
    for px, data, is_after in ((lx, before, False), (rx, after, True)):
        head_fill = _tint(accent, 0.10) if is_after else NEUTRAL
        body_fill = _tint(accent, 0.90) if is_after else SURFACE
        shape_box(slide, MSO_SHAPE.RECTANGLE, px, y, pw, h,
                  fill=body_fill, line=(accent if is_after else BORDER), line_w=0.75)
        shape_box(slide, MSO_SHAPE.RECTANGLE, px, y, pw, head_h,
                  text=[data.get("title", "")], fill=head_fill, line=None,
                  size=13, bold=True, color=WHITE)
        items = data.get("items", [])
        textbox(slide, px + 0.35, y + head_h + 0.25, pw - 0.7, h - head_h - 0.5,
                [f"・{it}" for it in items], size=11,
                color=(TEXT if is_after else TEXT_MUTED), line_spacing=1.5)
    midy = y + h / 2
    connector(slide, lx + pw + 0.2, midy, rx - 0.2, midy,
              color=accent, width=2.2, end_arrow=True)


# ---------------------------------------------------------------- 5. マトリクス
def diagram_matrix(slide, x, y, w, h, *, x_labels, y_labels, quadrants,
                   accent=PRIMARY, highlight=None):
    """2×2 マトリクス。quadrants=[TL, TR, BL, BR]（各 (title, sub?)）。

    x_labels=(左, 右)、y_labels=(上, 下)。highlight に象限 index を渡すと強調。
    """
    ml, mb = 1.5, 0.85          # 左（縦軸ラベル）・下（横軸ラベル）の余白
    gx = x + ml
    gw = w - ml
    gh = h - mb
    cell_gap = 0.18
    cw = (gw - cell_gap) / 2
    chh = (gh - cell_gap) / 2
    order = [(0, 0), (1, 0), (0, 1), (1, 1)]  # TL,TR,BL,BR → (col,row)
    for idx, (col, row) in enumerate(order):
        lab, sub = _lab_sub(quadrants[idx])
        cx = gx + col * (cw + cell_gap)
        cy = y + row * (chh + cell_gap)
        hot = highlight == idx
        fill = _tint(accent, 0.88) if hot else SURFACE
        line = accent if hot else BORDER
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, cy, cw, chh,
                  fill=fill, line=line, line_w=0.75)
        textbox(slide, cx + 0.3, cy + 0.25, cw - 0.6, 0.8, [lab],
                size=12, bold=True, color=(accent if hot else TEXT))
        if sub:
            textbox(slide, cx + 0.3, cy + 1.05, cw - 0.6, chh - 1.3, [sub],
                    size=9.5, color=TEXT_MUTED, line_spacing=1.4)
    # 軸（左＝縦軸↑・下＝横軸→）
    connector(slide, gx - 0.35, y + gh, gx - 0.35, y, color=TEXT_MUTED,
              width=1.2, end_arrow=True)
    connector(slide, gx, y + gh + 0.35, gx + gw, y + gh + 0.35, color=TEXT_MUTED,
              width=1.2, end_arrow=True)
    # 軸ラベル
    textbox(slide, x, y - 0.05, ml - 0.5, chh, [y_labels[0]], size=9.5,
            bold=True, color=TEXT_MUTED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    textbox(slide, x, y + gh - chh + 0.05, ml - 0.5, chh, [y_labels[1]], size=9.5,
            bold=True, color=TEXT_MUTED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    textbox(slide, gx, y + gh + 0.42, cw, 0.5, [x_labels[0]], size=9.5,
            bold=True, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    textbox(slide, gx + cw + cell_gap, y + gh + 0.42, cw, 0.5, [x_labels[1]],
            size=9.5, bold=True, color=TEXT_MUTED, align=PP_ALIGN.CENTER)


# ---------------------------------------------------------------- 6. 階段/ステップ
def diagram_steps(slide, x, y, w, h, *, steps, accent=PRIMARY):
    """階段/ステップ。steps=[(label, sub?), ...]。右肩上がりのブロックで成長を表現。"""
    n = len(steps)
    steps = [_lab_sub(s) for s in steps]
    lab_h = 0.6                  # ブロック上のラベル帯
    gap = 0.25
    bw = (w - gap * (n - 1)) / n
    usable = h - lab_h
    for i, (lab, sub) in enumerate(steps):
        bh = usable * (i + 1) / n
        bx = x + i * (bw + gap)
        by = y + h - bh
        t = 0.68 - 0.60 * (i / (n - 1) if n > 1 else 0)  # 右（高い）ほど濃い
        fill = _tint(accent, t)
        col = _on(fill)
        shape_box(slide, MSO_SHAPE.RECTANGLE, bx, by, bw, bh, text=[str(i + 1)],
                  fill=fill, line=WHITE, line_w=1.2, size=15, bold=True, color=col)
        textbox(slide, bx, y + h - bh - lab_h, bw, lab_h, [lab], size=10.5,
                bold=True, color=TEXT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ---------------------------------------------------------------- 7. サイクル
def diagram_cycle(slide, x, y, w, h, *, items, center=None, accent=PRIMARY):
    """サイクル。items=[(label, sub?), ...] を円環に並べ、矢印で循環を表す。

    center を渡すと中央にラベルを置く。
    """
    n = len(items)
    items = [_lab_sub(it) for it in items]
    cx, cy = x + w / 2, y + h / 2
    node = min(3.6, w / (n * 0.9))
    node = max(2.6, node)
    nh = node * 0.62
    rx = w / 2 - node / 2
    ry = h / 2 - nh / 2
    pts = []
    for i in range(n):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        px = cx + rx * math.cos(ang)
        py = cy + ry * math.sin(ang)
        pts.append((px, py))
    # 矢印（節点の少し内側同士をつなぐ）
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 1
        off = node * 0.42
        connector(slide, x1 + dx / d * off, y1 + dy / d * off,
                  x2 - dx / d * off, y2 - dy / d * off,
                  color=_tint(accent, 0.35), width=1.1, end_arrow=True)
    # 節点（円ノード＝フラット・白地に主色）
    for (px, py), (lab, sub) in zip(pts, items):
        txt = [lab] + ([sub] if sub else [])
        shape_box(slide, MSO_SHAPE.OVAL, px - node / 2, py - nh / 2,
                  node, nh, text=txt, fill=WHITE, line=accent,
                  line_w=1.4, size=11, bold=True, color=accent)
    if center:
        textbox(slide, cx - rx * 0.55, cy - nh / 2, rx * 1.1, nh, [center],
                size=13, bold=True, color=TEXT_MUTED,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ---------------------------------------------------------------- 8. タイムライン
def diagram_timeline(slide, x, y, w, h, *, events, accent=PRIMARY):
    """タイムライン。events=[(when, desc), ...]。横線＋節点、ラベル上下交互。"""
    n = len(events)
    events = [_lab_sub(e) for e in events]
    axis_y = y + h / 2
    dot = 0.42
    lane_h = h / 2 - dot
    connector(slide, x, axis_y, x + w, axis_y, color=BORDER, width=2.0)
    xs = [x + w * (i + 0.5) / n for i in range(n)]
    for i, (when, desc) in enumerate(events):
        px = xs[i]
        up = i % 2 == 0
        shape_box(slide, MSO_SHAPE.OVAL, px - dot / 2, axis_y - dot / 2, dot, dot,
                  fill=accent, line=WHITE, line_w=0.75)
        if up:
            textbox(slide, px - w / (2 * n), y, w / n, lane_h - 0.05,
                    [when, desc] if desc else [when], size=10, bold=False,
                    color=TEXT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)
        else:
            textbox(slide, px - w / (2 * n), axis_y + dot / 2 + 0.05, w / n, lane_h,
                    [when, desc] if desc else [when], size=10, bold=False,
                    color=TEXT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
        # when を強調（別テキストで太字）
        # （※ when/desc を1ボックスに入れているので簡潔のため色分けのみ）


# ---------------------------------------------------------------- 9. ランキング
def diagram_ranking(slide, x, y, w, h, *, items, accent=PRIMARY, show_bar=True):
    """ランキング。items=[(label, value?), ...] を上位順に。値があればバー長で可視化。"""
    n = len(items)
    norm = [_lab_sub(it) for it in items]
    vals = []
    for _, v in norm:
        try:
            vals.append(float(v))
        except (TypeError, ValueError):
            vals.append(None)
    have_val = show_bar and any(v is not None for v in vals)
    vmax = max([v for v in vals if v is not None], default=1) or 1
    gap = 0.22
    rh = (h - gap * (n - 1)) / n
    badge = min(rh * 0.78, 1.15)
    label_w = w * (0.36 if have_val else 0.9)
    bar_x = x + badge + 0.4 + label_w + 0.3
    bar_max = x + w - bar_x - 1.3
    for i, (lab, v) in enumerate(norm):
        ry = y + i * (rh + gap)
        top = i == 0
        row_fill = _tint(accent, 0.90) if top else SURFACE
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, ry, w, rh,
                  fill=row_fill, line=(accent if top else BORDER), line_w=0.8)
        # 順位バッジ（フラット・首位のみ主色ベタ、他は白地に主色文字）
        shape_box(slide, MSO_SHAPE.RECTANGLE, x + 0.25,
                  ry + (rh - badge) / 2, badge, badge, text=[str(i + 1)],
                  fill=(accent if top else WHITE),
                  line=(None if top else BORDER), line_w=0.75,
                  size=14, bold=True, color=(WHITE if top else accent))
        textbox(slide, x + badge + 0.55, ry, label_w, rh, [lab], size=12,
                bold=top, color=TEXT, anchor=MSO_ANCHOR.MIDDLE)
        if have_val and vals[i] is not None:
            bl = bar_max * (vals[i] / vmax)
            shape_box(slide, MSO_SHAPE.RECTANGLE, bar_x, ry + rh * 0.28, bl, rh * 0.44,
                      fill=(accent if top else _tint(accent, 0.55)), line=None)
            txt = ("%g" % vals[i])
            textbox(slide, bar_x + bl + 0.15, ry, 1.2, rh, [txt], size=11,
                    bold=True, color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)


# ---------------------------------------------------------------- 10. 数式
def diagram_formula(slide, x, y, w, h, *, terms, ops=None, accent=PRIMARY):
    """数式。terms=[(label, sub?), ...] を演算子でつなぐ。

    ops=[記号,...]（長さ len(terms)-1。既定は全て "＋"）。"＝" の直後の項は
    結果とみなし accent で強調する。
    """
    n = len(terms)
    terms = [_lab_sub(t) for t in terms]
    if ops is None:
        ops = ["＋"] * (n - 1)
    op_w = 1.2
    box_h = min(h, 3.0)
    by = y + (h - box_h) / 2
    total_op = op_w * (n - 1)
    box_w = (w - total_op) / n
    x_cur = x
    is_result = [False] * n
    for i, op in enumerate(ops):
        if op.strip() in ("＝", "="):
            is_result[i + 1] = True
    for i, (lab, sub) in enumerate(terms):
        res = is_result[i]
        fill = _tint(accent, 0.86) if res else SURFACE
        line = accent if res else BORDER
        col = accent if res else TEXT
        txt = [lab] + ([sub] if sub else [])
        shape_box(slide, MSO_SHAPE.RECTANGLE, x_cur, by, box_w, box_h, text=txt,
                  fill=fill, line=line, line_w=0.75, size=13, bold=True, color=col)
        x_cur += box_w
        if i < n - 1:
            textbox(slide, x_cur, by, op_w, box_h, [ops[i]], size=20, bold=True,
                    color=accent, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            x_cur += op_w


# ---------------------------------------------------------------- 11. グループ図
def diagram_group(slide, x, y, w, h, *, groups, accent=PRIMARY):
    """グループ図。groups=[(title, [member, ...]), ...] を見出し付き箱で束ねる。"""
    n = len(groups)
    gap = 0.6
    gw = (w - gap * (n - 1)) / n
    head_h = 0.85
    for gi, (title, members) in enumerate(groups):
        gx = x + gi * (gw + gap)
        shape_box(slide, MSO_SHAPE.RECTANGLE, gx, y, gw, h,
                  fill=WHITE, line=BORDER, line_w=0.75)
        shape_box(slide, MSO_SHAPE.RECTANGLE, gx, y, gw, head_h, text=[title],
                  fill=SURFACE, line=BORDER, line_w=0.75, size=12, bold=True, color=accent)
        m = len(members)
        pad = 0.35
        inner_top = y + head_h + pad
        inner_h = h - head_h - pad * 2
        mgap = 0.25
        mh = (inner_h - mgap * (m - 1)) / m if m else inner_h
        for mi, mem in enumerate(members):
            my = inner_top + mi * (mh + mgap)
            shape_box(slide, MSO_SHAPE.RECTANGLE, gx + pad, my, gw - pad * 2, mh,
                      text=[mem], fill=WHITE, line=BORDER, line_w=0.8,
                      size=10.5, bold=False, color=TEXT)


# ================================================================
#  タスクB: 本編C（IT/ビジネス/語学）の専用ビルダー
# ================================================================

# ---------------------------------------------------------------- 表（C4/C14/C15）
def diagram_table(slide, x, y, w, h, *, headers, rows, accent=PRIMARY,
                  col_widths=None, zebra=False, align_first_left=True):
    """罫線グリッド表（『表・図解デザイン集』D1 準拠）。headers=[...]、rows=[[cell,...], ...]。

    比較表・語彙/用語リスト・書式リファレンス等を兼ねる。col_widths は各列の相対比（省略で均等）。
    ヘッダは濃い青みスレート（CHART_INK）地＋白文字、本文は白地＋細罫線、行の交互塗り(zebra)は既定オフ。
    """
    ncol = len(headers)
    nrow = len(rows)
    if col_widths and len(col_widths) == ncol:
        tot = sum(col_widths)
        cws = [w * cw / tot for cw in col_widths]
    else:
        cws = [w / ncol] * ncol
    xs = [x + sum(cws[:i]) for i in range(ncol)]
    head_h = h * 0.9 / (nrow + 1) if nrow else h
    head_h = min(max(head_h, 0.85), 1.3)
    rh = (h - head_h) / nrow if nrow else 0
    # ヘッダ行（集 D1 準拠＝濃い青みスレート地・白文字・細罫線）
    for c in range(ncol):
        a = PP_ALIGN.LEFT if (align_first_left and c == 0) else PP_ALIGN.CENTER
        shape_box(slide, MSO_SHAPE.RECTANGLE, xs[c], y, cws[c], head_h,
                  text=[str(headers[c])], fill=CHART_INK, line=BORDER, line_w=0.75,
                  size=11, bold=True, color=WHITE, align=a)
    # 本文セル（ゼブラ）
    for r, row in enumerate(rows):
        ry = y + head_h + r * rh
        rfill = SURFACE if (zebra and r % 2 == 1) else WHITE
        for c in range(ncol):
            cell = row[c] if c < len(row) else ""
            a = PP_ALIGN.LEFT if (align_first_left and c == 0) else PP_ALIGN.CENTER
            col = TEXT if c == 0 else TEXT_MUTED
            shape_box(slide, MSO_SHAPE.RECTANGLE, xs[c], ry, cws[c], rh,
                      text=[str(cell)], fill=rfill, line=BORDER, line_w=0.8,
                      size=10.5, bold=(c == 0), color=col, align=a)


# ---------------------------------------------------------------- コード解説（C10）
def diagram_code(slide, x, y, w, h, *, lines, title=None, highlight=None,
                 notes=None, accent=PRIMARY):
    """暗色コードブロック＋行番号＋行ハイライト＋注釈。

    lines=[コード行, ...]。highlight=強調する行番号(1始まり)の集合/リスト。
    notes={行番号: "注釈"} で右側に引き出し注釈を出す（任意）。title で見出し帯。
    """
    highlight = set(highlight or [])
    notes = notes or {}
    note_w = 6.2 if notes else 0.0
    code_w = w - note_w - (0.4 if notes else 0.0)
    top = y
    head_h = 0.7 if title else 0.0
    if title:
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, y, code_w, head_h, text=[title],
                  fill=accent, line=None, size=10.5, bold=True, color=WHITE,
                  align=PP_ALIGN.LEFT)
        top = y + head_h
    body_h = h - head_h
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, top, code_w, body_h,
              fill=CODE_BG, line=None)
    n = len(lines)
    lh = body_h / max(n, 1)
    gutter = 0.85
    for i, ln in enumerate(lines):
        ly = top + i * lh
        if (i + 1) in highlight:
            shape_box(slide, MSO_SHAPE.RECTANGLE, x, ly, code_w, lh,
                      fill=CODE_HI, line=None)
            shape_box(slide, MSO_SHAPE.RECTANGLE, x, ly, 0.09, lh,
                      fill=accent, line=None)
        textbox(slide, x + 0.15, ly, gutter, lh, [str(i + 1)], size=9.5,
                color=CODE_LN, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE,
                font=MONO)
        textbox(slide, x + gutter + 0.25, ly, code_w - gutter - 0.4, lh, [ln],
                size=10.5, color=CODE_TX, anchor=MSO_ANCHOR.MIDDLE, font=MONO)
        if notes and (i + 1) in notes:
            nx = x + code_w + 0.4
            connector(slide, x + code_w + 0.05, ly + lh / 2, nx - 0.05, ly + lh / 2,
                      color=_tint(accent, 0.4), width=1.2)
            textbox(slide, nx, ly, note_w, lh, [f"← {notes[i + 1]}"], size=9.5,
                    color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)


# ---------------------------------------------------------------- 会話・ダイアログ（C12）
def diagram_conversation(slide, x, y, w, h, *, turns, accent=PRIMARY):
    """会話の吹き出し。turns=[(speaker, text, side), ...]。side="left"/"right"。

    左＝相手（無彩色）、右＝自分/AI（accent淡色）。語学の会話・対話例に使う。
    """
    n = len(turns)
    gap = 0.35
    th = (h - gap * (n - 1)) / n
    bubble_w = w * 0.66
    badge = min(th * 0.5, 1.0)
    for i, t in enumerate(turns):
        speaker = t[0]
        text = t[1]
        side = t[2] if len(t) > 2 else ("right" if i % 2 else "left")
        ty = y + i * (th + gap)
        right = side == "right"
        if right:
            bx = x + w - bubble_w
            fill = _tint(accent, 0.86)
            line = accent
            col = TEXT
            badge_x = x + w - badge
            badge_fill = accent
        else:
            bx = x
            fill = SURFACE
            line = BORDER
            col = TEXT
            badge_x = x
            badge_fill = NEUTRAL
        # 話者バッジ（頭文字・角丸）
        shape_box(slide, MSO_SHAPE.OVAL, badge_x, ty, badge, badge,
                  text=[speaker[:1]], fill=badge_fill, line=None,
                  size=11, bold=True, color=WHITE)
        # 吹き出し（フラット・直角）
        inset = badge + 0.3
        bxx = bx + (0 if right else inset)
        bww = bubble_w - inset
        shape_box(slide, MSO_SHAPE.RECTANGLE, bxx, ty, bww, th,
                  text=[text], fill=fill, line=line, line_w=0.75, size=11,
                  color=col, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)


# ---------------------------------------------------------------- 画像＋解説（C8）
def diagram_image_explain(slide, x, y, w, h, *, image=None, heading, bullets,
                          side="left", accent=PRIMARY):
    """左右2カラム：片側に画像、反対側に見出し＋箇条書き。

    image=画像パス（Noneならプレースホルダ枠）。side は画像を置く側。
    """
    panel_w = w * 0.46
    gap = 0.7
    if side == "left":
        px, tx = x, x + panel_w + gap
    else:
        px, tx = x + w - panel_w, x
    tw = w - panel_w - gap
    if image:
        # 枠を敷いてから画像を内側にフィット（アスペクト保持は picture 側）
        shape_box(slide, MSO_SHAPE.RECTANGLE, px, y, panel_w, h,
                  fill=SURFACE, line=BORDER, line_w=0.75)
        picture(slide, image, px + 0.2, y + 0.2, w=panel_w - 0.4)
    else:
        shape_box(slide, MSO_SHAPE.RECTANGLE, px, y, panel_w, h,
                  fill=_tint(accent, 0.92), line=accent, line_w=0.75,
                  text=["IMAGE"], size=11, bold=True, color=accent)
    textbox(slide, tx, y + 0.1, tw, 1.0, [heading], size=15, bold=True, color=TEXT)
    textbox(slide, tx, y + 1.3, tw, h - 1.4, [f"・{b}" for b in bullets],
            size=12, color=TEXT_MUTED, line_spacing=1.55)


# ---------------------------------------------------------------- UI操作ガイド（C9）
def diagram_ui_steps(slide, x, y, w, h, *, pins, image=None, steps=None,
                     accent=PRIMARY):
    """スクショ＋番号ピン。pins=[(rel_x, rel_y), ...]（画像内の相対位置0..1）。

    image=スクショパス（Noneならプレースホルダ枠）。steps=[手順文, ...] を渡すと
    右側に番号付きの手順リストを併置する。
    """
    has_steps = bool(steps)
    img_w = w * (0.62 if has_steps else 1.0)
    if image:
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, y, img_w, h,
                  fill=WHITE, line=BORDER, line_w=0.75)
        picture(slide, image, x + 0.15, y + 0.15, w=img_w - 0.3)
    else:
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, y, img_w, h,
                  fill=SURFACE, line=BORDER, line_w=0.75,
                  text=["SCREENSHOT"], size=11, bold=True, color=TEXT_MUTED)
    pin = 0.7
    for i, (rx, ry) in enumerate(pins):
        cx = x + img_w * rx - pin / 2
        cy = y + h * ry - pin / 2
        shape_box(slide, MSO_SHAPE.OVAL, cx, cy, pin, pin, text=[str(i + 1)],
                  fill=accent, line=WHITE, line_w=2.0, size=12, bold=True,
                  color=WHITE)
    if has_steps:
        sx = x + img_w + 0.5
        sw = w - img_w - 0.5
        gap = 0.3
        sh = (h - gap * (len(steps) - 1)) / len(steps)
        badge = min(sh * 0.6, 0.8)
        for i, st in enumerate(steps):
            sy = y + i * (sh + gap)
            shape_box(slide, MSO_SHAPE.OVAL, sx, sy + (sh - badge) / 2, badge, badge,
                      text=[str(i + 1)], fill=accent, line=None, size=11,
                      bold=True, color=WHITE)
            textbox(slide, sx + badge + 0.25, sy, sw - badge - 0.25, sh, [st],
                    size=11, color=TEXT, anchor=MSO_ANCHOR.MIDDLE)


# ================================================================
#  タスクD: 事業紹介デッキ（Goodpatch / Canary / trifa）参考の型
#  refs から蒸留した「配置の原則」だけを実装。配色は accent（既定＝青）へ置換し、
#  他社固有の写真・地図・ロゴは持ち込まない（refs/README.md の線引き）。
# ================================================================

# ---------------------------------------------------------------- 同心円バブル（TAM/包含）
def diagram_nested_circles(slide, x, y, w, h, *, items, accent=PRIMARY):
    """入れ子の同心円で規模・包含関係を表す（trifa の TAM 図が参考）。

    items=[(label, value), ...] を **外側（大）→内側（小）** の順で渡す。
    最外が最も濃く、内側ほど白へ寄る。各リングの見える上帯にラベル＋値を置く。
    円は下端を揃えて入れ子にする（縦の重なりが読みやすい）。
    """
    n = len(items)
    # 最大円の直径は矩形の高さと幅の小さい方に収める
    dmax = min(h, w)
    cx = x + w / 2                      # 円の水平中心
    base = y + (h - dmax) / 2 + dmax    # 全円で共有する下端 y
    for i, it in enumerate(items):
        lab, sub = _lab_sub(it)
        d = dmax * (1 - i / n)          # i 番目の直径（外→内で縮む）
        cxx = cx - d / 2
        cyy = base - d
        t = 0.0 if n == 1 else i / (n - 1)   # 外=0（濃）→内=1（淡）
        fill = _tint(accent, 0.12 + 0.72 * t)
        shape_box(slide, MSO_SHAPE.OVAL, cxx, cyy, d, d, fill=fill, line=None)
        # ラベルはそのリングの見える上帯（次の円に隠れない領域）に置く
        band = (d - dmax * (1 - (i + 1) / n)) / 2 if i < n - 1 else d
        band = max(min(band, d * 0.5), 0.8)
        col = _on(fill)
        txt = [lab] + ([str(sub)] if sub != "" else [])
        textbox(slide, cxx, cyy + band * 0.12, d, band, txt,
                size=12, bold=True, color=col, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.TOP)


# ---------------------------------------------------------------- 番号付き見出しリスト
def diagram_numbered_list(slide, x, y, w, h, *, items, accent=PRIMARY,
                          start=1):
    """01/02/03… の大きな連番＋下線見出し＋説明（trifa「eSIM市場を取り巻く環境」参考）。

    items=[(title, body), ...]。番号は accent の大字、見出しは下線、本文は muted。
    概念の並列提示・要因列挙・チェックポイントに使う。
    """
    n = len(items)
    gap = 0.4
    rh = (h - gap * (n - 1)) / n
    num_w = 1.6
    for i, it in enumerate(items):
        title, body = _lab_sub(it)
        ry = y + i * (rh + gap)
        # 連番（大字・accent）
        textbox(slide, x, ry, num_w, rh, ["%02d" % (start + i)],
                size=22, bold=True, color=accent, anchor=MSO_ANCHOR.TOP)
        tx = x + num_w + 0.2
        tw = x + w - tx
        # 見出し
        textbox(slide, tx, ry, tw, 0.8, [title], size=14, bold=True, color=TEXT)
        # 見出し下線
        connector(slide, tx, ry + 0.82, x + w, ry + 0.82,
                  color=_tint(accent, 0.55), width=1.2)
        # 説明本文
        if body:
            textbox(slide, tx, ry + 1.0, tw, rh - 1.0, [body],
                    size=11, color=TEXT_MUTED, line_spacing=1.5,
                    anchor=MSO_ANCHOR.TOP)


# ---------------------------------------------------------------- 左見出し＋右カード群（非対称2分割）
def diagram_split_hero(slide, x, y, w, h, *, heading, lead=None, cards,
                       accent=PRIMARY, check=True):
    """左＝大見出し＋リード / 右＝チェック付きカードを縦積み（Canary の本文型が参考）。

    heading=左の見出し、lead=補足リード（任意）、cards=[(title, body), ...]。
    check=True で各カード左に accent のチェック丸を出す。
    """
    left_w = w * 0.42
    gap = 0.8
    rx = x + left_w + gap
    rw = w - left_w - gap
    # 左：見出し＋リード
    textbox(slide, x, y + 0.1, left_w, h * 0.5, [heading],
            size=20, bold=True, color=TEXT, line_spacing=1.2,
            anchor=MSO_ANCHOR.TOP)
    if lead:
        textbox(slide, x, y + h * 0.52, left_w, h * 0.46, [lead],
                size=11.5, color=TEXT_MUTED, line_spacing=1.55,
                anchor=MSO_ANCHOR.TOP)
    # 右：カード縦積み
    m = len(cards)
    cgap = 0.35
    ch = (h - cgap * (m - 1)) / m
    badge = min(ch * 0.42, 0.9)
    for i, c in enumerate(cards):
        title, body = _lab_sub(c)
        cy = y + i * (ch + cgap)
        shape_box(slide, MSO_SHAPE.RECTANGLE, rx, cy, rw, ch,
                  fill=WHITE, line=BORDER, line_w=0.75, shadow=False)
        pad = 0.4
        txx = rx + pad
        if check:
            shape_box(slide, MSO_SHAPE.OVAL, rx + pad, cy + pad, badge, badge,
                      text=["✓"], fill=accent, line=None, size=12, bold=True,
                      color=WHITE)
            txx = rx + pad + badge + 0.35
        txw = rx + rw - pad - txx
        textbox(slide, txx, cy + pad - 0.05, txw, 0.7, [title],
                size=13, bold=True, color=TEXT)
        if body:
            textbox(slide, txx, cy + pad + 0.7, txw, ch - pad - 0.7, [body],
                    size=10.5, color=TEXT_MUTED, line_spacing=1.5,
                    anchor=MSO_ANCHOR.TOP)


# ---------------------------------------------------------------- 左KPI＋右注釈（データ＋解説）
def diagram_stat_annot(slide, x, y, w, h, *, stat, notes, accent=PRIMARY,
                       split=0.42):
    """左＝大きな数値タイル / 右＝見出し付き注釈の束（Goodpatch のグラフ＋注釈が参考）。

    stat=(value, label) または [(value, label), ...]（複数なら縦積みのKPIタイル）。
    notes=[(heading, body), ...] を右カラムに積む。split=左カラムの幅比。
    """
    left_w = w * split
    gap = 0.7
    rx = x + left_w + gap
    rw = w - left_w - gap
    # 左：KPI タイル（1つでも複数でも可）
    tiles = stat if (stat and isinstance(stat[0], (list, tuple))) else [stat]
    m = len(tiles)
    tgap = 0.4
    th = (h - tgap * (m - 1)) / m
    for i, (val, lab) in enumerate(tiles):
        ty = y + i * (th + tgap)
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, ty, left_w, th,
                  fill=_tint(accent, 0.90), line=None)
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, ty, 0.12, th, fill=accent, line=None)
        textbox(slide, x + 0.5, ty + th * 0.14, left_w - 0.7, th * 0.55,
                [str(val)], size=30, bold=True, color=accent,
                anchor=MSO_ANCHOR.BOTTOM)
        textbox(slide, x + 0.5, ty + th * 0.70, left_w - 0.7, th * 0.28,
                [str(lab)], size=11, bold=True, color=TEXT_MUTED,
                anchor=MSO_ANCHOR.TOP)
    # 右：注釈の束
    n = len(notes)
    ngap = 0.35
    nh = (h - ngap * (n - 1)) / n
    for i, nt in enumerate(notes):
        head, body = _lab_sub(nt)
        ny = y + i * (nh + ngap)
        shape_box(slide, MSO_SHAPE.RECTANGLE, rx, ny + 0.05, 0.09, nh - 0.1,
                  fill=_tint(accent, 0.45), line=None)
        textbox(slide, rx + 0.3, ny, rw - 0.3, 0.7, [head],
                size=12.5, bold=True, color=TEXT)
        if body:
            textbox(slide, rx + 0.3, ny + 0.7, rw - 0.3, nh - 0.7, [body],
                    size=10.5, color=TEXT_MUTED, line_spacing=1.5,
                    anchor=MSO_ANCHOR.TOP)
