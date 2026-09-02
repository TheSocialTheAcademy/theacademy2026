"""ページ型ライブラリ（型テンプレ集 v0.4・全28型の関数化）。

HANDOFF.md §9 タスクC。型テンプレ集（docs/catalog/course-slide-templates.html）の
A/B/C/D 全28型を「1型＝1関数」で実装する。content.txt の 【型名】 ブロックから
フィールドを渡して呼び分ける（判定表は .claude/skills/slides-gen/SKILL.md）。

規約:
- 各関数は `def type_name(prs, *, ...fields): return slide`。本文型は内部で
  `configure_body(section_label, title)` を張ってからコンテンツを描く。
- 描画は slides.py / diagrams.py のビルダー経由（→ validate() 自動登録）。色は
  ブランド定数のみ。コンテンツは y=3.0〜12.8 / x=1.07〜24.33 の矩形内。
- 表紙(A1)は prs.slides[0] を update_cover で書き換える特別扱い。章扉(A3)は L_CHAPTER。

RENDERERS でコード(A1/C10 等)・和名(コース表紙/コード解説 等)の双方から関数を引ける。
render(prs, key, fields) が薄いディスパッチャ。
"""
from pathlib import Path

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from slides import (
    PRIMARY, PRIMARY_LIGHT, SECONDARY, SUCCESS, DANGER, HIGHLIGHT,
    TEXT, TEXT_MUTED, BORDER, SURFACE, WHITE, T_H2,
    CHART_ACCENT, CHART_INK, CHART_GREY, CHART_GREY_L,
    L_BODY, L_CHAPTER, SLIDE_W_CM, RGBColor,
    textbox, shape_box, card, callout, connector, picture,
    bar_chart, line_chart, pie_chart,
    configure_body, configure_chapter, update_cover,
)
from diagrams import (
    _tint, _lab_sub,
    diagram_flow_h, diagram_flow_v, diagram_steps, diagram_before_after,
    diagram_table, diagram_code, diagram_conversation, diagram_image_explain,
    diagram_ui_steps, diagram_formula, diagram_group, diagram_cycle,
    diagram_pyramid, diagram_ranking, diagram_timeline,
)

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
LOGO_WHITE = ASSETS / "academy_logo_white.png"

X0, ZONE_W = 1.07, 23.26
LEAD_Y = 3.05
SLIDE_H_CM = 14.29


# ---------------------------------------------------------------- 共通ヘルパー
def _list(v):
    """"a｜b｜c" / "a|b|c" / list / None を list[str] に正規化。"""
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return list(v)
    for sep in ("｜", "|", "\n"):
        if sep in v:
            return [p.strip() for p in v.split(sep) if p.strip()]
    return [v]


def _pairs(v):
    """"見出し=説明｜..." → [(見出し, 説明), ...]。list of (a,b) もそのまま通す。"""
    out = []
    for item in _list(v):
        if isinstance(item, (list, tuple)):
            out.append((item[0], item[1] if len(item) > 1 else ""))
        elif "=" in item:
            k, _, val = item.partition("=")
            out.append((k.strip(), val.strip()))
        else:
            out.append((item, ""))
    return out


def _body(prs, section, title):
    s = prs.slides.add_slide(prs.slide_layouts[L_BODY])
    configure_body(s, section_label=section, title=title)
    return s


def _lead(s, text):
    if text:
        textbox(s, X0, LEAD_Y, ZONE_W, 0.62, [text], size=11.5, color=TEXT)


def _conclusion(s, text, *, y=11.05, accent=PRIMARY):
    if text:
        callout(s, X0, y, ZONE_W, 1.2, text, accent=accent)


# ================================================================ A: コース全体
def course_cover(prs, *, title, subtitle="", meta=None, **_):
    """A1 コース表紙。テンプレ表紙(slide0)のテキストを書き換える。"""
    lines = [{"text": title, "size": 30, "bold": True, "color": WHITE}]
    if subtitle:
        lines.append({"text": subtitle, "size": 16, "color": WHITE})
    for m in _list(meta):
        lines.append({"text": m, "size": 11, "color": WHITE})
    update_cover(prs.slides[0], lines=lines)
    return prs.slides[0]


def curriculum(prs, *, title="コースの全体像", items, section="CURRICULUM ／ 目次", **_):
    """A2 カリキュラム／目次。items=[(章タイトル, 概要), ...] を2カラムの番号付きで。"""
    s = _body(prs, section, title)
    chapters = _pairs(items)
    n = len(chapters)
    cols = 2 if n > 4 else 1
    rows = (n + cols - 1) // cols
    gap = 0.5
    cw = (ZONE_W - gap * (cols - 1)) / cols
    ch = (8.6 - gap * (rows - 1)) / rows
    for i, (t, sub) in enumerate(chapters):
        c, r = i % cols, i // cols
        x = X0 + c * (cw + gap)
        y = 3.5 + r * (ch + gap)
        shape_box(s, MSO_SHAPE.RECTANGLE, x, y, cw, ch,
                  fill=SURFACE, line=BORDER, line_w=0.8)
        badge = min(ch * 0.7, 1.15)
        shape_box(s, MSO_SHAPE.ROUNDED_RECTANGLE,
                  x + 0.3, y + (ch - badge) / 2, badge, badge, text=[f"{i + 1:02d}"],
                  fill=PRIMARY, line=None, size=13, bold=True, color=WHITE)
        textbox(s, x + badge + 0.6, y + 0.15, cw - badge - 0.9, 0.75, [t],
                size=13, bold=True, color=TEXT)
        if sub:
            textbox(s, x + badge + 0.6, y + 0.9, cw - badge - 0.9, ch - 1.05, [sub],
                    size=10, color=TEXT_MUTED, line_spacing=1.3)
    return s


