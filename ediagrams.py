"""ediagrams.py — 説明図（editorial line diagram）ビルダー。

単体アイコンではなく、**工程・接続・負荷・変化・対応関係**という「関係」を示す
小さな説明図だけを提供する。図解を入れること自体を目的にしないため、各関数は
「その関係を説明する必要があるとき」にだけ呼ぶ。

画風（全型で共通・逸脱しない）:
  - editorial line diagram style（細い線と最小限の面）
  - 色は `editorial.INK` 系＋`editorial.ACCENT` の**2色以内**
  - 影なし／3Dなし／光沢なし／キャラクター表現なし／円形アイコン背景なし
  - 角丸を使わない（直角のみ）。ベタ塗りの帯・カードを作らない
  - ラベルと線の関係が明確（ラベルは必ず対応する線・節点の直近に置く）

線幅は `editorial.RULE` の5値のみ。面は「トラック（量の下地）」と「淡い区切り面」
に限り、いずれも枠線を持たせない。

実装:
    edia_process         工程（横方向の背骨線＋節点。1工程だけアクセント）
    edia_connection      接続（中心の系と周辺要素を細線でつなぐ。線上に関係ラベル）
    edia_load            負荷（細いトラック＋実測バー。基準目盛と超過の明示）
    edia_change          変化（前後2点／推移の細線と差分の注記）
    edia_correspondence  対応関係（左右2列を細線で結ぶ対応表）
"""
from __future__ import annotations

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from slides import textbox, shape_box, connector
import editorial as ed
from editorial import (
    INK, INK_SUB, HAIR, ACCENT, ACCENT_PALE, SCALE, RULE, space,
    rule as _rule, vrule as _vrule,
)

__all__ = [
    "edia_process", "edia_connection", "edia_load",
    "edia_change", "edia_correspondence",
]

TICK = 0.28          # 節点の目印（背骨線から出す短いひげ）の長さ cm
LABEL_GAP = 0.16     # 線とラベルの間隔 cm（ラベルと線の対応を近接で示す）


def _norm(items):
    """("ラベル", "補足") / "ラベル=補足" の混在を (label, sub) に正規化する。"""
    out = []
    for it in items or []:
        if isinstance(it, (list, tuple)):
            out.append((str(it[0]), str(it[1]) if len(it) > 1 else ""))
        elif isinstance(it, str) and "=" in it:
            k, _, v = it.partition("=")
            out.append((k.strip(), v.strip()))
        else:
            out.append((str(it), ""))
    return out


def _norm_pairs(items):
    """[(名, 値)] / ["名=値"] を (名, 値) の列に正規化する。"""
    out = []
    for it in items or []:
        if isinstance(it, (list, tuple)):
            out.append((it[0], it[1]))
        else:
            k, _, v = str(it).partition("=")
            out.append((k.strip(), v.strip()))
    return out


def _label(slide, x, y, w, text, *, size, bold=False, color=INK,
           align=PP_ALIGN.LEFT, ls=1.35, middle_at=None, bottom_at=None,
           clamp=None):
    """ラベルを「必要なぶんだけの高さ」で置く。返り値は下端 y。

    middle_at / bottom_at を渡すと、その線・節点に対して上下の基準を合わせる
    （ラベルと線の対応を崩さないため、位置合わせはここに集約する）。
    clamp=(左端, 右端) で誌面外へはみ出さないよう横位置を丸める。
    """
    lines = [text] if isinstance(text, str) else [str(t) for t in text if str(t)]
    if not lines:
        return y
    h = ed.fit_h(lines, w, size, ls=ls, bold=bold)
    if middle_at is not None:
        y = middle_at - h / 2
    elif bottom_at is not None:
        y = bottom_at - h
    if clamp:
        x = min(max(x, clamp[0]), clamp[1] - w)
    textbox(slide, x, y, w, h, lines, size=size, bold=bold, color=color,
            align=align, line_spacing=ls)
    return round(y + h, 4)


