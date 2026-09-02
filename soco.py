"""soco.py — soco-st.com（ブランド公式アイコン）連携。

線画SVGを取得 → ブランド色に置換 → PNG化して python-pptx に配置する。
Phosphor（Iconify・自動）と**併用**し、使うかは都度判断する。

使い方:
    from soco import soco_icon, soco_icon_fit, soco_search
    soco_search("AI")                    # 候補アイコンID一覧（都度選択の補助）
    soco_icon(slide, "21276", x, y, w)   # 幅指定・高さ自動で配置
    soco_icon_fit(slide, "21276", x, y, box_w, box_h)  # 箱にフィット＆中央

注意（利用規約）: soco-st は商用可のフリー素材だが著作権は先方保持。素材の再配布・
販売は不可。必ず最新の利用規約 https://soco-st.com/guide を順守すること。
"""
import io
import re
import urllib.parse
from pathlib import Path

import requests
import cairosvg
from pptx.util import Cm

try:
    from brand import PRIMARY as _PRIMARY
    _DEFAULT_HEX = "#%02X%02X%02X" % (_PRIMARY[0], _PRIMARY[1], _PRIMARY[2])
except Exception:
    _DEFAULT_HEX = "#0141D4"

_UA = {"User-Agent": "Mozilla/5.0"}
_BASE = "https://soco-st.com/wp-content/themes/socost/upload"
_CACHE = Path.home() / ".cache" / "ksr-slides" / "soco"
_CACHE.mkdir(parents=True, exist_ok=True)


def _svg(icon_id: str, variant: str = "line") -> str:
    """線画(line)/塗り(paint) SVG を取得（ディスクキャッシュ付き）。"""
    icon_id = str(icon_id)
    f = _CACHE / f"{icon_id}_{variant}.svg"
    if f.exists():
        return f.read_text(encoding="utf-8")
    url = f"{_BASE}/{icon_id}_{variant}.svg"
    r = requests.get(url, headers=_UA, timeout=20)
    r.raise_for_status()
    if "<svg" not in r.text[:400]:
        raise ValueError(f"soco-st: id={icon_id} の {variant} SVG が見つかりません（IDを確認）")
    f.write_text(r.text, encoding="utf-8")
    return r.text


def _viewbox_aspect(svg: str) -> float:
    m = re.search(r'viewBox="[\d.\s-]*?([\d.]+)\s+([\d.]+)"', svg)
    if not m:
        m = re.search(r'width="([\d.]+)"[^>]*height="([\d.]+)"', svg)
    if not m:
        return 1.0
    w, h = float(m.group(1)), float(m.group(2))
    return (w / h) if h else 1.0


def _png_raw(icon_id: str, variant: str = "line") -> bytes:
    """soco-st の元色PNG（{id}_{variant}.png）をそのまま取得（ディスクキャッシュ付き）。"""
    icon_id = str(icon_id)
    f = _CACHE / f"{icon_id}_{variant}.png"
    if f.exists():
        return f.read_bytes()
    url = f"{_BASE}/{icon_id}_{variant}.png"
    r = requests.get(url, headers=_UA, timeout=20)
    r.raise_for_status()
    if r.content[:4] != b"\x89PNG":
        raise ValueError(f"soco-st: id={icon_id} の {variant} PNG が見つかりません（IDを確認）")
    f.write_bytes(r.content)
    return r.content


def _aspect(png: bytes) -> float:
    from PIL import Image
    w, h = Image.open(io.BytesIO(png)).size
    return (w / h) if h else 1.0


def soco_png(icon_id: str, color: str = None, variant: str = "line", px: int = 400) -> bytes:
    """soco-st アイコンの PNG バイト列。

    既定（color=None）は **soco-st 本来の色の PNG をそのまま** 返す（再着色しない）。
    ``color`` を hex で渡した時だけ SVG から着色する（通常は使わない）。
    ``variant`` は "line"（線画・既定）か "paint"（塗り・フルカラー）。
    """
    if color is None:
        return _png_raw(icon_id, variant)
    svg = _svg(icon_id, variant)
    svg = re.sub(r"fill:\s*#[0-9a-fA-F]{6}", f"fill:{color}", svg)
    svg = re.sub(r'fill="#[0-9a-fA-F]{6}"', f'fill="{color}"', svg)
    return cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=px)


def soco_icon(slide, icon_id: str, x: float, y: float, w: float, *,
              variant: str = "line", color: str = None):
    """soco-st アイコンを配置（cm・幅指定、高さはアスペクト維持）。既定は元色・背景なし。"""
    png = soco_png(icon_id, color, variant)
    return slide.shapes.add_picture(io.BytesIO(png), Cm(x), Cm(y), width=Cm(w))


def soco_icon_fit(slide, icon_id: str, x: float, y: float, box_w: float, box_h: float, *,
                  variant: str = "line", color: str = None):
    """soco-st アイコンを箱にアスペクト維持でフィット＆中央配置（既定は元色・背景なし）。"""
    png = soco_png(icon_id, color, variant)
    ar = _aspect(png)
    if box_w / box_h > ar:            # 箱が横長 → 高さ基準
        h = box_h
        w = h * ar
    else:                             # 箱が縦長 → 幅基準
        w = box_w
        h = w / ar
    cx = x + (box_w - w) / 2
    cy = y + (box_h - h) / 2
    return slide.shapes.add_picture(io.BytesIO(png), Cm(cx), Cm(cy), Cm(w), Cm(h))


def soco_place(slide, keyword: str, x: float, y: float, w: float, h: float, *,
               variant: str = "paint", index: int = 0):
    """キーワード検索→候補の1つを箱にフィット配置する簡易ヘルパー。

    章扉・修了などの主役イラスト用。既定はカラー版(paint)・背景なし。失敗時 False。
    """
    ids = soco_search(keyword)
    if not ids:
        return False
    soco_icon_fit(slide, ids[index % len(ids)], x, y, w, h, variant=variant)
    return True


def soco_search(keyword: str, limit: int = 12):
    """soco-st を検索し、候補アイコンIDのリストを返す（都度選択の補助）。

    公式APIは無いため検索結果ページ(/?s=)から /NNNN 形式のIDを抽出する。
    """
    url = "https://soco-st.com/?s=" + urllib.parse.quote(keyword)
    html = requests.get(url, headers=_UA, timeout=20).text
    out = []
    for i in re.findall(r"soco-st\.com/(\d{3,6})(?:/|\"|')", html):
        if i not in out:
            out.append(i)
    return out[:limit]