def chapter_cover(prs, *, num, title="", goals, course_name="", icon="ph:book-open",
                  illust=None, **_):
    """A3 チャプター扉。全面ブルー地・ロゴ・Chapterピル・「学べること：」。

    illust に soco-st 検索語を渡すと、右側の白パネル内にカラーイラストを主役配置する
    （併用方針：soco-st＝章扉・修了の主役）。未指定なら従来の淡い ph: トピックアイコン。
    """
    from pptx.enum.shapes import MSO_SHAPE
    from slides import add_icon
    s = prs.slides.add_slide(prs.slide_layouts[L_CHAPTER])
    shape_box(s, MSO_SHAPE.RECTANGLE, -0.3, -0.3, SLIDE_W_CM + 0.6, SLIDE_H_CM + 0.6,
              fill=PRIMARY, line=None)
    placed = False
    if illust:
        try:
            import soco
            # 右側に白の丸角パネル → その中にカラーイラスト（青地との干渉を避ける）
            shape_box(s, MSO_SHAPE.ROUNDED_RECTANGLE, 16.0, 3.2, 8.2, 8.0,
                      fill=WHITE, line=None)
            placed = soco.soco_place(s, illust, 16.7, 3.9, 6.8, 6.6, variant="paint")
        except Exception:
            placed = False
    if not placed:
        try:
            add_icon(s, icon, 16.4, 2.6, size=12.2, color="#3A66DE")
        except Exception:
            pass
    if LOGO_WHITE.exists():
        picture(s, str(LOGO_WHITE), 1.3, 0.95, w=5.4)
    cname = course_name or title
    textbox(s, 1.3, 3.7, 15.0, 3.2, [cname, "COURSE"], size=33, bold=True,
            color=WHITE, line_spacing=1.04)
    label = f"CHAPTER {num}" if str(num).isdigit() else str(num)
    pill = shape_box(s, MSO_SHAPE.ROUNDED_RECTANGLE, 1.3, 7.55, 5.4, 1.15,
                     text=[label], fill=WHITE, line=None, size=15, bold=True,
                     color=PRIMARY)
    try:
        pill.adjustments[0] = 0.5
    except Exception:
        pass
    textbox(s, 1.3, 9.25, 15.0, 0.6, ["このチャプターで学べること："], size=12, color=WHITE)
    textbox(s, 1.55, 9.95, 15.0, 2.6, [f"・{g}" for g in _list(goals)], size=11.5,
            color=WHITE, line_spacing=1.45)
    return s


# ================================================================ B: 導入
def lesson_cover(prs, *, title, subtitle="", section="LESSON", lead="", **_):
    """B1 レッスン表紙。本文レイアウトを使い、大きなタイトルで章の入口を示す。"""
    s = _body(prs, section, title)
    from pptx.enum.shapes import MSO_SHAPE
    shape_box(s, MSO_SHAPE.RECTANGLE, X0, 4.2, ZONE_W, 6.4,
              fill=_tint(PRIMARY, 0.94), line=None)
    textbox(s, X0 + 1.0, 5.4, ZONE_W - 2.0, 2.0, [title], size=28, bold=True,
            color=PRIMARY, line_spacing=1.1)
    if subtitle:
        textbox(s, X0 + 1.0, 7.6, ZONE_W - 2.0, 1.0, [subtitle], size=15,
                color=TEXT)
    if lead:
        textbox(s, X0 + 1.0, 8.7, ZONE_W - 2.0, 1.4, [lead], size=12,
                color=TEXT_MUTED, line_spacing=1.5)
    return s


def objectives(prs, *, title="このレッスンの目標", goals, section="OBJECTIVES ／ 学習目標",
               lead="", **_):
    """B2 学習目標。goals を達成イメージの箇条で。標準フローでは章扉に内蔵する型。"""
    from pptx.enum.shapes import MSO_SHAPE
    s = _body(prs, section, title)
    _lead(s, lead)
    gl = _list(goals)
    n = len(gl)
    gap = 0.35
    rh = (7.6 - gap * (n - 1)) / n
    for i, g in enumerate(gl):
        y = 4.0 + i * (rh + gap)
        shape_box(s, MSO_SHAPE.RECTANGLE, X0, y, ZONE_W, rh,
                  fill=SURFACE, line=BORDER, line_w=0.8)
        badge = min(rh * 0.62, 0.95)
        shape_box(s, MSO_SHAPE.OVAL, X0 + 0.35, y + (rh - badge) / 2, badge, badge,
                  text=["✓"], fill=SUCCESS, line=None, size=13, bold=True, color=WHITE)
        textbox(s, X0 + badge + 0.75, y, ZONE_W - badge - 1.1, rh, [g], size=13,
                color=TEXT, anchor=MSO_ANCHOR.MIDDLE)
    return s


