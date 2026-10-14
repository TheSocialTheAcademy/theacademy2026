from common import *
import hashlib, random, math
SEL = [C[0], C[2], C[3], C[4], C[7], C[1]]
GR = {'it': ('#1E9E62', '#3E78FE', '#BFEAD3'), 'mk': ('#E46A1F', '#F29A50', '#FFD9C2'), 'en': ('#0141D4', '#3E78FE', '#B9CCFF'), 'biz': ('#6B4FD8', '#3E78FE', '#D5CCFF'), 'cr': ('#D9467A', '#F76B38', '#F9C8D8')}
def rnd(s, salt=''): return random.Random(int(hashlib.md5((s + salt).encode()).hexdigest()[:8], 16))
def x2(c, cls=''): return f'{ic(c[3], "x2-i", 1.6)}<div class="x2-b {cls}"><p class="x2-k">つくるもの</p><p class="x2-d">{c[6]}</p></div>'
def wrap(style, svg, c, cls='', box=''): return f'<div class="cv {cls}" style="{style}"><svg class="bgs" viewBox="0 0 480 300" preserveAspectRatio="xMidYMid slice">{svg}</svg>{x2(c, box)}</div>'
# いまの C-4（比較用）
def c4(c):
    s, k = c[0], c[2]; a, b, l = GR[k]; r = rnd(s); x1, y1, x2_ = r.randint(-60, 40), r.randint(-80, 0), r.randint(260, 360); ang, cy, rad = r.randint(110, 160), r.randint(20, 90), r.randint(110, 150)
    return wrap(f'background:linear-gradient({ang}deg,{a} 0%,{b} 100%)', f'<path d="M{x1} {y1} C{x1 + 220} {y1 + 40}, {x1 + 120} {y1 + 230}, {x1 + 300} {y1 + 380} L{x1 - 40} {y1 + 380}Z" fill="#fff" opacity=".13"/><circle cx="{x2_}" cy="{cy}" r="{rad}" fill="#fff" opacity=".12"/><circle cx="{x2_ + 80}" cy="260" r="90" fill="{l}" opacity=".22"/>', c)
# B-1 道のり：柱をのぼる S 字の道（学びの積み上げ）
def b1(c):
    s, k = c[0], c[2]; a, b, l = GR[k]; r = rnd(s); cx = 330 + r.randint(-10, 20); w = 104
    lines = ''.join(f'<path d="M-20 {y} C80 {y - 30}, 160 {y + 30}, 260 {y - 10} S 420 {y - 40}, 520 {y}" fill="none" stroke="#fff" stroke-width="1" opacity=".13"/>' for y in range(10, 300, 22))
    L, R = cx - w / 2, cx + w / 2; t = r.randint(26, 46)
    road = f'M{L - 40} 312 C{L - 10} 300, {R + 30} 272, {R} 236 C{R - 20} 210, {L - 6} 214, {L} 182 C{L + 6} 150, {R + 18} 156, {R} 122 C{R - 10} 96, {L + 10} 98, {L + 18} 74 C{L + 26} 54, {cx + 10} 52, {cx + 8} {t}'
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="4.2" fill="#0F1B45"/>' for x, y in ((R - 6, 232), (L + 2, 180), (R - 4, 124)))
    flag = f'<path d="M{cx + 8} {t} v-22" stroke="#0F1B45" stroke-width="2"/><path d="M{cx + 8} {t - 22} l16 6 -16 6z" fill="#0F1B45"/>'
    svg = (f'{lines}<defs><linearGradient id="col{s}" x1="0" x2="1"><stop offset="0" stop-color="{l}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>'
           f'<rect x="{L}" y="{t + 4}" width="{w}" height="{310 - t}" fill="url(#col{s})" opacity=".95"/><path d="{road}" fill="none" stroke="#F7F8FB" stroke-width="14" stroke-linecap="round"/>{dots}{flag}')
    return wrap(f'background:linear-gradient(160deg,{a} 0%,{b} 100%)', svg, c, 'b1', 'x2-b--half')
