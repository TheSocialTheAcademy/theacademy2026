"""spreads.py — 誌面（スプレッド）構成。**内容に合わせて変える側**のライブラリ。

`editorial.py` が統一する7項目（書体の方向性・本文色・アクセント色・余白の感覚・
罫線の太さ・注釈の扱い・編集トーン）を必ず経由しつつ、そのうえで次の10項目を
**構成ごとに変える**。

    見出しの位置／カラム数と幅／数値の見せ方／図解の有無／写真の有無／
    余白の位置／本文の密度／要素の大きさ／情報の読み順／主役となる要素

各構成は `(slide, Signature)` を返す。`Signature` は「何を変えたか」の宣言で、
`audit.py` が実際の pptx から同じ軸を再計測して突き合わせる。

## 選び方

`choose(content, history)` は **内容の形**（数値が1つか／推移か／工程か／対応表か／
写真があるか／本文量）から構成を決める。順番でローテーションしない＝同じ資料でも
内容が変われば構成が変わり、内容が似ていれば直近と違う構成を選ぶ。

    from spreads import render_all
    render_all(prs, [
        {"section": "OVERVIEW ／ 全体像", "title": "…", "lead": "…",
         "body": ["…", "…"], "note": ["…"]},
        {"section": "PROCESS ／ 工程", "title": "…", "steps": [("受付", "…"), …]},
    ])
"""
from __future__ import annotations

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from slides import L_BODY, configure_body, textbox, shape_box, picture
import editorial as ed
from editorial import (
    GRID, INK, INK_SUB, HAIR, SCALE,
    baseline, space, rule, vrule, kicker, heading, lead, body, caption,
    figure, note, plane, Signature,
)
from ediagrams import (
    edia_process, edia_connection, edia_load, edia_change, edia_correspondence,
)

__all__ = ["SPREADS", "choose", "render", "render_all",
           "sp_statement", "sp_lead_and_void", "sp_two_voices", "sp_figure_first",
           "sp_process_band", "sp_correspondence_page", "sp_load_report",
           "sp_change_note", "sp_photo_frame", "sp_connection_map"]


# ---------------------------------------------------------------- 共通
def _page(prs, content):
    """本文レイアウトのページを起こす（chrome はテンプレ継承のまま触らない）。"""
    s = prs.slides.add_slide(prs.slide_layouts[L_BODY])
    configure_body(s, section_label=content.get("section", ""),
                   title=content.get("title", ""))
    return s


def _lines(v):
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return [str(i) for i in v if str(i).strip()]
    return [str(v)] if str(v).strip() else []


def _density_for(lines):
    """本文量から密度を決める（密度もページごとに変える対象）。"""
    chars = sum(len(t) for t in lines)
    if chars > 300 or len(lines) > 5:
        return "dense"
    if chars < 90:
        return "sparse"
    return "normal"


def _room(y, content):
    """y から誌面の足まで、本文に使える高さ（注釈のぶんを残す）。"""
    reserve = space(2.6) if _lines(content.get("note")) else space(0.6)
    return max(ed.FIELD_B - y - reserve, space(2))


# ---------------------------------------------------------------- 注釈は誌面の足に置く
def _foot(s, x, w, items):
    """注釈を誌面の下端に揃えて置く（扱いは全ページ共通・位置だけ変える）。"""
    items = _lines(items)
    if not items:
        return
    lines = ([f"{ed.NOTE_MARK}{i + 1} {t}" for i, t in enumerate(items)]
             if len(items) > 1 else [f"{ed.NOTE_MARK} {items[0]}"])
    h = ed.fit_h(lines, w, ed.NOTE_SIZE, ls=1.4) + space(0.45)
    n = int((ed.FIELD_B - h - ed.FIELD["y"]) / ed.BASE)
    ed.note(s, x, baseline(max(n, 0)), w, items)


# ================================================================ 1メッセージ
def sp_statement(prs, content):
    """主役＝1文。余白を下に大きく残し、罫線1本だけで支える。

    読み順は上から下の1本道。要素の大きさの差を最大にする（文字量の差で見せる）。
    """
    s = _page(prs, content)
    x, w = GRID.span(0, 9)
    msg = content.get("statement") or _lines(content.get("body"))[0]
    y = heading(s, x, baseline(2), w, msg, size=SCALE["display"])
    y = ed.after(y, gap=2)
    rule(s, x, y, GRID.span(0, 4)[1], weight="accent")
    if content.get("lead"):
        body(s, x, ed.after(y, gap=2), GRID.span(0, 6)[1],
             _lines(content["lead"]), density="sparse", color=INK_SUB)
    fx, fw = GRID.span(0, 6)
    _foot(s, fx, fw, content.get("note"))
    return s, Signature(head_pos="left-upper", columns="9", number="none",
                        diagram=False, photo=False, void="bottom-right",
                        density="sparse", hero="text", order="tb",
                        scale="contrast")


