"""wireframes.py — 本編スライドの「デザイン標準」レイヤー（ワイヤー完全一致）。

ユーザー作成 wireframe_master_050.pptx（全50型）の各レイアウトを The Academy
ブランド（Primary Blue #0141D4 ／ ヒラギノ＋Graphik）で"構図まで一致"させる層。

── 仕上げ規定（AIっぽさの除去・厳守）──
  1. アイコン・装飾イラスト・写真は使わない。要点は文字と図形だけ
  2. 土台は白／黒／グレー。色はメイン1色（accent＝Primary Blue）
  3. グラデ禁止・単色塗り。角丸/影禁止（直角フラット。データ点の円のみ可）
  4. ベタ塗り見出し帯は使わない。区切りは細いヘアライン
  5. accent はワイヤー準拠の位置（示唆/結論の見出し・焦点データ）に置く

本レイヤーは本文ゾーン（y≥3.0）だけに描く。各関数は既定データを持ち、gallery が
引数なしで全型を描ける。共通レイアウト:
    リード（上部1行）＋主コンテンツ＋下部示唆（フル幅バー or 右パネル）
"""
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE

DASH = MSO_LINE_DASH_STYLE.DASH

from slides import (
    PRIMARY, TEXT, TEXT_MUTED, BORDER, SURFACE, WHITE,
    RGBColor, textbox, shape_box, connector,
)
from diagrams import _tint, _lab_sub

# ---------------------------------------------------------------- ゾーン定数（cm）
X0 = 1.07
ZW = 23.26
ZY = 3.15
ZH = 9.45
ZB = ZY + ZH                 # 本文ゾーン下端 ≒ 12.60
GUT = 0.75                   # 主／パネル間の溝
PANEL_W = 6.7

LEAD_Y = ZY
LEAD_H = 0.66
BAR_H = 0.98                 # 下部バー高さ
BAR_Y = ZB - BAR_H           # 下部バー上端 ≒ 11.62

GREY = RGBColor(0xD9, 0xD9, 0xDE)      # 非強調の図形塗り
GREY_L = RGBColor(0xEC, 0xEC, 0xEF)
INK = TEXT


def _content(bottom=True, top_extra=0.0):
    """主コンテンツ矩形 (x, y, w, h)。bottom=True で下部バー分を空ける。"""
    my = LEAD_Y + LEAD_H + 0.35 + top_extra
    mh = (BAR_Y - 0.3 - my) if bottom else (ZB - my)
    return X0, my, ZW, mh


# ================================================================ 共通ヘルパー
def lead(slide, text, *, x=X0, w=ZW):
    textbox(slide, x, LEAD_Y, w, LEAD_H, [text], size=12.5, color=TEXT_MUTED,
            anchor=MSO_ANCHOR.MIDDLE)


def rule(slide, x, y, w, *, color=BORDER, width=1.0):
    connector(slide, x, y, x + w, y, color=color, width=width)


def vrule(slide, x, y, h, *, color=BORDER, width=1.0):
    connector(slide, x, y, x, y + h, color=color, width=width)


def dot(slide, cx, cy, *, d=0.18, color=PRIMARY, hollow=False):
    if hollow:
        shape_box(slide, MSO_SHAPE.OVAL, cx - d / 2, cy - d / 2, d, d,
                  fill=WHITE, line=color, line_w=1.8)
    else:
        shape_box(slide, MSO_SHAPE.OVAL, cx - d / 2, cy - d / 2, d, d,
                  fill=color, line=None)


def label_rule(slide, x, y, w, label, *, accent=PRIMARY, size=13.5, color=None):
    """見出しラベル＋直下のヘアライン下線（ワイヤーの節見出し）。"""
    textbox(slide, x, y, w, 0.6, [label], size=size, bold=True,
            color=(color if color is not None else accent))
    rule(slide, x, y + 0.62, w, color=_tint(accent, 0.5) if color is None else BORDER)


def num_tab(slide, x, y, w, num, label, *, accent=PRIMARY, focus=False):
    """「NN｜ラベル」ミニ見出し（accent番号＋縦罫＋ラベル）＋下線。"""
    textbox(slide, x, y, 0.95, 0.6, [num], size=13, bold=True, color=accent)
    vrule(slide, x + 1.0, y + 0.06, 0.5)
    textbox(slide, x + 1.25, y, w - 1.25, 0.6, [label], size=12.5, bold=True,
            color=(accent if focus else INK))
    rule(slide, x, y + 0.64, w)


def bottom_bar(slide, head, body, *, accent=PRIMARY, boxed=True, label_w=5.4):
    """下部フル幅の示唆バー。左=accent見出し＋縦罫、右=本文。"""
    x, y, w, h = X0, BAR_Y, ZW, BAR_H
    if boxed:
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, fill=WHITE,
                  line=BORDER, line_w=1.0)
    else:
        rule(slide, x, y, w)
    pad = 0.5
    textbox(slide, x + pad, y, label_w, h, [head], size=13, bold=True,
            color=accent, anchor=MSO_ANCHOR.MIDDLE)
    vrule(slide, x + pad + label_w, y + 0.25, h - 0.5)
    textbox(slide, x + pad + label_w + 0.4, y, w - label_w - pad * 2 - 0.4, h,
            [body], size=11.5, color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)


def insight_panel(slide, x, y, w, h, *, blocks, accent=PRIMARY, pad=0.55):
    """右側の示唆パネル（淡い主色地＋主色見出し＋主色系下線）。"""
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    bh = (h - pad * 2) / len(blocks)
    for i, (head, bodytext) in enumerate(blocks):
        by = y + pad + i * bh
        textbox(slide, x + pad, by, w - pad * 2, 0.7, [head], size=13.5,
                bold=True, color=accent)
        rule(slide, x + pad, by + 0.76, w - pad * 2, color=_tint(accent, 0.5))
        if bodytext:
            textbox(slide, x + pad, by + 0.98, w - pad * 2, bh - 1.1, [bodytext],
                    size=11, color=TEXT_MUTED, line_spacing=1.5, anchor=MSO_ANCHOR.TOP)


def kpi_number(slide, x, y, w, h, value, label=None, *, accent=PRIMARY,
               size=40, align=PP_ALIGN.LEFT):
    """大きなKPI数値（accent）＋任意ラベル。"""
    textbox(slide, x, y, w, h, [str(value)], size=size, bold=True, color=accent,
            align=align, anchor=MSO_ANCHOR.MIDDLE)
    if label:
        textbox(slide, x, y + h, w, 0.6, [label], size=11, color=TEXT_MUTED,
                align=align)


