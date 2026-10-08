# はじめての方へ（/beginners）ページを、LPの共通部品（02 WHY・06 受講までの流れ・09 公式LINE・07 迷ったら）から組み立てる
# 流れ（プロトタイプ準拠）：見出し → 3つの仕組み → こんな想いに → 受講までの流れ → 料金・お支払い／よくある不安 → 公式LINE → 迷ったら
import os, tempfile
S = os.path.dirname(os.path.abspath(__file__))          # このスクリプトのフォルダ（lp/scripts）
LPDIR = os.path.dirname(S)                              # 出力先（lp）
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')  # 共通部品を取り出すときの捨て出力
import os, re
os.environ['TA_COURSES_OUT'] = TMP_COURSES
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)
head, between, footer_on, ARROW, lp, nx2 = g['head'], g['between'], g['footer_on'], g['ARROW'], g['s'], g['nx2']
base_css = g['css']
OUT = os.path.join(LPDIR, 'beginners.html')

def ic(d, w=1.9): return f'<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{d}</g></svg>'
avatars = re.findall(r'<svg class="avt".*?</svg>', lp, re.S)
av = lambda i, size=48: re.sub(r'width="\d+" height="\d+"', f'width="{size}" height="{size}"', avatars[i % len(avatars)], count=1)
def sec(sid): return re.search(r'<section[^>]*id="%s".*?</section>' % sid, lp, re.S).group(0)
nonum = lambda h: re.sub(r'<p class="sec-num">\d+</p>', '', h)

# ── ① 見出し
pagehead = '''<section class="phead bg-head" aria-labelledby="page-title"><div class="wrap">
<nav class="crumb" aria-label="パンくずリスト"><a href="lp-design.html">トップ</a><span aria-hidden="true">/</span><span aria-current="page">はじめての方へ</span></nav>
<p class="sec-kicker bg-head__k">ABOUT THE ACADEMY</p>
<h1 class="phead__t" id="page-title">学びは、<wbr>もっと自由で、<wbr>実践的でいい。</h1>
<p class="phead__lead">学校でも職場でもない。<wbr>挑戦したい人が立ち寄り、<wbr>試し、<wbr>仲間と次の一歩を見つけられる。<wbr>私たちは、<wbr>そんな学びのサードプレイスをつくります。</p>
<ul class="phead__jump"><li><a href="#why">3つの仕組み</a></li><li><a href="#for-you">こんな方に</a></li><li><a href="#flow">受講までの流れ</a></li><li><a href="#price">料金・お支払い</a></li><li><a href="#faq">よくある不安</a></li><li><a href="#line">公式LINE</a></li></ul>
</div></section>'''

# ── ② 3つの仕組み（LP 02 をそのまま流用。リンク先だけ各ページへ）
AB = [('01', 'コースで', '学ぶ', '学びたい分野を選び、<wbr>演習とテンプレートで<wbr>実践的に身につける。', 'courses.html', 'コースを探す', '#0141D4', '#EAF0FF', 'assets/how/step-01-learn.webp', '受講画面。講義動画とチャプター一覧'),
      ('02', '学習ポートフォリオで', '残す', '成果物と学びの歩みを記録。<wbr>ロールモデルを見つけ、<wbr>続ける力に。', 'portfolio.html', 'ポートフォリオを見る', '#E07A2E', '#FFF1E6', 'assets/portfolio/hero-profile.webp', '公開ポートフォリオのプロフィール'),
      ('03', 'コミュニティーに', '飛び込む', '興味のある場に参加して、<wbr>新しいことを<wbr>体験しながら学ぶ。', 'lp-design.html#community', 'コミュニティーを見る', '#1E9E62', '#E7F6EE', 'assets/illust/about-community.webp', 'コミュニティーのトーク画面')]
