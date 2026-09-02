#!/usr/bin/env python3
"""参考スクショから配色を実測する（スポイト）。

使い方:
  .venv/bin/python3 refs/extract_palette.py refs/inbox/<file>          # 主要色を抽出
  .venv/bin/python3 refs/extract_palette.py refs/inbox/<file> 0.5 0.9  # 相対座標(x,y)の1点を採色

- 引数が画像のみ: 縮小→量子化して主要色を頻度順に HEX で出力（テーマ配色の当たり付け）。
- 引数に x y (0..1) を足す: その相対位置のピクセル色を1点採色（見出し帯・アクセント等のピンポイント確認）。
標準ライブラリ＋Pillow のみ（venv 導入済み）。
"""
import sys
from collections import Counter
from pathlib import Path

from PIL import Image


def to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])


def luminance(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def pick_point(img, rx, ry):
    w, h = img.size
    x = min(max(int(rx * w), 0), w - 1)
    y = min(max(int(ry * h), 0), h - 1)
    px = img.getpixel((x, y))[:3]
    print(f"点 ({rx:.2f},{ry:.2f}) → px({x},{y}) = {to_hex(px)}  rgb{px}")


def palette(img, k=8):
    small = img.convert("RGB").resize((200, 200))
    q = small.quantize(colors=k, method=Image.MEDIANCUT).convert("RGB")
    counts = Counter(q.getdata())
    total = sum(counts.values())
    print(f"主要色 上位{k}（頻度順）:")
    print(f"{'HEX':<9} {'割合':>6}  役割の当たり")
    for rgb, c in counts.most_common(k):
        pct = c / total * 100
        lum = luminance(rgb)
        role = ("背景/面(明)" if lum > 210 else
                "文字(暗)" if lum < 55 else
                "主色/アクセント候補")
        print(f"{to_hex(rgb):<9} {pct:5.1f}%  {role}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"見つかりません: {path}")
        sys.exit(1)
    img = Image.open(path)
    print(f"画像: {path.name}  size={img.size}")
    if len(sys.argv) >= 4:
        pick_point(img, float(sys.argv[2]), float(sys.argv[3]))
    else:
        palette(img)


if __name__ == "__main__":
    main()
