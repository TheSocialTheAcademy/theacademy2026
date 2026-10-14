from common import *
import hashlib, random
import os; T = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets', 'thumbs') + '/'
MONO = {'it': ('#1E9E62', '#2FAE73'), 'mk': ('#E46A1F', '#F29A50'), 'en': ('#0141D4', '#3E78FE'), 'biz': ('#6B4FD8', '#8A70E8'), 'cr': ('#D9467A', '#E8608F'), 'ca': ('#0F1B45', '#3A4A80')}
K = {'IT・デジタル': 'it', 'マーケティング': 'mk', '英語・TOEIC': 'en', 'ビジネス': 'biz', 'クリエイティブ': 'cr', 'キャリア・学び方': 'ca'}
# 記事：カテゴリ, タイトル, ひと言（大）, 補足, アイコン
ART = [('キャリア・学び方', '働きながら学びを続けるための、週2時間のつくり方', '週2時間', 'のつくり方', 'clock'),
       ('IT・デジタル', 'ChatGPTを仕事の相棒にする、最初の5つの使い方', '5つ', 'ChatGPTの使い方', 'spark'),
       ('マーケティング', '顧客理解から始めるSNSキャンペーン設計', '顧客理解', 'から始めるSNS設計', 'mega'),
       ('英語・TOEIC', '会議で使える、短い英語フレーズ20', '20', '会議の英語フレーズ', 'chat'),
       ('キャリア・学び方', '未経験から実績をつくる、ポートフォリオの育て方', '実績', 'をつくるポートフォリオ', 'user'),
       ('ビジネス', '小さなイベントを成功させる、当日の進行表のつくり方', '進行表', '当日のつくり方', 'calendar')]
def rnd(s): return random.Random(int(hashlib.md5(s.encode()).hexdigest()[:8], 16))
def shapes(v, r, col, op, line=False):
    F = (lambda o: f'fill="none" stroke="{col}" stroke-width="1.6" opacity="{min(1, o * 4):.2f}"') if line else (lambda o: f'fill="{col}" opacity="{o:.2f}"')
    if v == 0: return f'<circle cx="{r.randint(330, 380)}" cy="60" r="120" {F(op)}/><circle cx="430" cy="250" r="80" {F(op * .8)}/>'
    if v == 1: return ''.join(f'<path d="M-20 {y} C100 {y - 60}, 220 {y + 40}, 340 {y - 30} S 460 {y - 90}, 520 {y - 70}{" L520 320 L-20 320Z" if not line else ""}" {F(o)}/>' for y, o in ((150, op * .7), (205, op * .9), (255, op)))
    if v == 2: x = r.randint(200, 260); return ''.join(f'<path d="M{x + d} -20 L{x + d + w} -20 L{x + d + w - 260} 320 L{x + d - 260} 320Z" {F(o)}/>' for d, w, o in ((60, 60, op), (150, 34, op * 1.2), (210, 90, op * .8)))
    if v == 3: return ''.join(f'<circle cx="470" cy="10" r="{rr}" fill="none" stroke="{col}" stroke-width="{(sw if not line else 1.6)}" opacity="{(o if not line else .5)}"/>' for rr, sw, o in ((70, 26, op * 1.2), (140, 18, op), (210, 12, op * .85), (280, 8, op * .7)))
    if v == 4: return f'<g transform="rotate({r.randint(12, 28)} 360 120)"><rect x="290" y="10" width="160" height="160" rx="34" {F(op)}/><rect x="390" y="150" width="110" height="110" rx="26" {F(op * .8)}/></g>'
    return f'<path d="M320 -30 C430 -10, 520 80, 470 170 C430 250, 340 240, 300 170 C250 100, 240 -40, 320 -30Z" {F(op)}/>'
def svg(inner): return f'<svg class="bgs" viewBox="0 0 480 270" preserveAspectRatio="xMidYMid slice">{inner}</svg>'
# EA：淡色＋形（コースの姉妹。コースは濃い色、記事は淡い色）
def ea(a, i):
    c, t, kw, sub, icn = a; k = K[c]; nm, col, bg = CAT[k]; r = rnd(t)
    return f'<div class="ey" style="background:{bg};--cc:{col}">{svg(shapes(i % 6, r, col, .10))}<p class="lab">学びのヒント</p><p class="kw">{kw}</p><p class="sb">{sub}</p></div>'
# EB：白地に線の形（いちばん軽い）
def eb(a, i):
    c, t, kw, sub, icn = a; k = K[c]; nm, col, bg = CAT[k]; r = rnd(t)
    return f'<div class="ey eb" style="background:#fff;--cc:{col}">{svg(shapes(i % 6, r, col, .12, True))}<p class="lab">学びのヒント</p><p class="kw kw--ink">{kw}</p><span class="bar"></span><p class="sb">{sub}</p></div>'