# B-2 放射線：一点から広がる細い線（ひらめき・広がり）
def b2(c):
    s, k = c[0], c[2]; a, b, l = GR[k]; r = rnd(s); fx, fy = 300 + r.randint(-20, 60), 120 + r.randint(-30, 40)
    d = ''.join(f'M{fx + 46 * math.cos(t):.1f} {fy + 46 * math.sin(t):.1f}L{fx + 700 * math.cos(t):.1f} {fy + 700 * math.sin(t):.1f}' for t in (i * math.pi / 60 for i in range(120)))
    svg = (f'<defs><radialGradient id="rg{s}" gradientUnits="userSpaceOnUse" cx="{fx}" cy="{fy}" r="420"><stop offset="0" stop-color="{l}" stop-opacity="0"/><stop offset=".25" stop-color="{l}" stop-opacity=".35"/><stop offset="1" stop-color="{l}" stop-opacity=".95"/></radialGradient>'
           f'<linearGradient id="fade{s}" x1="0" x2="1"><stop offset="0" stop-color="{a}" stop-opacity=".9"/><stop offset=".55" stop-color="{a}" stop-opacity="0"/></linearGradient></defs>'
           f'<path d="{d}" stroke="url(#rg{s})" stroke-width="1.6"/><rect width="480" height="300" fill="url(#fade{s})"/>')
    return wrap(f'background:linear-gradient(135deg,{a} 0%,{b} 100%)', svg, c, 'b2')
# B-3／B-4 光の筋：左の一点から右へ広がる線の束（加速・前進）
def streaks(s, a, b, l, dark):
    r = rnd(s, 'st'); px, py = 30 + r.randint(0, 30), 110 + r.randint(-20, 30); out = []
    for i in range(46):
        y = -60 + i * 9 + r.uniform(-4, 4); bend = r.uniform(.3, .7)
        col = r.choice([b, l, a] if dark else [a, b, b]); op = r.uniform(.25, .9); w = r.uniform(.5, 2.2)
        dash = f' stroke-dasharray="{r.randint(10, 40)} {r.randint(4, 14)}"' if r.random() < .25 else ''
        out.append(f'<path d="M{px} {py} C{px + 160} {py}, {260} {py + (y - py) * bend:.1f}, 500 {y:.1f}" stroke="{col}" stroke-width="{w:.2f}" opacity="{op:.2f}" fill="none"{dash}/>')
    g = ''.join(out)
    return f'<defs><filter id="gl{s}{int(dark)}"><feGaussianBlur stdDeviation="5"/></filter></defs><g filter="url(#gl{s}{int(dark)})" opacity="{.9 if dark else .5}">{g}</g>{g}'
def b3(c):
    s, k = c[0], c[2]; a, b, l = GR[k]
    fade = f'<defs><linearGradient id="fd3{s}" x1="0" y1="0" x2="0" y2="1"><stop offset=".45" stop-color="#0A1230" stop-opacity="0"/><stop offset=".9" stop-color="#0A1230" stop-opacity=".85"/></linearGradient></defs><rect width="480" height="300" fill="url(#fd3{s})"/>'
    return wrap('background:radial-gradient(120% 120% at 100% 50%,#13224F 0%,#0A1230 70%)', streaks(s, a, b, l, True) + fade, c, 'b3')
def b4(c):
    s, k = c[0], c[2]; a, b, l = GR[k]
    fade = f'<defs><linearGradient id="fd4{s}" x1="0" y1="0" x2="0" y2="1"><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset=".88" stop-color="#fff" stop-opacity=".92"/></linearGradient></defs><rect width="480" height="300" fill="url(#fd4{s})"/>'
    return wrap(f'background:linear-gradient(90deg,#FFFFFF 0%,#F7F8FB 50%,{l}55 100%)', streaks(s, a, b, l, False) + fade, c, 'b4', 'x2-b--ink')
def card(fn, c):
    nm, col, bgc = CAT[c[2]]
    return f'<div class="cd"><div class="th">{fn(c)}</div><div class="bd"><span class="chip" style="--cc:{col};--cb:{bgc}">{nm}</span><h3>{c[1]}</h3><p class="mt">{c[5]}・{c[4]}</p></div></div>'