# ================================================================ リード＋大きな余白
def sp_lead_and_void(prs, content):
    """左に本文、右は**あえて空ける**。注釈だけが右下に降りてくる構成。"""
    s = _page(prs, content)
    lx, lw = GRID.span(0, 7)
    rx, rw = GRID.span(8, 4)
    y = baseline(0)
    if content.get("kicker"):
        y = ed.after(kicker(s, lx, y, lw, content["kicker"]), gap=2)
    y = ed.after(lead(s, lx, y, lw, content.get("lead", "")), gap=2)
    rule(s, lx, y, lw, weight="structure")
    lines = _lines(content.get("body"))
    by = ed.after(y, gap=2)
    body(s, lx, by, lw, lines, density=_density_for(lines),
         fit_to=_room(by, content))
    if content.get("aside"):
        # 右は本文を置かず、短い補足を下寄せで1つだけ（余白を情報の区切りに使う）
        caption(s, rx, baseline(13), rw, content["aside"])
    _foot(s, rx, rw, content.get("note"))
    return s, Signature(head_pos="left-top", columns="6:4", number="none",
                        diagram=False, photo=False, void="right",
                        density=_density_for(lines), hero="text", order="tb",
                        scale="even")


# ================================================================ 非対称2段
def sp_two_voices(prs, content):
    """非対称2段（広い本文＋狭い補足）。段の境は細い縦罫1本だけ。"""
    s = _page(prs, content)
    (lx, lw), (rx, rw) = GRID.split(7, 4)
    lines = _lines(content.get("body"))
    dens = _density_for(lines)
    y = baseline(0)
    if content.get("lead"):
        y = ed.after(lead(s, lx, y, lw, content["lead"]), gap=2)
    y = ed.after(heading(s, lx, y, lw,
                         content.get("head", content.get("title", ""))), gap=1)
    rule(s, lx, y, lw, weight="rule")
    by = ed.after(y, gap=2)
    body(s, lx, by, lw, lines, density=dens, fit_to=_room(by, content))
    vrule(s, rx - space(0.7), baseline(1), space(13), weight="thin")
    ry = baseline(1)
    for h_, t_ in _pairs(content.get("aside_blocks")):
        ry = ed.after(kicker(s, rx, ry, rw, h_, accent=False), gap=1)
        ry = ed.after(body(s, rx, ry, rw, _lines(t_), density="dense",
                           color=INK_SUB), gap=2)
    _foot(s, lx, lw, content.get("note"))
    return s, Signature(head_pos="left-mid", columns="7:4", number="none",
                        diagram=False, photo=False, void="right-bottom",
                        density=dens, hero="text", order="lr", scale="even")


# ================================================================ 数値が主役
def sp_figure_first(prs, content):
    """主役＝1つの数値。左に大きく数値、右に解釈。見出しは右上に小さく置く。"""
    s = _page(prs, content)
    nx, nw = GRID.span(0, 4)
    tx, tw = GRID.span(5, 7)
    y = figure(s, nx, baseline(2), nw, content.get("value", ""),
               unit=content.get("unit", ""), label=content.get("value_label", ""),
               size=SCALE["hero"])
    y = ed.after(y, gap=2)
    rule(s, nx, y, nw, weight="accent")
    if content.get("value_sub"):
        caption(s, nx, ed.after(y, gap=2), nw, content["value_sub"])
    ty = baseline(0)
    if content.get("kicker"):
        ty = ed.after(kicker(s, tx, ty, tw, content["kicker"], accent=False), gap=2)
    ty = ed.after(heading(s, tx, ty, tw,
                          content.get("head", content.get("title", ""))), gap=2)
    lines = _lines(content.get("body"))
    body(s, tx, ty, tw, lines, density=_density_for(lines),
         fit_to=_room(ty, content))
    _foot(s, nx, GRID.span(0, 7)[1], content.get("note"))
    return s, Signature(head_pos="right-top", columns="4:7", number="hero",
                        diagram=False, photo=False, void="left-bottom",
                        density=_density_for(lines), hero="number", order="lr",
                        scale="contrast")


