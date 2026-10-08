# コースのサムネイル（C-4 の背景＋X-2「つくるもの」）を、コース一覧のデータから画像で書き出す
# 中身は小さな線アイコン＋「つくるもの」＋成果物の名前（gen_courses.py の DELIV）。コース名はカードに出るので入れない
# 出力：lp/assets/thumbs/<slug>.webp（1280×800）。コースを足したら DELIV（gen_courses.py）と ICON に1行ずつ足して、このスクリプトを実行する
# 形の位置・グラデーションの角度はコースの slug から決まる（同じ slug なら毎回同じ画像）
#   python3 lp/scripts/gen_thumbs.py && NODE_PATH=$(npm root -g) node lp/scripts/gen_thumbs.js
import os, html, tempfile, json, hashlib, random
S = os.path.dirname(os.path.abspath(__file__)); LPDIR = os.path.dirname(S)
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)
CAT, C, DELIV = g['CAT'], g['C'], g['DELIV']
# カテゴリごとのグラデーション（カテゴリ色 → ブランドの青系、3つ目は形の差し色）
GR = {'it': ('#1E9E62', '#3E78FE', '#BFEAD3'), 'mk': ('#E46A1F', '#F29A50', '#FFD9C2'), 'en': ('#0141D4', '#3E78FE', '#B9CCFF'),
      'biz': ('#6B4FD8', '#3E78FE', '#D5CCFF'), 'cr': ('#D9467A', '#F76B38', '#F9C8D8')}
# カテゴリの単色グラデーション（同じ色相の濃→淡）。TA_THUMBS_MODE=mono／mono-cat のときに使う
GR_MONO = {'it': ('#1E9E62', '#4CC38A', '#BFEAD3'), 'mk': ('#E46A1F', '#F29A50', '#FFD9C2'), 'en': ('#0141D4', '#3E78FE', '#B9CCFF'),
           'biz': ('#6B4FD8', '#9A83F0', '#D5CCFF'), 'cr': ('#D9467A', '#F07AA3', '#F9C8D8')}
CAT_SHAPE = {'it': 2, 'mk': 1, 'en': 3, 'biz': 4, 'cr': 5}  # mono-cat：形もカテゴリで固定
MODE = os.environ.get('TA_THUMBS_MODE', 'mix')  # mix＝カテゴリ色→ブランドの青（いま）
ORDER = {}  # slug → 一覧での並び順（背景の形の割り当てに使う）
def rnd(slug): return random.Random(int(hashlib.md5(slug.encode()).hexdigest()[:8], 16))
P = {  # 線アイコン（24×24）
 'palette': '<path d="M12 3a9 9 0 0 0 0 18c1.2 0 1.8-.9 1.4-1.9-.4-1 .3-2.1 1.4-2.1H17a4 4 0 0 0 4-4 9 9 0 0 0-9-10z"/><circle cx="7.5" cy="11" r="1.2"/><circle cx="10.5" cy="7" r="1.2"/><circle cx="15" cy="7.5" r="1.2"/>',
 'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1 7 17M17 7l2.1-2.1"/>',
 'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="m12 13 1 2 2 .3-1.5 1.4.4 2.1-1.9-1-1.9 1 .4-2.1L9 15.3l2-.3z"/>',
 'camera': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'chart': '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/><path d="M15 8h4v4"/>',
 'chat': '<path d="M12 3.5c5 0 9 3.2 9 7.2s-4 7.2-9 7.2c-.7 0-1.4-.1-2-.2L6 20l.6-3.6C4.4 15 3 13 3 10.7 3 6.7 7 3.5 12 3.5z"/><path d="M8 10h8M8 13h5"/>',
 'code': '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
 'mega': '<path d="M4 11v3a1 1 0 0 0 1 1h2l6 4V6L7 10H5a1 1 0 0 0-1 1z"/><path d="M17 9a4 4 0 0 1 0 6M19.5 6.5a8 8 0 0 1 0 11"/>',
 'spark': '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
 'head': '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>',
 'gantt': '<path d="M3 4v16h18"/><path d="M7 7h6M9 11h8M12 15h7"/>',
}
ICON = {'sns-marketing': 'mega', 'ai-efficiency': 'spark', 'toeic-700': 'head', 'event-design': 'calendar', 'marketing-basic': 'chart', 'instagram': 'camera', 'automation': 'code',
        'chatgpt-basic': 'spark', 'line-official': 'chat', 'business-english': 'mail', 'project-management': 'gantt', 'canva-basic': 'palette', 'slack-gas-task': 'gear'}