# ---- 汎用チャート（手描き・単色・グリッド付き） ----------------------------
def vbars(slide, x, y, w, h, *, cats, vals, hi=None, ymax=None, accent=PRIMARY,
          grid=True, legend=None):
    """縦棒。hi の1本だけ accent、他はグレー。任意でY軸グリッド＋凡例。"""
    leg_h = 0.5 if legend else 0.0
    lab_h = 0.5
    plot = (x + 0.9, y, x + w, y + h - lab_h - leg_h)   # l,t,r,b
    pl, pt, pr, pb = plot
    vmax = ymax or (max(vals) * 1.1) or 1
    if grid:
        for g in range(5):
            gy = pb - (pb - pt) * g / 4
            rule(slide, pl, gy, pr - pl, color=GREY_L)
            textbox(slide, x, gy - 0.2, 0.75, 0.4, [str(int(vmax * g / 4))],
                    size=8, color=TEXT_MUTED, align=PP_ALIGN.RIGHT)
    n = len(vals)
    slot = (pr - pl) / n
    bw = min(slot * 0.5, 1.6)
    for i, v in enumerate(vals):
        bh = (pb - pt) * (v / vmax)
        bx = pl + i * slot + (slot - bw) / 2
        col = accent if (hi is not None and i == hi) else GREY
        shape_box(slide, MSO_SHAPE.RECTANGLE, bx, pb - bh, bw, bh, fill=col, line=None)
        textbox(slide, pl + i * slot, pb + 0.08, slot, 0.45, [str(cats[i])],
                size=9.5, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    rule(slide, pl, pb, pr - pl)
    if legend:
        ly = pb + lab_h + 0.05
        lx = pl
        for lab, on in legend:      # [(ラベル, is_accent)]
            shape_box(slide, MSO_SHAPE.RECTANGLE, lx, ly + 0.05, 0.3, 0.3,
                      fill=accent if on else GREY, line=None)
            textbox(slide, lx + 0.4, ly, 3.0, 0.4, [lab], size=9, color=TEXT_MUTED)
            lx += 0.4 + 0.25 * len(lab) + 0.8


def hbars(slide, x, y, w, h, *, rows, hi=0, accent=PRIMARY, show_pct=True):
    """横棒（内訳）。rows=[(ラベル, 値0..1 or 実数), ...]。hi だけ accent。"""
    n = len(rows)
    gap = 0.25
    rh = (h - gap * (n - 1)) / n
    lab_w = 2.0
    pct_w = 1.4 if show_pct else 0.0
    bar_max = w - lab_w - pct_w - 0.5
    vmax = max(v for _, v in rows) or 1
    for i, (lab, v) in enumerate(rows):
        ry = y + i * (rh + gap)
        textbox(slide, x, ry, lab_w, rh, [lab], size=10.5, color=TEXT_MUTED,
                anchor=MSO_ANCHOR.MIDDLE)
        bl = bar_max * (v / vmax)
        col = accent if i == hi else GREY
        shape_box(slide, MSO_SHAPE.RECTANGLE, x + lab_w, ry + rh * 0.2, bl, rh * 0.6,
                  fill=col, line=None)
        if show_pct:
            pct = f"{round(v * 100)}%" if vmax <= 1.0 else f"{v:g}"
            textbox(slide, x + w - pct_w, ry, pct_w, rh, [pct], size=10.5,
                    color=TEXT_MUTED, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def linechart(slide, x, y, w, h, *, cats, vals, ymax=None, accent=PRIMARY,
              grid=True):
    """折れ線（単色accent・マーカー・Y軸グリッド）。"""
    lab_h = 0.5
    pl, pt, pr, pb = x + 0.9, y, x + w, y + h - lab_h
    vmax = ymax or (max(vals) * 1.1) or 1
    if grid:
        for g in range(5):
            gy = pb - (pb - pt) * g / 4
            rule(slide, pl, gy, pr - pl, color=GREY_L)
            textbox(slide, x, gy - 0.2, 0.75, 0.4, [str(int(vmax * g / 4))],
                    size=8, color=TEXT_MUTED, align=PP_ALIGN.RIGHT)
    n = len(vals)
    pts = [(pl + (pr - pl) * i / (n - 1), pb - (pb - pt) * (v / vmax))
           for i, v in enumerate(vals)]
    for a, b in zip(pts, pts[1:]):
        connector(slide, a[0], a[1], b[0], b[1], color=accent, width=2.0)
    for px, py in pts:
        dot(slide, px, py, d=0.2, color=accent)
    rule(slide, pl, pb, pr - pl)
    for i, c in enumerate(cats):
        lx = min(max(pts[i][0] - 0.7, X0), X0 + ZW - 1.4)
        textbox(slide, lx, pb + 0.08, 1.4, 0.4, [str(c)], size=9,
                color=TEXT_MUTED, align=PP_ALIGN.CENTER)


def dual_line(slide, x, y, w, h, *, cats, plan, actual, accent=PRIMARY):
    """2系列折れ線。plan=破線グレー・actual=実線accent（計画対実績）。凡例付き。"""
    lab_h, leg_h = 0.5, 0.5
    pl, pt, pr, pb = x + 0.9, y, x + w, y + h - lab_h - leg_h
    vmax = 100
    for g in range(5):
        gy = pb - (pb - pt) * g / 4
        rule(slide, pl, gy, pr - pl, color=GREY_L)
        textbox(slide, x, gy - 0.2, 0.75, 0.4, [str(int(vmax * g / 4))], size=8,
                color=TEXT_MUTED, align=PP_ALIGN.RIGHT)
    n = len(cats)

    def series(vals, color, dash):
        pts = [(pl + (pr - pl) * i / (n - 1), pb - (pb - pt) * (v / vmax))
               for i, v in enumerate(vals)]
        for a, b in zip(pts, pts[1:]):
            connector(slide, a[0], a[1], b[0], b[1], color=color, width=1.8, dash=(DASH if dash else None))
        for px, py in pts:
            dot(slide, px, py, d=0.18, color=color)
    series(plan, GREY, "dash")
    series(actual, accent, None)
    rule(slide, pl, pb, pr - pl)
    for i, c in enumerate(cats):
        lx = min(max(pl + (pr - pl) * i / (n - 1) - 0.7, X0), X0 + ZW - 1.4)
        textbox(slide, lx, pb + 0.08, 1.4, 0.4, [str(c)], size=9, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    ly = pb + lab_h + 0.05
    for k, (lab, col, dash) in enumerate((("計画", GREY, True), ("実績", accent, False))):
        lx = pl + (pr - pl) / 2 - 2.2 + k * 2.6
        connector(slide, lx, ly + 0.2, lx + 0.7, ly + 0.2, color=col, width=1.8, dash=DASH if dash else None)
        textbox(slide, lx + 0.85, ly, 1.6, 0.4, [lab], size=9.5, color=TEXT_MUTED)


def data_table(slide, x, y, w, h, *, headers, rows, hi_col=None, hi_row=None,
               hi_cell=None, col_ratios=None, sub_headers=None, accent=PRIMARY):
    """罫線表。先頭列は左寄せ、hi_col/hi_row/hi_cell を accent＋淡色で強調。

    sub_headers=各列ヘッダの下段小ラベル（例 "30%"）。
    """
    ncol = len(headers)
    if col_ratios and len(col_ratios) == ncol:
        tot = sum(col_ratios)
        cws = [w * r / tot for r in col_ratios]
    else:
        cws = [w / ncol] * ncol
    xs = [x + sum(cws[:i]) for i in range(ncol)]
    head_h = min(max(h / (len(rows) + 1.4), 0.9), 1.25)
    rh = (h - head_h) / len(rows)
    for c in range(ncol):
        focus = c == hi_col
        shape_box(slide, MSO_SHAPE.RECTANGLE, xs[c], y, cws[c], head_h,
                  fill=_tint(accent, 0.9) if focus else SURFACE, line=BORDER, line_w=1.0)
        a = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
        if sub_headers and sub_headers[c]:
            textbox(slide, xs[c], y + 0.15, cws[c], 0.5, [str(headers[c])], size=11.5,
                    bold=True, color=(accent if focus else INK), align=a)
            textbox(slide, xs[c], y + head_h - 0.5, cws[c], 0.4, [str(sub_headers[c])],
                    size=9, color=TEXT_MUTED, align=a)
        else:
            textbox(slide, xs[c], y, cws[c], head_h, [str(headers[c])], size=11.5,
                    bold=True, color=(accent if focus else INK), align=a, anchor=MSO_ANCHOR.MIDDLE)
    for r, row in enumerate(rows):
        ry = y + head_h + r * rh
        rowhot = r == hi_row
        for c in range(ncol):
            cellhot = rowhot or c == hi_col or (hi_cell == (r, c))
            a = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
            emph = (c == hi_col and rowhot) or (hi_cell == (r, c))
            shape_box(slide, MSO_SHAPE.RECTANGLE, xs[c], ry, cws[c], rh,
                      text=[str(row[c])], fill=_tint(accent, 0.94) if cellhot else WHITE,
                      line=(_tint(accent, 0.4) if emph else BORDER), line_w=1.0,
                      size=(11 if c == 0 else 11.5), bold=(c == 0 or emph),
                      color=(accent if emph else (TEXT_MUTED if c == 0 else INK)), align=a)


# ================================================================ 50型
# ---- 01 データ＋示唆型 ------------------------------------------------------
def wf_data_insight(slide, *, lead_text="結論につながる本文やリード文を1〜2行で入力します。",
                    chart_title="グラフタイトル", cats=("項目A", "項目B", "項目C", "項目D", "項目E"),
                    vals=(40, 60, 80, 53, 30), hi=2,
                    insight=("示唆", "グラフから読み取れる重要な発見や、次に伝えたい結論を簡潔に入力します。"),
                    accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    textbox(slide, x, my, mw, 0.6, [chart_title], size=13, bold=True, color=INK)
    vbars(slide, x, my + 0.8, mw, mh - 0.8, cats=cats, vals=vals, hi=hi,
          ymax=100, accent=accent, legend=[("注目項目", True), ("その他", False)])
    insight_panel(slide, x + mw + GUT, my, PANEL_W, mh, blocks=[insight], accent=accent)


# ---- 02 左右比較型 ----------------------------------------------------------
def wf_compare_lr(slide, *, lead_text="比較する目的や観点を1〜2行で入力します。",
                  a=("比較対象A", ("特徴や説明を入力", "特徴や説明を入力", "特徴や説明を入力"), "65%"),
                  b=("比較対象B", ("特徴や説明を入力", "特徴や説明を入力", "特徴や説明を入力"), "85%"),
                  bottom=("結論・示唆", "両者の違いから導かれる重要な結論を入力します。"),
                  accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    colw = (w - 0.8) / 2
    vrule(slide, x + colw + 0.4, my + 0.2, mh - 0.4)
    for ci, (title, feats, num) in enumerate((a, b)):
        cx = x + ci * (colw + 0.8)
        label_rule(slide, cx, my, colw, title, accent=accent)
        textbox(slide, cx, my + 0.9, colw, 2.4, list(feats), size=11,
                color=TEXT_MUTED, line_spacing=1.5, anchor=MSO_ANCHOR.TOP)
        textbox(slide, cx, my + mh - 2.4, colw, 0.5, ["重要数値"], size=10.5,
                color=TEXT_MUTED)
        textbox(slide, cx, my + mh - 1.9, colw, 1.5, [num], size=40, bold=True,
                color=accent)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 03 結論＋3つの根拠型 ---------------------------------------------------
def wf_conclusion_reasons(slide, *,
                          lead_text="最も伝えたい主張と、その根拠を並べて示します。",
                          conclusion="最も伝えたい主張を簡潔に入力します。",
                          conclusion_sub="結論を補足する本文を2〜3行で入力します。",
                          reasons=(("根拠の見出し", "数値や事実を入力"),
                                   ("根拠の見出し", "数値や事実を入力"),
                                   ("根拠の見出し", "数値や事実を入力")),
                          accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w * 0.40
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, my, mw, mh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, x + 0.6, my + 0.5, mw - 1.2, 0.7, ["結論"], size=13.5, bold=True, color=accent)
    rule(slide, x + 0.6, my + 1.26, mw - 1.2, color=_tint(accent, 0.5))
    textbox(slide, x + 0.6, my + 1.7, mw - 1.2, mh * 0.4, [conclusion], size=17,
            bold=True, color=INK, line_spacing=1.25)
    textbox(slide, x + 0.6, my + mh - 2.0, mw - 1.2, 1.6, [conclusion_sub], size=11,
            color=TEXT_MUTED, line_spacing=1.5)
    rx = x + mw + GUT
    rw = X0 + w - rx
    n = len(reasons)
    rh = mh / n
    for i, (head, body) in enumerate(reasons):
        ry = my + i * rh
        if i > 0:
            rule(slide, rx, ry, rw)
        textbox(slide, rx, ry, 1.7, rh, ["%02d" % (i + 1)], size=26, bold=True,
                color=accent, anchor=MSO_ANCHOR.MIDDLE)
        vrule(slide, rx + 1.75, ry + rh * 0.3, rh * 0.4)
        textbox(slide, rx + 2.0, ry + rh * 0.22, rw - 2.0, 0.7, [head], size=13.5,
                bold=True, color=INK)
        textbox(slide, rx + 2.0, ry + rh * 0.22 + 0.72, rw - 2.0, 0.7, [body],
                size=11, color=TEXT_MUTED)


# ---- 04 課題・原因・解決型 --------------------------------------------------
def wf_problem_cause_solution(slide, *,
                              lead_text="現状の問題と、解決までの流れを説明します。",
                              cards=(("01", "課題", "起きている問題", "現象や困っていることを入力します。"),
                                     ("02", "原因", "問題の背景", "ボトルネックや原因を入力します。"),
                                     ("03", "解決策", "実施すること", "具体的な打ち手を入力します。")),
                              bottom=("重要な示唆", "解決策によって実現する変化を入力します。"),
                              accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    n = len(cards)
    gap = 0.5
    cw = (w - gap * (n - 1)) / n
    for i, (num, label, head, body) in enumerate(cards):
        cx = x + i * (cw + gap)
        focus = i == n - 1
        fill = _tint(accent, 0.92) if focus else WHITE
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, my, cw, mh, fill=fill,
                  line=(_tint(accent, 0.45) if focus else BORDER), line_w=1.0)
        pad = 0.5
        num_tab(slide, cx + pad, my + 0.5, cw - pad * 2, num, label, accent=accent, focus=focus)
        textbox(slide, cx + pad, my + 1.5, cw - pad * 2, 0.9, [head], size=15,
                bold=True, color=(accent if focus else INK))
        rule(slide, cx + pad, my + 2.5, cw - pad * 2)
        textbox(slide, cx + pad, my + 2.75, cw - pad * 2, mh - 3.0, [body],
                size=11, color=TEXT_MUTED, line_spacing=1.5, anchor=MSO_ANCHOR.TOP)
        if i < n - 1:
            connector(slide, cx + cw, my + mh / 2, cx + cw + gap, my + mh / 2,
                      color=BORDER, width=1.2)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 05 プロセス・手順型 ----------------------------------------------------
def wf_process_steps(slide, *, lead_text="全体の流れや手順を簡潔に説明します。",
                     steps=(("01", "工程名", "工程の説明を入力"), ("02", "工程名", "工程の説明を入力"),
                            ("03", "工程名", "工程の説明を入力"), ("04", "工程名", "工程の説明を入力")),
                     meta=(("期間", ""), ("担当", ""), ("成果物", "")),
                     goal=("最終到達点", "このプロセスで実現する状態を入力します。"),
                     accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    n = len(steps)
    cw = w / n
    axis_y = my + 2.1
    rule(slide, x + cw * 0.12, axis_y, w - cw * 0.24, color=GREY)
    for i, (num, name, body) in enumerate(steps):
        cx = x + i * cw
        focus = i == n - 1
        ac = accent if focus else INK
        textbox(slide, cx, my, cw, 0.5, ["STEP"], size=10, bold=True,
                color=accent, align=PP_ALIGN.CENTER)
        textbox(slide, cx, my + 0.45, cw, 1.1, [num], size=30, bold=True,
                color=ac, align=PP_ALIGN.CENTER)
        dot(slide, cx + cw / 2, axis_y, d=0.28, color=accent if focus else GREY)
        textbox(slide, cx, axis_y + 0.35, cw, 0.6, [name], size=13, bold=True,
                color=ac, align=PP_ALIGN.CENTER)
        textbox(slide, cx, axis_y + 1.0, cw, 1.0, [body + "\n" + body], size=10,
                color=TEXT_MUTED, align=PP_ALIGN.CENTER, line_spacing=1.4)
    # 下段：左=メタ表 / 右=最終到達点
    ty = my + mh - 2.2
    tw = w * 0.42
    rowh = 2.0 / len(meta)
    for i, (k, v) in enumerate(meta):
        yy = ty + i * rowh
        textbox(slide, x, yy, 1.6, rowh, [k], size=10.5, bold=True, color=INK,
                anchor=MSO_ANCHOR.MIDDLE)
        vrule(slide, x + 1.7, yy + 0.1, rowh - 0.2)
        rule(slide, x, yy + rowh, tw)
    rule(slide, x, ty, tw)
    gx = x + w * 0.5
    label_rule(slide, gx, ty + 0.3, w * 0.5, goal[0], accent=accent)
    textbox(slide, gx, ty + 1.1, w * 0.5, 0.8, [goal[1]], size=11.5, color=TEXT_MUTED)


# ---- 06 重要数値＋推移グラフ型 ---------------------------------------------
def wf_kpi_trend(slide, *, lead_text="重要な成果と、その変化を説明します。",
                 kpi_label="重要数値", value="87%", meaning="数値が表す意味を入力",
                 delta="前年差＋12pt", chart_title="推移グラフ",
                 cats=("1月", "2月", "3月", "4月", "5月", "6月"),
                 vals=(45, 54, 60, 70, 75, 88),
                 bottom=("数値から読み取れる示唆", "変化の背景や、次に注目すべきポイントを入力します。"),
                 accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    lw = w * 0.28
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, my, lw, mh, fill=WHITE, line=BORDER, line_w=1.0)
    pad = 0.5
    textbox(slide, x + pad, my + 0.35, lw - pad * 2, 0.6, [kpi_label], size=12.5, bold=True, color=INK)
    textbox(slide, x + pad, my + 1.1, lw - pad * 2, 1.4, [value], size=40, bold=True, color=accent)
    rule(slide, x + pad, my + mh * 0.5, lw - pad * 2, color=_tint(accent, 0.5))
    textbox(slide, x + pad, my + mh * 0.55, lw - pad * 2, 0.6, [meaning], size=11, color=TEXT_MUTED)
    rule(slide, x + pad, my + mh * 0.72, lw - pad * 2)
    textbox(slide, x + pad, my + mh * 0.78, lw - pad * 2, 0.6, [delta], size=11.5, color=INK)
    # 右：推移グラフ（枠内）
    rx = x + lw + GUT
    rw = X0 + w - rx
    shape_box(slide, MSO_SHAPE.RECTANGLE, rx, my, rw, mh, fill=WHITE, line=BORDER, line_w=1.0)
    textbox(slide, rx + 0.5, my + 0.3, rw - 3.5, 0.6, [chart_title], size=12.5, bold=True, color=INK)
    shape_box(slide, MSO_SHAPE.RECTANGLE, rx + rw - 2.4, my + 0.3, 1.9, 0.55,
              text=["注目地点"], fill=accent, line=None, size=10, bold=True, color=WHITE)
    linechart(slide, rx + 0.5, my + 1.1, rw - 1.0, mh - 1.6, cats=cats, vals=vals,
              ymax=100, accent=accent)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent, boxed=False)


# ---- 07 全体数値＋内訳型 ----------------------------------------------------
def wf_total_breakdown(slide, *, lead_text="全体の数値を、構成要素に分けて説明します。",
                       total=("全体", "1,250", "件", "数値の意味を入力",
                              "※ この数値の補足説明や前提条件を入力します。"),
                       rows=(("項目A", 0.40), ("項目B", 0.30), ("項目C", 0.20), ("項目D", 0.10)),
                       bottom=("最も重要な示唆", "割合が大きい項目や特徴を入力します。"),
                       accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    lw = w * 0.44
    vrule(slide, x + lw + 0.3, my + 0.2, mh - 0.4)
    label_rule(slide, x, my, lw - 0.6, total[0], accent=accent, color=INK)
    textbox(slide, x, my + mh * 0.28, lw * 0.72, 1.6, [total[1]], size=48, bold=True, color=accent)
    textbox(slide, x + lw * 0.7, my + mh * 0.4, 1.2, 1.0, [total[2]], size=18, bold=True,
            color=INK, anchor=MSO_ANCHOR.MIDDLE)
    textbox(slide, x, my + mh * 0.62, lw - 0.6, 0.6, [total[3]], size=12,
            color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    textbox(slide, x, my + mh - 0.7, lw - 0.6, 0.5, [total[4]], size=9.5, color=TEXT_MUTED)
    rx = x + lw + 0.7
    rw = X0 + w - rx
    label_rule(slide, rx, my, rw, "内訳", accent=accent, color=INK)
    hbars(slide, rx, my + 0.9, rw, mh - 1.1,
          rows=[(l, v) for l, v in rows], hi=0, accent=accent, show_pct=True)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 08 マトリクス型 --------------------------------------------------------
def wf_matrix(slide, *, lead_text="2つの評価軸で対象を整理します。",
              ax="評価軸A", ay="評価軸B",
              items=(("A", 0.72, 0.7), ("B", 0.3, 0.75), ("C", 0.32, 0.3),
                     ("D", 0.68, 0.28), ("E", 0.82, 0.6)),
              hi_quad=1, quad_labels=("象限2", "象限1", "象限3", "象限4"),
              insight=(("優先領域", "最も注目すべき象限と、その理由を入力します。"),
                       ("結論", "優先順位や次のアクションを入力します。")),
              accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    gh = mh - 0.6
    for q in range(4):
        qx = x + (mw / 2) * (q % 2)
        qy = my + (gh / 2) * (q // 2)
        fill = _tint(accent, 0.92) if q == hi_quad else WHITE
        shape_box(slide, MSO_SHAPE.RECTANGLE, qx, qy, mw / 2, gh / 2, fill=fill,
                  line=BORDER, line_w=1.0)
        textbox(slide, qx + 0.35, qy + 0.3, mw / 2 - 0.7, 0.6, [quad_labels[q]],
                size=12, bold=True, color=(accent if q == hi_quad else INK))
    textbox(slide, x + 0.2, my + 0.1, 4, 0.4, [f"{ay}：高い"], size=9, color=TEXT_MUTED)
    textbox(slide, x + 0.2, my + gh - 0.5, 4, 0.4, [f"{ay}：低い"], size=9, color=TEXT_MUTED)
    textbox(slide, x + 0.5, my + gh + 0.08, 4, 0.4, [f"{ax}：低い"], size=9, color=TEXT_MUTED)
    textbox(slide, x + mw - 4.2, my + gh + 0.08, 4, 0.4, [f"{ax}：高い"], size=9,
            color=TEXT_MUTED, align=PP_ALIGN.RIGHT)
    for lab, rx, ry in items:
        d = 0.72
        cx = x + mw * rx - d / 2
        cy = my + gh * (1 - ry) - d / 2
        shape_box(slide, MSO_SHAPE.OVAL, cx, cy, d, d, text=[lab], fill=GREY,
                  line=None, size=10.5, bold=True, color=INK)
    insight_panel(slide, x + mw + GUT, my, PANEL_W, mh, blocks=insight, accent=accent)


# ---- 09 時系列・変化型 ------------------------------------------------------
def wf_timeline_change(slide, *, lead_text="過去から将来までの変化を説明します。",
                       cols=(("過去", "20XX", "当時の状態", "重要な出来事を入力"),
                             ("現在", "20XX", "現在の状態", "重要な出来事を入力"),
                             ("次の段階", "20XX", "次に実施すること", "重要な予定を入力"),
                             ("将来", "20XX", "目指す状態", "実現したい姿を入力")),
                       bottom=("変化の方向性", "全体を通じて起きる変化を入力します。"),
                       accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    n = len(cols)
    cw = w / n
    axis_y = my + 1.0
    rule(slide, x + cw * 0.5, axis_y, w - cw, color=GREY)
    for i, (head, year, state, body) in enumerate(cols):
        cx = x + i * cw
        focus = i == n - 1
        ac = accent if focus else INK
        textbox(slide, cx, my, cw, 0.6, [head], size=13, bold=True, color=ac,
                align=PP_ALIGN.CENTER)
        dot(slide, cx + cw / 2, axis_y, d=0.34, color=accent if focus else GREY,
            hollow=not focus)
        textbox(slide, cx, axis_y + 0.4, cw, 0.5, [year], size=11,
                color=(accent if focus else TEXT_MUTED), align=PP_ALIGN.CENTER)
        textbox(slide, cx, axis_y + 1.0, cw, 0.6, [state], size=12.5, bold=True,
                color=ac, align=PP_ALIGN.CENTER)
        textbox(slide, cx, axis_y + 1.7, cw, 1.0, [body + "\n" + body], size=10,
                color=TEXT_MUTED, align=PP_ALIGN.CENTER, line_spacing=1.4)
    # 下部＝中央寄せ（黒見出し・箱なし）
    rule(slide, x, BAR_Y, w)
    textbox(slide, x, BAR_Y + 0.05, w, 0.6, [bottom[0]], size=15, bold=True,
            color=INK, align=PP_ALIGN.CENTER)
    textbox(slide, x, BAR_Y + 0.62, w, 0.4, [bottom[1]], size=11, color=TEXT_MUTED,
            align=PP_ALIGN.CENTER)


# ---- 10 全体像・構造分解型 --------------------------------------------------
def wf_structure_decompose(slide, *, lead_text="複雑な仕組みを、構成要素に分けて説明します。",
                           center=("全体を表す概念", "仕組みやサービスの中心を入力"),
                           parts=(("構成要素1", "要素の説明を入力"), ("構成要素2", "要素の説明を入力"),
                                  ("構成要素3", "要素の説明を入力"), ("構成要素4", "要素の説明を入力")),
                           base=("共通する基盤", "全体を支える仕組みや前提を入力します。"),
                           insight=("示唆", "構造全体から分かることを入力"),
                           accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    lw = w * 0.33
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, my, lw, mh, fill=WHITE, line=BORDER, line_w=1.0)
    textbox(slide, x + 0.3, my + mh * 0.36, lw - 0.6, 0.8, [center[0]], size=15,
            bold=True, color=INK, align=PP_ALIGN.CENTER)
    textbox(slide, x + 0.3, my + mh * 0.5, lw - 0.6, 0.6, [center[1]], size=10.5,
            color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    rx = x + w * 0.46
    rw = X0 + w - rx
    n = len(parts)
    gap = 0.25
    ph = (mh - gap * (n - 1)) / n
    trunk = x + lw + (rx - (x + lw)) * 0.45
    connector(slide, x + lw, my + mh / 2, trunk, my + mh / 2, color=BORDER, width=1.2)
    vrule(slide, trunk, my + ph / 2, mh - ph)
    for i, (head, body) in enumerate(parts):
        py = my + i * (ph + gap)
        shape_box(slide, MSO_SHAPE.RECTANGLE, rx, py, rw, ph, fill=WHITE, line=BORDER, line_w=1.0)
        connector(slide, trunk, py + ph / 2, rx, py + ph / 2, color=BORDER, width=1.2)
        textbox(slide, rx + 0.4, py, rw * 0.4, ph, [head], size=12.5, bold=True,
                color=INK, anchor=MSO_ANCHOR.MIDDLE)
        textbox(slide, rx + rw * 0.42, py, rw * 0.55, ph, [body], size=10.5,
                color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)
    # 下部＝左バー(共通基盤)＋右小パネル(示唆)
    bx_w = w * 0.62
    px = x + bx_w + GUT
    pw = X0 + w - px
    py = BAR_Y - 0.2
    ph = BAR_H + 0.2
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, py, bx_w, ph, fill=SURFACE, line=BORDER, line_w=1.0)
    textbox(slide, x + 0.5, py, 4.0, ph, [base[0]], size=12.5, bold=True,
            color=INK, anchor=MSO_ANCHOR.MIDDLE)
    vrule(slide, x + 4.6, py + 0.25, ph - 0.5)
    textbox(slide, x + 4.9, py, bx_w - 5.2, ph, [base[1]], size=11,
            color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)
    shape_box(slide, MSO_SHAPE.RECTANGLE, px, py, pw, ph, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, px + 0.4, py + 0.12, pw - 0.8, 0.45, [insight[0]], size=12,
            bold=True, color=accent)
    rule(slide, px + 0.4, py + 0.58, pw - 0.8, color=_tint(accent, 0.5))
    textbox(slide, px + 0.4, py + 0.64, pw - 0.8, 0.5, [insight[1]], size=9.5, color=TEXT_MUTED)


# ---- 11 事例・成果型 --------------------------------------------------------
def wf_case_result(slide, *, lead_text=None,
                   overview=("プロジェクト概要", "クライアント／プロジェクト： プロジェクト名を入力します",
                             "対象： 対象を入力します", "期間： 期間を入力します"),
                   left=(("導入前の課題", "解決したかった問題を入力します。"),
                         ("実施したこと", "具体的な施策や取り組みを入力します。")),
                   result=("成果", "42%", "削減"),
                   bottom=("成功要因・示唆", "成果につながったポイントや、他でも活用できる知見を入力します。"),
                   accent=PRIMARY):
    x, my0, w, _ = _content(bottom=True)
    my = LEAD_Y                       # 概要行を上部に置くのでリード枠は使わない
    # 概要行（ラベル＋インライン3項目＋下線）
    textbox(slide, x, my, 6, 0.6, [overview[0]], size=13, bold=True, color=accent)
    textbox(slide, x, my + 0.6, 10, 0.5, [overview[1]], size=10.5, color=TEXT_MUTED)
    textbox(slide, x + w * 0.42, my + 0.6, w * 0.28, 0.5, [overview[2]], size=10.5, color=TEXT_MUTED)
    textbox(slide, x + w * 0.72, my + 0.6, w * 0.28, 0.5, [overview[3]], size=10.5, color=TEXT_MUTED)
    rule(slide, x, my + 1.15, w)
    cy = my + 1.4
    ch = BAR_Y - 0.3 - cy
    lw = w * 0.30
    for i, (head, body) in enumerate(left):
        by = cy + i * (ch / 2 + 0.0) + i * 0.0
        bh = (ch - 0.4) / 2
        yy = cy + i * (bh + 0.4)
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, yy, lw, bh, fill=WHITE, line=BORDER, line_w=1.0)
        label_rule(slide, x + 0.4, yy + 0.35, lw - 0.8, head, accent=accent)
        textbox(slide, x + 0.4, yy + 1.2, lw - 0.8, bh - 1.4, [body], size=11,
                color=TEXT_MUTED, line_spacing=1.5, anchor=MSO_ANCHOR.TOP)
    # 右：成果
    rx = x + lw + GUT
    rw = X0 + w - rx
    label_rule(slide, rx, cy, 3.2, result[0], accent=accent)
    textbox(slide, rx + 1.5, cy + 0.7, 4.0, 1.4, [result[1]], size=44, bold=True, color=accent)
    textbox(slide, rx + 5.8, cy + 1.1, 3.0, 1.0, [result[2]], size=20, bold=True,
            color=INK, anchor=MSO_ANCHOR.MIDDLE)
    shape_box(slide, MSO_SHAPE.RECTANGLE, rx, cy + 2.3, rw, ch - 2.3, fill=WHITE, line=BORDER, line_w=1.0)
    hbars(slide, rx + 0.6, cy + 2.8, rw - 1.2, ch - 3.2,
          rows=[("Before", 100), ("After", 58)], hi=1, accent=accent, show_pct=False)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 12 問い＋回答型 --------------------------------------------------------
def wf_question_answer(slide, *, lead_text=None,
                       q=("読み手が抱く疑問を入力します。", "この問いが生まれる背景を入力します。"),
                       a=("回答・結論を入力", "回答を補足する説明を2〜3行で入力します。"),
                       data_title="回答を支えるデータ", data=(37, 68, 90), data_cats=("項目A", "項目B", "項目C"),
                       bottom=("次に伝えたい示唆", "この回答を踏まえて考えるべきことを入力します。"),
                       accent=PRIMARY):
    x, my, w, mh = _content(bottom=True, top_extra=-0.7)
    colw = (w - GUT) / 2
    # 左＝Q（白箱）
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, my, colw, mh, fill=WHITE, line=BORDER, line_w=1.0)
    textbox(slide, x + 0.6, my + 0.4, 2, 1.2, ["Q"], size=34, bold=True, color=INK)
    textbox(slide, x + 0.6, my + 1.7, colw - 1.2, 0.9, [q[0]], size=15, bold=True, color=INK)
    textbox(slide, x + 0.6, my + 2.6, colw - 1.2, 0.6, [q[1]], size=11, color=TEXT_MUTED)
    # 右＝A（淡主色箱）
    ax = x + colw + GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, ax, my, colw, mh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, ax + 0.6, my + 0.4, 2, 1.2, ["A"], size=34, bold=True, color=accent)
    textbox(slide, ax + 0.6, my + 1.7, colw - 1.2, 0.7, [a[0]], size=14, bold=True, color=accent)
    textbox(slide, ax + 0.6, my + 2.4, colw - 1.2, 0.5, [a[1]], size=11, color=TEXT_MUTED)
    rule(slide, ax + 0.6, my + 3.0, colw - 1.2, color=_tint(accent, 0.5))
    textbox(slide, ax + 0.6, my + 3.15, colw - 1.2, 0.5, [data_title], size=11.5, bold=True, color=accent)
    vbars(slide, ax + 0.6, my + 3.7, colw - 1.2, mh - 4.0, cats=data_cats, vals=list(data),
          hi=len(data) - 1, ymax=100, accent=accent, grid=True)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 13 1メッセージ型 -------------------------------------------------------
def wf_one_message(slide, *, message="最も伝えたいメッセージを、\n一文で大きく入力します。",
                   sub="メッセージを補足する説明を1〜2行で入力します。",
                   note="根拠・補足情報を入力", accent=PRIMARY):
    x, my, w, mh = _content(bottom=False)
    lines = message.split("\n")
    textbox(slide, x + 1.5, my + mh * 0.20, w - 3, 3.1, lines, size=28, bold=True,
            color=INK, line_spacing=1.3, anchor=MSO_ANCHOR.TOP)
    textbox(slide, x + 1.5, my + mh * 0.66, w - 3, 0.8, [sub], size=13, color=TEXT_MUTED)
    rule(slide, x, ZB - 0.55, w)
    textbox(slide, x, ZB - 0.5, w, 0.45, [note], size=10.5, color=TEXT_MUTED)


# ---- 14 重要数値単独型 ------------------------------------------------------
def wf_kpi_single(slide, *, lead_text="最も重要な数値だけを強く印象づけます。",
                  value="87%", value_label="数値が示す内容を入力",
                  meaning=("数値の意味", "この数値から分かることを簡潔に入力します。"),
                  subs=(("前年差", "+12pt"), ("目標差", "-3pt")),
                  insight=("示唆", "この数値を踏まえた判断や次の行動を入力します。"),
                  accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    textbox(slide, x, my + 0.1, mw, mh * 0.42, [str(value)], size=72, bold=True,
            color=accent, anchor=MSO_ANCHOR.BOTTOM)
    textbox(slide, x, my + mh * 0.46, mw, 0.7, [value_label], size=13, color=TEXT_MUTED)
    rule(slide, x, my + mh * 0.62, mw * 0.5)
    textbox(slide, x, my + mh * 0.67, mw, 0.6, [meaning[0]], size=12.5, bold=True, color=INK)
    textbox(slide, x, my + mh * 0.67 + 0.6, mw, 1.0, [meaning[1]], size=11,
            color=TEXT_MUTED, line_spacing=1.5)
    sw = mw / len(subs)
    for i, (sl, sv) in enumerate(subs):
        sx = x + i * sw
        textbox(slide, sx, my + mh - 1.3, sw, 0.5, [sl], size=10, color=TEXT_MUTED)
        textbox(slide, sx, my + mh - 0.85, sw, 0.85, [sv], size=18, bold=True, color=INK)
    insight_panel(slide, x + mw + GUT, my, PANEL_W, mh, blocks=[insight], accent=accent)


# ---- 15 Before／After型 ----------------------------------------------------
def wf_before_after(slide, *, lead_text="変化の前後を並べて、改善効果を伝えます。",
                    before=("Before", "変更前の状態", ("課題や特徴を入力",) * 3, "120分"),
                    after=("After", "変更後の状態", ("改善した内容を入力",) * 3, "15分"),
                    bottom=("変化・効果", "前後の違いから分かる成果を入力します。"),
                    accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    colw = (w - 1.0) / 2
    for side, (tag, sub, rows, big), focus in ((0, before, False), (1, after, True)):
        cx = x + side * (colw + 1.0)
        fill = _tint(accent, 0.92) if focus else WHITE
        line = _tint(accent, 0.45) if focus else BORDER
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, my, colw, mh, fill=fill, line=line, line_w=1.0)
        pad = 0.55
        textbox(slide, cx + pad, my + 0.35, colw - pad * 2, 0.7, [tag], size=16,
                bold=True, color=(accent if focus else INK))
        textbox(slide, cx + pad, my + 1.05, colw - pad * 2, 0.5, [sub], size=11.5,
                bold=True, color=INK)
        rule(slide, cx + pad, my + 1.6, colw - pad * 2, color=line)
        n = len(rows)
        ry0 = my + 1.85
        rh = 0.75
        for i, r in enumerate(rows):
            shape_box(slide, MSO_SHAPE.RECTANGLE, cx + pad, ry0 + i * (rh + 0.18),
                      colw - pad * 2, rh, text=[r], fill=GREY_L, line=None,
                      size=10.5, color=INK, align=PP_ALIGN.LEFT)
        rule(slide, cx + pad, my + mh - 1.3, colw - pad * 2, color=line)
        textbox(slide, cx + pad, my + mh - 1.15, colw - pad * 2, 1.0, [big], size=26,
                bold=True, color=(accent if focus else INK), align=PP_ALIGN.CENTER)
    connector(slide, x + colw + 0.35, my + mh / 2, x + colw + 0.65, my + mh / 2,
              color=GREY, width=1.4)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 16 メリット・デメリット型 ---------------------------------------------
def wf_pros_cons(slide, *, lead_text="良い点と注意点を並べ、判断材料を整理します。",
                 pros=("メリット", (("見出しを入力", "メリットの説明を入力"),) * 4),
                 cons=("デメリット", (("見出しを入力", "注意点の説明を入力"),) * 4),
                 bottom=("判断のポイント", "どの条件なら採用すべきかを入力します。"),
                 accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    colw = (w - 0.8) / 2
    vrule(slide, x + colw + 0.4, my + 0.2, mh - 0.4)
    for side, (title, rows), focus in ((0, pros, True), (1, cons, False)):
        cx = x + side * (colw + 0.8)
        textbox(slide, cx, my, colw, 0.7, [title], size=15, bold=True,
                color=(accent if focus else INK))
        n = len(rows)
        rh = (mh - 0.9) / n
        for i, (head, desc) in enumerate(rows):
            ry = my + 0.9 + i * rh
            if i > 0:
                rule(slide, cx, ry, colw)
            textbox(slide, cx, ry, 1.1, rh, ["%02d" % (i + 1)], size=15, bold=True,
                    color=(accent if focus else INK), anchor=MSO_ANCHOR.MIDDLE)
            vrule(slide, cx + 1.15, ry + rh * 0.25, rh * 0.5)
            textbox(slide, cx + 1.4, ry + rh * 0.18, colw - 1.4, 0.55, [head],
                    size=12.5, bold=True, color=INK)
            textbox(slide, cx + 1.4, ry + rh * 0.18 + 0.55, colw - 1.4, 0.5, [desc],
                    size=10, color=TEXT_MUTED)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 17 選択肢比較表型 ------------------------------------------------------
def wf_options_table(slide, *, lead_text="複数の選択肢を、同じ評価軸で比較します。",
                     headers=("評価項目", "選択肢A", "選択肢B", "選択肢C"),
                     rows=(("費用", "△", "○", "—"), ("導入期間", "△", "○", "—"),
                           ("効果", "○", "○", "△"), ("使いやすさ", "△", "○", "—"),
                           ("拡張性", "—", "○", "△")),
                     hi_col=2, reco=("おすすめの選択肢", "比較結果と推奨理由を簡潔に入力します。"),
                     accent=PRIMARY):
    lead(slide, lead_text, )
    x, my, w, mh = _content(bottom=True, top_extra=0.3)
    ncol = len(headers)
    c0 = w * 0.22
    cw = (w - c0) / (ncol - 1)
    xs = [x] + [x + c0 + i * cw for i in range(ncol - 1)]
    widths = [c0] + [cw] * (ncol - 1)
    head_h = 0.95
    rh = (mh - head_h) / len(rows)
    # 推奨ラベル（強調列の上）
    hx = xs[hi_col]
    textbox(slide, hx, my - 0.5, widths[hi_col], 0.45, ["推奨"], size=11, bold=True,
            color=accent, align=PP_ALIGN.CENTER)
    # ヘッダ
    for c in range(ncol):
        focus = c == hi_col
        fill = _tint(accent, 0.9) if focus else SURFACE
        shape_box(slide, MSO_SHAPE.RECTANGLE, xs[c], my, widths[c], head_h,
                  text=[headers[c]], fill=fill, line=BORDER, line_w=1.0,
                  size=11.5, bold=True, color=(accent if focus else INK),
                  align=PP_ALIGN.CENTER)
    # 本文セル
    for r, row in enumerate(rows):
        ry = my + head_h + r * rh
        for c in range(ncol):
            focus = c == hi_col
            fill = _tint(accent, 0.95) if focus else WHITE
            a = PP_ALIGN.CENTER if c > 0 else PP_ALIGN.CENTER
            col = INK if c == 0 else INK
            shape_box(slide, MSO_SHAPE.RECTANGLE, xs[c], ry, widths[c], rh,
                      text=[str(row[c])], fill=fill, line=BORDER, line_w=1.0,
                      size=(11.5 if c == 0 else 12), bold=(c == 0), color=col, align=a)
    bottom_bar(slide, reco[0], reco[1], accent=accent)


# ---- 18 ランキング型 --------------------------------------------------------
def wf_ranking(slide, *, lead_text="複数の項目を順位順に整理して示します。",
               items=(("項目A", 95, "最も高い項目"), ("項目B", 82), ("項目C", 68),
                      ("項目D", 54), ("項目E", 41)),
               insight=("示唆", "上位項目の特徴や、順位から読み取れることを入力します。"),
               accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    n = len(items)
    rh = mh / n
    vmax = max(it[1] for it in items) or 1
    bar_x = x + 3.6
    val_x = x + mw - 3.4
    bar_max = val_x - bar_x - 0.4
    for i, it in enumerate(items):
        name, val = it[0], it[1]
        note = it[2] if len(it) > 2 else ""
        ry = my + i * rh
        if i > 0:
            rule(slide, x, ry, mw)
        top = i == 0
        textbox(slide, x, ry, 1.3, rh, [str(i + 1)], size=26, bold=True,
                color=(accent if top else INK), anchor=MSO_ANCHOR.MIDDLE)
        vrule(slide, x + 1.35, ry + rh * 0.28, rh * 0.44)
        textbox(slide, x + 1.6, ry, 2.0, rh, [name], size=12.5, bold=True,
                color=(accent if top else INK), anchor=MSO_ANCHOR.MIDDLE)
        bl = bar_max * (val / vmax)
        shape_box(slide, MSO_SHAPE.RECTANGLE, bar_x, ry + rh * 0.36, bl, rh * 0.28,
                  fill=(accent if top else GREY), line=None)
        textbox(slide, val_x, ry, 1.4, rh, [str(val)], size=14, bold=True,
                color=INK, anchor=MSO_ANCHOR.MIDDLE)
        if note:
            textbox(slide, val_x + 1.5, ry, 2.2, rh, [note], size=9.5,
                    color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)
    insight_panel(slide, x + mw + GUT, my, PANEL_W, mh, blocks=[insight], accent=accent)


# ---- 19 ファネル型 ----------------------------------------------------------
def wf_funnel(slide, *, lead_text="段階ごとの人数や件数の減少を可視化します。",
              stages=(("認知", 10000), ("興味", 6500), ("検討", 3200),
                      ("申込", 1200), ("成約", 600)),
              insight=("ボトルネック", "最も離脱が大きい段階と、改善すべきポイントを入力します。"),
              accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    rate_w = 2.0
    fun_w = mw - rate_w
    n = len(stages)
    gap = 0.22
    rh = (mh - gap * (n - 1)) / n
    vals = [v for _, v in stages]
    vmax = vals[0] or 1
    last = n - 1
    textbox(slide, x + fun_w + 0.2, my - 0.05, rate_w, 0.45, ["通過率"], size=10,
            bold=True, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    for i, (name, v) in enumerate(stages):
        frac = 0.42 + 0.58 * (v / vmax)
        bw = fun_w * frac
        bx = x + (fun_w - bw) / 2
        by = my + i * (rh + gap)
        col = accent if i == last else GREY_L
        tcol = WHITE if i == last else INK
        shape_box(slide, MSO_SHAPE.TRAPEZOID, bx, by, bw, rh, text=[f"{name}  {v:,}"],
                  fill=col, line=None, size=12, bold=True, color=tcol, anchor=MSO_ANCHOR.MIDDLE)
        if i < last:
            pct = round(vals[i + 1] / v * 100)
            textbox(slide, x + fun_w + 0.2, by + rh * 0.55, rate_w, rh, [f"{pct}%"],
                    size=13, bold=True, color=INK, align=PP_ALIGN.CENTER)
    insight_panel(slide, x + mw + GUT, my, PANEL_W, mh, blocks=[insight], accent=accent)


# ---- 20 ピラミッド・階層型 --------------------------------------------------
def wf_pyramid_levels(slide, *, lead_text="要素の優先順位や階層関係を整理します。",
                      levels=(("最上位", "最も重要な目的"), ("第2階層", "重要な方針"),
                              ("第3階層", "具体的な戦略"), ("基盤", "日常の施策や行動")),
                      note="上位と下位のつながりや、全体を支える考え方を入力します。",
                      accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    pw = w * 0.5
    pcx = x + pw / 2
    n = len(levels)
    bh = mh / n
    for i, (name, sub) in enumerate(levels):
        frac = 0.34 + 0.66 * (i + 1) / n
        bw = pw * frac
        by = my + i * bh
        focus = i == 0
        shape_box(slide, MSO_SHAPE.TRAPEZOID, pcx - bw / 2, by, bw, bh - 0.06,
                  fill=_tint(accent, 0.9) if focus else GREY_L, line=None)
        textbox(slide, pcx - bw / 2, by + bh * 0.12, bw, 0.55, [name], size=13,
                bold=True, color=(accent if focus else INK), align=PP_ALIGN.CENTER)
        textbox(slide, pcx - bw / 2, by + bh * 0.55, bw, 0.4, [sub], size=10,
                color=TEXT_MUTED, align=PP_ALIGN.CENTER)
        # 右注釈
        ax = x + pw + 1.2
        connector(slide, pcx + bw / 2, by + bh / 2, ax - 0.2, by + bh / 2,
                  color=BORDER, width=1.0)
        dot(slide, ax - 0.2, by + bh / 2, d=0.12, color=GREY)
        textbox(slide, ax, by + 0.05, X0 + w - ax, 0.5, ["階層の意味"], size=12,
                bold=True, color=INK)
        textbox(slide, ax, by + 0.55, X0 + w - ax, bh - 0.6, [note], size=10,
                color=TEXT_MUTED, line_spacing=1.4, anchor=MSO_ANCHOR.TOP)


# ---- 21 循環・サイクル型 ----------------------------------------------------
def wf_cycle(slide, *, lead_text="繰り返し行う活動や改善の循環を説明します。",
             nodes=(("01", "計画", "実施内容を決める"), ("02", "実行", "活動を進める"),
                    ("03", "確認", "結果を振り返る"), ("04", "改善", "次の方法を決める")),
             insight=(("循環の目的", "一度で終わらず、継続する理由を入力します。"),
                      ("改善のポイント", "サイクルを速く回すための工夫を入力します。")),
             accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    cx = x + mw / 2
    cy = my + mh / 2
    r = min(mw, mh) / 2 - 1.4
    d = 2.4
    import math
    pos = []
    for k in range(4):
        ang = -math.pi / 2 + k * math.pi / 2      # 上→右→下→左
        nx = cx + r * math.cos(ang)
        ny = cy + r * math.sin(ang)
        pos.append((nx, ny))
    # 矢印（隣接ノード間・時計回り）
    for k in range(4):
        a = pos[k]
        b = pos[(k + 1) % 4]
        connector(slide, a[0], a[1], b[0], b[1], color=_tint(accent, 0.3),
                  width=1.4, end_arrow=True)
    for k, (num, name, sub) in enumerate(nodes):
        nx, ny = pos[k]
        focus = k == 0
        shape_box(slide, MSO_SHAPE.OVAL, nx - d / 2, ny - d / 2, d, d,
                  fill=WHITE, line=(accent if focus else GREY), line_w=1.6)
        textbox(slide, nx - d / 2, ny - d / 2 + 0.35, d, 0.45, [num], size=12,
                bold=True, color=(accent if focus else INK), align=PP_ALIGN.CENTER)
        textbox(slide, nx - d / 2, ny - d / 2 + 0.85, d, 0.5, [name], size=13,
                bold=True, color=(accent if focus else INK), align=PP_ALIGN.CENTER)
        textbox(slide, nx - d / 2, ny - d / 2 + 1.4, d, 0.4, [sub], size=9,
                color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    insight_panel(slide, x + mw + GUT, my, PANEL_W, mh, blocks=insight, accent=accent)


# ---- 22 ロードマップ型 ------------------------------------------------------
def wf_roadmap(slide, *, lead_text="目標までの段階と、各時期に行うことを整理します。",
               phases=(("PHASE 1", "準備"), ("PHASE 2", "試行"), ("PHASE 3", "展開"), ("PHASE 4", "定着")),
               rows=(("施策", ("実施項目A", "実施項目B", "実施項目C", "実施項目D")),
                     ("体制", ("体制の設計", "試行チームの運用", "組織体制の拡張", "全社体制への統合")),
                     ("検証", ("現状の把握", "効果の検証", "効果の拡大検証", "定着効果の測定"))),
               hi=(0, 1), goal=("最終到達点", "ロードマップ完了後に実現する状態を入力します。"),
               accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False, top_extra=0.5)
    gw = w * 0.74
    lc = gw * 0.13
    pc = (gw - lc) / len(phases)
    # フェーズ見出し
    for i, (ph, name) in enumerate(phases):
        px = x + lc + i * pc
        focus = i == 1
        textbox(slide, px, my - 1.0, pc, 0.4, [ph], size=9, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
        textbox(slide, px, my - 0.6, pc, 0.5, [name], size=13, bold=True,
                color=(accent if focus else INK), align=PP_ALIGN.CENTER)
        rule(slide, px + 0.2, my - 0.05, pc - 0.4, color=_tint(accent, 0.5) if focus else BORDER)
    nrow = len(rows)
    rh = mh / nrow
    for r, (rlabel, cells) in enumerate(rows):
        ry = my + r * rh
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, ry, lc, rh, text=[rlabel],
                  fill=SURFACE, line=BORDER, line_w=1.0, size=12, bold=True, color=INK)
        for c, cell in enumerate(cells):
            cx = x + lc + c * pc
            shape_box(slide, MSO_SHAPE.RECTANGLE, cx, ry, pc, rh, fill=WHITE, line=BORDER, line_w=1.0)
            focus = (r, c) in hi
            shape_box(slide, MSO_SHAPE.RECTANGLE, cx + 0.25, ry + 0.35, pc - 0.5, 0.6,
                      text=[cell], fill=_tint(accent, 0.85) if focus else GREY_L,
                      line=(_tint(accent, 0.4) if focus else None), line_w=1.0,
                      size=9.5, color=INK)
            shape_box(slide, MSO_SHAPE.RECTANGLE, cx + 0.25, ry + 1.1, pc - 0.5, 0.5,
                      fill=GREY_L, line=None)
    # 右：最終到達点
    gx = x + gw + GUT
    gwid = X0 + w - gx
    shape_box(slide, MSO_SHAPE.RECTANGLE, gx, my - 1.0, gwid, mh + 1.0,
              fill=WHITE, line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, gx + 0.4, my - 0.5, gwid - 0.8, 0.6, [goal[0]], size=13.5, bold=True, color=accent)
    rule(slide, gx + 0.4, my + 0.2, gwid - 0.8, color=_tint(accent, 0.5))
    textbox(slide, gx + 0.4, my + 0.5, gwid - 0.8, 2.0, [goal[1]], size=11,
            color=TEXT_MUTED, line_spacing=1.5, anchor=MSO_ANCHOR.TOP)


# ---- 23 判断フロー型 --------------------------------------------------------
def wf_decision_flow(slide, *, lead_text="条件に応じた判断と、次の行動を整理します。",
                     question="判断する問い",
                     yes=("YESの場合", "実施する行動を入力"), no=("NOの場合", "別の対応を入力"),
                     final=("最終判断", "決定内容と次のアクションを入力"),
                     bottom=("判断基準", "分岐に使う条件や、判断時に確認すべき前提を入力します。"),
                     accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    cy = my + mh / 2
    dw = 2.6
    # 菱形
    shape_box(slide, MSO_SHAPE.DIAMOND, x, cy - dw / 2, dw, dw, text=[question],
              fill=WHITE, line=accent, line_w=1.4, size=11, bold=True, color=INK)
    bx = x + dw + 1.8
    bw = 5.0
    bh = 1.6
    yb = my + 0.2
    nb = my + mh - bh - 0.2
    # 分岐線
    connector(slide, x + dw, cy, bx - 0.9, cy, color=BORDER, width=1.2)
    connector(slide, bx - 0.9, yb + bh / 2, bx - 0.9, nb + bh / 2, color=BORDER, width=1.2)
    connector(slide, bx - 0.9, yb + bh / 2, bx, yb + bh / 2, color=BORDER, width=1.2)
    connector(slide, bx - 0.9, nb + bh / 2, bx, nb + bh / 2, color=BORDER, width=1.2)
    textbox(slide, bx - 1.6, yb - 0.1, 1.2, 0.4, ["YES"], size=10, bold=True, color=accent)
    textbox(slide, bx - 1.6, nb - 0.1, 1.2, 0.4, ["NO"], size=10, bold=True, color=TEXT_MUTED)
    # YES/NO ボックス
    for (title, sub), byy, focus in ((yes, yb, True), (no, nb, False)):
        shape_box(slide, MSO_SHAPE.RECTANGLE, bx, byy, bw, bh,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        textbox(slide, bx, byy + 0.25, bw, 0.6, [title], size=13, bold=True,
                color=(accent if focus else INK), align=PP_ALIGN.CENTER)
        textbox(slide, bx, byy + 0.9, bw, 0.5, [sub], size=10.5, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    # 合流→最終判断
    fx = bx + bw + 1.6
    fw = X0 + w - fx
    connector(slide, bx + bw, yb + bh / 2, fx - 0.8, yb + bh / 2, color=BORDER, width=1.2)
    connector(slide, bx + bw, nb + bh / 2, fx - 0.8, nb + bh / 2, color=BORDER, width=1.2)
    connector(slide, fx - 0.8, yb + bh / 2, fx - 0.8, nb + bh / 2, color=BORDER, width=1.2)
    connector(slide, fx - 0.8, cy, fx, cy, color=BORDER, width=1.2)
    shape_box(slide, MSO_SHAPE.RECTANGLE, fx, cy - 1.4, fw, 2.8, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, fx, cy - 0.9, fw, 0.6, [final[0]], size=15, bold=True, color=accent, align=PP_ALIGN.CENTER)
    rule(slide, fx + 1.0, cy - 0.15, fw - 2.0, color=_tint(accent, 0.5))
    textbox(slide, fx, cy + 0.2, fw, 0.9, [final[1]], size=11, color=TEXT_MUTED,
            align=PP_ALIGN.CENTER, line_spacing=1.4)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 24 因果関係型 ----------------------------------------------------------
def wf_causality(slide, *, lead_text="原因から結果までのつながりを順番に示します。",
                 causes=(("01", "原因1", "最初の要因"), ("02", "原因2", "次に起きる変化"),
                         ("03", "原因3", "影響が広がる理由"), ("04", "直接要因", "結果につながる要因")),
                 result=("結果", "最終的に起きることを入力します。"),
                 bottom=("最も重要な因果", "どの原因に働きかけると、結果を最も大きく変えられるかを入力します。"),
                 accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    res_w = 4.4
    gap = 0.5
    n = len(causes)
    cw = (w - res_w - gap * n) / n
    for i, (num, head, sub) in enumerate(causes):
        cx = x + i * (cw + gap)
        focus = i == n - 1
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, my, cw, mh,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        pad = 0.4
        textbox(slide, cx + pad, my + 0.4, cw - pad * 2, 0.5, [num], size=13, bold=True, color=accent)
        textbox(slide, cx + pad, my + 1.0, cw - pad * 2, 0.6, [head], size=14, bold=True,
                color=(accent if focus else INK))
        rule(slide, cx + pad, my + 1.75, cw - pad * 2)
        textbox(slide, cx + pad, my + 2.0, cw - pad * 2, mh - 2.2, [sub], size=10.5,
                color=TEXT_MUTED, line_spacing=1.4, anchor=MSO_ANCHOR.TOP)
        connector(slide, cx + cw, my + mh / 2, cx + cw + gap, my + mh / 2, color=BORDER, width=1.2)
    rx = x + w - res_w
    shape_box(slide, MSO_SHAPE.RECTANGLE, rx, my, res_w, mh, fill=_tint(accent, 0.9),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, rx, my + mh * 0.28, res_w, 0.8, [result[0]], size=18, bold=True,
            color=accent, align=PP_ALIGN.CENTER)
    rule(slide, rx + 0.8, my + mh * 0.42, res_w - 1.6, color=_tint(accent, 0.5))
    textbox(slide, rx + 0.5, my + mh * 0.5, res_w - 1.0, 1.4, [result[1]], size=11,
            color=INK, align=PP_ALIGN.CENTER, line_spacing=1.4)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 25 相関・関係図型 ------------------------------------------------------
def wf_relation(slide, *, lead_text="中心となる要素と、周囲との関係を整理します。",
                center=("中心要素", "テーマを入力"),
                left=(("関連要素A", "関係を入力"), ("関連要素B", "関係を入力"), ("関連要素C", "関係を入力")),
                right=(("関連要素D", "関係を入力"), ("関連要素E", "関係を入力"), ("関連要素F", "関係を入力")),
                insight=("関係の示唆", "つながりが強い要素や、影響の方向を入力します。"),
                accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    cx = x + mw / 2
    cy = my + mh / 2
    cd = 2.7
    bw = 3.4
    bh = 1.5

    def col(items, side):
        n = len(items)
        for i, (head, sub) in enumerate(items):
            by = my + (mh - bh) * (i / (n - 1)) if n > 1 else my
            bx = x if side < 0 else x + mw - bw
            shape_box(slide, MSO_SHAPE.RECTANGLE, bx, by, bw, bh, fill=WHITE, line=BORDER, line_w=1.0)
            textbox(slide, bx + 0.3, by + 0.3, bw - 0.6, 0.5, [head], size=12, bold=True, color=INK)
            textbox(slide, bx + 0.3, by + 0.85, bw - 0.6, 0.5, [sub], size=10, color=TEXT_MUTED)
            ex = bx + bw if side < 0 else bx
            mid = cx - cd / 2 - 0.6 if side < 0 else cx + cd / 2 + 0.6
            connector(slide, ex, by + bh / 2, mid, by + bh / 2, color=BORDER, width=1.0)
            connector(slide, mid, by + bh / 2, mid, cy, color=BORDER, width=1.0)
            connector(slide, mid, cy, cx + side * cd / 2, cy, color=BORDER, width=1.0)
    col(left, -1)
    col(right, +1)
    shape_box(slide, MSO_SHAPE.OVAL, cx - cd / 2, cy - cd / 2, cd, cd, fill=WHITE,
              line=accent, line_w=1.6)
    textbox(slide, cx - cd / 2, cy - 0.55, cd, 0.6, [center[0]], size=13, bold=True,
            color=accent, align=PP_ALIGN.CENTER)
    textbox(slide, cx - cd / 2, cy + 0.1, cd, 0.5, [center[1]], size=10, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    insight_panel(slide, x + mw + GUT, my, PANEL_W, mh, blocks=[insight], accent=accent)


# ---- 26 カスタマージャーニー型 ---------------------------------------------
def wf_journey(slide, *, lead_text="顧客の行動や感情を、段階ごとに整理します。",
               stages=(("認知", "STEP 1"), ("興味", "STEP 2"), ("比較", "STEP 3"),
                       ("購入", "STEP 4"), ("継続", "STEP 5")),
               rows=("行動", "考えていること", "接点", "課題"),
               hi_stage=3, hi_cell=(3, 2),
               bottom=("改善機会", "顧客体験を改善すべき段階と、その理由を入力します。"),
               accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    ncol = len(stages)
    lc = w * 0.14
    cw = (w - lc) / ncol
    head_h = 1.35
    rh = (mh - head_h) / len(rows)
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, my, lc, head_h, fill=WHITE, line=BORDER, line_w=1.0)
    for c, (name, step) in enumerate(stages):
        cx = x + lc + c * cw
        focus = c == hi_stage
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, my, cw, head_h, fill=WHITE, line=BORDER, line_w=1.0)
        textbox(slide, cx, my + 0.22, cw, 0.5, [name], size=12.5, bold=True,
                color=(accent if focus else INK), align=PP_ALIGN.CENTER)
        textbox(slide, cx, my + 0.78, cw, 0.45, [step], size=9, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    for r, rlabel in enumerate(rows):
        ry = my + head_h + r * rh
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, ry, lc, rh, text=[rlabel], fill=WHITE,
                  line=BORDER, line_w=1.0, size=11.5, bold=True, color=INK)
        for c in range(ncol):
            cx = x + lc + c * cw
            focus = (r, c) == hi_cell
            shape_box(slide, MSO_SHAPE.RECTANGLE, cx, ry, cw, rh,
                      text=[f"{rlabel[:2]}を入力"],
                      fill=_tint(accent, 0.92) if focus else WHITE,
                      line=(_tint(accent, 0.4) if focus else BORDER), line_w=1.0,
                      size=10, color=(accent if focus else TEXT_MUTED), align=PP_ALIGN.CENTER)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 27 計画対実績型 --------------------------------------------------------
def wf_plan_actual(slide, *, lead_text="計画値と実績値の差を、推移と数値で確認します。",
                   chart_title="計画と実績の推移",
                   cats=("1月", "2月", "3月", "4月", "5月", "6月"),
                   plan=(50, 58, 65, 72, 80, 88), actual=(48, 55, 61, 67, 74, 82),
                   panel=("差分", "-6pt", "計画未達", "差が生まれた原因と、次に修正することを入力します。"),
                   accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, my, mw, mh, fill=WHITE, line=BORDER, line_w=1.0)
    textbox(slide, x + 0.5, my + 0.3, mw - 1, 0.6, [chart_title], size=12.5, bold=True, color=INK)
    dual_line(slide, x + 0.5, my + 1.1, mw - 1.0, mh - 1.6, cats=cats, plan=list(plan),
              actual=list(actual), accent=accent)
    px = x + mw + GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, px, my, PANEL_W, mh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    pad = 0.55
    textbox(slide, px + pad, my + 0.5, PANEL_W - pad * 2, 0.6, [panel[0]], size=13.5, bold=True, color=accent)
    textbox(slide, px + pad, my + 1.2, PANEL_W - pad * 2, 1.3, [panel[1]], size=36, bold=True, color=accent)
    rule(slide, px + pad, my + mh * 0.5, PANEL_W - pad * 2, color=_tint(accent, 0.5))
    textbox(slide, px + pad, my + mh * 0.55, PANEL_W - pad * 2, 0.6, [panel[2]], size=12.5, bold=True, color=INK)
    textbox(slide, px + pad, my + mh * 0.68, PANEL_W - pad * 2, 1.6, [panel[3]], size=11,
            color=TEXT_MUTED, line_spacing=1.5, anchor=MSO_ANCHOR.TOP)


# ---- 28 ギャップ分析型 ------------------------------------------------------
def wf_gap(slide, *, lead_text="現状と理想の差を特定し、埋める方法を整理します。",
           now=("現在", "現在の状態", "現状の数値や特徴を入力します。"),
           gap=("GAP", "-35", "ポイント", "差を生む要因",
                ("要因1　説明を入力", "要因2　説明を入力", "要因3　説明を入力")),
           ideal=("理想", "目指す状態", "目標の数値や状態を入力します。"),
           bottom=("ギャップを埋める施策", "優先して実施する施策と、達成までの道筋を入力します。"),
           accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    sidew = w * 0.24
    cw = w - sidew * 2 - 1.2
    # 現在（白）
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, my, sidew, mh, fill=WHITE, line=BORDER, line_w=1.0)
    textbox(slide, x + 0.5, my + 0.5, sidew - 1, 0.6, [now[0]], size=15, bold=True, color=INK)
    textbox(slide, x + 0.5, my + 1.3, sidew - 1, 0.6, [now[1]], size=13, bold=True, color=INK)
    rule(slide, x + 0.5, my + 2.05, sidew - 1)
    textbox(slide, x + 0.5, my + 2.3, sidew - 1, 1.2, [now[2]], size=10.5, color=TEXT_MUTED, line_spacing=1.4)
    # GAP（中央・淡主色）
    gx = x + sidew + 0.6
    shape_box(slide, MSO_SHAPE.RECTANGLE, gx, my, cw, mh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, gx + 0.6, my + 0.4, cw - 1.2, 0.5, [gap[0]], size=12, bold=True, color=accent)
    textbox(slide, gx + 0.6, my + 0.9, cw * 0.5, 1.5, [gap[1]], size=44, bold=True, color=accent)
    textbox(slide, gx + cw * 0.5, my + 1.5, cw * 0.4, 0.8, [gap[2]], size=16, bold=True,
            color=INK, anchor=MSO_ANCHOR.MIDDLE)
    rule(slide, gx + 0.6, my + mh * 0.55, cw - 1.2, color=_tint(accent, 0.5))
    textbox(slide, gx + 0.6, my + mh * 0.6, cw - 1.2, 0.5, [gap[3]], size=12, bold=True, color=INK)
    textbox(slide, gx + 0.6, my + mh * 0.72, cw - 1.2, 1.3, list(gap[4]), size=10.5,
            color=TEXT_MUTED, line_spacing=1.4, anchor=MSO_ANCHOR.TOP)
    # 理想（淡主色）
    ix = gx + cw + 0.6
    shape_box(slide, MSO_SHAPE.RECTANGLE, ix, my, sidew, mh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, ix + 0.5, my + 0.5, sidew - 1, 0.6, [ideal[0]], size=15, bold=True, color=accent)
    textbox(slide, ix + 0.5, my + 1.3, sidew - 1, 0.6, [ideal[1]], size=13, bold=True, color=accent)
    rule(slide, ix + 0.5, my + 2.05, sidew - 1, color=_tint(accent, 0.5))
    textbox(slide, ix + 0.5, my + 2.3, sidew - 1, 1.2, [ideal[2]], size=10.5, color=TEXT_MUTED, line_spacing=1.4)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 29 表＋示唆型 ----------------------------------------------------------
def wf_table_insight(slide, *, lead_text="詳細データを表で示し、読み取るべきポイントを添えます。",
                     headers=("項目", "実績", "前年差", "目標", "評価"),
                     rows=(("項目A", "85", "+12", "90", "良好"), ("項目B", "72", "+5", "80", "要改善"),
                           ("項目C", "68", "-3", "75", "注意"), ("項目D", "91", "+8", "90", "達成"),
                           ("項目E", "54", "+2", "70", "要改善")),
                     hi_col=4,
                     insight=(("示唆", ""), ("注目すべき項目", "表の中で特に重要な差や、判断につながるポイントを入力します。")),
                     accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    data_table(slide, x, my, mw, mh, headers=headers, rows=rows, hi_col=hi_col,
               col_ratios=(1.6, 1, 1, 1, 1.2), accent=accent)
    insight_panel(slide, x + mw + GUT, my, PANEL_W, mh, blocks=insight, accent=accent)


# ---- 30 リスク＋対策型 ------------------------------------------------------
def wf_risk_action(slide, *, lead_text="想定されるリスクと、対応策をセットで整理します。",
                   headers=("リスク", "発生可能性", "影響度", "対策"),
                   rows=(("リスク1　内容を入力", "高", "高", "予防策と発生時の対応を入力"),
                         ("リスク2　内容を入力", "中", "高", "予防策と発生時の対応を入力"),
                         ("リスク3　内容を入力", "低", "中", "予防策と発生時の対応を入力"),
                         ("リスク4　内容を入力", "低", "中", "予防策と発生時の対応を入力")),
                   hi_col=3, bottom=("最優先リスク", "最初に備えるべきリスクと、その理由を入力します。"),
                   accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    data_table(slide, x, my, w, mh, headers=headers, rows=rows, hi_col=hi_col,
               col_ratios=(2.4, 1.1, 1.1, 3.4), accent=accent)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 31 優先順位型 ----------------------------------------------------------
def wf_priority(slide, *, lead_text="効果と実行難易度から、取り組む順番を決めます。",
                quad_labels=("検討", "最優先", "後回し", "余力で実施"), hi_quad=1,
                items=(("A", 0.7, 0.72), ("B", 0.82, 0.6), ("C", 0.32, 0.72),
                       ("D", 0.3, 0.3), ("E", 0.68, 0.28)),
                order=("施策A", "施策B", "施策C", "施策D"),
                accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    gh = mh - 0.6
    for q in range(4):
        qx = x + (mw / 2) * (q % 2)
        qy = my + (gh / 2) * (q // 2)
        focus = q == hi_quad
        shape_box(slide, MSO_SHAPE.RECTANGLE, qx, qy, mw / 2, gh / 2,
                  fill=_tint(accent, 0.92) if focus else WHITE, line=BORDER, line_w=1.0)
        textbox(slide, qx + 0.35, qy + 0.3, mw / 2 - 0.7, 0.6, [quad_labels[q]],
                size=12.5, bold=True, color=(accent if focus else INK))
    textbox(slide, x + 0.2, my + 0.1, 4, 0.4, ["効果：高い"], size=9, color=TEXT_MUTED)
    textbox(slide, x + 0.2, my + gh - 0.5, 4, 0.4, ["効果：低い"], size=9, color=TEXT_MUTED)
    textbox(slide, x + 0.5, my + gh + 0.08, 4, 0.4, ["難易度：低い"], size=9, color=TEXT_MUTED)
    textbox(slide, x + mw - 4.2, my + gh + 0.08, 4, 0.4, ["難易度：高い"], size=9,
            color=TEXT_MUTED, align=PP_ALIGN.RIGHT)
    for lab, rx, ry in items:
        d = 0.72
        top_r = (int(rx > 0.5), int(ry > 0.5))
        q = (0 if ry > 0.5 else 2) + (1 if rx > 0.5 else 0)
        focus = q == hi_quad
        cx = x + mw * rx - d / 2
        cy = my + gh * (1 - ry) - d / 2
        shape_box(slide, MSO_SHAPE.OVAL, cx, cy, d, d, text=[lab],
                  fill=_tint(accent, 0.35) if focus else GREY, line=None,
                  size=10.5, bold=True, color=(accent if focus else INK))
    # 右パネル＝実施する順番（番号リスト）
    px = x + mw + GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, px, my, PANEL_W, mh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, px + 0.55, my + 0.5, PANEL_W - 1.1, 0.6, ["実施する順番"], size=13.5, bold=True, color=accent)
    rule(slide, px + 0.55, my + 1.25, PANEL_W - 1.1, color=_tint(accent, 0.5))
    n = len(order)
    oy = my + 1.6
    oh = (mh - 2.0) / n
    for i, name in enumerate(order):
        yy = oy + i * oh
        if i > 0:
            rule(slide, px + 0.55, yy, PANEL_W - 1.1, color=_tint(accent, 0.6))
        textbox(slide, px + 0.55, yy, 1.1, oh, ["%02d" % (i + 1)], size=13, bold=True,
                color=accent, anchor=MSO_ANCHOR.MIDDLE)
        textbox(slide, px + 1.8, yy, PANEL_W - 2.3, oh, [name], size=12, bold=True,
                color=INK, anchor=MSO_ANCHOR.MIDDLE)


# ---- 32 まとめ＋次のアクション型 -------------------------------------------
def wf_summary_actions(slide, *, lead_text="ここまでの要点を整理し、次に行うことを明確にします。",
                       summary=(("重要なポイントを入力", "結論を補足する短い説明を入力します。"),) * 3,
                       actions=(("ACTION 1", "最初に実施すること"), ("ACTION 2", "次に実施すること"),
                                ("ACTION 3", "継続して行うこと")),
                       bottom=("最終メッセージ", "読み手に依頼することや、次の意思決定を入力します。"),
                       accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    colw = (w - 0.9) / 2
    vrule(slide, x + colw + 0.45, my + 0.2, mh - 0.4)
    # 左＝まとめ
    textbox(slide, x, my, colw, 0.6, ["まとめ"], size=15, bold=True, color=accent)
    n = len(summary)
    rh = (mh - 0.9) / n
    for i, (head, sub) in enumerate(summary):
        ry = my + 0.9 + i * rh
        if i > 0:
            rule(slide, x, ry, colw)
        textbox(slide, x, ry + rh * 0.15, 1.2, 0.6, ["%02d" % (i + 1)], size=15, bold=True, color=accent)
        textbox(slide, x + 1.3, ry + rh * 0.12, colw - 1.3, 0.55, [head], size=13, bold=True, color=INK)
        textbox(slide, x + 1.3, ry + rh * 0.12 + 0.55, colw - 1.3, 0.5, [sub], size=10.5, color=TEXT_MUTED)
    # 右＝次のアクション
    ax = x + colw + 0.9
    textbox(slide, ax, my, colw, 0.6, ["次のアクション"], size=15, bold=True, color=accent)
    m = len(actions)
    ah = (mh - 0.9) / m
    for i, (tag, title) in enumerate(actions):
        ay = my + 0.9 + i * (ah)
        focus = i == 0
        shape_box(slide, MSO_SHAPE.RECTANGLE, ax, ay, colw, ah - 0.25,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        textbox(slide, ax + 0.4, ay + 0.2, 3.0, 0.4, [tag], size=9.5, bold=True, color=TEXT_MUTED)
        textbox(slide, ax + 0.4, ay + 0.6, colw - 4.0, 0.6, [title], size=13, bold=True, color=INK)
        textbox(slide, ax + colw - 3.3, ay + 0.2, 1.6, 0.4, ["担当者"], size=9, color=TEXT_MUTED)
        textbox(slide, ax + colw - 1.6, ay + 0.2, 1.4, 0.4, ["期限"], size=9, color=TEXT_MUTED)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 33 並列グラフ比較型 ----------------------------------------------------
def wf_dual_charts(slide, *, lead_text=None,
                   a=("指標Aの推移", ("A", "B", "C", "D", "E"), (18, 24, 31, 39, 52)),
                   b=("指標Bの推移", ("A", "B", "C", "D", "E"), (12, 19, 28, 36, 47)),
                   bottom=("示唆", "2つのグラフを横断して読み取れる示唆を入力します。"),
                   accent=PRIMARY):
    x, my, w, mh = _content(bottom=True, top_extra=-0.4)
    colw = (w - GUT) / 2
    for side, (title, cats, vals) in enumerate((a, b)):
        cx = x + side * (colw + GUT)
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, my, colw, mh, fill=WHITE, line=BORDER, line_w=1.0)
        textbox(slide, cx + 0.5, my + 0.3, colw - 3, 0.6, [title], size=12.5, bold=True, color=INK)
        textbox(slide, cx + colw - 2.4, my + 0.3, 2.0, 0.5, ["単位を入力"], size=9,
                color=TEXT_MUTED, align=PP_ALIGN.RIGHT)
        vbars(slide, cx + 0.5, my + 1.1, colw - 1.0, mh - 1.6, cats=cats, vals=list(vals),
              hi=len(vals) - 1, ymax=max(vals) * 1.15, accent=accent, grid=True)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 34 重点方針＋実行構造型 -----------------------------------------------
def wf_policy_execution(slide, *, headline="このページで伝えたい重点方針を入力します。",
                        headsub="方針の背景や到達したい状態を、1〜2行で補足します。",
                        areas=(("重点領域 01", "見出しを入力", "この領域で何を変えるのか、どのように取り組むのかを入力します。"),
                               ("重点領域 02", "見出しを入力", "この領域で何を変えるのか、どのように取り組むのかを入力します。")),
                        flow=(("基盤", "必要な資源や前提を入力"), ("実行", "主要な施策や行動を入力"), ("成果", "実現する状態を入力")),
                        goal=("到達点", "実行の先に生まれる状態や、次の成長につながる結果を入力します。"),
                        accent=PRIMARY):
    # 見出し行（リード枠は使わず上部に大見出し）
    textbox(slide, X0, ZY - 0.05, ZW * 0.6, 0.9, [headline], size=17, bold=True, color=INK)
    textbox(slide, X0 + ZW * 0.62, ZY + 0.05, ZW * 0.38, 0.8, [headsub], size=10.5,
            color=TEXT_MUTED, line_spacing=1.4)
    rule(slide, X0, ZY + 1.0, ZW)
    x, my, w = X0, ZY + 1.3, ZW
    mh = ZB - my
    lw = w * 0.42
    ah = mh / 2
    for i, (label, head, body) in enumerate(areas):
        ay = my + i * ah
        if i > 0:
            rule(slide, x, ay, lw)
        textbox(slide, x, ay + 0.15, lw, 0.4, [label], size=10, bold=True, color=accent)
        textbox(slide, x, ay + 0.55, lw, 0.6, [head], size=14, bold=True, color=INK)
        textbox(slide, x, ay + 1.2, lw, 0.8, [body], size=10.5, color=TEXT_MUTED, line_spacing=1.4)
    # 右＝実行構造
    rx = x + lw + GUT
    rw = X0 + w - rx
    textbox(slide, rx, my, rw, 0.5, ["実行構造"], size=12.5, bold=True, color=INK)
    n = len(flow)
    gap = 0.7
    bw = (rw - gap * (n - 1)) / n
    fy = my + 0.7
    fh = 2.3
    for i, (name, sub) in enumerate(flow):
        bx = rx + i * (bw + gap)
        focus = i == n - 1
        shape_box(slide, MSO_SHAPE.RECTANGLE, bx, fy, bw, fh,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        textbox(slide, bx, fy + 0.35, bw, 0.6, [name], size=13, bold=True,
                color=(accent if focus else INK), align=PP_ALIGN.CENTER)
        textbox(slide, bx + 0.2, fy + 1.0, bw - 0.4, 1.15, [sub], size=9.5, color=TEXT_MUTED,
                align=PP_ALIGN.CENTER, line_spacing=1.2, anchor=MSO_ANCHOR.TOP)
        if i < n - 1:
            connector(slide, bx + bw, fy + fh / 2, bx + bw + gap, fy + fh / 2,
                      color=GREY, width=1.4, end_arrow=True)
    # 到達点バー
    gy = fy + fh + 0.5
    shape_box(slide, MSO_SHAPE.RECTANGLE, rx, gy, rw, ZB - gy - 0.1, fill=WHITE, line=BORDER, line_w=1.0)
    textbox(slide, rx + 0.4, gy, 2.5, ZB - gy - 0.1, [goal[0]], size=11.5, bold=True,
            color=accent, anchor=MSO_ANCHOR.MIDDLE)
    vrule(slide, rx + 2.9, gy + 0.25, (ZB - gy - 0.1) - 0.5)
    textbox(slide, rx + 3.2, gy, rw - 3.5, ZB - gy - 0.1, [goal[1]], size=10.5,
            color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.3)


# ---- 35 ロジックツリー型 ----------------------------------------------------
def wf_logic_tree(slide, *, lead_text="中心課題を分解し、原因や論点を漏れなく整理します。",
                  root=("中心課題", "分解したい問いを入力"),
                  branches=(("主要論点A", "一次要因を入力", ("詳細論点 1", "詳細論点 2")),
                            ("主要論点B", "一次要因を入力", ("詳細論点 3", "詳細論点 4")),
                            ("主要論点C", "一次要因を入力", ("詳細論点 5", "詳細論点 6"))),
                  hi_branch=1, hi_leaf=(1, 0),
                  insight=("優先して検証する論点", "影響が大きく、最初に確認すべき枝を入力します。\n\n各枝の重複や抜けを確認します。"),
                  accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    rw_ = 4.0
    bw_ = 4.0
    lw_ = mw - rw_ - bw_ - 1.2
    # root
    ry0 = my + mh / 2 - 1.1
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, ry0, lw_, 2.2, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, x + 0.3, ry0 + 0.6, lw_ - 0.6, 0.6, [root[0]], size=13, bold=True,
            color=accent, align=PP_ALIGN.CENTER)
    textbox(slide, x + 0.3, ry0 + 1.2, lw_ - 0.6, 0.5, [root[1]], size=9.5,
            color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    bx = x + lw_ + 0.6
    n = len(branches)
    bh_ = 1.75
    slot = mh / n
    trunk = x + lw_ + 0.3
    connector(slide, x + lw_, my + mh / 2, trunk, my + mh / 2, color=BORDER, width=1.2)
    tops = [my + slot * i + (slot - bh_) / 2 for i in range(n)]
    vrule(slide, trunk, tops[0] + bh_ / 2, tops[-1] - tops[0])
    lx = bx + bw_ + 0.6
    for i, (head, sub, leaves) in enumerate(branches):
        by = tops[i]
        focus = i == hi_branch
        connector(slide, trunk, by + bh_ / 2, bx, by + bh_ / 2, color=BORDER, width=1.2)
        shape_box(slide, MSO_SHAPE.RECTANGLE, bx, by, bw_, bh_,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        textbox(slide, bx, by + 0.4, bw_, 0.5, [head], size=12.5, bold=True,
                color=(accent if focus else INK), align=PP_ALIGN.CENTER)
        textbox(slide, bx, by + 0.95, bw_, 0.4, [sub], size=9.5, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
        # leaves
        lh = 0.75
        ltrunk = bx + bw_ + 0.3
        connector(slide, bx + bw_, by + bh_ / 2, ltrunk, by + bh_ / 2, color=BORDER, width=1.0)
        lty = [by + 0.1, by + bh_ - lh - 0.1]
        vrule(slide, ltrunk, lty[0] + lh / 2, lty[1] - lty[0])
        for j, leaf in enumerate(leaves):
            lyy = lty[j]
            lf = (i, j) == hi_leaf
            connector(slide, ltrunk, lyy + lh / 2, lx, lyy + lh / 2, color=BORDER, width=1.0)
            shape_box(slide, MSO_SHAPE.RECTANGLE, lx, lyy, rw_, lh, text=[leaf],
                      fill=_tint(accent, 0.92) if lf else WHITE,
                      line=_tint(accent, 0.4) if lf else BORDER, line_w=1.0,
                      size=11, bold=True, color=(accent if lf else INK))
    insight_panel(slide, x + mw + GUT, my, PANEL_W, mh, blocks=[insight], accent=accent)


# ---- 36 KPIドライバー型 ----------------------------------------------------
def wf_kpi_driver(slide, *, lead_text="最終目標を動かす指標と、具体的な改善施策をつなげます。",
                  kgi=("KGI｜最終目標", "重要な成果指標を入力"),
                  kpis=(("KPI 01", "獲得数", "1,250"), ("KPI 02", "転換率", "42%"), ("KPI 03", "継続率", "78%")),
                  action="改善施策", action_sub="具体的な打ち手を入力", hi=1,
                  bottom=("重点ドライバー", "目標への寄与が最も大きい指標と、その理由を入力します。"),
                  accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    n = len(kpis)
    gap = 0.6
    cw = (w - gap * (n - 1)) / n
    # KGI（中央上）
    kgw = cw * 1.6
    kgx = x + w / 2 - kgw / 2
    shape_box(slide, MSO_SHAPE.RECTANGLE, kgx, my, kgw, 1.4, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, kgx + 0.4, my + 0.2, kgw - 0.8, 0.4, [kgi[0]], size=9.5, bold=True, color=accent)
    textbox(slide, kgx + 0.4, my + 0.6, kgw - 0.8, 0.6, [kgi[1]], size=13, bold=True, color=INK)
    # ブラケット
    ky = my + 1.4
    ky2 = my + 2.1
    connector(slide, x + w / 2, ky, x + w / 2, ky2, color=BORDER, width=1.2)
    centers = [x + i * (cw + gap) + cw / 2 for i in range(n)]
    connector(slide, centers[0], ky2, centers[-1], ky2, color=BORDER, width=1.2)
    kpi_y = ky2 + 0.15
    kpi_h = 1.6
    act_y = kpi_y + kpi_h + 0.55
    act_h = ZB - BAR_H - 0.3 - act_y
    for i, (tag, name, val) in enumerate(kpis):
        cx = x + i * (cw + gap)
        focus = i == hi
        connector(slide, centers[i], ky2, centers[i], kpi_y, color=BORDER, width=1.2)
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, kpi_y, cw, kpi_h,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        textbox(slide, cx + 0.4, kpi_y + 0.25, cw - 0.8, 0.4, [tag], size=9.5, bold=True, color=TEXT_MUTED)
        textbox(slide, cx + 0.4, kpi_y + 0.7, cw * 0.5, 0.7, [name], size=14, bold=True, color=INK)
        textbox(slide, cx + cw * 0.45, kpi_y + 0.7, cw * 0.5 - 0.4, 0.7, [val], size=18,
                bold=True, color=accent, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
        connector(slide, centers[i], kpi_y + kpi_h, centers[i], act_y, color=BORDER, width=1.2)
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, act_y, cw, act_h,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        textbox(slide, cx, act_y + 0.25, cw, 0.5, [action], size=12, bold=True,
                color=(accent if focus else INK), align=PP_ALIGN.CENTER)
        textbox(slide, cx + 0.3, act_y + 0.8, cw - 0.6, 0.5, [action_sub], size=9.5,
                color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 37 戦略カスケード型 ----------------------------------------------------
def wf_strategy_cascade(slide, *, lead_text="上位目標を、方針・施策・評価指標へ段階的に落とし込みます。",
                        top="最上位の目標・目指す状態",
                        cols=(("戦略方針 A", "実施内容を入力", "KPI・判定基準を入力"),
                              ("戦略方針 B", "実施内容を入力", "KPI・判定基準を入力"),
                              ("戦略方針 C", "実施内容を入力", "KPI・判定基準を入力")),
                        hi=1, bottom=("整合性の確認", "各施策が上位目標へどう貢献するかを入力します。"),
                        accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    tw = w * 0.42
    shape_box(slide, MSO_SHAPE.RECTANGLE, x + w / 2 - tw / 2, my, tw, 1.1,
              text=[top], fill=_tint(accent, 0.92), line=_tint(accent, 0.45), line_w=1.0,
              size=14, bold=True, color=accent)
    n = len(cols)
    gap = 0.6
    cw = (w - gap * (n - 1)) / n
    ky = my + 1.1
    ky2 = my + 1.7
    centers = [x + i * (cw + gap) + cw / 2 for i in range(n)]
    connector(slide, x + w / 2, ky, x + w / 2, ky2, color=BORDER, width=1.2)
    connector(slide, centers[0], ky2, centers[-1], ky2, color=BORDER, width=1.2)
    row1_y = ky2 + 0.15
    row1_h = 1.1
    row2_y = row1_y + row1_h + 0.4
    row3_y = row2_y + 1.5 + 0.35
    row3_h = ZB - BAR_H - 0.3 - row3_y
    for i, (policy, action, kpi) in enumerate(cols):
        cx = x + i * (cw + gap)
        focus = i == hi
        connector(slide, centers[i], ky2, centers[i], row1_y, color=BORDER, width=1.2)
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, row1_y, cw, row1_h,
                  text=[policy], fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0,
                  size=13, bold=True, color=(accent if focus else INK))
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, row2_y, cw, 1.5, fill=WHITE, line=BORDER, line_w=1.0)
        textbox(slide, cx + 0.4, row2_y + 0.25, cw - 0.8, 0.4, ["重点施策"], size=9.5, color=TEXT_MUTED)
        textbox(slide, cx + 0.4, row2_y + 0.7, cw - 0.8, 0.6, [action], size=13, bold=True, color=INK)
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, row3_y, cw, row3_h,
                  text=[kpi], fill=_tint(accent, 0.9) if focus else SURFACE,
                  line=None, size=10.5, bold=True, color=(accent if focus else INK))
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 38 同心円・対象範囲型 --------------------------------------------------
def wf_concentric_scope(slide, *, lead_text="対象範囲や優先領域を、中心から外側への包含関係で整理します。",
                        rings=("外部領域", "重点領域", "中核"), inner_sub="最優先",
                        items=(("01", "中核", "最初に集中する対象と理由を入力します。"),
                               ("02", "重点領域", "次に拡張する対象や条件を入力します。"),
                               ("03", "外部領域", "将来的に検討する範囲を入力します。")),
                        boundary=("境界の条件", "領域を分ける基準を入力"),
                        accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w * 0.42
    cx = x + mw / 2
    cy = my + mh / 2
    dmax = min(mw, mh) - 0.4
    fills = (GREY_L, GREY, _tint(accent, 0.85))
    lines = (BORDER, None, accent)
    for i in range(3):
        d = dmax * (1 - i * 0.32)
        shape_box(slide, MSO_SHAPE.OVAL, cx - d / 2, cy - d / 2, d, d,
                  fill=fills[i], line=lines[i], line_w=1.6 if i == 2 else 1.0)
    textbox(slide, cx - dmax / 2 + 0.1, cy - dmax / 2 + 0.1, 3, 0.5, [rings[0]], size=11, bold=True, color=TEXT_MUTED)
    textbox(slide, cx - dmax * 0.27, cy - dmax * 0.24, 3, 0.5, [rings[1]], size=11, bold=True, color=INK)
    textbox(slide, cx - 1.2, cy - 0.45, 2.4, 0.5, [rings[2]], size=12, bold=True, color=accent, align=PP_ALIGN.CENTER)
    textbox(slide, cx - 1.2, cy + 0.15, 2.4, 0.4, [inner_sub], size=9.5, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    # 右＝num-tab リスト＋境界条件バー
    rx = x + mw + GUT
    rw = X0 + w - rx
    n = len(items)
    ih = (mh - 1.1) / n
    for i, (num, label, body) in enumerate(items):
        iy = my + i * ih
        focus = i == 0
        shape_box(slide, MSO_SHAPE.RECTANGLE, rx, iy, rw, ih - 0.25,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        textbox(slide, rx + 0.5, iy, 0.9, ih - 0.25, [num], size=12, bold=True,
                color=accent, anchor=MSO_ANCHOR.MIDDLE)
        vrule(slide, rx + 1.5, iy + 0.3, ih - 0.85)
        textbox(slide, rx + 1.75, iy, 2.4, ih - 0.25, [label], size=12, bold=True,
                color=(accent if focus else INK), anchor=MSO_ANCHOR.MIDDLE)
        textbox(slide, rx + 4.3, iy, rw - 4.6, ih - 0.25, [body], size=10.5,
                color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)
    byy = my + mh - 0.9
    shape_box(slide, MSO_SHAPE.RECTANGLE, rx, byy, rw, 0.9, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, rx + 0.5, byy, 3.2, 0.9, [boundary[0]], size=11.5, bold=True, color=accent, anchor=MSO_ANCHOR.MIDDLE)
    textbox(slide, rx + 3.9, byy, rw - 4.2, 0.9, [boundary[1]], size=10.5, color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)


# ---- 39 ベン図・重なり型 ----------------------------------------------------
def wf_venn(slide, *, lead_text="複数要素の共通点と独自性を整理し、価値が生まれる交点を示します。",
            a=("要素A", "固有の特徴を入力"), b=("要素B", "固有の特徴を入力"), overlap="共通価値",
            insight=(("交点から生まれる価値", ""),
                     ("最も重要な共通領域", "両者の強みが重なることで実現する価値や、選ばれる理由を入力します。")),
            note="必要に応じて、3つ目の要素を追加できます。", accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    d = min(mh, mw * 0.62)
    cy = my + mh / 2
    ax = x + mw * 0.5 - d * 0.72
    bxx = x + mw * 0.5 - d * 0.28
    shape_box(slide, MSO_SHAPE.OVAL, ax, cy - d / 2, d, d, fill=None, line=GREY, line_w=1.6)
    shape_box(slide, MSO_SHAPE.OVAL, bxx, cy - d / 2, d, d, fill=None, line=accent, line_w=1.6)
    ov = d * 0.44
    shape_box(slide, MSO_SHAPE.OVAL, (ax + bxx) / 2 + d / 2 - ov / 2, cy - ov / 2, ov, ov,
              fill=_tint(accent, 0.88), line=None)
    textbox(slide, ax - 0.2, cy - d / 2 + 0.4, 2.6, 0.5, [a[0]], size=13, bold=True, color=INK)
    textbox(slide, ax + 0.1, cy - d / 2 + 1.0, 2.2, 0.8, [a[1]], size=10, color=TEXT_MUTED,
            align=PP_ALIGN.CENTER, line_spacing=1.3)
    textbox(slide, bxx + d - 2.4, cy - d / 2 + 0.4, 2.6, 0.5, [b[0]], size=13, bold=True,
            color=accent, align=PP_ALIGN.RIGHT)
    textbox(slide, bxx + d - 2.3, cy - d / 2 + 1.0, 2.2, 0.8, [b[1]], size=10, color=TEXT_MUTED,
            align=PP_ALIGN.CENTER, line_spacing=1.3)
    textbox(slide, (ax + bxx) / 2 + d / 2 - ov / 2, cy - 0.25, ov, 0.5, [overlap], size=11,
            bold=True, color=accent, align=PP_ALIGN.CENTER)
    pnl = insight_panel
    pnl(slide, x + mw + GUT, my, PANEL_W, mh, blocks=insight, accent=accent)
    textbox(slide, x + mw + GUT + 0.55, my + mh - 1.0, PANEL_W - 1.1, 0.6, [note],
            size=9.5, color=TEXT_MUTED, line_spacing=1.3)


# ---- 40 レイヤー・基盤構造型 -----------------------------------------------
def wf_layers(slide, *, lead_text="下位層が上位層を支える構造と、各層の役割を整理します。",
              layers=(("01", "提供価値", "最上位で実現する価値を入力"),
                      ("02", "業務・サービス", "利用者へ提供する機能を入力"),
                      ("03", "共通機能", "複数領域で利用する機能を入力"),
                      ("04", "データ・基盤", "全体を支える資源や前提を入力")),
              hi=(0, 3), cross=("横断要素", ("ガバナンス", "セキュリティ", "人材・運用"),
                                "すべての層に共通して必要な条件を入力します。"),
              accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    n = len(layers)
    gap = 0.2
    lh = (mh - gap * (n - 1)) / n
    for i, (num, label, body) in enumerate(layers):
        ly = my + i * (lh + gap)
        focus = i in hi
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, ly, mw, lh,
                  fill=_tint(accent, 0.9) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        textbox(slide, x + 0.5, ly, 1.1, lh, [num], size=13, bold=True, color=accent,
                anchor=MSO_ANCHOR.MIDDLE)
        textbox(slide, x + 1.8, ly, 3.6, lh, [label], size=13.5, bold=True,
                color=(accent if focus else INK), anchor=MSO_ANCHOR.MIDDLE)
        vrule(slide, x + 5.6, ly + 0.3, lh - 0.6)
        textbox(slide, x + 5.9, ly, mw - 6.3, lh, [body], size=11, color=TEXT_MUTED,
                anchor=MSO_ANCHOR.MIDDLE)
    # 右＝横断要素
    px = x + mw + GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, px, my, PANEL_W, mh, fill=WHITE, line=BORDER, line_w=1.0)
    pad = 0.55
    textbox(slide, px + pad, my + 0.45, PANEL_W - pad * 2, 0.6, [cross[0]], size=13.5, bold=True, color=accent)
    rule(slide, px + pad, my + 1.15, PANEL_W - pad * 2, color=_tint(accent, 0.5))
    items = cross[1]
    iy0 = my + 1.5
    ih = 1.0
    for i, it in enumerate(items):
        yy = iy0 + i * ih
        if i > 0:
            rule(slide, px + pad, yy, PANEL_W - pad * 2)
        textbox(slide, px + pad, yy, PANEL_W - pad * 2, ih, [it], size=12.5, bold=True,
                color=INK, anchor=MSO_ANCHOR.MIDDLE)
    textbox(slide, px + pad, iy0 + len(items) * ih + 0.3, PANEL_W - pad * 2, 1.4,
            [cross[2]], size=10, color=TEXT_MUTED, line_spacing=1.4, anchor=MSO_ANCHOR.TOP)


# ---- 42 RACI・役割分担型 ----------------------------------------------------
def wf_raci(slide, *, lead_text="業務ごとの実行・承認・相談・共有の責任関係を明確にします。",
            headers=("業務・成果物", "責任者", "実行担当", "相談先", "共有先"),
            rows=(("要件の整理", "A", "R", "C", "I"), ("設計・準備", "A", "R", "C", "I"),
                  ("実施・運用", "A", "R", "C", "I"), ("品質の確認", "A", "R", "C", "I"),
                  ("最終承認", "A", "R", "C", "I")),
            hi_col=1, hi_cell=(2, 1),
            legend=(("R", "実行する"), ("A", "最終責任を持つ"), ("C", "相談を受ける"), ("I", "情報共有を受ける")),
            accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    data_table(slide, x, my, mw, mh, headers=headers, rows=rows, hi_col=hi_col,
               hi_cell=hi_cell, col_ratios=(2.2, 1, 1, 1, 1), accent=accent)
    px = x + mw + GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, px, my, PANEL_W, mh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    pad = 0.55
    textbox(slide, px + pad, my + 0.45, PANEL_W - pad * 2, 0.6, ["役割の定義"], size=13.5, bold=True, color=accent)
    rule(slide, px + pad, my + 1.15, PANEL_W - pad * 2, color=_tint(accent, 0.5))
    ly0 = my + 1.5
    lh = (mh - 1.9) / len(legend)
    for i, (k, v) in enumerate(legend):
        yy = ly0 + i * lh
        textbox(slide, px + pad, yy, 1.0, lh, [k], size=13, bold=True,
                color=(accent if k in ("A",) else INK), anchor=MSO_ANCHOR.MIDDLE)
        textbox(slide, px + pad + 1.1, yy, PANEL_W - pad * 2 - 1.1, lh, [v], size=11,
                color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)


# ---- 43 加重評価スコア型 ----------------------------------------------------
def wf_weighted_score(slide, *, lead_text="複数の選択肢を、重要度を加味した共通基準で評価します。",
                      headers=("選択肢", "効果", "実現性", "費用", "速度", "合計"),
                      weights=("", "30%", "25%", "20%", "25%", ""),
                      rows=(("選択肢A", "4", "5", "3", "4", "4.1"), ("選択肢B", "5", "3", "4", "5", "4.3"),
                            ("選択肢C", "3", "4", "5", "3", "3.7"), ("選択肢D", "4", "2", "4", "3", "3.3"),
                            ("選択肢E", "2", "5", "3", "4", "3.5")),
                      hi_col=5, hi_row=1, reco=("推奨案", "選択肢B", "総合得点と重要条件を踏まえた判断理由を入力します。"),
                      accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    data_table(slide, x, my, mw, mh, headers=headers, rows=rows, hi_col=hi_col,
               hi_row=hi_row, sub_headers=weights, col_ratios=(1.5, 1, 1, 1, 1, 1.1), accent=accent)
    px = x + mw + GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, px, my, PANEL_W, mh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    pad = 0.55
    textbox(slide, px + pad, my + 0.5, PANEL_W - pad * 2, 0.5, [reco[0]], size=12.5, bold=True, color=accent)
    textbox(slide, px + pad, my + 1.1, PANEL_W - pad * 2, 1.0, [reco[1]], size=22, bold=True, color=INK)
    rule(slide, px + pad, my + mh * 0.42, PANEL_W - pad * 2, color=_tint(accent, 0.5))
    textbox(slide, px + pad, my + mh * 0.48, PANEL_W - pad * 2, 2.0, [reco[2]], size=11,
            color=TEXT_MUTED, line_spacing=1.5, anchor=MSO_ANCHOR.TOP)


# ---- 44 シナリオ比較型 ------------------------------------------------------
def wf_scenarios(slide, *, lead_text="複数の将来シナリオと、発生条件・対応方針を比較します。",
                 scenarios=(("下振れ", "75"), ("標準", "100"), ("上振れ", "125")),
                 rows=(("前提", "主要な条件を入力"), ("予測値", None), ("兆候", "発生を示すサイン"), ("対応", "取るべき行動")),
                 hi=1, bottom=("切り替え条件", "どの兆候が出たら対応方針を切り替えるかを入力します。"),
                 accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=True)
    n = len(scenarios)
    gap = 0.6
    cw = (w - gap * (n - 1)) / n
    for i, (name, pred) in enumerate(scenarios):
        cx = x + i * (cw + gap)
        focus = i == hi
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, my, cw, mh,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        pad = 0.5
        textbox(slide, cx + pad, my + 0.35, cw - pad * 2, 0.6, [name], size=15, bold=True,
                color=(accent if focus else INK), align=PP_ALIGN.CENTER)
        rule(slide, cx + pad + 0.5, my + 1.05, cw - pad * 2 - 1.0,
             color=_tint(accent, 0.5) if focus else BORDER)
        m = len(rows)
        ry0 = my + 1.4
        rrh = (mh - 1.7) / m
        for r, (label, val) in enumerate(rows):
            ry = ry0 + r * rrh
            textbox(slide, cx + pad, ry, 1.4, rrh, [label], size=10.5, color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)
            vrule(slide, cx + pad + 1.5, ry + rrh * 0.2, rrh * 0.6)
            if label == "予測値":
                textbox(slide, cx + pad + 1.7, ry, cw - pad * 2 - 1.7, rrh, [pred], size=17,
                        bold=True, color=accent, anchor=MSO_ANCHOR.MIDDLE)
            else:
                textbox(slide, cx + pad + 1.7, ry, cw - pad * 2 - 1.7, rrh, [val], size=11,
                        color=INK, anchor=MSO_ANCHOR.MIDDLE)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 45 仮説検証型 ----------------------------------------------------------
def wf_hypothesis(slide, *, lead_text="仮説を肯定・否定する材料を並べ、現時点の判定と次の検証を示します。",
                  hypothesis=("仮説", "検証したい主張や前提を一文で入力します。"),
                  pro=("肯定する材料", ("確認できた事実を入力", "数値や観察結果を入力", "追加の証拠を入力")),
                  con=("否定する材料", ("矛盾する事実を入力", "不足している情報を入力", "別の可能性を入力")),
                  verdict=("判定", "継続検証", "現時点の判断"),
                  bottom=("次に確認すること", "判定を確定するために必要な追加検証を入力します。"),
                  accent=PRIMARY):
    x, my, w, mh = _content(bottom=True, top_extra=-0.7)
    # 仮説バー
    hh = 1.1
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, my, w, hh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, x + 0.5, my, 3.0, hh, [hypothesis[0]], size=13, bold=True, color=accent, anchor=MSO_ANCHOR.MIDDLE)
    vrule(slide, x + 3.4, my + 0.25, hh - 0.5)
    textbox(slide, x + 3.8, my, w - 4.3, hh, [hypothesis[1]], size=14, bold=True, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    # 3ボックス
    by = my + hh + 0.4
    bh = (my + mh) - by
    vw = w * 0.22
    cw = (w - vw - 0.6 * 2) / 2
    for side, (title, items), focus in ((0, pro, True), (1, con, False)):
        cx = x + side * (cw + 0.6)
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, by, cw, bh, fill=WHITE, line=BORDER, line_w=1.0)
        textbox(slide, cx + 0.5, by + 0.35, cw - 1, 0.6, [title], size=14, bold=True,
                color=(accent if focus else INK))
        rule(slide, cx + 0.5, by + 1.05, cw - 1, color=_tint(accent, 0.5) if focus else BORDER)
        textbox(slide, cx + 0.5, by + 1.3, cw - 1, bh - 1.5, ["・" + s for s in items],
                size=11, color=TEXT_MUTED, line_spacing=1.6, anchor=MSO_ANCHOR.TOP)
    vx = x + w - vw
    shape_box(slide, MSO_SHAPE.RECTANGLE, vx, by, vw, bh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, vx, by + 0.4, vw, 0.5, [verdict[0]], size=12, bold=True, color=accent, align=PP_ALIGN.CENTER)
    textbox(slide, vx, by + bh * 0.36, vw, 0.7, [verdict[1]], size=17, bold=True, color=INK, align=PP_ALIGN.CENTER)
    rule(slide, vx + 0.6, by + bh * 0.56, vw - 1.2, color=_tint(accent, 0.5))
    textbox(slide, vx, by + bh * 0.62, vw, 0.5, [verdict[2]], size=10.5, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 41 スイムレーン型 ------------------------------------------------------
def wf_swimlane(slide, *, lead_text="複数の担当者や部門をまたぐ業務と、引き継ぎの流れを整理します。",
                lanes=("担当部門A", "担当部門B", "担当部門C"), steps=5, hi_step=3,
                flow=((0, 0, "受付", False), (0, 1, "確認", False), (1, 1, "処理", False),
                      (1, 2, "承認", True), (2, 2, "反映", True), (2, 3, "共有", False),
                      (0, 4, "完了", False)),
                accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    lc = w * 0.15
    head_h = 1.0
    cw = (w - lc) / steps
    nlane = len(lanes)
    lh = (mh - head_h) / nlane
    # ヘッダ（STEP）
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, my, lc, head_h, fill=WHITE, line=BORDER, line_w=1.0)
    for c in range(steps):
        cx = x + lc + c * cw
        shape_box(slide, MSO_SHAPE.RECTANGLE, cx, my, cw, head_h, fill=WHITE, line=BORDER, line_w=1.0)
        textbox(slide, cx, my, cw, head_h, [f"STEP {c + 1}"], size=10.5, bold=True,
                color=(accent if c == hi_step else TEXT_MUTED), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # レーン
    for r, lane in enumerate(lanes):
        ly = my + head_h + r * lh
        focus = r == 1
        shape_box(slide, MSO_SHAPE.RECTANGLE, x, ly, lc, lh, text=[lane],
                  fill=_tint(accent, 0.92) if focus else SURFACE, line=BORDER, line_w=1.0,
                  size=11.5, bold=True, color=(accent if focus else INK))
        for c in range(steps):
            shape_box(slide, MSO_SHAPE.RECTANGLE, x + lc + c * cw, ly, cw, lh,
                      fill=WHITE, line=BORDER, line_w=0.75)

    def cell_center(r, c):
        return (x + lc + c * cw + cw / 2, my + head_h + r * lh + lh / 2)
    # ボックス配置
    bw, bh = cw * 0.62, lh * 0.5
    pos = {}
    for (r, c, label, f) in flow:
        ccx, ccy = cell_center(r, c)
        pos[(r, c)] = (ccx, ccy)
        shape_box(slide, MSO_SHAPE.RECTANGLE, ccx - bw / 2, ccy - bh / 2, bw, bh, text=[label],
                  fill=_tint(accent, 0.9) if f else WHITE,
                  line=_tint(accent, 0.45) if f else BORDER, line_w=1.0,
                  size=11, bold=True, color=(accent if f else INK))
    # 矢印（フロー順に隣接ボックスを接続）
    for (a, b) in zip(flow, flow[1:]):
        ax, ay = pos[(a[0], a[1])]
        bx, by = pos[(b[0], b[1])]
        connector(slide, ax + bw / 2, ay, bx - bw / 2, by, color=GREY, width=1.2, end_arrow=True)


# ---- 46 ウォーターフォール・増減要因型 -------------------------------------
def wf_waterfall(slide, *, lead_text="開始値から最終値までの増減を、要因別に分解します。",
                 chart_title="前年差の増減要因",
                 steps=(("前年", 100, "base"), ("新規", 18, "up"), ("単価", 10, "up"),
                        ("解約", -12, "down"), ("費用", -8, "down"), ("今年", 108, "total")),
                 panel=("最大の変動要因", "＋18", "増減への寄与が最も大きい要因と、次に取る対応を入力します。"),
                 accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, my, mw, mh, fill=WHITE, line=BORDER, line_w=1.0)
    textbox(slide, x + 0.5, my + 0.3, mw - 1, 0.6, [chart_title], size=12.5, bold=True, color=INK)
    pl, pt, pr, pb = x + 0.7, my + 1.2, x + mw - 0.5, my + mh - 1.0
    vmax = max(abs(v) for _, v, _ in steps) if steps else 1
    tot = max(s[1] for s in steps if s[2] in ("base", "total"))
    vmax = tot * 1.15
    n = len(steps)
    slot = (pr - pl) / n
    bw = slot * 0.5
    cum = 0
    unit = (pb - pt) / vmax
    for i, (name, val, kind) in enumerate(steps):
        bx = pl + i * slot + (slot - bw) / 2
        if kind in ("base", "total"):
            h = val * unit
            top = pb - h
            col = accent if kind == "total" else GREY
            shape_box(slide, MSO_SHAPE.RECTANGLE, bx, top, bw, h, fill=col, line=None)
            cum = val
            lbl = str(val)
            lcol = INK
        else:
            h = abs(val) * unit
            if val >= 0:
                top = pb - (cum + val) * unit
                col = _tint(accent, 0.55)
            else:
                top = pb - cum * unit
                col = GREY
            shape_box(slide, MSO_SHAPE.RECTANGLE, bx, top, bw, h, fill=col, line=None)
            cum += val
            lbl = ("＋" if val > 0 else "") + str(val)
            lcol = accent if val > 0 else TEXT_MUTED
        textbox(slide, bx - 0.4, top - 0.5, bw + 0.8, 0.4, [lbl], size=10.5, bold=True,
                color=lcol, align=PP_ALIGN.CENTER)
        textbox(slide, pl + i * slot, pb + 0.1, slot, 0.4, [name], size=10,
                color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    rule(slide, pl, pb, pr - pl)
    # 右パネル
    px = x + mw + GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, px, my, PANEL_W, mh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    pad = 0.55
    textbox(slide, px + pad, my + 0.5, PANEL_W - pad * 2, 0.6, [panel[0]], size=13, bold=True, color=accent)
    textbox(slide, px + pad, my + 1.2, PANEL_W - pad * 2, 1.3, [panel[1]], size=36, bold=True, color=accent)
    rule(slide, px + pad, my + mh * 0.5, PANEL_W - pad * 2, color=_tint(accent, 0.5))
    textbox(slide, px + pad, my + mh * 0.56, PANEL_W - pad * 2, 2.4, [panel[2]], size=11,
            color=TEXT_MUTED, line_spacing=1.5, anchor=MSO_ANCHOR.TOP)


# ---- 47 構成比変化型 --------------------------------------------------------
def wf_composition_change(slide, *, lead_text="全体に占める各要素の割合が、前後でどう変わったかを示します。",
                          before=(("項目A", 35), ("項目B", 25), ("項目C", 25), ("項目D", 15)),
                          after=(("項目A", 48), ("項目B", 22), ("項目C", 18), ("項目D", 12)),
                          change="項目Aが＋13pt",
                          insight=("変化の示唆", "構成比が変化した理由と、その影響を入力します。"),
                          accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    seg_cols = (accent, _tint(accent, 0.5), GREY, GREY_L)
    lab_w = 1.8
    bar_x = x + lab_w
    bar_w = mw - lab_w
    barh = 1.5

    def stack(rows, yy, label):
        textbox(slide, x, yy, lab_w - 0.2, barh, [label], size=12, bold=True,
                color=(accent if label == "After" else INK), anchor=MSO_ANCHOR.MIDDLE)
        cx = bar_x
        for i, (name, pct) in enumerate(rows):
            seg = bar_w * pct / 100
            col = seg_cols[i % len(seg_cols)]
            shape_box(slide, MSO_SHAPE.RECTANGLE, cx, yy, seg, barh, text=[f"{pct}%"],
                      fill=col, line=WHITE, line_w=1.5, size=11, bold=True,
                      color=WHITE if i < 2 else INK)
            cx += seg
    stack(before, my + 0.3, "Before")
    textbox(slide, bar_x, my + 2.15, bar_w, 0.5, ["↓  " + change], size=12, bold=True,
            color=accent, align=PP_ALIGN.CENTER)
    stack(after, my + 2.9, "After")
    # 凡例
    ly = my + 4.7
    lx = bar_x
    for i, (name, _) in enumerate(before):
        shape_box(slide, MSO_SHAPE.RECTANGLE, lx, ly, 0.35, 0.35, fill=seg_cols[i % 4], line=None)
        textbox(slide, lx + 0.45, ly - 0.05, 2.2, 0.45, [name], size=10, color=TEXT_MUTED)
        lx += 3.0
    insight_panel(slide, x + mw + GUT, my, PANEL_W, mh, blocks=[insight], accent=accent)


# ---- 48 ヒートマップ型 ------------------------------------------------------
def wf_heatmap(slide, *, lead_text="行と列の交点を濃淡で示し、分布の偏りや注目領域を発見します。",
               cols=("区分A", "区分B", "区分C", "区分D", "区分E", "区分F"),
               rows=("項目1", "項目2", "項目3", "項目4", "項目5"),
               values=((1, 2, 3, 2, 1, 2), (2, 3, 4, 3, 2, 1), (1, 2, 5, 4, 3, 2),
                       (2, 1, 3, 2, 4, 3), (1, 2, 2, 3, 2, 1)),
               vmax=5, insight=("注目領域", "最も値が高い交点と、背景にある要因を入力します。"),
               note="重点：項目3 × 区分C", accent=PRIMARY):
    lead(slide, lead_text)
    x, my, w, mh = _content(bottom=False)
    mw = w - PANEL_W - GUT
    lc = mw * 0.16
    ch = 0.9
    ncol = len(cols)
    cw = (mw - lc) / ncol
    rh = (mh - ch) / len(rows)
    for c, cn in enumerate(cols):
        textbox(slide, x + lc + c * cw, my, cw, ch, [cn], size=10.5, bold=True,
                color=INK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    for r, rn in enumerate(rows):
        ry = my + ch + r * rh
        textbox(slide, x, ry, lc - 0.2, rh, [rn], size=10.5, bold=True, color=INK,
                align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
        for c in range(ncol):
            v = values[r][c]
            t = 0.95 - 0.8 * (v / vmax)     # 高いほど濃い
            shape_box(slide, MSO_SHAPE.RECTANGLE, x + lc + c * cw, ry, cw - 0.06, rh - 0.06,
                      text=[str(v)], fill=_tint(accent, t), line=WHITE, line_w=1.5,
                      size=11, bold=True, color=(WHITE if v / vmax > 0.6 else INK), align=PP_ALIGN.CENTER)
    px = x + mw + GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, px, my, PANEL_W, mh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    pad = 0.55
    textbox(slide, px + pad, my + 0.5, PANEL_W - pad * 2, 0.6, [insight[0]], size=13.5, bold=True, color=accent)
    rule(slide, px + pad, my + 1.2, PANEL_W - pad * 2, color=_tint(accent, 0.5))
    textbox(slide, px + pad, my + 1.5, PANEL_W - pad * 2, 2.0, [insight[1]], size=11,
            color=TEXT_MUTED, line_spacing=1.5, anchor=MSO_ANCHOR.TOP)
    textbox(slide, px + pad, my + mh - 1.2, PANEL_W - pad * 2, 0.8, [note], size=11,
            bold=True, color=accent, line_spacing=1.3)


# ---- 49 顧客の声→論点→施策型 -----------------------------------------------
def wf_voice_to_action(slide, *, lead_text="複数の定性情報を共通論点へまとめ、具体的な改善施策へ変換します。",
                       heads=("顧客の声・観察事実", "共通論点", "改善施策"),
                       voices=("代表的な発言や観察結果を入力します。",) * 3,
                       issues=("論点 1", "論点 2", "論点 3"),
                       actions=(("施策 A", "具体的な改善内容を入力"), ("施策 B", "具体的な改善内容を入力"),
                                ("施策 C", "具体的な改善内容を入力")),
                       hi_row=1, bottom=("優先する改善", "複数の声に共通し、効果が大きい施策を入力します。"),
                       accent=PRIMARY):
    lead(slide, lead_text, )
    x, my, w, mh = _content(bottom=True, top_extra=0.2)
    cw = (w - 1.4) / 3
    xs = [x, x + cw + 0.7, x + (cw + 0.7) * 2]
    textbox(slide, xs[0], my - 0.7, cw, 0.5, [heads[0]], size=13, bold=True, color=INK)
    textbox(slide, xs[1], my - 0.7, cw, 0.5, [heads[1]], size=13, bold=True, color=INK, align=PP_ALIGN.CENTER)
    textbox(slide, xs[2], my - 0.7, cw, 0.5, [heads[2]], size=13, bold=True, color=accent)
    n = 3
    rh = mh / n
    bh = rh - 0.35
    for r in range(n):
        ry = my + r * rh
        focus = r == hi_row
        # 声
        shape_box(slide, MSO_SHAPE.RECTANGLE, xs[0], ry, cw, bh, fill=WHITE, line=BORDER, line_w=1.0)
        textbox(slide, xs[0] + 0.35, ry + 0.2, 0.6, 0.6, ["“"], size=20, bold=True, color=_tint(accent, 0.3))
        textbox(slide, xs[0] + 0.95, ry + 0.3, cw - 1.3, bh - 0.5, [voices[r]], size=10,
                color=TEXT_MUTED, line_spacing=1.4, anchor=MSO_ANCHOR.MIDDLE)
        # 論点
        shape_box(slide, MSO_SHAPE.RECTANGLE, xs[1], ry, cw, bh,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0,
                  text=[issues[r]], size=13, bold=True, color=(accent if focus else INK))
        # 施策
        shape_box(slide, MSO_SHAPE.RECTANGLE, xs[2], ry, cw, bh,
                  fill=_tint(accent, 0.92) if focus else WHITE,
                  line=_tint(accent, 0.45) if focus else BORDER, line_w=1.0)
        textbox(slide, xs[2] + 0.4, ry + 0.3, cw - 0.8, 0.4, [actions[r][0]], size=9.5,
                bold=True, color=(accent if focus else TEXT_MUTED))
        textbox(slide, xs[2] + 0.4, ry + 0.75, cw - 0.8, bh - 1.0, [actions[r][1]], size=11.5,
                bold=True, color=INK)
        # コネクタ
        connector(slide, xs[0] + cw, ry + bh / 2, xs[1], ry + bh / 2, color=GREY, width=1.0)
        connector(slide, xs[1] + cw, ry + bh / 2, xs[2], ry + bh / 2, color=GREY, width=1.0)
    bottom_bar(slide, bottom[0], bottom[1], accent=accent)


# ---- 50 KPIダッシュボード型 -------------------------------------------------
def wf_kpi_dashboard(slide, *, lead_text="複数の主要指標を一画面で確認し、異常と次の対応を把握します。",
                     kpis=(("売上", "1.25億", "＋8%"), ("顧客数", "2,480", "＋120"),
                           ("転換率", "32%", "−2pt"), ("継続率", "86%", "＋4pt")),
                     trend_title="主要KPIの推移", trend_cats=("1月", "2月", "3月", "4月", "5月", "6月"),
                     trend=(58, 64, 71, 69, 78, 84),
                     watch=(("転換率", "目標を2pt下回る"), ("新規顧客", "増加ペースが鈍化"),
                            ("継続率", "改善傾向を維持")),
                     accent=PRIMARY):
    lead(slide, lead_text)
    x, _, w, _ = _content()
    kw = w / len(kpis)
    ky = LEAD_Y + LEAD_H + 0.25
    kh = 1.7
    for i, (name, val, dl) in enumerate(kpis):
        kx = x + i * kw
        if i > 0:
            vrule(slide, kx, ky + 0.1, kh - 0.2)
        textbox(slide, kx + 0.3, ky, kw - 0.4, 0.5, [name], size=11, color=TEXT_MUTED)
        textbox(slide, kx + 0.3, ky + 0.5, kw - 0.4, 1.0, [val], size=24, bold=True, color=accent)
        textbox(slide, kx + 0.3, ky + 1.4, kw - 0.4, 0.35, [dl], size=11, bold=True, color=TEXT_MUTED)
    by = ky + kh + 0.4
    bh = ZB - by
    mw = w - 7.6 - GUT
    shape_box(slide, MSO_SHAPE.RECTANGLE, x, by, mw, bh, fill=WHITE, line=BORDER, line_w=1.0)
    textbox(slide, x + 0.5, by + 0.3, mw - 1, 0.6, [trend_title], size=12.5, bold=True, color=INK)
    linechart(slide, x + 0.5, by + 1.1, mw - 1.0, bh - 1.6, cats=trend_cats, vals=list(trend),
              ymax=100, accent=accent)
    px = x + mw + GUT
    pw = 7.6
    shape_box(slide, MSO_SHAPE.RECTANGLE, px, by, pw, bh, fill=_tint(accent, 0.92),
              line=_tint(accent, 0.45), line_w=1.0)
    textbox(slide, px + 0.5, by + 0.35, pw - 1.0, 0.6, ["確認が必要な項目"], size=13, bold=True, color=accent)
    rule(slide, px + 0.5, by + 1.05, pw - 1.0, color=_tint(accent, 0.5))
    wy = by + 1.3
    wh = (bh - 1.5) / len(watch)
    for i, (name, note) in enumerate(watch):
        yy = wy + i * wh
        textbox(slide, px + 0.5, yy, 2.4, wh, [name], size=11, bold=True, color=INK, anchor=MSO_ANCHOR.MIDDLE)
        textbox(slide, px + 3.0, yy, pw - 3.5, wh, [note], size=10.5, color=TEXT_MUTED, anchor=MSO_ANCHOR.MIDDLE)
        if i < len(watch) - 1:
            rule(slide, px + 0.5, yy + wh, pw - 1.0, color=_tint(accent, 0.5))
