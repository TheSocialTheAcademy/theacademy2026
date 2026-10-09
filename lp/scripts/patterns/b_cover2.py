from common import *; from mock import mock, MOCK_CSS
import hashlib, random
SEL = [C[0], C[2], C[3], C[4], C[7], C[1]]
GR = {'it': ('#1E9E62', '#3E78FE', '#BFEAD3'), 'mk': ('#E46A1F', '#F29A50', '#FFD9C2'), 'en': ('#0141D4', '#3E78FE', '#B9CCFF'), 'biz': ('#6B4FD8', '#3E78FE', '#D5CCFF'), 'cr': ('#D9467A', '#F76B38', '#F9C8D8')}
def rnd(s): return random.Random(int(hashlib.md5(s.encode()).hexdigest()[:8], 16))
def bg(c, inner):
    s, k = c[0], c[2]; a, b, l = GR[k]; r = rnd(s); x1, y1, x2 = r.randint(-60, 40), r.randint(-80, 0), r.randint(260, 360); ang, cy, rad = r.randint(110, 160), r.randint(20, 90), r.randint(110, 150)
    return (f'<div class="cv" style="background:linear-gradient({ang}deg,{a} 0%,{b} 100%)"><svg class="bgs" viewBox="0 0 480 300"><path d="M{x1} {y1} C{x1 + 220} {y1 + 40}, {x1 + 120} {y1 + 230}, {x1 + 300} {y1 + 380} L{x1 - 40} {y1 + 380}Z" fill="#fff" opacity=".13"/>'
            f'<circle cx="{x2}" cy="{cy}" r="{rad}" fill="#fff" opacity=".12"/><circle cx="{x2 + 80}" cy="260" r="90" fill="{l}" opacity=".22"/></svg>{inner}</div>')
# X-1 アイコンだけ
def x1(c): return bg(c, ic(c[3], 'x1-i', 1.3))
# X-2 つくるもの（成果物の名前）＋小さなアイコン
def x2(c): return bg(c, f'{ic(c[3], "x2-i", 1.6)}<div class="x2-b"><p class="x2-k">つくるもの</p><p class="x2-d">{c[6]}</p></div>')
# X-3 学習の目安を大きく
def x3(c):
    f = c[5].split('・'); big = f[-1] if '分' in f[-1] else f[0]
    return bg(c, f'<p class="x3-b">{big.replace("約", "<small>約</small>")}</p><p class="x3-s">{"動画で学べる時間" if "分" in big else ("受講期間" if "週" in big or "月" in big else "")}</p>')
# X-4 成果物の模型（白）
def x4(c): return bg(c, f'<div class="x4-m">{mock(c[7], c[8], CAT[c[2]][1], c[6])}</div><span class="x4-t">作例</span>')
def card(fn, c):
    nm, col, b = CAT[c[2]]
    return f'<div class="cd"><div class="th">{fn(c)}</div><div class="bd"><span class="chip" style="--cc:{col};--cb:{b}">{nm}</span><h3>{c[1]}</h3><p class="mt">{c[5]}・{c[4]}</p></div></div>'
