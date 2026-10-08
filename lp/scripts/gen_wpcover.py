# お役立ち資料の表紙（W-4：カテゴリ色のグラデーション＋半透明の形）を書き出す
# 出力：lp/assets/resources/<資料のID>.webp（1280×720）。資料のデータは gen_resources.py の RES（表紙の見出しは RES の 8 番目、[]が強調）
#   python3 lp/scripts/gen_wpcover.py && TA_JOB=/tmp/ta_wpcover.json NODE_PATH=$(npm root -g) node lp/scripts/gen_thumbs.js && TA_JOB=/tmp/ta_wpcover.json python3 lp/scripts/thumbs_webp.py
import os, re, json, tempfile, hashlib, random
S = os.path.dirname(os.path.abspath(__file__)); LPDIR = os.path.dirname(S)
src = open(os.path.join(S, 'gen_resources.py')).read()
RES = eval(re.search(r'^RES = (\[.*?^\])', src, re.S | re.M).group(1))
GR = {'it': ('#1E9E62', '#2FAE73', '#BFEAD3'), 'mk': ('#E46A1F', '#F29A50', '#FFD9C2'), 'en': ('#0141D4', '#3E78FE', '#B9CCFF'),
      'biz': ('#6B4FD8', '#8A70E8', '#D5CCFF'), 'cr': ('#D9467A', '#E8608F', '#F9C8D8'), 'ca': ('#0F1B45', '#3A4A80', '#C9D3EA')}
BOOK = '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h7"/>'
def rnd(s): return random.Random(int(hashlib.md5(s.encode()).hexdigest()[:8], 16))
def tile(r):
    rid, tag, title, desc, fmt, cat, pdf, head = r[:8]; a, b, l = GR[cat]; rr = rnd(rid)
    v = rr.randint(0, 2)
    shapes = [f'<circle cx="{rr.randint(380, 440)}" cy="40" r="120" fill="#fff" opacity=".12"/><rect x="300" y="170" width="160" height="160" rx="34" fill="#fff" opacity=".1" transform="rotate(18 380 250)"/>',
              f'<path d="M-20 230 C100 170, 220 270, 340 200 S 460 140, 520 160 L520 320 L-20 320Z" fill="#fff" opacity=".1"/><circle cx="430" cy="50" r="90" fill="{l}" opacity=".22"/>',
              ''.join(f'<circle cx="470" cy="10" r="{x}" fill="none" stroke="#fff" stroke-width="{w}" opacity=".12"/>' for x, w in ((70, 24), (140, 16), (210, 10)))][v]
    h = head.replace('[', '<em>').replace(']', '</em>')
    return (f'<div class="th" id="t-{rid}" style="background:linear-gradient(135deg,{a},{b})"><svg class="bg" viewBox="0 0 480 270">{shapes}</svg>'
            f'<span class="tg"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{BOOK}</svg>無料資料</span>'
            f'<p class="t">{h}</p><p class="f">{fmt}</p></div>')
CSS = '''*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Noto Sans JP',sans-serif;background:#fff;display:flex;flex-wrap:wrap;gap:20px;padding:20px;width:1400px}
.th{position:relative;width:640px;height:360px;overflow:hidden;color:#fff;word-break:keep-all;isolation:isolate}.bg{position:absolute;inset:0;width:100%;height:100%;z-index:-1}
.tg{position:absolute;left:34px;top:30px;display:flex;align-items:center;gap:8px;font-size:17px;font-weight:800;background:rgba(255,255,255,.18);padding:5px 16px;border-radius:999px}.tg svg{width:20px;height:20px}
.t{position:absolute;left:34px;right:34px;bottom:64px;font-size:36px;font-weight:900;line-height:1.45}.t em{font-style:normal;background:rgba(255,255,255,.22);padding:0 8px;border-radius:6px}
.f{position:absolute;left:34px;bottom:28px;font-size:17px;opacity:.88}'''
out = os.path.join(tempfile.gettempdir(), 'ta_wpcover.html')
open(out, 'w').write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(tile(r) for r in RES)}</body></html>')
json.dump({'html': out, 'dir': os.path.join(LPDIR, 'assets', 'resources'), 'slugs': [r[0] for r in RES], 'prefix': 'ta_wp_'}, open(os.path.join(tempfile.gettempdir(), 'ta_wpcover.json'), 'w'))
print('ok wpcover html', len(RES), out)