# EC：ノートの1ページ（罫線＋見出し）
def ec(a, i):
    c, t, kw, sub, icn = a; k = K[c]; nm, col, bg = CAT[k]
    rules = ''.join(f'<path d="M0 {y}H480" stroke="#D9DEE8" stroke-width="1"/>' for y in range(36, 270, 26))
    margin = f'<path d="M64 0V270" stroke="{col}" stroke-width="2" opacity=".55"/>'
    return (f'<div class="ey ec" style="background:#FCFCFA;--cc:{col}">{svg(rules + margin)}'
            f'<span class="tab">{nm}</span>{ic(icn, "ec-i", 1.5)}<p class="kw kw--ink ec-k">{kw}</p><p class="sb ec-s">{sub}</p></div>')
# ED：大きな文字（ひと言をはみ出すほど大きく）
def ed(a, i):
    c, t, kw, sub, icn = a; k = K[c]; nm, col, bg = CAT[k]; c1, c2 = MONO[k]
    return f'<div class="ey ed" style="background:{bg};--cc:{col}"><p class="ed-k">{kw}</p><p class="lab">学びのヒント</p><p class="sb ed-s">{sub}</p></div>'
def card(fn, a, i):
    k = K[a[0]]; nm, col, bg = CAT[k]
    return f'<div class="cd"><div class="th">{fn(a, i)}</div><div class="bd"><p class="mt"><span class="chip" style="--cc:{col};--cb:{bg}">{nm}</span>2026.09.08・5分で読める</p><h3>{a[1]}</h3></div></div>'
row = lambda fn: '<div class="grid g3">' + ''.join(card(fn, a, i) for i, a in enumerate(ART)) + '</div>'
def course(slug, name, catk, meta):
    nm, col, bg = CAT[catk]
    return f'<div class="cd"><div class="th th--c"><img src="{T}{slug}.webp" alt=""></div><div class="bd"><span class="chip" style="--cc:{col};--cb:{bg}">{nm}</span><h3>{name}</h3><p class="mt">{meta}</p></div></div>'
mix = lambda fn: ('<p class="lbl">コース（いまのサムネイル）</p><div class="grid g3">' + course('sns-marketing', 'SNSマーケティング実践', 'mk', '8週間・プロ') + course('ai-efficiency', '生成AI 業務改善', 'it', '6週間・プロ') + course('toeic-700', 'TOEIC L&R 700点突破', 'en', '3か月・プレミア') + '</div>'
                  + '<p class="lbl" style="margin-top:18px">記事（この型）</p><div class="grid g3">' + ''.join(card(fn, a, i) for i, a in enumerate(ART[:3])) + '</div>')
css = '''.g3{grid-template-columns:repeat(3,1fr);gap:22px}.cd{background:#fff;border-radius:14px;box-shadow:0 0 0 1px #E6E9F0;overflow:hidden}.th{aspect-ratio:16/9}.th--c{aspect-ratio:16/10}.th--c img{width:100%;height:100%;object-fit:cover;display:block}
.ey{position:relative;width:100%;height:100%;overflow:hidden;isolation:isolate;color:#0F1B45;word-break:keep-all;overflow-wrap:anywhere}.ey>svg.bgs{position:absolute;inset:0;width:100%;height:100%;z-index:-1}
.bd{padding:14px 18px 18px}.chip{display:inline-block;background:var(--cb);color:var(--cc);font-size:11.5px;font-weight:700;padding:2px 10px;border-radius:999px;margin-right:8px}.bd h3{font-size:16px;margin:8px 0 4px;line-height:1.5}.mt{font-size:12.5px;color:#676688}
.lab{position:absolute;left:20px;top:16px;font-size:10.5px;font-weight:900;letter-spacing:.14em;color:var(--cc)}
.kw{position:absolute;left:20px;bottom:44px;font-size:44px;font-weight:900;line-height:1.05;color:var(--cc);letter-spacing:.01em}.kw--ink{color:#0F1B45}.sb{position:absolute;left:20px;bottom:18px;font-size:15px;font-weight:800}
.eb .kw{bottom:50px}.bar{position:absolute;left:20px;bottom:42px;width:36px;height:4px;border-radius:2px;background:var(--cc)}
.tab{position:absolute;left:80px;top:0;background:var(--cc);color:#fff;font-size:11px;font-weight:700;padding:5px 12px 6px;border-radius:0 0 8px 8px}.ec-i{position:absolute;right:18px;top:14px;width:24px;height:24px;color:var(--cc)}
.ec-k{left:80px;bottom:46px;font-size:38px}.ec-s{left:80px}
.ed-k{position:absolute;left:-6px;right:-30px;top:42%;transform:translateY(-50%);font-size:110px;font-weight:900;line-height:1;color:var(--cc);opacity:.92;white-space:nowrap;letter-spacing:-.02em}.ed-s{bottom:16px}
.cmp{width:100%;border-collapse:collapse;font-size:14px}.cmp th,.cmp td{border-bottom:1px solid #E6E9F0;padding:10px 12px;text-align:left}.cmp th{background:#F7F8FB;font-weight:700}
.why{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:6px}.why div{background:#F7F8FB;border-radius:12px;padding:14px 16px;font-size:13.5px;line-height:1.7;color:#4A4E6A}.why b{display:block;color:#0F1B45;font-size:14.5px;margin-bottom:4px}'''
why = ('<section class="pat"><h2>考え直した理由</h2><div class="why">'
       '<div><b>① コースと見分ける</b>コースのサムネイルが「濃い単色＋形」に決まったので、記事は同じ家族に見せつつ、ひと目で「読み物」と分かる必要がある。</div>'
       '<div><b>② タイトルと重ねない</b>カードの下にタイトルが出るので、画像にはタイトルを書かず、記事の「ひと言」だけを大きく置く（前回の E-B の考え方は残す）。</div>'
       '<div><b>③ 探さずに作れる</b>記事が増えても、写真を探さずにデータ（カテゴリ・ひと言）から自動で作れる。今ある画像の流用（E-C）はやめられる。</div></div></section>')