why = f'''<section class="why bg-why" id="why" aria-labelledby="why-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">ABOUT</p><h2 class="sec-title" id="why-title">学ぶ、残す、飛び込む。</h2>
<p class="sec-lead">3つの仕組みで、<wbr>忙しくても学びを<wbr>「できる」に変え、<wbr>キャリアへ<wbr>つなげていきます。</p></div></header>
<ul class="n1">{''.join(f'<li style="--ac:{ac};--bg:{bg}"><div class="n1__v"><img src="{img}" alt="{alt}" loading="lazy"></div><p class="nb-n">POINT {n}</p><h3 class="nb-h">{pre}<em>{verb}</em></h3><p class="nb-d">{d}</p><a class="nb-a" href="{h}">{b}{ARROW}</a></li>' for n, pre, verb, d, h, b, ac, bg, img, alt in AB)}</ul>
</div></section>'''

# ── ③ こんな想いに（心の声と場面で自分ごと化）
VOICES = [(1, '#FFF1E6', '#E07A2E', 'いつか、自分の名前で働きたい', '「今度こそ、<wbr>最後まで形にしたい」', '本や動画で始めた勉強が、<wbr>途中で止まったまま。<wbr>仕事で見せられる成果物まで、<wbr>仕上げたい方に。', 'courses.html', 'コースを探す'),
          (2, '#E7F6EE', '#1E9E62', '社内のデジタル化を任された', '「手探りを、<wbr>自信に変えたい」', '詳しい人が周りにいない中で進めている。<wbr>基礎から整理して、<wbr>胸を張って進めたい方に。', 'courses.html#goal-it', 'IT・デジタルのコース'),
          (3, '#F0EDFF', '#6B57D8', '積み重ねを、次につなげたい', '「頑張ってきたことを、<wbr>伝えたい」', '資格や学びの積み重ねをポートフォリオにして、<wbr>次の仕事やチャンスにつなげたい方に。', 'portfolio.html', 'ポートフォリオを見る')]
for_you = f'''<section class="bg-for" id="for-you" aria-labelledby="for-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">FOR YOU</p><h2 class="sec-title" id="for-title">たとえば、<wbr>こんな想いに。</h2>
<p class="sec-lead">ひとつでも重なったら、<wbr>The Academyが力になれるかもしれません。</p></div></header>
<ul class="m1">{''.join(f'<li style="--bg:{bg};--ac:{ac}"><div class="m1__v"><img src="assets/illust/for-you-{n}.webp" alt="" loading="lazy"></div><div class="m1__b"><span class="m1__who">{w}</span><h3>{t}</h3><p>{d}</p><a href="{h}">{b}{ARROW}</a></div></li>' for n, bg, ac, w, t, d, h, b in VOICES)}</ul>
</div></section>'''

# ── ④ 受講までの流れ（LP 06 をそのまま流用）
flow = nonum(sec('flow')).replace('class="flow6"', 'class="flow6 bg-flow"')
flow = re.sub(r'<a href="[^"]*#flow">詳しくは「はじめての方へ」</a>', '', flow)

# ── ⑤ 料金・お支払い／よくある不安
CARD = ic('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h4"/>')
TAG = ic('<path d="M20 12 12 20 4 12V4h8z"/><circle cx="8.5" cy="8.5" r="1.5"/>')
BAG = ic('<path d="M5 8h14l-1 12H6zM9 8V6a3 3 0 0 1 6 0v2"/>')
YEN = ic('<path d="M6 4l6 8 6-8M12 12v8M8 13h8M8 17h8"/>')
brands = ''.join(f'<span>{b}</span>' for b in ['VISA', 'Mastercard', 'AMEX', 'JCB', 'Diners', 'DISCOVER'])
FAQ = [('無料相談は必ず受けないといけませんか？', 'いいえ。希望する方のみです。<wbr>コースのページから直接お申し込みいただけます。'),
       ('忙しくて続けられるか不安です', '週2h〜で完結する学習設計です。<wbr>学び方の詳細は<a href="how-to-learn.html">「学び方・受講成果」</a>で紹介しています。'),
       ('返金はできますか？', 'コースはデジタルコンテンツのため、決済の完了後の返金はお受けしていません。ただし、当社の責任によりコースを受講できない場合は、個別に対応します。<a href="faq.html#q-refund">よくある質問</a>'),
       ('パソコンがなくても受講できますか？', 'はい。スマートフォン・タブレットでも動画を受講できます。スライド資料も含まれるため大きな画面がおすすめで、課題の作成などはパソコンのほうが進めやすい場合があります。')]