row = lambda fn: '<div class="grid g3">' + ''.join(card(fn, c) for c in SEL) + '</div>'
def ref(t): return f'<div class="ref"><span>参考にした要素：{t}</span></div>'
css = '''.g3{grid-template-columns:repeat(3,1fr);gap:22px}.cd{background:#fff;border-radius:14px;box-shadow:0 0 0 1px #E6E9F0;overflow:hidden}.th{aspect-ratio:16/10}
.cv{position:relative;width:100%;height:100%;overflow:hidden;isolation:isolate;color:#fff;word-break:keep-all;overflow-wrap:anywhere}.cv>svg.bgs{position:absolute;inset:0;width:100%;height:100%;z-index:-1}
.bd{padding:14px 18px 18px}.chip{display:inline-block;background:var(--cb);color:var(--cc);font-size:11.5px;font-weight:700;padding:2px 10px;border-radius:999px}.bd h3{font-size:17px;margin:8px 0 4px}.mt{font-size:12.5px;color:#676688}
.x2-i{position:absolute;left:22px;top:20px;width:30px;height:30px;color:#fff;opacity:.95}.x2-b{position:absolute;left:22px;right:60px;bottom:18px}.x2-k{font-size:11.5px;font-weight:700;letter-spacing:.08em;opacity:.85;margin-bottom:3px}.x2-d{font-size:19px;font-weight:900;line-height:1.35}
.x2-b--half{right:46%}.b4{color:#0F1B45}.b4 .x2-i{color:#0F1B45}
.ref{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 16px}.ref span{font-size:12.5px;background:#F7F8FB;border-radius:999px;padding:5px 12px;color:#4A4E6A}
.cmp{width:100%;border-collapse:collapse;font-size:14px}.cmp th,.cmp td{border-bottom:1px solid #E6E9F0;padding:10px 12px;text-align:left}.cmp th{background:#F7F8FB;font-weight:700}'''
pats = [
 pat('いま', 'C-4 グラデーション＋形（比較用）', 'いまサイトに入っている背景です。', [], row(c4)),
 pat('B-1', '道のり（柱をのぼる S 字の道）', 'カテゴリ色の地に、柱をのぼっていく白い道と、途中の印（章）・頂上の旗を置きます。「学びを積み上げて、ゴール（成果物）に着く」というコースの流れをそのまま絵にした案です。左上には細い等高線を薄く敷きます。',
     [('◎', 'コースの意味（積み上げ・ゴール）が伝わる'), ('○', '道の形・柱の位置はコースごとに自動で変わる'), ('△', '絵が右半分を使うので、成果物名の幅がせまい')], ref('S字の道・頂上・等高線') + row(b1), True),
 pat('B-2', '放射線（一点から広がる線）', '一点から細い線が放射状に広がります。中心は暗く、外へ行くほど明るい色。左側は文字が読めるよう地色でなだらかに隠します。',
     [('○', '集中・ひらめきの印象'), ('○', '中心の位置はコースごとに自動で変わる'), ('△', '線が細かく、小さいサイズでは模様に見える')], ref('放射状の細い線・中心の暗い円') + row(b2)),
 pat('B-3', '光の筋（濃紺）', '濃紺の地に、左の一点から右へ広がる光の線の束。加速・前進の印象です。線の一部は点線にして、データが流れるような動きを出しています。',
     [('◎', 'スピード感・先進的な印象'), ('△', '白いサイトの中で暗さが目立つ'), ('△', 'カテゴリ色の見分けが弱くなる')], ref('光の線の束・暗い地・点線') + row(b3)),
 pat('B-4', '光の筋（明るい地）', 'B-3 と同じ線の束を、白〜淡いカテゴリ色の地に置いた案。文字は濃紺。白いサイトに自然になじみます。',
     [('◎', 'サイトの白と調和'), ('○', '前進の印象は残る'), ('△', '一覧で目立つ力は弱め')], ref('光の線の束（明るい地に置き換え）') + row(b4)),
]
cmp = '<section class="pat"><h2>比べると</h2><table class="cmp"><tr><th></th><th>いま C-4</th><th>B-1 道のり</th><th>B-2 放射線</th><th>B-3 光の筋（濃紺）</th><th>B-4 光の筋（明るい）</th></tr>' + ''.join('<tr>' + ''.join(f'<{"th" if j == 0 else "td"}>{v}</{"th" if j == 0 else "td"}>' for j, v in enumerate(r)) + '</tr>' for r in [
 ('伝わる意味', 'やわらかさ', '◎ 積み上げ・ゴール', 'ひらめき', '前進・スピード', '前進'), ('カテゴリの見分け', '◎', '◎', '○', '△', '○'), ('白いサイトとの調和', '○', '○', '○', '△', '◎'),
 ('成果物名の読みやすさ', '◎', '○（幅が半分）', '○', '◎', '◎'), ('自動生成', '◎', '◎', '◎', '◎', '◎')]) + '</table><p class="d" style="margin-top:14px">おすすめは <b>B-1 道のり</b>。背景が「飾り」ではなく、コースの意味（章を進んで成果物にたどり着く）を表すので、X-2 の「つくるもの」と話がつながります。人物は入れず、道の印と旗で表しています。</p></section>'
open('bg.html', 'w').write(board('サムネイルの背景　ほかの4つの型', '参考画像（S字の道・放射線・光の筋）の「表現」を、いまのカテゴリ色で作り直しました。中身は X-2（つくるもの）のまま、カードに入れた状態で比べています。形や配置は参考画像を写していません。', pats + [cmp], css))