def motivation(prs, *, title, lead="", points, section="WHY ／ なぜ学ぶのか",
               conclusion="", icons=None, **_):
    """B3 導入・動機づけ。学ぶ理由・得られる変化を3点程度のカードで。

    icons に "ph:xxx｜…" を渡すと、各カードの見出し左にアクセントアイコンを1つ置く
    （強調したい文章＝見出しの横にアイコン、という方針）。数は points に合わせて割当。
    """
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR
    s = _body(prs, section, title)
    _lead(s, lead)
    pts = _pairs(points)
    ic = _list(icons)
    n = len(pts)
    gap = 0.6
    cw = (ZONE_W - gap * (n - 1)) / n
    for i, (t, sub) in enumerate(pts):
        x = X0 + i * (cw + gap)
        if ic:
            # カード背景＋見出し左にアイコン（強調点の横）＋本文
            box = shape_box(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 4.2, cw, 5.6,
                            fill=WHITE, line=BORDER, line_w=0.75)
            try:
                box.adjustments[0] = 0.05
            except Exception:
                pass
            placed = False
            try:
                from slides import add_icon
                add_icon(s, ic[i % len(ic)], x + 0.6, 4.75, size=1.15, color="#0141D4")
                placed = True
            except Exception:
                pass
            tx = x + (2.05 if placed else 0.6)
            textbox(s, tx, 4.8, cw - (tx - x) - 0.5, 1.1, [t], size=15, bold=True,
                    color=TEXT, anchor=MSO_ANCHOR.MIDDLE)
            textbox(s, x + 0.6, 6.35, cw - 1.2, 3.0, [sub], size=11.5,
                    color=TEXT_MUTED, line_spacing=1.5)
        else:
            card(s, x, 4.2, cw, 5.6, chip=str(i + 1), title=t, body=sub)
    _conclusion(s, conclusion)
    return s


def prerequisites(prs, *, title="前提知識・用語", terms, section="PREREQUISITES ／ 前提",
                  lead="", **_):
    """B4 前提知識・用語。terms=[(用語, 説明), ...] を表で整理。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    rows = [[t, d] for t, d in _pairs(terms)]
    diagram_table(s, X0, 3.95, ZONE_W, 7.6, headers=["用語", "意味"],
                  col_widths=[1, 2.4], rows=rows)
    return s


# ================================================================ C: 本編
def concept(prs, *, title, lead="", flow=None, conclusion="",
            section="CONCEPT ／ 概念", **_):
    """C1 概念解説。定義＋横フローで「部品」を見せる。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    steps = [_lab_sub(x) for x in _pairs(flow)] if flow else []
    if steps:
        diagram_flow_h(s, X0, 5.4, ZONE_W, 3.4, steps=steps)
    _conclusion(s, conclusion)
    return s


def steps_page(prs, *, title, lead="", items, conclusion="",
               section="HOW-TO ／ 手順", **_):
    """C2 手順・ステップ。items=[(見出し, 説明), ...] を段階カード＋矢印で。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    diagram_steps(s, X0, 4.0, ZONE_W, 6.6, steps=_pairs(items))
    _conclusion(s, conclusion)
    return s


def example(prs, *, title, lead="", scenario="", points=None, conclusion="",
            section="EXAMPLE ／ 具体例", **_):
    """C3 具体例・ケース。走る事例を1つ提示し、要点を添える。"""
    from pptx.enum.shapes import MSO_SHAPE
    s = _body(prs, section, title)
    _lead(s, lead)
    if scenario:
        callout(s, X0, 3.95, ZONE_W, 1.5, scenario, accent=HIGHLIGHT)
    pts = _list(points)
    if pts:
        n = len(pts)
        gap = 0.5
        cw = (ZONE_W - gap * (n - 1)) / n
        for i, p in enumerate(pts):
            card(s, X0 + i * (cw + gap), 5.9, cw, 4.0, chip=str(i + 1), body=p)
    _conclusion(s, conclusion)
    return s


def comparison(prs, *, title, lead="", headers, rows, conclusion="",
               section="COMPARE ／ 比較", **_):
    """C4 比較・選択。表で複数案を並べて比較。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    body_rows = [_list(r) for r in _list(rows)] if not isinstance(rows[0], (list, tuple)) else rows
    diagram_table(s, X0, 3.95, ZONE_W, 7.0, headers=_list(headers), rows=body_rows)
    _conclusion(s, conclusion)
    return s


