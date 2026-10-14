from common import *
import hashlib, random
SEL = [C[0], C[1], C[2], C[3], C[4], C[7]]
# カテゴリごとのグラデーション（今のカテゴリ色＋ブランドの青系）
GR = {'it': ('#1E9E62', '#3E78FE', '#BFEAD3'), 'mk': ('#E46A1F', '#F7B267', '#FFD9C2'), 'en': ('#0141D4', '#3E78FE', '#B9CCFF'),
      'biz': ('#6B4FD8', '#3E78FE', '#D5CCFF'), 'cr': ('#D9467A', '#F76B38', '#F9C8D8'), 'ca': ('#0F1B45', '#3E78FE', '#C9D3EA')}
def rnd(slug): return random.Random(int(hashlib.md5(slug.encode()).hexdigest()[:8], 16))
NOISE = '<filter id="{i}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope=".55"/></feComponentTransfer></filter>'
def name(c): return c[1].replace('Slack×GAS スマート管理ツール', 'Slack×GAS<wbr> スマート管理ツール')
def txt(c, dark=False):
    nm, col, bg = CAT[c[2]]
    return f'<span class="ck {"ck--d" if dark else ""}" style="--cc:{col}">{nm}</span><p class="cn{" cn--l" if len(c[1]) > 12 else ""}">{name(c)}</p><p class="cl">THE ACADEMY</p>'
# ① グラデーションの曲線（粒子感のある大きな曲面）
def c1(c):
    s, k = c[0], c[2]; a, b, l = GR[k]; r = rnd(s); y = 130 + r.randint(-25, 25); x = 250 + r.randint(-20, 30); i = 'n1' + s; v = r.randint(0, 2)
    if v == 0:   # 上下2枚の曲面
        p1, p2 = f'M{x} -10 C{x + 40} {y - 60} {x + 110} {y - 8} 490 {y} L490 -10Z', f'M{x + 30} 310 C{x + 50} {y + 70} {x + 120} {y + 10} 490 {y + 4} L490 310Z'
    elif v == 1:  # 右下から立ち上がる大きな丘と、上の細い帯
        p1, p2 = f'M{x + 120} -10 C{x + 150} 30 {x + 200} 50 490 {40 + r.randint(0, 30)} L490 -10Z', f'M{x - 40} 310 C{x + 10} {y + 60} {x + 90} {y - 70} 490 {y - 90} L490 310Z'
    else:         # 上から大きく垂れる曲面と、下の小さな曲面
        p1, p2 = f'M{x - 20} -10 C{x - 10} {y + 40} {x + 80} {y + 70} 490 {y + 60} L490 -10Z', f'M{x + 120} 310 C{x + 140} {y + 120} {x + 190} {y + 100} 490 {y + 96} L490 310Z'
    return (f'<div class="cv c1"><svg viewBox="0 0 480 300" preserveAspectRatio="none"><defs>{NOISE.format(i=i)}'
            f'<linearGradient id="g1{s}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{l}"/><stop offset=".55" stop-color="{b}"/><stop offset="1" stop-color="{a}"/></linearGradient>'
            f'<linearGradient id="g2{s}" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{a}"/><stop offset=".6" stop-color="{b}"/><stop offset="1" stop-color="{l}"/></linearGradient>'
            f'<clipPath id="cp{s}"><path d="{p1}"/><path d="{p2}"/></clipPath></defs><path d="{p1}" fill="url(#g1{s})"/><path d="{p2}" fill="url(#g2{s})"/>'
            f'<g clip-path="url(#cp{s})" style="mix-blend-mode:overlay"><rect width="480" height="300" filter="url(#{i})"/></g></svg>{txt(c)}</div>')