# ================================================================ 工程
def edia_process(slide, x, y, w, h, *, steps, accent_at=None, caption=""):
    """工程図。横一本の背骨線に節点を打ち、上にラベル・下に補足を置く。

    Args:
        steps: [(工程名, 補足), ...]（"名=補足" 文字列も可）。3〜6件が読みやすい。
        accent_at: アクセントを置く工程の index（焦点1箇所。None で無し）。
        caption: 図の下に置く1行の説明（省略可）。

    箱を並べない＝工程は「線の上の位置」で示す。矢じりは終端に1つだけ置き、
    向きを1回だけ宣言する（各区間に矢印を打たない＝線を増やさない）。
    """
    ed.figure_area(slide, x, y, w, h)
    items = _norm(steps)
    n = len(items)
    if n < 2:
        raise ValueError("edia_process には2件以上の工程が要る")

    spine_y = y + h * 0.44
    # 背骨線（終端にだけ矢じり）。区間ごとの矢印は引かない。
    connector(slide, x, spine_y, x + w, spine_y,
              color=HAIR, width=RULE["rule"], end_arrow=True)

    seg = w / n
    for i, (label, sub) in enumerate(items):
        cx = x + seg * i + seg / 2
        on = (i == accent_at)
        col = ACCENT if on else INK
        # 節点＝背骨から上へ出す短いひげ（ラベルと線の対応を作る）
        connector(slide, cx, spine_y - TICK, cx, spine_y,
                  color=col, width=RULE["structure"] if on else RULE["thin"])
        _label(slide, cx - seg / 2 + space(0.2), 0, seg - space(0.4), label,
               size=SCALE["head"] if on else SCALE["body"], bold=on, color=col,
               align=PP_ALIGN.CENTER, bottom_at=spine_y - TICK - LABEL_GAP,
               clamp=(x, x + w))
        if sub:
            _label(slide, cx - seg / 2 + space(0.2),
                   spine_y + LABEL_GAP + space(0.3), seg - space(0.4), sub,
                   size=SCALE["note"], color=INK_SUB, align=PP_ALIGN.CENTER,
                   ls=1.4, clamp=(x, x + w))
    if caption:
        _label(slide, x, y + h - space(1.1), w, caption,
               size=SCALE["note"], color=INK_SUB)
    return slide


# ================================================================ 接続
def edia_connection(slide, x, y, w, h, *, core, nodes, side="right",
                    core_sub="", caption=""):
    """接続図。中心の系（core）と周辺要素を細線でつなぎ、線上に関係を書く。

    Args:
        core: 中心の名前（上下のヘアラインで挟むだけ。囲わない・塗らない）。
        nodes: [(要素名, 関係ラベル), ...]。関係ラベルは接続線の直上に置く。
        side: "right"＝中心を左に置き右へ展開／"left"＝その逆。
    """
    ed.figure_area(slide, x, y, w, h)
    items = _norm(nodes)
    n = len(items)
    if n < 2:
        raise ValueError("edia_connection には2件以上の接続先が要る")

    core_w = w * 0.28
    node_w = w * 0.42
    gap = w - core_w - node_w
    if side == "right":
        core_x, node_x = x, x + core_w + gap
        node_edge = node_x
    else:
        node_x, core_x = x, x + node_w + gap
        node_edge = node_x + node_w

    # 中心＝上下のヘアラインで挟むだけ（囲まない・塗らない）
    core_top = y + h / 2 - space(2.2)
    _rule(slide, core_x, core_top, core_w, weight="structure", color=ACCENT)
    cy_ = _label(slide, core_x, core_top + space(0.3), core_w, core,
                 size=SCALE["head"], bold=True)
    if core_sub:
        cy_ = _label(slide, core_x, cy_ + space(0.2), core_w, core_sub,
                     size=SCALE["note"], color=INK_SUB, ls=1.4)
    _rule(slide, core_x, cy_ + space(0.3), core_w, weight="hair")
    hub_x = (core_x + core_w) if side == "right" else core_x
    hub_y = (core_top + cy_ + space(0.3)) / 2

    # 周辺要素＝行として積み、中心の縁から各行へ細線を引く
    row_h = h / n
    for i, (label, relation) in enumerate(items):
        ry = y + row_h * i
        cy = ry + row_h / 2
        connector(slide, hub_x, hub_y, node_edge, cy,
                  color=HAIR, width=RULE["thin"], end_arrow=True)
        if relation:
            # 関係ラベルは自分の線の上（6割の位置）に沿わせる。線ごとに位置が
            # ずれるので、どのラベルがどの接続を指すかが一目で決まる。
            tx_ = hub_x + (node_edge - hub_x) * 0.60
            ty_ = hub_y + (cy - hub_y) * 0.60
            _label(slide, tx_ - gap * 0.35, 0, gap * 0.7, relation,
                   size=SCALE["note"], color=INK_SUB, align=PP_ALIGN.CENTER,
                   bottom_at=ty_ - LABEL_GAP, clamp=(x, x + w))
        _vrule(slide, node_edge, ry + space(0.3), row_h - space(0.6), weight="thin")
        lx = node_edge + space(0.4) if side == "right" else node_x
        _label(slide, lx, 0, node_w - space(0.5), label,
               size=SCALE["body"], middle_at=cy, clamp=(x, x + w))
    if caption:
        _label(slide, x, y + h - space(1.0), w, caption,
               size=SCALE["note"], color=INK_SUB)
    return slide