def data(prs, *, title, lead="", chart="bar", categories, series=None, values=None,
         conclusion="", section="DATA ／ データ", **_):
    """C5 データ・エビデンス。棒/折れ線/円グラフで数値を示す。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    cats = _list(categories)
    cy, ch = 4.1, 6.4
    if chart == "pie":
        from pptx.enum.shapes import MSO_SHAPE
        vals = [float(v) for v in _list(values)]
        # 太リング＋左寄せ配置。ラベルはグラフ上に載せず、右に凡例で数字を整列（文字とのバランス）
        pie_chart(s, X0, cy, 10.5, ch, categories=cats, values=vals, hole_size=52,
                  show_percentage=False)
        total = sum(vals) or 1
        ramp = [CHART_ACCENT, CHART_INK, CHART_GREY, CHART_GREY_L, SECONDARY, TEXT_MUTED]
        lx, lw = X0 + 11.6, ZONE_W - 11.6
        n = len(cats); rh = min(1.05, 5.6 / max(n, 1)); ly = cy + (ch - rh * n) / 2
        for i, (c, v) in enumerate(zip(cats, vals)):
            y = ly + i * rh
            shape_box(s, MSO_SHAPE.RECTANGLE, lx, y + rh / 2 - 0.16, 0.32, 0.32,
                      fill=ramp[i % len(ramp)], line=None)
            textbox(s, lx + 0.6, y, lw - 3.2, rh, [c], size=12, color=TEXT,
                    anchor=__import__("pptx").enum.text.MSO_ANCHOR.MIDDLE)
            textbox(s, lx + lw - 2.6, y, 2.6, rh, [f"{v/total*100:.0f}%"], size=13,
                    bold=True, color=PRIMARY, align=__import__("pptx").enum.text.PP_ALIGN.RIGHT,
                    anchor=__import__("pptx").enum.text.MSO_ANCHOR.MIDDLE)
    elif chart == "line":
        line_chart(s, X0, cy, ZONE_W, ch, categories=cats, series=series or [])
    else:
        bar_chart(s, X0, cy, ZONE_W, ch, categories=cats, series=series or [])
    _conclusion(s, conclusion)
    return s


def structure(prs, *, title, lead="", groups=None, cycle=None, pyramid=None,
              conclusion="", section="STRUCTURE ／ 構造", **_):
    """C6 構造・関係図。groups/cycle/pyramid のいずれかで関係を図解。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    if cycle:
        diagram_cycle(s, X0 + 3, 3.95, ZONE_W - 6, 6.6, items=_pairs(cycle))
    elif pyramid:
        diagram_pyramid(s, X0 + 3, 3.95, ZONE_W - 6, 6.6, levels=_pairs(pyramid))
    else:
        diagram_group(s, X0, 3.95, ZONE_W, 6.8,
                      groups=[(t, _list(m)) for t, m in _pairs(groups)])
    _conclusion(s, conclusion)
    return s


def pitfalls(prs, *, title, lead="", bad, good, section="CAUTION ／ よくある失敗", **_):
    """C7 よくある失敗・注意。左＝失敗(注意色)／右＝こうする(成功色)。赤は使わない。"""
    from pptx.enum.shapes import MSO_SHAPE
    s = _body(prs, section, title)
    _lead(s, lead)
    diagram_before_after(s, X0, 3.95, ZONE_W, 7.2,
                         before={"title": "よくある失敗", "items": _list(bad)},
                         after={"title": "こうする", "items": _list(good)})
    return s


def image_explain(prs, *, title, lead="", image=None, heading="", bullets,
                  side="left", section="VISUAL ／ 図版解説", **_):
    """C8 画像・図版＋解説。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    diagram_image_explain(s, X0, 4.0, ZONE_W, 6.6, image=image, side=side,
                          heading=heading or title, bullets=_list(bullets))
    return s


def ui_guide(prs, *, title, lead="", image=None, pins, steps, section="UI ／ 操作ガイド", **_):
    """C9 画面操作・UIガイド。スクショ＋番号ピン＋手順。pins は "x,y｜x,y" 形式可。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    pin_list = []
    for p in _list(pins):
        if isinstance(p, (list, tuple)):
            pin_list.append((float(p[0]), float(p[1])))
        else:
            a, _, b = p.partition(",")
            pin_list.append((float(a), float(b)))
    diagram_ui_steps(s, X0, 4.0, ZONE_W, 6.6, image=image, pins=pin_list,
                     steps=_list(steps))
    return s


def code_explain(prs, *, title, lead="", code, code_title=None, highlight=None,
                 notes=None, section="CODE ／ コード解説", **_):
    """C10 コード解説。暗色コードブロック＋行ハイライト＋注釈。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    hi = [int(x) for x in _list(highlight)] if highlight else None
    note_map = {}
    for n, t in _pairs(notes):
        try:
            note_map[int(n)] = t
        except ValueError:
            pass
    diagram_code(s, X0, 3.95, ZONE_W, 7.4, lines=_list(code), title=code_title,
                 highlight=hi, notes=note_map or None)
    return s


def parallel_text(prs, *, title, lead="", pairs, section="EXAMPLE ／ 例文・対訳", **_):
    """C11 例文・対訳。pairs=[(原文, 訳), ...] を2列表で。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    rows = [[a, b] for a, b in _pairs(pairs)]
    diagram_table(s, X0, 3.95, ZONE_W, 7.4, headers=["原文", "対訳"],
                  col_widths=[1, 1], rows=rows, align_first_left=True)
    return s