# ② リボンの波（白地に流れる半透明の帯と細い線）
def c2(c):
    s, k = c[0], c[2]; a, b, l = GR[k]; r = rnd(s); h = r.randint(-15, 15); i = 'b2' + s
    rib = lambda d, sh=0: f'M-30 {300 + d} C140 {300 + d}, {250 + h} {290 + d}, {320 + h + sh} {190 + d * .4} S {400 + h} {-10 + d * .3}, {470 + sh} -30'
    waves = ''.join(f'<path d="{rib(d)}" fill="none" stroke="url(#w{s})" stroke-width="{w}" stroke-linecap="round" opacity="{o}"/>' for d, w, o in ((-30, 90, .28), (0, 60, .5), (30, 34, .9)))
    lines = ''.join(f'<path d="{rib(d, 8)}" fill="none" stroke="#fff" stroke-width="1.3" opacity=".95"/>' for d in (12, 42))
    return (f'<div class="cv c2"><svg viewBox="0 0 480 300"><defs><linearGradient id="w{s}" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{l}" stop-opacity=".3"/><stop offset=".55" stop-color="{b}"/><stop offset="1" stop-color="{a}"/></linearGradient>'
            f'<filter id="{i}"><feGaussianBlur stdDeviation="8"/></filter></defs><g filter="url(#{i})" opacity=".7">{waves}</g>{waves}{lines}</svg>{txt(c)}</div>')
# ③ 光の面（濃紺に、カテゴリ色の光が差す）
def c3(c):
    s, k = c[0], c[2]; a, b, l = GR[k]; r = rnd(s); fx, fy, ang = r.randint(55, 80), r.randint(25, 55), r.randint(180, 260)
    nm, col, bg = CAT[k]
    return (f'<div class="cv c3" style="background:conic-gradient(from {ang}deg at {fx}% {fy}%, #0B1433 0deg, {a} 38deg, {l} 52deg, {b} 70deg, #0B1433 120deg, #0B1433 360deg)">'
            f'<div class="c3-v"></div>{ic(c[3], "c3-i", 1.5)}<span class="c3-no">{C.index(c) + 1:02d}</span>{txt(c, True)}</div>')
# ④ やわらかいグラデーション＋形（鮮やかな地に半透明の形）
def c4(c):
    s, k = c[0], c[2]; a, b, l = GR[k]; r = rnd(s); x1, y1, x2 = r.randint(-60, 40), r.randint(-80, 0), r.randint(260, 360)
    return (f'<div class="cv c4" style="background:linear-gradient({r.randint(110, 160)}deg,{a} 0%,{b} 100%)"><svg viewBox="0 0 480 300">'
            f'<path d="M{x1} {y1} C{x1 + 220} {y1 + 40}, {x1 + 120} {y1 + 230}, {x1 + 300} {y1 + 380} L{x1 - 40} {y1 + 380}Z" fill="#fff" opacity=".13"/>'
            f'<circle cx="{x2}" cy="{r.randint(20, 90)}" r="{r.randint(110, 150)}" fill="#fff" opacity=".12"/><circle cx="{x2 + 80}" cy="260" r="90" fill="{l}" opacity=".22"/></svg>{txt(c, True)}</div>')
# ⑤ 図形の積み木（地色＋カテゴリ色の平らな図形を基準線に並べる）
SH = {'circle': '<circle cx="30" cy="30" r="30"/>', 'square': '<rect width="60" height="60" rx="14"/>', 'hex': '<path d="M15 2h30l15 28-15 28H15L0 30z"/>',
      'clover': '<path d="M30 30m-15 -15a15 15 0 1 1 30 0a15 15 0 1 1 0 30a15 15 0 1 1 -30 0a15 15 0 1 1 0 -30z"/>', 'half': '<path d="M0 60A30 30 0 0 1 60 60Z"/>',
      'pill': '<rect width="60" height="60" rx="30"/>'}
def c5(c):
    s, k = c[0], c[2]; a, b, l = GR[k]; r = rnd(s); nm, col, bg = CAT[k]
    keys = r.sample(list(SH), 3); fills = [col, l, '#0F1B45' if r.random() < .5 else b]; r.shuffle(fills)
    shapes = ''.join(f'<svg class="c5-s" viewBox="0 0 60 60" style="color:{f}"><g fill="currentColor">{SH[kk]}</g></svg>' for kk, f in zip(keys, fills))
    top = SH[r.choice(['hex', 'circle', 'clover'])]
    return (f'<div class="cv c5"><div class="c5-row"><div class="c5-stack"><svg class="c5-s" viewBox="0 0 60 60" style="color:{l}"><g fill="currentColor">{top}</g></svg>{shapes.split("</svg>")[0]}</svg></div>'
            + ''.join(x + '</svg>' for x in shapes.split('</svg>')[1:3]) + f'</div><span class="ck" style="--cc:{col}">{nm}</span><p class="cn">{name(c)}</p><p class="cl">THE ACADEMY</p></div>')