price = f'''<section class="bg-price" id="price" aria-label="料金・お支払いとよくある不安"><div class="wrap">
<div class="q3"><p class="sec-kicker">PRICE</p><h2 class="sec-title">料金・お支払い</h2>
<div class="q3__band">
 <div class="q3__main"><span class="q3__ic">{BAG}</span><div><small>料金</small><b>¥2,980〜</b><p>コースごとの買い切り（月額なし）。<wbr>価格は内容・期間で変わります</p></div></div>
 <div class="q3__it"><small>{CARD}お支払い</small><b>クレジットカード</b><div class="q3__br">{brands}</div></div>
 <div class="q3__it q3__it--cp"><small>{TAG}クーポン</small><b>全コース 500円OFF</b><p>公式LINEの友だち限定。<wbr>カートでコードを入力</p></div>
 <div class="q3__cta"><a class="q3__go" href="courses.html">コースと価格を見る{ARROW}</a></div>
</div></div>
<div class="q3f" id="faq"><div class="q3f__h"><p class="sec-kicker">Q&amp;A</p><h2 class="sec-title">よくある不安</h2>
<p class="fq-more"><a href="faq.html">よくある質問をすべて見る{ARROW}</a><a href="how-to-learn.html">学び方をもっと知る{ARROW}</a></p></div>
<div class="q3f__l">{''.join(f'<details class="fq"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ))}</div></div>
</div></section>'''

# ── ⑥ 公式LINE（LP 09 をそのまま流用）
line = nonum(sec('line'))