# ================================================================ 工程図が主役
def sp_process_band(prs, content):
    """主役＝工程図。図を上段いっぱいに敷き、見出しと解釈を**下段**に置く。"""
    s = _page(prs, content)
    x, w = GRID.span(0, 12)
    edia_process(s, x, baseline(1), w, space(9),
                 steps=content.get("steps", []),
                 accent_at=content.get("accent_at"))
    rule(s, x, baseline(12), w, weight="rule")
    (hx, hw), (bx, bw) = GRID.split(4, 7)
    heading(s, hx, baseline(13), hw, content.get("head", content.get("title", "")))
    lines = _lines(content.get("body"))
    body(s, bx, baseline(13), bw, lines, density="dense")
    _foot(s, hx, hw, content.get("note"))
    return s, Signature(head_pos="bottom-left", columns="12/4:7", number="none",
                        diagram=True, photo=False, void="top-right",
                        density="normal", hero="diagram", order="tb",
                        scale="contrast")


# ================================================================ 対応関係
def sp_correspondence_page(prs, content):
    """主役＝対応関係の図。表を先に読ませ、問いと注釈を右の狭い段に置く。"""
    s = _page(prs, content)
    (mx, mw), (qx, qw) = GRID.split(8, 3)
    edia_correspondence(s, mx, baseline(1), mw, space(16),
                        pairs=content.get("pairs", []),
                        left_head=content.get("left_head", ""),
                        right_head=content.get("right_head", ""),
                        accent_at=content.get("accent_at"))
    y = baseline(1)
    if content.get("kicker"):
        y = ed.after(kicker(s, qx, y, qw, content["kicker"], accent=False), gap=2)
    y = ed.after(heading(s, qx, y, qw,
                         content.get("head", content.get("title", ""))), gap=2)
    if content.get("lead"):
        body(s, qx, y, qw, _lines(content["lead"]), density="dense",
             color=INK_SUB, fit_to=_room(y, content))
    _foot(s, qx, qw, content.get("note"))
    return s, Signature(head_pos="right-top", columns="8:3", number="none",
                        diagram=True, photo=False, void="right-bottom",
                        density="dense", hero="diagram", order="lr",
                        scale="contrast")


# ================================================================ 負荷
def sp_load_report(prs, content):
    """主役＝負荷図。数値は図の中で読ませ、右に一段だけ解釈を置く。"""
    s = _page(prs, content)
    (gx, gw), (tx, tw) = GRID.split(8, 3)
    lead(s, gx, baseline(0), gw, content.get("lead", ""))
    edia_load(s, gx, baseline(4), gw, space(12),
              items=content.get("load", []),
              unit=content.get("unit", ""),
              capacity=content.get("capacity"),
              capacity_label=content.get("capacity_label", "上限"))
    px_, pw_ = GRID.span(8, 4)          # 溝ごと1列ぶん広い面（右へ寄せた区切り）
    plane(s, px_, baseline(2), pw_, space(11), tone="plain")
    ty = ed.after(kicker(s, tx, baseline(3), tw,
                         content.get("aside_head", "READING"), accent=False), gap=1)
    body(s, tx, ty, tw, _lines(content.get("body")), density="dense")
    _foot(s, gx, gw, content.get("note"))
    return s, Signature(head_pos="left-top", columns="8:3", number="inline",
                        diagram=True, photo=False, void="bottom", density="dense",
                        hero="diagram", order="lr", scale="contrast")


# ================================================================ 変化
def sp_change_note(prs, content):
    """主役＝変化。図は右に寄せ、左に解釈を積む（読み順は左→右に折り返す）。"""
    s = _page(prs, content)
    (tx, tw), (gx, gw) = GRID.split(4, 7)
    y = baseline(0)
    if content.get("kicker"):
        y = ed.after(kicker(s, tx, y, tw, content["kicker"]), gap=2)
    y = ed.after(heading(s, tx, y, tw,
                         content.get("head", content.get("title", ""))), gap=2)
    lines = _lines(content.get("body"))
    body(s, tx, y, tw, lines, density=_density_for(lines), fit_to=_room(y, content))
    edia_change(s, gx + space(1.2), baseline(2), gw - space(2.4), space(12),
                points=content.get("points", []),
                unit=content.get("unit", ""),
                delta_label=content.get("delta_label", "変化"))
    _foot(s, tx, GRID.span(0, 8)[1], content.get("note"))
    return s, Signature(head_pos="left-top", columns="4:7", number="chart",
                        diagram=True, photo=False, void="left-bottom",
                        density=_density_for(lines), hero="diagram", order="zig",
                        scale="contrast")