def dialog(prs, *, title, lead="", turns, section="DIALOG ／ 会話", **_):
    """C12 会話・ダイアログ。turns=[(話者, 台詞, side), ...]。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    parsed = []
    for t in _list(turns):
        if isinstance(t, (list, tuple)):
            parsed.append(tuple(t))
        else:
            parts = [p.strip() for p in t.split(":")]
            if len(parts) >= 2:
                parsed.append((parts[0], parts[1], parts[2] if len(parts) > 2 else None))
    diagram_conversation(s, X0, 3.95, ZONE_W, 7.4, turns=parsed)
    return s


def grammar(prs, *, title, lead="", terms, ops=None, examples=None,
            conclusion="", section="GRAMMAR ／ 文法・構文", **_):
    """C13 文法・構文パターン。部品ボックスを ＋/＝ でつなぎ、例文を添える。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    diagram_formula(s, X0, 4.0, ZONE_W, 3.0, terms=_pairs(terms), ops=_list(ops) or None)
    ex = _list(examples)
    if ex:
        textbox(s, X0, 7.6, ZONE_W, 0.6, ["例文"], size=11, bold=True, color=PRIMARY)
        textbox(s, X0, 8.25, ZONE_W, 2.5, [f"・{e}" for e in ex], size=12,
                color=TEXT, line_spacing=1.55)
    _conclusion(s, conclusion)
    return s


def vocabulary(prs, *, title="語彙・用語リスト", lead="", words,
               section="VOCABULARY ／ 語彙", **_):
    """C14 語彙・用語リスト。words=[(語, 意味, 例), ...]（例は任意）を表で。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    rows, has_ex = [], False
    for item in _list(words):
        if isinstance(item, (list, tuple)):
            row = list(item)
        else:
            row = [p.strip() for p in item.split("=")]
        if len(row) > 2:
            has_ex = True
        rows.append(row)
    if has_ex:
        rows = [(r + ["", ""])[:3] for r in rows]
        diagram_table(s, X0, 3.95, ZONE_W, 7.4, headers=["語", "意味", "例"],
                      col_widths=[1, 1.6, 1.6], rows=rows)
    else:
        rows = [(r + [""])[:2] for r in rows]
        diagram_table(s, X0, 3.95, ZONE_W, 7.4, headers=["語", "意味"],
                      col_widths=[1, 2.2], rows=rows)
    return s


def format_template(prs, *, title="テンプレート・書式", lead="", template,
                    fill_ins=None, section="TEMPLATE ／ 書式", **_):
    """C15 テンプレート・書式。穴埋め書式をコードブロックで提示。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    hi = [int(x) for x in _list(fill_ins)] if fill_ins else None
    diagram_code(s, X0, 3.95, ZONE_W, 7.4, lines=_list(template),
                 title="コピーして使える型", highlight=hi)
    return s