css = r'''
  /* ══ はじめての方へ（/beginners）══════════════ */
  .bg-head .phead__t { margin-top: 8px; font-size: clamp(32px, 4.4vw, 52px); line-height: 1.3; word-break: keep-all; overflow-wrap: anywhere; }
  .bg-head__k { margin: 22px 0 0; } .bg-head .phead__lead { max-width: 720px; }
  .bg-why { padding: clamp(64px, 7vw, 96px) 0; background: #fff; }
  .n1 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; margin: 0; padding: 0; list-style: none; }
  .n1__v { display: grid; place-items: center; height: 260px; padding: 22px; border-radius: 24px; background: var(--bg); overflow: hidden; }
  .n1__v img { display: block; max-width: 100%; max-height: 100%; width: auto; height: auto; border-radius: 10px; box-shadow: 0 14px 32px rgba(15,27,69,.14); }
  .nb-n { margin: 20px 0 0; color: var(--ac); font: 800 13px/1 'Helvetica Neue', Arial, sans-serif; letter-spacing: .14em; }
  .nb-h { margin: 8px 0 0; color: var(--ink); font-size: 22px; } .nb-h em { font-style: normal; color: var(--ac); }
  .nb-d { margin: 8px 0 0; color: var(--ts-mid); font-size: 14px; line-height: 1.85; word-break: keep-all; overflow-wrap: anywhere; }
  .nb-a { display: inline-flex; align-items: center; gap: 6px; margin-top: 14px; color: var(--ac); font-size: 14px; font-weight: 700; text-decoration: none; } .nb-a svg { width: 16px; height: 16px; }
  .bg-for { padding: clamp(64px, 7vw, 96px) 0; background: var(--bg-gray, #F7F8FB); }
  .bg-flow { background: #fff; }
  .lineS { background: #fff; } .cnext { background: var(--bg-gray, #F7F8FB); }
  .bg-price { padding: clamp(64px, 7vw, 96px) 0; background: var(--bg-gray, #F7F8FB); }
  .bg-for .sec-title, .bg-price .sec-title { word-break: keep-all; overflow-wrap: anywhere; }
  /* こんな想いに */
  .m1 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin: 0; padding: 0; list-style: none; }
  .m1 li { display: flex; flex-direction: column; border-radius: 24px; background: #fff; box-shadow: 0 0 0 1px var(--line); overflow: hidden; }
  .m1__v { display: grid; place-items: end center; height: 240px; padding: 24px 24px 0; background: var(--bg); } .m1__v img { display: block; max-height: 210px; max-width: 80%; width: auto; height: auto; }
  .m1__b { display: flex; flex-direction: column; flex: 1; padding: 22px 26px 26px; }
  .m1__who { align-self: flex-start; padding: 4px 12px; border-radius: 99px; background: var(--bg); color: var(--ac); font-size: 12.5px; font-weight: 700; }
  .m1 h3 { margin: 14px 0 0; color: var(--ink); font-size: 21px; line-height: 1.5; word-break: keep-all; overflow-wrap: anywhere; }
  .m1 p { flex: 1; margin: 10px 0 0; color: var(--ts-mid); font-size: 14px; line-height: 1.85; word-break: keep-all; overflow-wrap: anywhere; }
  .m1 a { display: inline-flex; align-items: center; gap: 6px; margin-top: 18px; color: var(--ac); font-size: 14px; font-weight: 700; text-decoration: none; } .m1 a svg { width: 16px; height: 16px; }
  /* 料金・よくある不安 */
  .q3__band { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr) minmax(0, 1fr) auto; align-items: stretch; margin-top: 24px; border-radius: 24px; background: #fff; box-shadow: 0 0 0 1px var(--line); overflow: hidden; }
  .q3__band > div { padding: 24px 26px; } .q3__band > div + div { border-left: 1px solid var(--line); }
  .q3__main { display: flex; gap: 14px; align-items: center; background: #EAF0FF; }
  .q3__it, .q3__cta { display: flex; flex-direction: column; justify-content: center; }
  .q3__ic { display: grid; place-items: center; flex: none; width: 52px; height: 52px; border-radius: 14px; background: var(--ts-primary); color: #fff; } .q3__ic svg { width: 26px; height: 26px; }
  .q3__it--cp b { color: #06A04A; }
  .q3__band small { display: flex; align-items: center; gap: 6px; color: var(--ts-mid); font-size: 12px; font-weight: 700; } .q3__band small svg { width: 16px; height: 16px; color: var(--ts-primary); }
  .q3__band b { display: block; margin-top: 4px; color: var(--ink); font-size: 17px; word-break: keep-all; overflow-wrap: anywhere; } .q3__main b { color: var(--ts-primary); font-size: 22px; }
  .q3__band p { margin: 4px 0 0; color: var(--ts-mid); font-size: 12.5px; line-height: 1.7; word-break: keep-all; overflow-wrap: anywhere; }
  .q3__br { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 8px; } .q3__br span { padding: 2px 7px; border-radius: 5px; background: #F1F4FA; color: var(--ink); font: 700 10.5px/1.4 'Helvetica Neue', Arial, sans-serif; }
  .q3__band > .q3__cta { border-left: 0; padding-left: 0; }
  .q3__go { display: inline-flex; align-items: center; justify-content: center; gap: 6px; padding: 12px 18px; border-radius: 12px; background: var(--ts-primary); color: #fff; font-size: 14px; font-weight: 700; text-decoration: none; white-space: nowrap; } .q3__go svg { width: 16px; height: 16px; }
  .q3f { display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: 40px; margin-top: clamp(56px, 6vw, 80px); align-items: start; }
  .q3f .fq-more { flex-direction: column; align-items: flex-start; }
  .q3f__l { padding: 6px 26px; border-radius: 22px; background: #fff; box-shadow: 0 0 0 1px var(--line); } .q3f__l .fq:first-child { border-top: 0; } .q3f__l .fq:last-child { border-bottom: 0; }
  .fq { border-bottom: 1px solid var(--line); } .fq:first-child { border-top: 1px solid var(--line); }
  .fq summary { position: relative; padding: 18px 40px 18px 34px; color: var(--ink); font-size: 15.5px; font-weight: 700; cursor: pointer; list-style: none; }
  .fq summary::-webkit-details-marker { display: none; }
  .fq summary::before { content: "Q"; position: absolute; left: 0; top: 17px; color: var(--ts-primary); font: 800 17px/1.3 'Helvetica Neue', Arial, sans-serif; }
  .fq summary::after { content: ""; position: absolute; right: 8px; top: 50%; width: 9px; height: 9px; border-right: 2px solid var(--ts-mid); border-bottom: 2px solid var(--ts-mid); transform: translateY(-70%) rotate(45deg); transition: transform .2s; }
  .fq[open] summary::after { transform: translateY(-30%) rotate(-135deg); }
  .fq p { margin: 0; padding: 0 0 20px 34px; color: var(--ts-mid); font-size: 14.5px; line-height: 1.8; } .fq a { color: var(--ts-primary); font-weight: 700; }
  .fq .todo { display: inline-block; padding: 1px 8px; border-radius: 6px; background: #FFF1E7; color: #E46A1F; font-size: 12px; font-weight: 700; }
  .fq-more { display: flex; flex-wrap: wrap; gap: 8px 24px; margin: 20px 0 0; } .fq-more a { display: inline-flex; align-items: center; gap: 6px; color: var(--ts-primary); font-size: 14px; font-weight: 700; text-decoration: none; } .fq-more svg { width: 16px; height: 16px; }
  @media (max-width: 1180px) { .q3__band { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); } .q3__main { grid-column: 1 / -1; } .q3__band > div + div { border-left: 0; } .q3__it { border-top: 1px solid var(--line); } .q3__it + .q3__it { border-left: 1px solid var(--line) !important; } .q3__band > .q3__cta { grid-column: 1 / -1; padding: 0 26px 24px; border-top: 1px solid var(--line); padding-top: 20px; } }
  @media (max-width: 1000px) { .n1 { grid-template-columns: minmax(0, 1fr); } .n1__v { height: 280px; } .m1 { grid-template-columns: minmax(0, 1fr); } .m1__v { height: 220px; } .q3f { grid-template-columns: minmax(0, 1fr); gap: 20px; } .q3f .fq-more { flex-direction: row; } }
  @media (max-width: 640px) { .n1__v { height: 220px; padding: 16px; } .q3__band { grid-template-columns: minmax(0, 1fr); } .q3__it + .q3__it { border-left: 0 !important; } .q3__band > div { padding: 20px; } .q3__band > .q3__cta { padding: 20px; } .q3__go { width: 100%; } .q3f__l { padding: 4px 18px; } .m1 h3 { font-size: 19px; } .m1 p { word-break: normal; line-break: strict; } .m1__v { height: 200px; } .m1__v img { max-height: 176px; } }
'''