row = lambda fn: '<div class="grid g3">' + ''.join(card(fn, c) for c in SEL) + '</div>'
css = MOCK_CSS + '''.g3{grid-template-columns:repeat(3,1fr);gap:22px}.cd{background:#fff;border-radius:14px;box-shadow:0 0 0 1px #E6E9F0;overflow:hidden}.th{aspect-ratio:16/10}
.cv{position:relative;width:100%;height:100%;overflow:hidden;isolation:isolate;color:#fff;word-break:keep-all;overflow-wrap:anywhere}.cv>svg.bgs{position:absolute;inset:0;width:100%;height:100%;z-index:-1}
.bd{padding:14px 18px 18px}.chip{display:inline-block;background:var(--cb);color:var(--cc);font-size:11.5px;font-weight:700;padding:2px 10px;border-radius:999px}.bd h3{font-size:17px;margin:8px 0 4px}.mt{font-size:12.5px;color:#676688}
.x1-i{position:absolute;left:50%;top:50%;width:96px;height:96px;transform:translate(-50%,-50%);color:#fff}
.x2-i{position:absolute;left:22px;top:20px;width:30px;height:30px;color:#fff;opacity:.95}.x2-b{position:absolute;left:22px;right:70px;bottom:18px}.x2-k{font-size:11.5px;font-weight:700;letter-spacing:.08em;opacity:.85;margin-bottom:3px}
.x2-d{font-size:19px;font-weight:900;line-height:1.35}
.x3-b{position:absolute;left:22px;bottom:34px;font:800 54px/1 'Helvetica Neue',Arial,'Noto Sans JP',sans-serif;letter-spacing:-.01em}.x3-b small{font-size:22px;margin-right:4px;font-weight:700}.x3-s{position:absolute;left:24px;bottom:16px;font-size:11.5px;font-weight:700;opacity:.85}
.x4-m{color:#0F1B45;position:absolute;inset:6% 16% 0 16%;--mk:6.6px}.x4-m .mk-pg{inset:8% 4% -6% 4%}.x4-m .mk-pg2{display:none}.x4-t{position:absolute;right:12px;top:10px;background:rgba(15,27,69,.55);font-size:10.5px;font-weight:700;padding:2px 9px;border-radius:4px}
.cmp{width:100%;border-collapse:collapse;font-size:14px}.cmp th,.cmp td{border-bottom:1px solid #E6E9F0;padding:10px 12px;text-align:left}.cmp th{background:#F7F8FB;font-weight:700}'''
pats = [
 pat('X-1', 'アイコンだけ', '背景の上に、コースの線アイコンを白で1つだけ置きます。文字がないので、下のコース名と重なりません。いまの theacademyjapan.org の「大きなアイコン」の考え方も引き継げます。',
     [('◎', '一番すっきり・重複なし'), ('◎', '自動生成が一番かんたん'), ('△', 'アイコンだけでは中身までは伝わらない')], row(x1)),
 pat('X-2', 'つくるもの（成果物の名前）', '「つくるもの」と、そのコースで完成する成果物の名前を入れます。下のカードにはない情報なので重複せず、「学んで、つくる」をサムネイルの段階で伝えられます。',
     [('◎', 'カードにない情報を足せる'), ('◎', 'サイトのコンセプト（成果物）と一致'), ('○', '成果物名が決まれば自動生成')], row(x2), True),
 pat('X-3', '学習の目安を大きく', '「約107分」「8週間」など、学習の目安を大きな数字で見せます。ただし下のカードにも同じ情報があるため、重複は残ります。',
     [('○', '数字は一目で目に入る'), ('×', 'カードの期間・時間と重複')], row(x3)),
 pat('X-4', '成果物の模型', '成果物の模型（企画書・スマホ・表・チャット・スライド）を白い紙で置きます。いちばん中身が伝わりますが、サムネイルの大きさでは模型の文字は読めません。',
     [('◎', 'つくるものが絵で分かる'), ('△', '小さいと情報が細かすぎる'), ('△', 'コース詳細の成果物画像と見た目が重なる')], row(x4)),
]
cmp = '<section class="pat"><h2>比べると</h2><table class="cmp"><tr><th></th><th>X-1 アイコンだけ</th><th>X-2 つくるもの</th><th>X-3 学習の目安</th><th>X-4 成果物の模型</th></tr>' + ''.join('<tr>' + ''.join(f'<{"th" if j == 0 else "td"}>{v}</{"th" if j == 0 else "td"}>' for j, v in enumerate(r)) + '</tr>' for r in [
 ('下のカードとの重複', 'なし', 'なし（カードにない情報）', 'あり（期間・時間）', 'なし'), ('伝わること', 'テーマ', '◎ 完成するもの', '学習量', '◎ 完成するもの（絵）'), ('小さいサイズ（スマホ）', '◎', '○', '◎', '△'), ('自動生成', '◎', '◎', '◎', '○')]) + '</table><p class="d" style="margin-top:14px">おすすめは <b>X-2</b>。カードにすでにある「コース名・カテゴリ・期間」を繰り返さず、カードにない「何が完成するか」を足せます。サイト全体の「学んで、つくる」とも一致します。成果物名がまだ仮のコースは、確定まで X-1（アイコンだけ）にしておく使い分けもできます。</p></section>'
open('cover2.html', 'w').write(board('コースのサムネイル　背景（C-4）の上に入れるもの', 'コース名とカテゴリは下のカードに出ているため、サムネイルには別の情報を入れる案です。背景は C-4 のまま。カードに入れた状態で比べています。', pats + [cmp], css))
