"""downloads/ の素材ZIPを、中身（ファイル名・フォルダ構成・見た目）を変えずに軽くする。
- PNG：oxipng で劣化なしに再圧縮（メタデータのうち表示に関係ないものだけ除去）
- SVG：中に埋め込まれた PNG（data:image/png;base64）も同じく再圧縮
- ZIP：最大圧縮で詰め直す
使い方：pip install pyoxipng && python3 lp/scripts/slim_zips.py downloads/*.zip
"""
import base64, io, os, re, sys, zipfile
import oxipng

B64 = re.compile(rb'(data:image/png;base64,)([A-Za-z0-9+/=\s]+)')

def png(data):
    try:
        out = oxipng.optimize_from_memory(data, level=3, strip=oxipng.StripChunks.safe())
        return out if len(out) < len(data) else data
    except Exception:
        return data

def svg(data):
    def rep(m):
        raw = base64.b64decode(re.sub(rb'\s', b'', m.group(2)))
        return m.group(1) + base64.b64encode(png(raw))
    return B64.sub(rep, data)

for path in sys.argv[1:]:
    before = os.path.getsize(path); buf = io.BytesIO()
    with zipfile.ZipFile(path) as zi, zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zo:
        for info in zi.infolist():
            data = zi.read(info)
            name = info.filename.lower()
            if name.endswith('.png'): data = png(data)
            elif name.endswith('.svg'): data = svg(data)
            zo.writestr(info, data, compress_type=zipfile.ZIP_STORED if name.endswith(('.png', '.jpg', '.webp')) else zipfile.ZIP_DEFLATED)
    open(path, 'wb').write(buf.getvalue())
    print(f'{os.path.basename(path)}: {before / 1e6:.1f}MB -> {os.path.getsize(path) / 1e6:.1f}MB')