# ================================================================ 負荷
def edia_load(slide, x, y, w, h, *, items, unit="", capacity=None,
              capacity_label="上限", caption=""):
    """負荷図。細いトラックの上に実測バーを重ね、基準（上限）を縦線で示す。

    Args:
        items: [(名前, 数値), ...]。
        capacity: 上限値（None なら最大値を上限とみなし縦線を引かない）。
        unit: 数値に添える単位。
    """
    ed.figure_area(slide, x, y, w, h)
    rows = [(str(a), float(b)) for a, b in _norm_pairs(items)]
    n = len(rows)
    top = float(capacity) if capacity else max(v for _, v in rows)
    if top <= 0:
        raise ValueError("edia_load の値は正の数で渡す")
    # 上限を超えた量が見えるよう、目盛は「上限」ではなく最大値まで取る。
    scale = max(top, max(v for _, v in rows)) * 1.04

    label_w = w * 0.24
    val_w = w * 0.12
    track_x = x + label_w
    track_w = w - label_w - val_w - space(1.0)
    row_h = h / n
    bar_h = min(space(0.5), row_h * 0.34)

    over = max((v for _, v in rows), default=0) > top
    for i, (label, v) in enumerate(rows):
        cy = y + row_h * i + row_h / 2
        _label(slide, x, 0, label_w - space(0.4), label,
               size=SCALE["body"], middle_at=cy)
        # トラック（下地・最小限の面）
        shape_box(slide, MSO_SHAPE.RECTANGLE, track_x, cy - bar_h / 2,
                  track_w, bar_h, fill=ACCENT_PALE, line=None)
        ratio = v / scale
        hot = v > top
        shape_box(slide, MSO_SHAPE.RECTANGLE, track_x, cy - bar_h / 2,
                  max(track_w * ratio, 0.06), bar_h,
                  fill=ACCENT if hot else INK, line=None)
        _label(slide, track_x + track_w + space(0.5), 0, val_w, f"{v:g}{unit}",
               size=SCALE["small"], bold=hot, color=ACCENT if hot else INK,
               align=PP_ALIGN.RIGHT, middle_at=cy, clamp=(x, x + w))

    if capacity:
        # 上限＝トラック右端の縦線。ラベルは線の直上（線との対応を明示）
        cx = track_x + track_w * (top / scale)
        _vrule(slide, cx, y, h, weight="structure", color=ACCENT if over else INK_SUB)
        # 基準線のラベルは常に補助色（注釈の扱いは全ページ共通）。超過は線と
        # 超えたバー・数値がアクセントで示す。
        _label(slide, cx - w * 0.15, 0, w * 0.30,
               f"{capacity_label} {float(capacity):g}{unit}",
               size=SCALE["small"], color=INK_SUB,
               align=PP_ALIGN.CENTER, bottom_at=y - LABEL_GAP, clamp=(x, x + w))
    if caption:
        _label(slide, x, y + h + space(0.2), w, caption,
               size=SCALE["note"], color=INK_SUB)
    return slide