# ================================================================ D: 締め
def exercise(prs, *, title="やってみよう", lead="", task, hints=None, conclusion="",
             section="WORK ／ 実践", **_):
    """D1 ワーク・実践。取り組む課題＋ヒント。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    callout(s, X0, 3.95, ZONE_W, 1.8, task, accent=PRIMARY)
    hl = _list(hints)
    if hl:
        n = len(hl)
        gap = 0.5
        cw = (ZONE_W - gap * (n - 1)) / n
        for i, h in enumerate(hl):
            card(s, X0 + i * (cw + gap), 6.2, cw, 3.6, kicker=f"HINT {i + 1}", body=h)
    _conclusion(s, conclusion)
    return s


def quiz(prs, *, title="理解チェック", question, options, answer=None, explanation="",
         section="CHECK ／ 理解チェック", **_):
    """D2 理解チェック。設問＋選択肢（正解を成功色で）＋解説。"""
    from pptx.enum.shapes import MSO_SHAPE
    s = _body(prs, section, title)
    callout(s, X0, 3.55, ZONE_W, 1.5, question, accent=HIGHLIGHT)
    opts = _list(options)
    n = len(opts)
    gap = 0.3
    rh = (4.4 - gap * (n - 1)) / n
    letters = "ABCDEFGH"
    for i, o in enumerate(opts):
        y = 5.4 + i * (rh + gap)
        correct = answer is not None and str(answer).strip().upper() in (letters[i], str(i + 1))
        # 正解＝アクセント青で強調（ブランド統一。緑は使わない）／不正解＝淡グレー
        fill = _tint(PRIMARY, 0.85) if correct else SURFACE
        line = PRIMARY if correct else BORDER
        shape_box(s, MSO_SHAPE.RECTANGLE, X0, y, ZONE_W, rh, fill=fill, line=line, line_w=0.9)
        badge = min(rh * 0.7, 0.9)
        shape_box(s, MSO_SHAPE.OVAL, X0 + 0.3, y + (rh - badge) / 2, badge, badge,
                  text=[letters[i]], fill=(PRIMARY if correct else TEXT_MUTED), line=None,
                  size=12, bold=True, color=WHITE)
        textbox(s, X0 + badge + 0.7, y, ZONE_W - badge - 1.0, rh, [o], size=12,
                color=TEXT, anchor=MSO_ANCHOR.MIDDLE)
    if explanation:
        _conclusion(s, explanation, accent=PRIMARY)
    return s


def checklist(prs, *, title="チェックリスト", lead="", items, section="CHECKLIST ／ 確認", **_):
    """D3 チェックリスト。チェックボックス付きの確認項目。"""
    from pptx.enum.shapes import MSO_SHAPE
    s = _body(prs, section, title)
    _lead(s, lead)
    its = _list(items)
    n = len(its)
    gap = 0.32
    rh = (7.8 - gap * (n - 1)) / n
    for i, it in enumerate(its):
        y = 3.95 + i * (rh + gap)
        shape_box(s, MSO_SHAPE.RECTANGLE, X0, y, ZONE_W, rh, fill=SURFACE,
                  line=BORDER, line_w=0.8)
        box = min(rh * 0.55, 0.7)
        shape_box(s, MSO_SHAPE.RECTANGLE, X0 + 0.4, y + (rh - box) / 2, box, box,
                  text=["✓"], fill=WHITE, line=PRIMARY, line_w=1.5, size=12,
                  bold=True, color=PRIMARY)
        textbox(s, X0 + box + 0.8, y, ZONE_W - box - 1.2, rh, [it], size=12,
                color=TEXT, anchor=MSO_ANCHOR.MIDDLE)
    return s


def summary(prs, *, title="まとめ", lead="", points, takeaway="",
            section="SUMMARY ／ まとめ", **_):
    """D4 まとめ。要点を番号付きで整理し、最後に一言。"""
    from pptx.enum.shapes import MSO_SHAPE
    s = _body(prs, section, title)
    _lead(s, lead)
    pts = _list(points)
    n = len(pts)
    gap = 0.35
    rh = (6.6 - gap * (n - 1)) / n
    for i, p in enumerate(pts):
        y = 3.95 + i * (rh + gap)
        badge = min(rh * 0.7, 0.95)
        shape_box(s, MSO_SHAPE.ROUNDED_RECTANGLE, X0, y + (rh - badge) / 2, badge, badge,
                  text=[str(i + 1)], fill=PRIMARY, line=None, size=13, bold=True, color=WHITE)
        textbox(s, X0 + badge + 0.5, y, ZONE_W - badge - 0.8, rh, [p], size=13,
                color=TEXT, anchor=MSO_ANCHOR.MIDDLE)
    if takeaway:
        _conclusion(s, takeaway)
    return s


def next_up(prs, *, title="次回予告・さらに学ぶ", lead="", next_topic="", resources=None,
            section="NEXT ／ 次に進む", **_):
    """D5 次回予告・さらに学ぶ。次のテーマ＋発展リソース。"""
    s = _body(prs, section, title)
    _lead(s, lead)
    if next_topic:
        callout(s, X0, 3.95, ZONE_W, 1.8, next_topic, accent=PRIMARY)
    res = _list(resources)
    if res:
        textbox(s, X0, 6.2, ZONE_W, 0.6, ["さらに学ぶ"], size=12, bold=True, color=PRIMARY)
        n = len(res)
        gap = 0.5
        cw = (ZONE_W - gap * (n - 1)) / n
        for i, r in enumerate(res):
            card(s, X0 + i * (cw + gap), 6.95, cw, 3.0, body=r)
    return s


def complete(prs, *, title="修了おめでとうございます", lead="", message="", cta="",
             illust=None, section="COMPLETE ／ 修了", **_):
    """D6 修了・行動喚起。ねぎらい＋次の一歩の後押し。

    illust に soco-st 検索語を渡すと、パネル上部に主役イラストを配置する（併用方針）。
    """
    from pptx.enum.shapes import MSO_SHAPE
    s = _body(prs, section, title)
    _lead(s, lead)
    shape_box(s, MSO_SHAPE.RECTANGLE, X0, 4.2, ZONE_W, 5.2,
              fill=_tint(PRIMARY, 0.92), line=None)
    msg_y, cta_y = 5.0, 7.6
    if illust:
        try:
            import soco
            if soco.soco_place(s, illust, X0 + ZONE_W / 2 - 1.5, 4.55, 3.0, 2.2, variant="paint"):
                msg_y, cta_y = 6.9, 8.5
        except Exception:
            pass
    textbox(s, X0 + 1.0, msg_y, ZONE_W - 2.0, 1.7, [message or title], size=20,
            bold=True, color=PRIMARY, align=PP_ALIGN.CENTER, line_spacing=1.2)
    if cta:
        textbox(s, X0 + 1.0, cta_y, ZONE_W - 2.0, 1.0, [cta], size=13, color=TEXT,
                align=PP_ALIGN.CENTER)
    return s


# ================================================================ ディスパッチャ
RENDERERS = {
    # コード（型テンプレ集の idx）
    "A1": course_cover, "A2": curriculum, "A3": chapter_cover,
    "B1": lesson_cover, "B2": objectives, "B3": motivation, "B4": prerequisites,
    "C1": concept, "C2": steps_page, "C3": example, "C4": comparison,
    "C5": data, "C6": structure, "C7": pitfalls, "C8": image_explain,
    "C9": ui_guide, "C10": code_explain, "C11": parallel_text, "C12": dialog,
    "C13": grammar, "C14": vocabulary, "C15": format_template,
    "D1": exercise, "D2": quiz, "D3": checklist, "D4": summary,
    "D5": next_up, "D6": complete,
    # 和名（content.txt の 【型名】）
    "コース表紙": course_cover, "カリキュラム": curriculum, "目次": curriculum,
    "チャプター扉": chapter_cover, "レッスン表紙": lesson_cover, "学習目標": objectives,
    "導入": motivation, "動機づけ": motivation, "前提知識": prerequisites, "前提": prerequisites,
    "概念解説": concept, "概念": concept, "手順": steps_page, "ステップ": steps_page,
    "具体例": example, "ケース": example, "比較": comparison, "選択": comparison,
    "データ": data, "エビデンス": data, "構造": structure, "関係図": structure,
    "よくある失敗": pitfalls, "注意": pitfalls, "画像解説": image_explain, "図版": image_explain,
    "画面操作": ui_guide, "UIガイド": ui_guide, "コード解説": code_explain, "コード": code_explain,
    "例文": parallel_text, "対訳": parallel_text, "会話": dialog, "ダイアログ": dialog,
    "文法": grammar, "構文": grammar, "語彙": vocabulary, "用語リスト": vocabulary,
    "テンプレート": format_template, "書式": format_template,
    "ワーク": exercise, "実践": exercise, "理解チェック": quiz, "クイズ": quiz,
    "チェックリスト": checklist, "まとめ": summary, "次回予告": next_up, "さらに学ぶ": next_up,
    "修了": complete, "行動喚起": complete,
}


def render(prs, key, fields):
    """型キー（idx or 和名）でページ関数を呼ぶ。未知キーは KeyError。"""
    fn = RENDERERS[key.strip()]
    return fn(prs, **fields)


# ================================================================ 本編ワイヤー50型（wireframes.py 接続）
# wireframes.py の wf_*(slide, ...) は「見出し設定済みの本文 slide」に本文ゾーンだけ描く。
# ここでは _body(prs, section, title) で見出し込みの本文スライドを起こしてから wf_* を呼ぶ
# ラッパを生成し、idx（W01..W50）・型名（和名）・wf 関数名の3系統で RENDERERS から引けるようにする。
# 見出し（section/title）は fields で上書き可。それ以外の fields は wf_* にそのまま渡す。
import wireframes as _wf  # noqa: E402  (slides/diagrams のみ依存・循環なし)

# (idx, 型名=和名キー, wf関数, 既定セクションラベル, 既定タイトル)
_WF_SPEC = [
    ("W01", "データ＋示唆", _wf.wf_data_insight, "01 ／ データ＋示唆型", "データから示唆を導く"),
    ("W02", "左右比較", _wf.wf_compare_lr, "02 ／ 左右比較型", "2つを並べて比較する"),
    ("W03", "結論＋3つの根拠", _wf.wf_conclusion_reasons, "03 ／ 結論＋3つの根拠型", "結論を3つの根拠で支える"),
    ("W04", "課題・原因・解決", _wf.wf_problem_cause_solution, "04 ／ 課題・原因・解決型", "課題から解決策までを示す"),
    ("W05", "プロセス・手順", _wf.wf_process_steps, "05 ／ プロセス・手順型", "全体の流れを手順で示す"),
    ("W06", "重要数値＋推移", _wf.wf_kpi_trend, "06 ／ 重要数値＋推移グラフ型", "成果とその変化を示す"),
    ("W07", "全体数値＋内訳", _wf.wf_total_breakdown, "07 ／ 全体数値＋内訳型", "全体を内訳に分解する"),
    ("W08", "マトリクス", _wf.wf_matrix, "08 ／ マトリクス型", "2軸で対象を位置づける"),
    ("W09", "時系列・変化", _wf.wf_timeline_change, "09 ／ 時系列・変化型", "過去から将来への変化"),
    ("W10", "全体像・構造分解", _wf.wf_structure_decompose, "10 ／ 全体像・構造分解型", "仕組みを構成要素に分ける"),
    ("W11", "事例・成果", _wf.wf_case_result, "11 ／ 事例・成果型", "事例と成果を示す"),
    ("W12", "問い＋回答", _wf.wf_question_answer, "12 ／ 問い＋回答型", "問いに答える"),
    ("W13", "1メッセージ", _wf.wf_one_message, "13 ／ 1メッセージ型", "一文で強く伝える"),
    ("W14", "重要数値単独", _wf.wf_kpi_single, "14 ／ 重要数値単独型", "1つの数値で印象づける"),
    ("W15", "Before／After", _wf.wf_before_after, "15 ／ Before／After型", "変化の前後を並べる"),
    ("W16", "メリット・デメリット", _wf.wf_pros_cons, "16 ／ メリット・デメリット型", "良い点と注意点を並べる"),
    ("W17", "選択肢比較表", _wf.wf_options_table, "17 ／ 選択肢比較表型", "選択肢を同じ軸で比較する"),
    ("W18", "ランキング", _wf.wf_ranking, "18 ／ ランキング型", "順位順に整理して示す"),
    ("W19", "ファネル", _wf.wf_funnel, "19 ／ ファネル型", "段階ごとの減少を可視化する"),
    ("W20", "ピラミッド・階層", _wf.wf_pyramid_levels, "20 ／ ピラミッド・階層型", "優先順位や階層を整理する"),
    ("W21", "循環・サイクル", _wf.wf_cycle, "21 ／ 循環・サイクル型", "繰り返す改善の循環を示す"),
    ("W22", "ロードマップ", _wf.wf_roadmap, "22 ／ ロードマップ型", "段階と各時期の施策を示す"),
    ("W23", "判断フロー", _wf.wf_decision_flow, "23 ／ 判断フロー型", "条件に応じた判断を示す"),
    ("W24", "因果関係", _wf.wf_causality, "24 ／ 因果関係型", "原因から結果までを示す"),
    ("W25", "相関・関係図", _wf.wf_relation, "25 ／ 相関・関係図型", "中心と周囲の関係を示す"),
    ("W26", "カスタマージャーニー", _wf.wf_journey, "26 ／ カスタマージャーニー型", "顧客の段階ごとの体験"),
    ("W27", "計画対実績", _wf.wf_plan_actual, "27 ／ 計画対実績型", "計画と実績の差を確認する"),
    ("W28", "ギャップ分析", _wf.wf_gap, "28 ／ ギャップ分析型", "現状と理想の差を埋める"),
    ("W29", "表＋示唆", _wf.wf_table_insight, "29 ／ 表＋示唆型", "表に読み取りポイントを添える"),
    ("W30", "リスク＋対策", _wf.wf_risk_action, "30 ／ リスク＋対策型", "リスクと対策をセットで示す"),
    ("W31", "優先順位", _wf.wf_priority, "31 ／ 優先順位型", "取り組む順番を決める"),
    ("W32", "まとめ＋次アクション", _wf.wf_summary_actions, "32 ／ まとめ＋次のアクション型", "要点と次の行動を示す"),
    ("W33", "並列グラフ比較", _wf.wf_dual_charts, "33 ／ 並列グラフ比較型", "2つのグラフを並べて読む"),
    ("W34", "重点方針＋実行構造", _wf.wf_policy_execution, "34 ／ 重点方針＋実行構造型", "方針と実行構造を示す"),
    ("W35", "ロジックツリー", _wf.wf_logic_tree, "35 ／ ロジックツリー型", "課題を分解して整理する"),
    ("W36", "KPIドライバー", _wf.wf_kpi_driver, "36 ／ KPIドライバー型", "目標と施策をつなげる"),
    ("W37", "戦略カスケード", _wf.wf_strategy_cascade, "37 ／ 戦略カスケード型", "目標を段階的に落とし込む"),
    ("W38", "同心円・対象範囲", _wf.wf_concentric_scope, "38 ／ 同心円・対象範囲型", "対象範囲を包含関係で示す"),
    ("W39", "ベン図・重なり", _wf.wf_venn, "39 ／ ベン図・重なり型", "共通点と交点の価値を示す"),
    ("W40", "レイヤー・基盤構造", _wf.wf_layers, "40 ／ レイヤー・基盤構造型", "下位が上位を支える構造"),
    ("W41", "スイムレーン", _wf.wf_swimlane, "41 ／ スイムレーン型", "部門をまたぐ業務の流れ"),
    ("W42", "RACI・役割分担", _wf.wf_raci, "42 ／ RACI・役割分担型", "責任関係を明確にする"),
    ("W43", "加重評価スコア", _wf.wf_weighted_score, "43 ／ 加重評価スコア型", "重要度を加味して評価する"),
    ("W44", "シナリオ比較", _wf.wf_scenarios, "44 ／ シナリオ比較型", "将来シナリオを比較する"),
    ("W45", "仮説検証", _wf.wf_hypothesis, "45 ／ 仮説検証型", "肯定・否定材料で判定する"),
    ("W46", "ウォーターフォール", _wf.wf_waterfall, "46 ／ ウォーターフォール型", "増減を要因別に分解する"),
    ("W47", "構成比変化", _wf.wf_composition_change, "47 ／ 構成比変化型", "割合の前後変化を示す"),
    ("W48", "ヒートマップ", _wf.wf_heatmap, "48 ／ ヒートマップ型", "分布の偏りを濃淡で示す"),
    ("W49", "顧客の声→論点→施策", _wf.wf_voice_to_action, "49 ／ 顧客の声→論点→施策型", "定性情報を施策へ変換する"),
    ("W50", "KPIダッシュボード", _wf.wf_kpi_dashboard, "50 ／ KPIダッシュボード型", "主要指標を一画面で確認する"),
]


def _make_wf_page(wf_fn, def_section, def_title):
    """wf_*(slide, ...) を pages 流儀の page(prs, ...) に変換するラッパを返す。"""
    def page(prs, *, section=def_section, title=def_title, **fields):
        s = _body(prs, section, title)
        wf_fn(s, **fields)
        return s
    page.__name__ = wf_fn.__name__ + "_page"
    page.__doc__ = f"本編ワイヤー型 {wf_fn.__name__}。既定見出し『{def_section} / {def_title}』。"
    return page


WF_RENDERERS = {}
for _idx, _name, _fn, _sec, _ttl in _WF_SPEC:
    _page = _make_wf_page(_fn, _sec, _ttl)
    for _k in (_idx, _name, _fn.__name__):
        WF_RENDERERS[_k] = _page

# 28型を優先しつつ本編50型を合流（万一の和名衝突は 28 型側を残す）。
for _k, _v in WF_RENDERERS.items():
    RENDERERS.setdefault(_k, _v)
