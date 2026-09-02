"""WF化チャート：グラフ集の各グラフを WF 流儀の誌面に構成する。

グラフ集はグラフのみなので、周辺のテキスト位置まで型で用意する：
    番号｜型名（小・見出し帯） → 大タイトル → リード1行
    ┌─ 主ビジュアル（左・枠付き＋グラフ見出し）─┐  ┌─ 示唆パネル（右）─┐
    └──────────────────────┘  └──────────┘
    出典・注釈（小・下）

チャート本体は wireframes.py（vbars/hbars/linechart/data_table）と slides.py（pie/bar）を
再利用。1本/1点だけアクセント・残りグレーの集ルールを踏襲。
"""
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

import wireframes as wf
from slides import (
    L_BODY, configure_body, textbox, shape_box, pie_chart, bar_chart,
    TEXT, TEXT_MUTED, BORDER, PRIMARY, WHITE,
    CHART_INK, CHART_GREY, CHART_GREY_L,
)

X0, ZW, PANEL_W = wf.X0, wf.ZW, wf.PANEL_W
MAIN_W = ZW - PANEL_W - 0.6
PANEL_X = X0 + MAIN_W + 0.6
MY, MH = 4.35, 7.15
# 主ビジュアル内側（グラフ描画域）
IX, IY = X0 + 0.6, MY + 1.2
IW, IH = MAIN_W - 1.2, MH - 2.0


def frame(prs, kicker, title, lead, *, insight=None, footnote="", chart_title="",
          framed=True):
    """WF 誌面の外枠（見出し・リード・示唆パネル・出典）を敷き、主ビジュアル域を返す。"""
    s = prs.slides.add_slide(prs.slide_layouts[L_BODY])
    configure_body(s, section_label=kicker, title=title)
    wf.lead(s, lead)
    if framed:
        shape_box(s, MSO_SHAPE.RECTANGLE, X0, MY, MAIN_W, MH, fill=None,
                  line=BORDER, line_w=1.0)
    if chart_title:
        textbox(s, IX, MY + 0.3, IW, 0.6, [chart_title], size=13, bold=True, color=TEXT)
    if insight:
        wf.insight_panel(s, PANEL_X, MY, PANEL_W, MH, blocks=insight)
    if footnote:
        textbox(s, X0, 11.95, ZW, 0.5, [footnote], size=9, color=TEXT_MUTED)
    return s