# ================================================================ 変化
def edia_change(slide, x, y, w, h, *, points, unit="", delta_label="変化",
                caption=""):
    """変化図。推移を細い折れ線で描き、始点と終点、差分だけを注記する。

    Args:
        points: [(ラベル, 値), ...]（2点なら before/after、3点以上で推移）。
    """
    ed.figure_area(slide, x, y, w, h)
    pts = [(str(a), float(b)) for a, b in _norm_pairs(points)]
    n = len(pts)
    if n < 2:
        raise ValueError("edia_change には2点以上が要る")

    vals = [v for _, v in pts]
    lo, hi = min(vals), max(vals)
    rng = (hi - lo) or 1.0
    plot_y = y + space(2.0)
    plot_h = h - space(6.0)
    step = w / (n - 1)
    lab_w = min(step * 1.1, w * 0.5)

    def py(v):
        return plot_y + plot_h * (1 - (v - lo) / rng)

    # 基準線（最小値の高さ）＝値の高さを読むための1本だけ
    _rule(slide, x, plot_y + plot_h, w, weight="hair")

    for i in range(n - 1):
        connector(slide, x + step * i, py(vals[i]),
                  x + step * (i + 1), py(vals[i + 1]),
                  color=INK, width=RULE["structure"])

    for i, (label, v) in enumerate(pts):
        cx = x + step * i
        d = 0.16
        shape_box(slide, MSO_SHAPE.OVAL, cx - d / 2, py(v) - d / 2, d, d,
                  fill=ACCENT if i == n - 1 else INK, line=None)
        if i in (0, n - 1):
            _label(slide, cx - lab_w / 2, 0, lab_w, f"{v:g}{unit}",
                   size=SCALE["head"], bold=True,
                   color=ACCENT if i == n - 1 else INK, align=PP_ALIGN.CENTER,
                   bottom_at=py(v) - LABEL_GAP, clamp=(x, x + w))
        # 端の目盛は外側に寄せる（中央寄せのまま押し込むと隣とぶつかる）
        if i == 0:
            lx_, la_ = cx - space(0.3), PP_ALIGN.LEFT
        elif i == n - 1:
            lx_, la_ = cx + space(0.3) - lab_w, PP_ALIGN.RIGHT
        else:
            lx_, la_ = cx - lab_w / 2, PP_ALIGN.CENTER
        _label(slide, lx_, plot_y + plot_h + space(0.35), lab_w, label,
               size=SCALE["note"], color=INK_SUB, align=la_, clamp=(x, x + w))

    # 差分＝右下に1行（増減の向きは符号で示す）
    diff = vals[-1] - vals[0]
    sign = "+" if diff > 0 else ""
    _label(slide, x + w * 0.4, y + h - space(1.4), w * 0.6,
           f"{delta_label} {sign}{diff:g}{unit}",
           size=SCALE["small"], bold=True, color=INK, align=PP_ALIGN.RIGHT)
    if caption:
        _label(slide, x, y + h - space(1.4), w * 0.38, caption,
               size=SCALE["note"], color=INK_SUB)
    return slide


# ================================================================ 対応関係
def edia_correspondence(slide, x, y, w, h, *, pairs, left_head="", right_head="",
                        accent_at=None, caption=""):
    """対応関係図。左右2列を細線で結ぶ（左の何が右の何に対応するか）。

    Args:
        pairs: [(左, 右), ...]。
        accent_at: 焦点にする対応の index（1組だけアクセント）。
    """
    ed.figure_area(slide, x, y, w, h)
    rows = _norm_pairs(pairs)
    n = len(rows)
    if n < 2:
        raise ValueError("edia_correspondence には2件以上が要る")

    col_w = w * 0.38
    mid_x = x + col_w
    mid_w = w - col_w * 2
    right_x = x + w - col_w

    head_h = 0.0
    if left_head or right_head:
        if left_head:
            _label(slide, x, y, col_w, left_head, size=SCALE["kicker"],
                   bold=True, color=INK_SUB)
        if right_head:
            _label(slide, right_x, y, col_w, right_head, size=SCALE["kicker"],
                   bold=True, color=INK_SUB)
        head_h = space(1.3)
        _rule(slide, x, y + head_h - space(0.25), col_w, weight="hair")
        _rule(slide, right_x, y + head_h - space(0.25), col_w, weight="hair")

    top = y + head_h + space(0.3)
    row_h = (h - head_h - space(0.3)) / n
    for i, (left, right) in enumerate(rows):
        cy = top + row_h * i + row_h / 2
        on = (i == accent_at)
        col = ACCENT if on else INK
        _label(slide, x, 0, col_w, str(left), size=SCALE["body"], bold=on,
               color=col, middle_at=cy)
        _label(slide, right_x, 0, col_w, str(right), size=SCALE["body"], bold=on,
               color=col, middle_at=cy)
        connector(slide, mid_x + space(0.3), cy, mid_x + mid_w - space(0.3), cy,
                  color=col if on else HAIR,
                  width=RULE["structure"] if on else RULE["hair"],
                  end_arrow=True)
        if i < n - 1:
            _rule(slide, x, top + row_h * (i + 1), w, weight="hair")
    if caption:
        _label(slide, x, y + h + space(0.2), w, caption,
               size=SCALE["note"], color=INK_SUB)
    return slide
