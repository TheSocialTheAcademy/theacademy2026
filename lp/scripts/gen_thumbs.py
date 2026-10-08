# コースのサムネイル（C-4：カテゴリ色のグラデーション＋半透明の形）を、コース一覧のデータから画像で書き出す
# 出力：lp/assets/thumbs/<slug>.webp（1280×800）。コースを足したら NAME に改行位置を1行足して（不要なら省略可）、このスクリプトを実行する
# 形の位置・グラデーションの角度はコースの slug から決まる（同じ slug なら毎回同じ画像）
#   python3 lp/scripts/gen_thumbs.py && NODE_PATH=$(npm root -g) node lp/scripts/gen_thumbs.js
import os, html, tempfile, json, hashlib, random
S = os.path.dirname(os.path.abspath(__file__)); LPDIR = os.path.dirname(S)
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)
CAT, C, cur_meta = g['CAT'], g['C'], g['cur_meta']
# カテゴリごとのグラデーション（カテゴリ色 → ブランドの青系、3つ目は形の差し色）
GR = {'it': ('#1E9E62', '#3E78FE', '#BFEAD3'), 'mk': ('#E46A1F', '#F29A50', '#FFD9C2'), 'en': ('#0141D4', '#3E78FE', '#B9CCFF'),
      'biz': ('#6B4FD8', '#3E78FE', '#D5CCFF'), 'cr': ('#D9467A', '#F76B38', '#F9C8D8')}
def rnd(slug): return random.Random(int(hashlib.md5(slug.encode()).hexdigest()[:8], 16))
# サムネイルでのコース名の改行位置（<wbr>）
NAME = {'sns-marketing': 'SNSマーケティング<wbr>実践', 'ai-efficiency': '生成AI<wbr> 業務改善', 'toeic-700': 'TOEIC L&R<wbr> 700点突破', 'marketing-basic': 'マーケティング<wbr>戦略基礎', 'automation': '自動化ツール<wbr>開発', 'chatgpt-basic': '初級編<wbr> ChatGPT', 'line-official': '公式LINE<wbr>運用', 'business-english': 'ビジネス英語<wbr>初級', 'project-management': 'プロジェクト<wbr>マネジメント', 'slack-gas-task': 'Slack×GAS<wbr> スマート管理ツール'}
rows = [(c[0], html.unescape(c[1]), c[2], c[7], c[5], c[6]) for c in C] + [('slack-gas-task', 'Slack×GAS スマート管理ツール', 'it', 'ツール', '仕様書つき', None)]
def tile(slug, title, cat, lv, dur, time):
    name = CAT[cat][0]; c1, c2, c3 = GR[cat]; r = rnd(slug)
    x1, y1, x2 = r.randint(-60, 40), r.randint(-80, 0), r.randint(260, 360)
    ang, cy, rad = r.randint(110, 160), r.randint(20, 90), r.randint(110, 150)
    disp = NAME.get(slug) or html.escape(title)
    shapes = (f'<svg viewBox="0 0 480 300"><path d="M{x1} {y1} C{x1 + 220} {y1 + 40}, {x1 + 120} {y1 + 230}, {x1 + 300} {y1 + 380} L{x1 - 40} {y1 + 380}Z" fill="#fff" opacity=".13"/>'
              f'<circle cx="{x2}" cy="{cy}" r="{rad}" fill="#fff" opacity=".12"/><circle cx="{x2 + 80}" cy="260" r="90" fill="{c3}" opacity=".22"/></svg>')
    return (f'<div class="th" id="t-{slug}" style="background:linear-gradient({ang}deg,{c1} 0%,{c2} 100%)">{shapes}<span class="k">{name}</span>'
            f'<p class="n">{disp}</p><p class="l">THE ACADEMY</p></div>')
CSS = '''*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Noto Sans JP',sans-serif;background:#fff;display:flex;flex-wrap:wrap;gap:20px;padding:20px;width:1400px}
.th{position:relative;width:640px;height:400px;overflow:hidden;color:#fff;word-break:keep-all;overflow-wrap:anywhere;isolation:isolate}
.th svg{position:absolute;inset:0;width:100%;height:100%;z-index:-1}
.k{position:absolute;left:36px;top:32px;background:rgba(255,255,255,.18);color:#fff;font-size:17px;font-weight:700;padding:5px 16px;border-radius:999px}
.n{position:absolute;left:36px;right:120px;bottom:62px;font-size:38px;font-weight:900;line-height:1.3;letter-spacing:.01em}
.l{position:absolute;left:36px;bottom:30px;font-size:14px;font-weight:900;letter-spacing:.16em;opacity:.7}'''
out = os.path.join(tempfile.gettempdir(), 'ta_thumbs.html')
open(out, 'w').write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(tile(*r) for r in rows)}</body></html>')
json.dump({'html': out, 'dir': os.path.join(LPDIR, 'assets', 'thumbs'), 'slugs': [r[0] for r in rows]}, open(os.path.join(tempfile.gettempdir(), 'ta_thumbs.json'), 'w'))
print('ok thumbs html', len(rows), out)