row = lambda fn: '<div class="grid g3">' + ''.join(f'<div>{fn(c)}<p class="cap">{c[1]}</p></div>' for c in SEL) + '</div>'
css = '''.g3{grid-template-columns:repeat(3,1fr)}.cv{position:relative;aspect-ratio:16/10;border-radius:10px;overflow:hidden;word-break:keep-all;overflow-wrap:anywhere;isolation:isolate}
.cv>svg{position:absolute;inset:0;width:100%;height:100%;z-index:-1}.ck{position:absolute;left:20px;top:18px;background:#fff;color:var(--cc);font-size:11px;font-weight:700;padding:3px 10px;border-radius:999px}
.ck--d{background:rgba(255,255,255,.16);color:#fff;backdrop-filter:blur(4px)}.cn{position:absolute;left:20px;bottom:34px;max-width:58%;font-size:22px;font-weight:900;line-height:1.3;color:#0F1B45}
.cn--l{font-size:18px}.cl{position:absolute;left:20px;bottom:15px;font-size:9.5px;font-weight:900;letter-spacing:.16em;color:#0F1B45;opacity:.55}
.c1{background:#F7F8FB}.c2{background:linear-gradient(180deg,#fff 0%,#F7F8FB 100%)}.c2 .cn{bottom:auto;top:52px;max-width:56%}
.c3{color:#fff}.c3 .cn,.c3 .cl,.c4 .cn,.c4 .cl{color:#fff}.c3-v{position:absolute;inset:0;background:radial-gradient(120% 90% at 0% 100%,rgba(11,20,51,.92) 0%,rgba(11,20,51,0) 60%);z-index:-1}
.c3 .ck{left:20px}.cv>svg.c3-i{inset:auto;z-index:1;position:absolute;right:20px;top:18px;width:26px;height:26px;color:#fff;opacity:.9}.c3-no{position:absolute;right:20px;bottom:14px;font:700 13px/1 'Helvetica Neue',Arial,sans-serif;letter-spacing:.08em;opacity:.8}
.c4 .cn{max-width:70%}.c5{background:#F7F8FB}.c5-row{position:absolute;right:20px;top:20px;bottom:98px;display:flex;align-items:flex-end;gap:6px;border-bottom:1.5px solid #0F1B45;padding:0 6px}
.c5-stack{display:flex;flex-direction:column;gap:4px}.c5-s{width:58px;height:58px;display:block}.c5 .cn{bottom:34px;max-width:88%}.c5 .ck{top:auto;bottom:auto;top:18px}
.ref{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 16px}.ref span{font-size:12.5px;background:#F7F8FB;border-radius:999px;padding:5px 12px;color:#4A4E6A}
.cmp{width:100%;border-collapse:collapse;font-size:14px}.cmp th,.cmp td{border-bottom:1px solid #E6E9F0;padding:10px 12px;text-align:left}.cmp th{background:#F7F8FB;font-weight:700}
.big{display:grid;grid-template-columns:1.35fr 1fr;gap:18px;align-items:start}.big .cv .cn{font-size:34px}.big .cv .ck{font-size:13px;padding:4px 12px;left:28px;top:26px}.big .cv .cn,.big .cv .cl{left:28px}'''
def ref(t): return f'<div class="ref"><span>参考にした要素：{t}</span></div>'
pats = [
 pat('C-1', 'グラデーションの曲線', '淡い地に、カテゴリ色からブランドの青へ流れる大きな曲面を2枚。表面にうっすら粒子感を乗せ、文字は左の余白に置きます。曲面の位置はコース名から自動で少しずつずらすので、同じカテゴリでも1枚ずつ表情が変わります。',
     [('◎', '上品で、写真がなくても成立する'), ('◎', '色と曲面の位置をデータから自動生成'), ('○', '左に文字の余白が必ず残る')], ref('曲面のグラデーション・粒子感・広い余白') + row(c1), True),
 pat('C-2', 'リボンの波', '白地の右下から、カテゴリ色の半透明の帯が流れ、細い白い線が沿います。軽く、明るい印象。文字は上に置きます。',
     [('○', '明るく、ページの白と自然につながる'), ('△', '帯の色が淡く、カテゴリの見分けは弱め')], ref('流れる帯・細い光の線・白地') + row(c2)),
 pat('C-3', '光の面（濃紺）', '濃紺の地に、カテゴリ色の光が斜めに差し込みます。右上に線アイコン、右下にコース番号。並べたときに一番「シリーズ」らしく見えます。',
     [('◎', '並べたときの統一感が一番強い'), ('○', '番号でコースの数が増えても管理しやすい'), ('△', 'サイト全体は白基調なので、一覧で暗さが目立つ')], ref('同じ配置で光の向きだけ変える・番号・暗い地') + row(c3)),
 pat('C-4', 'やわらかいグラデーション＋形', 'カテゴリ色の鮮やかなグラデーションに、半透明の大きな形を重ね、白い文字を置きます。元気でにぎやかな印象。',
     [('○', '一覧で目に留まりやすい'), ('△', '色が強く、ページの青と競合しやすい（T-A に近い）')], ref('鮮やかなグラデーション・半透明の形・白い文字') + row(c4)),
 pat('C-5', '図形の積み木', '淡い地に、丸・角丸・六角形などの平らな図形を基準線の上に積み、下に大きなコース名。図形の組み合わせはコース名から自動で決めます。',
     [('◎', '親しみやすく、学びの「積み上げ」が伝わる'), ('○', 'データから自動生成'), ('△', '図形の並びが他社の表現と似ないよう注意が必要')], ref('平らな図形・基準線・大きな文字') + row(c5)),
]
CC = [C[2], C[10]]
big = ('<section class="pat"><h2><em class="rec">C-1</em>大きく使ったとき（コース詳細の表紙・Wix ストアの商品画像）</h2><p class="d">同じ型のまま拡大しても崩れません。サムネイルとコース詳細の表紙を同じ画像1枚で済ませられます。</p><div class="big">'
       + f'<div>{c1(CC[0])}<p class="cap">{CC[0][1]}</p></div><div>{c1(CC[1])}<p class="cap">{CC[1][1]}</p></div></div></section>')