pats = [
 pat('EA', '淡い色＋形（コースの姉妹）', 'コースと同じ6種類の形と同じカテゴリ色を使い、地色だけを淡くします。「濃い＝コース／淡い＝記事」というルールで、並んでも見分けがつき、サイト全体の統一感も保てます。キャリア・学び方は濃紺。',
     [('◎', 'コースと同じ仕組みで自動生成'), ('◎', '濃淡で記事とコースを見分けられる'), ('○', 'ひと言を決めるだけ')], row(ea), True),
 pat('EB', '白地に線の形', '白地に、カテゴリ色の細い線で形を描きます。いちばん軽く、文章を読む場所らしい落ち着いた印象です。',
     [('○', '軽い・上品'), ('△', '一覧では印象が弱く、記事どうしの違いも出にくい')], row(eb)),
 pat('EC', 'ノートの1ページ', '罫線のノートに、カテゴリ色の見出しタブとひと言。「学びのヒント」らしさが一番伝わりますが、絵がすべて同じになりやすい型です。',
     [('◎', '「学びのメモ」らしさ'), ('△', '全記事が同じ絵に見える'), ('△', '罫線が細く、スマホでは見えにくい')], row(ec)),
 pat('ED', '大きな文字', 'ひと言を、はみ出すほど大きく置きます。雑誌の表紙のような強さがあり、記事ごとの違いもはっきりします。',
     [('◎', '記事ごとの違いが一番出る'), ('○', '文字だけで作れる'), ('△', '長いひと言（5文字以上）は入らない')], row(ed)),
 '<section class="pat"><h2><em class="rec">EA</em>トップで、コースと記事が並んだとき</h2><p class="d">コースは濃い色、記事は淡い色。同じ形の家族でも、ひと目で「コース」と「読み物」が分かれます。</p>' + mix(ea) + '</section>',
]
cmp = '<section class="pat"><h2>比べると</h2><table class="cmp"><tr><th></th><th>EA 淡い色＋形</th><th>EB 白地に線</th><th>EC ノート</th><th>ED 大きな文字</th><th>前回 E-C（今ある画像）</th></tr>' + ''.join('<tr>' + ''.join(f'<{"th" if j == 0 else "td"}>{v}</{"th" if j == 0 else "td"}>' for j, v in enumerate(r)) + '</tr>' for r in [
 ('コースとの見分け', '◎ 濃淡で分かれる', '◎', '◎', '○', '△ 成果物画像と重なる'), ('サイトの統一感', '◎ 同じ形の家族', '○', '△', '○', '△'), ('記事ごとの違い', '○', '△', '△', '◎', '○'),
 ('作りやすさ', '◎ 自動', '◎ 自動', '◎ 自動', '◎ 自動', '× 画像選び'), ('スマホでの見やすさ', '◎', '○', '△', '◎', '○')]) + '</table><p class="d" style="margin-top:14px">おすすめは <b>EA</b>。コースのサムネイルと同じ仕組み（カテゴリ色・6種類の形）で作れるので、生成スクリプトも共通にできます。「濃い＝コース／淡い＝記事」の1ルールで、トップのように両方が並ぶ場所でも混ざりません。</p></section>'
open('eye2.html', 'w').write(board('記事のアイキャッチ　考え直した4つの型', 'コースのサムネイル（カテゴリの単色＋形6種類＋つくるもの）が決まったので、記事のアイキャッチを「コースと見分けられるか」「タイトルと重ならないか」「探さずに作れるか」で考え直しました。', [why] + pats + [cmp], css))