# ============================================================ 円・ドーナツ（C）
def wf_donut(prs, *, kicker, title, lead, categories, values, hole=55, center=None,
             center_unit="", insight=None, footnote="", chart_title=""):
    """C1/C3 ドーナツ。center を渡すと中央数字。1扇アクセント・残りグレー。"""
    s = frame(prs, kicker, title, lead, insight=insight, footnote=footnote,
              chart_title=chart_title, framed=True)
    d = min(IW, IH) * 0.98
    dx = IX + (IW - d) / 2
    dy = IY + (IH - d) / 2
    pie_chart(s, dx, dy, d, d, categories=categories, values=values,
              hole_size=hole, highlight=0)
    if center is not None:
        textbox(s, dx, dy + d / 2 - 0.9, d, 1.3, [str(center)], size=40, bold=True,
                color=TEXT, align=PP_ALIGN.CENTER)
        if center_unit:
            textbox(s, dx, dy + d / 2 + 0.35, d, 0.6, [center_unit], size=13,
                    color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    return s


# ============================================================ 横棒（B）降順
def wf_hbar(prs, *, kicker, title, lead, rows, hi=0, insight=None, footnote="",
            chart_title=""):
    """B1 降順横棒。rows=[(label, value), ...]（大きい順で渡す）。hi を強調。"""
    s = frame(prs, kicker, title, lead, insight=insight, footnote=footnote,
              chart_title=chart_title, framed=True)
    wf.hbars(s, IX, IY, IW, IH, rows=rows, hi=hi)
    return s


# ============================================================ 縦棒（V）時系列
def wf_vbar(prs, *, kicker, title, lead, cats, vals, hi=None, legend=None,
            insight=None, footnote="", chart_title=""):
    """V1 時系列・単系列＋直近強調。hi の1本を強調。"""
    s = frame(prs, kicker, title, lead, insight=insight, footnote=footnote,
              chart_title=chart_title, framed=True)
    if hi is None:
        hi = len(vals) - 1
    wf.vbars(s, IX, IY, IW, IH, cats=cats, vals=vals, hi=hi, legend=legend)
    return s


# ============================================================ 折れ線（T）
def wf_line(prs, *, kicker, title, lead, cats, vals, end_label=None, insight=None,
            footnote="", chart_title=""):
    """T1 単線＋線末ラベル。"""
    s = frame(prs, kicker, title, lead, insight=insight, footnote=footnote,
              chart_title=chart_title, framed=True)
    wf.linechart(s, IX, IY, IW, IH, cats=cats, vals=vals, accent=CHART_INK)
    if end_label:
        textbox(s, IX + IW - 3.0, IY - 0.1, 3.0, 0.8, [str(end_label)], size=18,
                bold=True, color=TEXT, align=PP_ALIGN.RIGHT)
    return s


# ============================================================ 積み上げ（S）
def wf_stacked(prs, *, kicker, title, lead, categories, series, pct=False,
               insight=None, footnote="", chart_title=""):
    """S1/S2 積み上げ縦棒。series=[(名, [値,...]), ...]。pct=True で 100%積み上げ相当。"""
    s = frame(prs, kicker, title, lead, insight=insight, footnote=footnote,
              chart_title=chart_title, framed=True)
    bar_chart(s, IX, IY, IW, IH, categories=categories, series=series, stacked=True,
              colors=[CHART_INK, CHART_GREY, CHART_GREY_L], number_format="#,##0",
              gap_width=90)
    return s


# ============================================================ ウォーターフォール（W）
def wf_waterfall(prs, *, kicker, title, lead, steps, insight=None, footnote="",
                 chart_title=""):
    """W1 増減分解。steps=[(label, value, kind)]。kind: 'base'/'up'/'down'。"""
    s = frame(prs, kicker, title, lead, insight=insight, footnote=footnote,
              chart_title=chart_title, framed=True)
    n = len(steps)
    vmax = max(abs(v) for _, v, _ in steps) or 1
    # 累積の高さを積む（base は床から、up/down は浮く）
    plot_x, plot_y = IX + 0.3, IY + 0.2
    plot_w, plot_h = IW - 0.6, IH - 0.9
    slot = plot_w / n
    bw = min(slot * 0.55, 1.6)
    run = 0.0
    base_run = None
    for i, (lab, val, kind) in enumerate(steps):
        if kind == "base":
            top = val
            bottom = 0
            run = val
        elif kind == "up":
            bottom = run
            top = run + val
            run = top
        else:  # down
            top = run
            bottom = run - val
            run = bottom
        by_top = plot_y + plot_h * (1 - top / (vmax))
        by_bot = plot_y + plot_h * (1 - bottom / (vmax))
        col = CHART_INK if kind in ("base", "up") else CHART_GREY
        if kind == "base":
            col = PRIMARY if i == n - 1 else CHART_INK
        bx = plot_x + i * slot + (slot - bw) / 2
        shape_box(s, MSO_SHAPE.RECTANGLE, bx, min(by_top, by_bot), bw,
                  abs(by_bot - by_top), fill=col, line=None)
        textbox(s, plot_x + i * slot, plot_y + plot_h + 0.05, slot, 0.45, [str(lab)],
                size=9, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
        textbox(s, bx - 0.3, min(by_top, by_bot) - 0.5, bw + 0.6, 0.4,
                [("＋" if kind == "up" else "−" if kind == "down" else "") + str(val)],
                size=9.5, bold=True, color=(col if kind != "base" else TEXT),
                align=PP_ALIGN.CENTER)
    return s