# ================================================================ 接続
def sp_connection_map(prs, content):
    """主役＝接続図。上に問い、下いっぱいに関係図。余白は上に寄せる。"""
    s = _page(prs, content)
    x, w = GRID.span(0, 12)
    hx, hw = GRID.span(0, 5)
    heading(s, hx, baseline(0), hw,
            content.get("head", content.get("title", "")), size=SCALE["head"])
    if content.get("lead"):
        cx_, cw_ = GRID.span(6, 6)
        caption(s, cx_, baseline(1), cw_, content["lead"])
    rule(s, x, baseline(4), w, weight="hair")
    edia_connection(s, x, baseline(5), w, space(13),
                    core=content.get("core", ""),
                    core_sub=content.get("core_sub", ""),
                    nodes=content.get("nodes", []),
                    side=content.get("side", "right"))
    fx, fw = GRID.span(7, 5)
    _foot(s, fx, fw, content.get("note"))
    return s, Signature(head_pos="left-top", columns="12", number="none",
                        diagram=True, photo=False, void="top-right",
                        density="sparse", hero="diagram", order="radial",
                        scale="contrast")


# ================================================================ 写真
def sp_photo_frame(prs, content):
    """主役＝写真。片側に大きく置き、本文は狭い段に落とす（左右は内容で選ぶ）。"""
    s = _page(prs, content)
    side = content.get("side", "left")
    if side == "left":
        (px, pw), (tx, tw) = GRID.split(7, 4)
    else:
        (tx, tw), (px, pw) = GRID.split(4, 7)
    ph = space(14)
    img = content.get("image")
    if img:
        picture(s, img, px, baseline(1), w=pw)
    else:
        # 写真が無いときは枠だけを置く（ベタ塗りのダミー面を作らない）
        shape_box(s, MSO_SHAPE.RECTANGLE, px, baseline(1), pw, ph,
                  fill=None, line=HAIR, line_w=ed.RULE["thin"])
        textbox(s, px, baseline(1) + ph / 2 - space(0.6), pw, space(1.2),
                [content.get("image_placeholder", "写真")],
                size=SCALE["note"], color=INK_SUB, align=PP_ALIGN.CENTER)
    if content.get("photo_caption"):
        caption(s, px, ed.after(baseline(1) + ph, gap=1), pw,
                content["photo_caption"])
    ty = baseline(1)
    if content.get("kicker"):
        ty = ed.after(kicker(s, tx, ty, tw, content["kicker"]), gap=2)
    ty = ed.after(heading(s, tx, ty, tw,
                          content.get("head", content.get("title", ""))), gap=2)
    lines = _lines(content.get("body"))
    body(s, tx, ty, tw, lines, density=_density_for(lines),
         fit_to=_room(ty, content))
    _foot(s, tx, tw, content.get("note"))
    return s, Signature(head_pos="right-top" if side == "left" else "left-top",
                        columns="7:4" if side == "left" else "4:7",
                        number="none", diagram=False, photo=True,
                        void="bottom", density=_density_for(lines),
                        hero="photo", order="lr", scale="contrast")


def _pairs(v):
    """[("見出し","本文"), ...] / ["見出し=本文", ...] を正規化する。"""
    out = []
    src = list(v or []) if isinstance(v, (list, tuple)) else _lines(v)
    for item in src:
        if isinstance(item, (list, tuple)):
            out.append((str(item[0]), item[1] if len(item) > 1 else ""))
        else:
            k, _, t = str(item).partition("=")
            out.append((k.strip(), t.strip()))
    return out


# ============================================================================
# 構成の選択（順番のローテーションではなく、内容の形で選ぶ）
# ============================================================================

SPREADS = {
    "statement": sp_statement,
    "lead_and_void": sp_lead_and_void,
    "two_voices": sp_two_voices,
    "figure_first": sp_figure_first,
    "process_band": sp_process_band,
    "correspondence": sp_correspondence_page,
    "load_report": sp_load_report,
    "change_note": sp_change_note,
    "connection_map": sp_connection_map,
    "photo_frame": sp_photo_frame,
}