rows = [(c[0], html.unescape(c[1]), c[2], c[7], c[5], c[6]) for c in C] + [('slack-gas-task', 'Slack×GAS スマート管理ツール', 'it', 'ツール', '仕様書つき', None)]
ORDER.update({r[0]: i for i, r in enumerate(rows)})  # 一覧に並ぶ順で形を変える（隣どうしが同じ形にならない）
# 背景の形（どれも「グラデーション＋半透明の白い形」。並んだときに同じ絵が続かないよう、コースの並び順で6種類を順番に割り当てる）
def shapes_of(v, r, c3):
    W = lambda o: f'fill="#fff" opacity="{o}"'
    if v == 0:  # 円（はじまりの形）
        x1, y1, x2, cy, rad = r.randint(-60, 40), r.randint(-80, 0), r.randint(260, 360), r.randint(20, 90), r.randint(110, 150)
        return (f'<path d="M{x1} {y1} C{x1 + 220} {y1 + 40}, {x1 + 120} {y1 + 230}, {x1 + 300} {y1 + 380} L{x1 - 40} {y1 + 380}Z" {W(.13)}/>'
                f'<circle cx="{x2}" cy="{cy}" r="{rad}" {W(.12)}/><circle cx="{x2 + 80}" cy="260" r="90" fill="{c3}" opacity=".22"/>')
    if v == 1:  # 重なる波
        h = r.randint(-20, 20)
        return ''.join(f'<path d="M-20 {y + h} C100 {y - 60 + h}, 220 {y + 40}, 340 {y - 30} S 460 {y - 90 + h}, 520 {y - 70} L520 320 L-20 320Z" {W(o)}/>' for y, o in ((150, .09), (205, .11), (255, .12)))
    if v == 2:  # 斜めの帯
        x = r.randint(150, 230)
        return ''.join(f'<path d="M{x + d} -20 L{x + d + w} -20 L{x + d + w - 260} 320 L{x + d - 260} 320Z" {W(o)}/>' for d, w, o in ((0, 70, .12), (100, 40, .16), (170, 110, .10))) + f'<circle cx="430" cy="40" r="60" fill="{c3}" opacity=".2"/>'
    if v == 3:  # 同心の輪
        cx, cy = r.choice([(470, 10), (460, 290), (400, -20)])
        return ''.join(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#fff" stroke-width="{sw}" opacity="{o}"/>' for rr, sw, o in ((70, 26, .16), (140, 18, .13), (210, 12, .11), (280, 8, .09)))
    if v == 4:  # 傾いた角丸の四角
        a = r.randint(12, 28)
        return (f'<g transform="rotate({a} 360 120)"><rect x="270" y="10" width="170" height="170" rx="36" {W(.14)}/><rect x="380" y="150" width="120" height="120" rx="28" {W(.10)}/>'
                f'<rect x="180" y="-90" width="110" height="110" rx="26" fill="{c3}" opacity=".22"/></g>')
    # v == 5：大きな有機的な形＋点の並び
    dx = r.randint(-20, 20)
    dots = ''.join(f'<circle cx="{40 + i * 18}" cy="{36 + j * 18}" r="2.4" {W(.35)}/>' for i in range(5) for j in range(3))
    return (f'<path d="M{300 + dx} -30 C{420 + dx} -10, {520} 80, {470} 170 C{430} 250, {330 + dx} 240, {280 + dx} 170 C{230 + dx} 100, {220 + dx} -40, {300 + dx} -30Z" {W(.15)}/>'
            f'<circle cx="{420 + dx}" cy="270" r="70" fill="{c3}" opacity=".22"/><g transform="translate(260 0)">{dots}</g>')
def tile(slug, title, cat, lv, dur, time):
    c1, c2, c3 = (GR if MODE == 'mix' else GR_MONO)[cat]; r = rnd(slug); v = CAT_SHAPE[cat] if MODE == 'mono-cat' else ORDER[slug] % 6
    ang = r.randint(110, 160) if v % 2 == 0 else r.randint(200, 250)
    shapes = f'<svg class="bg" viewBox="0 0 480 300">{shapes_of(v, r, c3)}</svg>'
    icon = f'<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{P[ICON[slug]]}</svg>'
    return (f'<div class="th" id="t-{slug}" style="background:linear-gradient({ang}deg,{c1} 0%,{c2} 100%)">{shapes}{icon}'
            f'<div class="b"><p class="k">つくるもの</p><p class="d">{DELIV[slug]}</p></div></div>')
CSS = '''*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Noto Sans JP',sans-serif;background:#fff;display:flex;flex-wrap:wrap;gap:20px;padding:20px;width:1400px}
.th{position:relative;width:640px;height:400px;overflow:hidden;color:#fff;word-break:keep-all;overflow-wrap:anywhere;isolation:isolate}
.bg{position:absolute;inset:0;width:100%;height:100%;z-index:-1}.i{position:absolute;left:32px;top:30px;width:48px;height:48px}
.b{position:absolute;left:32px;right:60px;bottom:28px}.k{font-size:18px;font-weight:700;letter-spacing:.08em;opacity:.85;margin-bottom:4px}
.d{font-size:35px;font-weight:900;line-height:1.35}'''
out = os.path.join(tempfile.gettempdir(), 'ta_thumbs.html')
open(out, 'w').write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(tile(*r) for r in rows)}</body></html>')
json.dump({'html': out, 'dir': os.environ.get('TA_THUMBS_DIR') or os.path.join(LPDIR, 'assets', 'thumbs'), 'slugs': [r[0] for r in rows]}, open(os.path.join(tempfile.gettempdir(), 'ta_thumbs.json'), 'w'))
print('ok thumbs html', len(rows), out)