LN_SM = '<svg class="ln" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3C6.5 3 2 6.6 2 11c0 3.9 3.5 7.2 8.3 7.9.3.1.8.2.9.5.1.3.1.7 0 1l-.1.9c0 .3-.2 1 .9.5s5.9-3.5 8-6C21.4 14.3 22 12.7 22 11c0-4.4-4.5-8-10-8z"/></svg>'
between = re.sub(r'<div class="topbar" id="topbar" data-ann="[^"]*"><a href="[^"]*">.*?</a>', '<div class="topbar" id="topbar" data-ann="line-coupon-2026"><a href="#line">' + LN_SM + '公式LINEの友だち限定　全コース500円OFFクーポン配信中 <b>友だち追加する →</b></a>', between, count=1, flags=re.S)
html = (head + base_css + css
        + between.replace('<a href="beginners.html">はじめての方へ</a>', '<a href="beginners.html" aria-current="page">はじめての方へ</a>')
        + '<main>\n' + pagehead + why + for_you + flow + price + line + nx2 + '\n' + footer_on)
html = re.sub(r'<title>[^<]*</title>', '<title>はじめての方へ | The Academy</title>', html, count=1)
html = html.replace('href="/beginners', 'href="beginners.html')
open(OUT, 'w').write(html)
print('ok', len(html))
