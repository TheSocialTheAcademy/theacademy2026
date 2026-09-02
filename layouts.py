"""誌面的（非対称）本文レイアウト。フレームワークが「同じ型を続けない」よう選び回す。

すべて同じ引数 (prs, *, section, title, bullets, note="") を取り、内容は共通でも
見せ方（構図）を変える。避けるのは 3等分/全中央/全部囲う/同サイズ/同余白。
使うのは 大きな主張＋小さな根拠／罫線なし段組み／上結論・下詳細 など「使用してよい例」。
"""
import pages
from slides import (
    textbox, shape_box, connector,
    PRIMARY, PRIMARY_LIGHT, TEXT, TEXT_MUTED, BORDER, SURFACE, WHITE,
)
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

X0, ZW = pages.X0, pages.ZONE_W


def _clean(bullets):
    return [b for b in (bullets or []) if str(b).strip()]


# ---------------------------------------------------------------- A 大きな主張＋小さな根拠
def lay_claim_evidence(prs, *, section, title, bullets, note=""):
    """先頭を大きな主張（左）、残りを小さな根拠（右・囲わない・ヘアライン）。"""
    s = pages._body(prs, section, title)
    b = _clean(bullets)
    claim = b[0] if b else title
    ev = b[1:] if len(b) > 1 else []
    textbox(s, X0, 4.7, 12.0, 3.6, [claim], size=25, bold=True, color=TEXT,
            line_spacing=1.3)
    connector(s, X0, 8.6, 12.3, 8.6, color=PRIMARY, width=2.0)
    if note:
        textbox(s, X0, 9.0, 12.0, 2.0, [note], size=12.5, color=TEXT_MUTED,
                line_spacing=1.55)
    rx, rw = 14.3, 9.9
    n = max(len(ev), 1)
    rh = min(2.3, 6.8 / n)
    y = 4.8
    for i, e in enumerate(ev):
        yy = y + i * rh
        textbox(s, rx, yy, 0.95, rh, ["—"], size=14, bold=True, color=PRIMARY,
                anchor=MSO_ANCHOR.MIDDLE)
        textbox(s, rx + 1.05, yy, rw - 1.05, rh, [e], size=14, color=TEXT,
                anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.4)
        if i < len(ev) - 1:
            connector(s, rx, yy + rh - 0.2, rx + rw, yy + rh - 0.2, color=BORDER,
                      width=0.75)
    return s


# ---------------------------------------------------------------- B 罫線なし段組み＋余白注釈
def lay_editorial_list(prs, *, section, title, bullets, note=""):
    """左に細い accent バー＋番号なしの要点リスト（囲わない）、右余白に注釈。"""
    s = pages._body(prs, section, title)
    b = _clean(bullets)
    # 左端に短い accent バー（囲みの代わりの強弱）
    shape_box(s, MSO_SHAPE.RECTANGLE, X0, 4.6, 0.14, 6.2, fill=PRIMARY, line=None)
    lx, lw = X0 + 0.7, 14.6
    n = max(len(b), 1)
    rh = min(2.3, 6.4 / n)
    y = 4.7
    for i, t in enumerate(b):
        yy = y + i * rh
        textbox(s, lx, yy, lw, rh, [t], size=16, color=TEXT, anchor=MSO_ANCHOR.MIDDLE,
                line_spacing=1.4)
    if note:
        textbox(s, 16.6, 4.9, 7.5, 5.6, [note], size=12, color=TEXT_MUTED,
                line_spacing=1.7)
    return s


# ---------------------------------------------------------------- C 上に結論、下に詳細
def lay_stack(prs, *, section, title, bullets, note=""):
    """先頭を大きな結論（上・囲わない）、残りを下段に不均等な横並びで（→でつなぐ）。"""
    s = pages._body(prs, section, title)
    b = _clean(bullets)
    head = b[0] if b else title
    rest = b[1:] if len(b) > 1 else []
    textbox(s, X0, 4.5, ZW, 2.0, [head], size=24, bold=True, color=TEXT,
            line_spacing=1.25)
    connector(s, X0, 6.9, X0 + ZW, 6.9, color=BORDER, width=0.75)
    if rest:
        n = len(rest)
        gap = 1.0
        # 不均等幅：先頭をやや広く
        weights = [1.3] + [1.0] * (n - 1)
        tot = sum(weights)
        cw = [(ZW - gap * (n - 1)) * w / tot for w in weights]
        x = X0
        for i, (t, w) in enumerate(zip(rest, cw)):
            textbox(s, x, 7.5, w, 3.4, [t], size=14, color=TEXT, line_spacing=1.5)
            if i < n - 1:
                textbox(s, x + w + 0.1, 7.5, gap - 0.2, 1.2, ["›"], size=20,
                        bold=True, color=PRIMARY, align=PP_ALIGN.CENTER)
            x += w + gap
    if note:
        textbox(s, X0, 11.2, ZW, 0.8, [note], size=11, color=TEXT_MUTED)
    return s


# ---------------------------------------------------------------- ローテーション
# details / examples の fan-out で順に選び回す（連続で同じ構図にしない）。
ROTATION = [lay_claim_evidence, lay_editorial_list, lay_stack]


def rotate(index):
    """index 番目に使うレイアウト関数を返す。"""
    return ROTATION[index % len(ROTATION)]