cmp = '<section class="pat"><h2>比べると（いまの T-B と並べて）</h2><table class="cmp"><tr><th></th><th>いまの T-B</th><th>C-1 曲線</th><th>C-2 リボン</th><th>C-3 光の面</th><th>C-4 グラデ＋形</th><th>C-5 積み木</th></tr>' + ''.join('<tr>' + ''.join(f'<{"th" if j == 0 else "td"}>{v}</{"th" if j == 0 else "td"}>' for j, v in enumerate(r)) + '</tr>' for r in [
 ('質感・印象', 'すっきり', '◎ 上品', '○ 軽い', '◎ 引き締まる', '○ 元気', '○ 親しみ'), ('カテゴリの見分け', '◎', '◎', '△', '○', '◎', '○'), ('白いサイトとの調和', '◎', '◎', '◎', '△ 暗い', '△ 色が強い', '◎'),
 ('自動生成', '◎', '◎', '◎', '◎', '◎', '◎'), ('コースが増えたとき', '同じ絵になりやすい', '◎ 1枚ずつ表情が変わる', '○', '◎ 番号で管理', '○', '◎ 組み合わせが変わる')]) + '</table><p class="d" style="margin-top:14px">おすすめは <b>C-1</b>。T-B の「カテゴリ色・余白・文字の位置」をそのまま引き継ぎつつ、アイコンの代わりに曲面のグラデーションで質感を上げる案です。同じカテゴリのコースが増えても、曲面の位置が自動で変わるので「同じ絵が並ぶ」問題が起きません。</p></section>'
open('cover.html', 'w').write(board('コースの表紙　参考画像をもとにした5つの型', '参考画像（曲面のグラデーション・流れる帯・光の面・鮮やかなグラデーション・平らな図形）の「表現」だけを取り入れ、色はいまのカテゴリ5色とブランドの青のまま作りました。形や配置は参考画像を写していません。表示は6コース分の例です。', pats + [big, cmp], css))