# 構成が宣言する Signature（choose の重複回避に使う代表値）。
_REPRESENTATIVE = {
    "statement": Signature(head_pos="left-upper", columns="9", hero="text",
                           density="sparse", void="bottom-right", order="tb",
                           scale="contrast"),
    "lead_and_void": Signature(head_pos="left-top", columns="6:4", hero="text",
                               void="right", order="tb"),
    "two_voices": Signature(head_pos="left-mid", columns="7:4", hero="text",
                            void="right-bottom", order="lr"),
    "figure_first": Signature(head_pos="right-top", columns="4:7", number="hero",
                              hero="number", void="left-bottom", order="lr",
                              scale="contrast"),
    "process_band": Signature(head_pos="bottom-left", columns="12/4:7",
                              diagram=True, hero="diagram", void="top-right",
                              order="tb", scale="contrast"),
    "correspondence": Signature(head_pos="right-top", columns="8:3", diagram=True,
                                hero="diagram", void="right-bottom", order="lr",
                                density="dense", scale="contrast"),
    "load_report": Signature(head_pos="left-top", columns="8:3", number="inline",
                             diagram=True, hero="diagram", void="bottom",
                             density="dense", order="lr", scale="contrast"),
    "change_note": Signature(head_pos="left-top", columns="4:7", number="chart",
                             diagram=True, hero="diagram", void="left-bottom",
                             order="zig", scale="contrast"),
    "connection_map": Signature(head_pos="left-top", columns="12", diagram=True,
                                hero="diagram", void="top-right",
                                density="sparse", order="radial",
                                scale="contrast"),
    "photo_frame": Signature(head_pos="right-top", columns="7:4", photo=True,
                             hero="photo", void="bottom", order="lr",
                             scale="contrast"),
}

# 内容の形 → 使える構成（先頭ほど素直な当てはめ）。
_BY_SHAPE = {
    "steps": ["process_band"],
    "pairs": ["correspondence"],
    "load": ["load_report"],
    "points": ["change_note"],
    "nodes": ["connection_map"],
    "image": ["photo_frame"],
    "value": ["figure_first"],
    "statement": ["statement"],
}

# どの形にも当てはまらない「文章だけ」のページ用（ここで初めて回し分ける）。
_TEXT_ONLY = ["lead_and_void", "two_voices", "statement"]


def choose(content, history=None):
    """内容の形から構成名を決める。直近と似すぎる構成は避ける。

    Args:
        content: ページの内容 dict。
        history: 直近に使った構成名のリスト（新しいものが末尾）。
    Returns:
        SPREADS のキー。
    """
    if content.get("spread"):
        return content["spread"]
    history = list(history or [])
    recent = history[-3:]

    cands: list[str] = []
    for field_, names in _BY_SHAPE.items():
        if content.get(field_):
            cands += names
    if content.get("photo") and "photo_frame" not in cands:
        cands.append("photo_frame")
    if not cands:
        cands = list(_TEXT_ONLY)
        lines = _lines(content.get("body"))
        if content.get("aside_blocks"):
            cands = ["two_voices"] + [c for c in cands if c != "two_voices"]
        elif sum(len(t) for t in lines) < 60:
            cands = ["statement"] + [c for c in cands if c != "statement"]

    # 直近3ページと「軸が3つ未満しか違わない」構成は後ろに回す。
    def _penalty(name):
        sig = _REPRESENTATIVE[name]
        p = 0
        for i, prev in enumerate(reversed(recent)):
            if prev == name:
                p += 100 - i * 10
            elif sig.distance(_REPRESENTATIVE[prev]) < 3:
                p += 20 - i * 5
        return p

    return min(cands, key=lambda n: (_penalty(n), cands.index(n)))


def render(prs, content, history=None):
    """1ページ描く。返り値は (slide, Signature, 構成名)。"""
    name = choose(content, history)
    slide, sig = SPREADS[name](prs, content)
    return slide, sig, name


def render_all(prs, contents):
    """ページ群をまとめて描く。返り値は [(構成名, Signature), ...]。

    編集トーンは描く前にまとめて検査し、引っかかれば例外で止める
    （トーンは統一項目なので、ページごとの判断に委ねない）。
    """
    issues = []
    for c in contents:
        issues += ed.tone_lint([v for k, v in c.items()
                                if k in ("title", "lead", "body", "statement",
                                         "head", "note", "aside")])
    if issues:
        raise ValueError("編集トーン違反:\n  - " + "\n  - ".join(issues))

    out, history = [], []
    for c in contents:
        _, sig, name = render(prs, c, history)
        history.append(name)
        out.append((name, sig))
    return out
