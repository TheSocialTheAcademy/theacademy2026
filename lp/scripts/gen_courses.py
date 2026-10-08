# コースを探す（/courses）ページを lp-design.html の共通部品（ヘッダー・フッター・CSS）から組み立てる
import os, tempfile
S = os.path.dirname(os.path.abspath(__file__))          # このスクリプトのフォルダ（lp/scripts）
LPDIR = os.path.dirname(S)                              # 出力先（lp）
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')  # 共通部品を取り出すときの捨て出力
import json, re
LP = os.path.join(LPDIR, 'lp-design.html')
OUT = os.environ.pop('TA_COURSES_OUT', None) or os.path.join(LPDIR, 'courses.html')  # ほかのスクリプトから呼ぶときは捨て出力に書く
s = open(LP).read()

head = s[:s.index('</style>')]                       # <!DOCTYPE>〜共通CSS
between = s[s.index('</style>'):s.index('<main>')]  # </style></head><body>…ヘッダー
footer_on = s[s.index('</main>'):]                   # </main>＋フッター＋スクリプト
nx = s[s.index('<section class="next'):]
nx = nx[:nx.index('</section>') + len('</section>')]  # LP 07（2択の行動ボタン）を部品として流用

ARROW = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CAL = '<svg viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></g></svg>'
CLOCK = '<svg viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></g></svg>'
LEVEL = '<svg viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 19v-4M12 19V10M19 19V5"/></g></svg>'
def ic(d, w=1.9): return f'<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{d}</g></svg>'

# カテゴリ：色とアイコン（コース画像ができるまでの仮サムネイルにも使う）
CAT = {
 'it':  ('IT・デジタル',   '#1E9E62', '#E9F7F0', ic('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4M8 9l2 2-2 2M13 13h3"/>')),
 'mk':  ('マーケティング', '#E46A1F', '#FFF1E7', ic('<path d="M4 11v3a1 1 0 0 0 1 1h2l6 4V6L7 10H5a1 1 0 0 0-1 1z"/><path d="M17 9a4 4 0 0 1 0 6M19.5 6.5a8 8 0 0 1 0 11"/>')),
 'en':  ('英語・TOEIC',    '#0141D4', '#EAF0FF', ic('<path d="M4 5h9M8.5 3v2M11 5c0 4-3 7-6.5 8.5M6 9c1.5 2.5 4 4 6.5 4.5"/><path d="M13 21l4-9 4 9M14.5 18h5"/>')),
 'biz': ('ビジネス',       '#6B4FD8', '#F0ECFF', ic('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>')),
 'cr':  ('クリエイティブ', '#D9467A', '#FDECF2', ic('<path d="M12 3a9 9 0 0 0 0 18c1.2 0 1.8-.9 1.4-1.9-.4-1 .3-2.1 1.4-2.1H17a4 4 0 0 0 4-4 9 9 0 0 0-9-10z"/><circle cx="7.5" cy="11" r="1.2"/><circle cx="10.5" cy="7" r="1.2"/><circle cx="15" cy="7.5" r="1.2"/>')),
}
# 目的（LP 01の目的カードと同じ名前）→ カテゴリ
GOALS = [
 ('all', 'すべて', None, None),
 ('it', '仕事を効率化したい', ['it', 'biz'], ic('<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>')),
 ('mk', '発信を強みにしたい', ['mk', 'cr'], ic('<path d="M4 11v3a1 1 0 0 0 1 1h2l6 4V6L7 10H5a1 1 0 0 0-1 1z"/><path d="M17 9a4 4 0 0 1 0 6"/>')),
 ('en', '英語で選択肢を広げたい', ['en'], ic('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/>')),
]
# コース一覧（今のサイトで販売中のコースは、価格・レベルを今のサイトに合わせる。章数・時間は course_data.json から）
C = [
 ('sns-marketing', 'SNSマーケティング実践', 'mk', '顧客理解から数値改善までを、一つのキャンペーンとして実践します。', None, '8週間', '週2〜3時間', 'プロ', 'assets/photos/sns-phone.webp'),
 ('ai-efficiency', '生成AI 業務改善', 'it', '生成AIとノーコードで、調査・資料作成・定型業務を効率化します。', None, '6週間', '週2時間', 'プロ', 'assets/photos/ai-laptop.webp'),
 ('toeic-700', 'TOEIC L&amp;R 700点突破', 'en', '海外経験豊富なコーチと、4技能をバランスよく強化します。', None, '3か月', '週2回・全24回', 'プレミア', 'assets/photos/toeic-study.webp'),
 ('event-design', 'イベントデザイン', 'biz', '目的設定から当日運営まで、成果につながるイベントづくりを学びます。', 9800, None, None, 'ベーシック', None),
 ('marketing-basic', 'マーケティング戦略基礎', 'mk', '市場分析から戦略立案・実行・検証までを体系的に学びます。', 11800, None, None, 'ベーシック', None),
 ('instagram', 'インスタグラム', 'mk', 'インスタグラムで、個人やビジネスを効果的にプロモーションします。', 7900, None, None, 'ベーシック', None),
 ('automation', '自動化ツール開発', 'it', 'JavaScriptの基礎から、仕様に基づいた自動化ツールを開発します。', 12800, None, None, 'ベーシック', None),
 ('chatgpt-basic', '初級編 ChatGPT', 'it', 'ChatGPTの概要から活用方法までを総合的に学びます。', 2980, None, None, 'ベーシック', None),
 ('line-official', '公式LINE運用', 'it', '資料請求・予約受付などを、公式LINEで自分で構築します。', 3980, None, None, 'ベーシック', None),
 ('business-english', 'ビジネス英語初級', 'en', 'ビジネス英語の基本表現を実践的に学びます。', 3000, None, None, 'ベーシック', None),
 ('project-management', 'プロジェクトマネジメント', 'biz', 'プロジェクト管理の知識を、実務に活かせる形で身につけます。', 4980, None, None, 'ベーシック', None),
 ('canva-basic', 'Canva初級', 'cr', 'Canva無料版で「自分らしさ」を伝えるデザインを学びます。', 6400, None, None, 'ベーシック', None),
]

# 今の theacademyjapan.org のコース詳細（章立て・時間・こんな方に・できるようになること）。Wix 側の内容が正
CD = json.load(open(os.path.join(S, 'course_data.json')))['courses']
def cur_meta(slug):  # 期間の決まっていないコースは、今のサイトの章数・動画時間を出す
    d = CD.get(slug) or {}
    return (f'全{len(d["chapters"])}章', f'約{d["minutes"]}分') if d.get('chapters') and d.get('minutes') else (None, None)

LINE_SM = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3.5c5 0 9 3.2 9 7.2 0 3.9-3.8 7.1-8.6 7.2-.5.4-2.7 2.3-4.2 2.6-.4.1-.4-.3-.3-.6l.5-2.4C5.3 16.3 3 13.7 3 10.7 3 6.7 7 3.5 12 3.5z"/></svg>'
def chref(slug): return f'course-{slug}.html'  # コース詳細（K2）
def THUMB(slug): return f'assets/thumbs/{slug}.webp'  # コースのサムネイル（C-4：グラデーション＋半透明の形）
def card(i, c):
    slug, title, cat, desc, price, dur, time, lv, img = c
    name, col, bg, svg = CAT[cat]
    if not dur: dur, time = cur_meta(slug)
    thumb = f'<div class="cv cv--img"><img src="{THUMB(slug)}" loading="lazy" alt=""></div>'  # サムネイル（C-4）。gen_thumbs.py で作る
    meta = ''.join(f'<span>{ic_}{t}</span>' for ic_, t in ((CAL, dur), (CLOCK, time), (LEVEL, lv)) if t)
    p = '' if price else '<b class="price">¥—</b><span class="todo">価格を入れる</span>'
    cp = (f'<div class="cpr"><span class="cpr__o">通常 ¥{price:,}</span><p class="cpr__n"><small>{LINE_SM}LINEクーポン適用</small><b>¥{price - 500:,}</b></p>'
          f'<em class="cpr__c">公式LINEの友だち限定・カートでコード入力</em></div>') if price else ''
    href = chref(slug)
    return (f'<a class="course" href="{href}" data-cat="{cat}" data-level="{lv}" data-price="{price or ""}" data-order="{i}">'
            f'<div class="thumb">{thumb}</div><div class="body"><span class="cat" style="--cc:{col};--cb:{bg}">{name}</span><h3>{title}</h3>'
            f'<p class="meta">{meta}</p><p class="desc">{desc}</p>{cp}'
            f'<div class="foot"><p class="p">{p}</p><span class="more">詳しく見る<i>{ARROW}</i></span></div></div></a>')
cards = ''.join(card(i, c) for i, c in enumerate(C))

goal_btns = ''.join(
    f'<button type="button" class="goalf" id="goal-btn-{k}" data-goal="{k}" aria-pressed="{str(k == "all").lower()}">' + (f'<span class="goalf__i">{g_ic}</span>' if g_ic else '') + f'<span>{t}</span></button>'
    for k, t, cats, g_ic in GOALS)
cat_opts = ''.join(f'<option value="{k}">{v[0]}</option>' for k, v in CAT.items())

# ── 特集 ──
slack_mock = '''<div class="fz-slack" aria-hidden="true">
  <div class="fz-slack__side"><b>The Academy</b><span># general</span><span class="on"># project-a</span><span># faq</span><span># random</span></div>
  <div class="fz-slack__main">
    <p class="fz-slack__ch"># project-a</p>
    <div class="fz-msg"><span class="fz-av" style="--a:#E46A1F">B</span><div><b>タスクBot</b><small>9:00</small><p>今日の期限：<em>企画書レビュー</em>（担当：さとう）</p></div></div>
    <div class="fz-msg"><span class="fz-av" style="--a:#1E9E62">S</span><div><b>さとう</b><small>9:12</small><p>レビュー完了しました ✅</p></div></div>
    <div class="fz-gantt"><p>ガントチャート</p><i style="--s:0;--w:45%"></i><i style="--s:30%;--w:40%"></i><i style="--s:60%;--w:35%" class="late"></i></div>
  </div>
</div>'''
slack_facts = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in (('¥0', '月額サービス手数料'), ('Slack内', 'で完結'), ('FAQ・ガント', 'をまとめて確認'), ('仕様書', '付きで簡単設定')))
toeic_facts = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in (('3', 'か月'), ('週2', '回'), ('全24', '回'), ('1対1', 'マンツーマン')))

feature = f'''<section class="cfeat" id="featured" aria-labelledby="featured-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">FEATURED</p><h2 class="sec-title" id="featured-title">特集</h2><p class="sec-lead">いま注目のツールとプログラムを紹介します。</p></div></header>
<div class="cfeat__grid">
<a class="fz" href="course-slack-gas-task.html"><div class="fz__v fz__v--white"><img src="assets/courses/feat-slack.webp" alt="PCのタスク一覧とスマホのSlack画面。月額サービス手数料0円、Slack内でタスク管理・FAQ・ガントチャートを確認できる" loading="lazy"></div>
<div class="fz__b"><p class="fz__k"><span>特集 1</span>Slack×GAS タスク管理システム</p>
<h3 class="fz__t">プロジェクト進行のズレやムダを、<wbr>減らす。</h3>
<p class="fz__d">Slackだけで完結する、次世代のタスク管理システムです。タスク・FAQ・ガントチャートをSlackの中で確認できます。分かりやすい仕様書付きで、セットアップも簡単です。</p>
<ul class="fz__facts">{slack_facts}</ul>
<span class="fz__go">詳しくはこちら{ARROW}</span></div></a>
<a class="fz" href="course-toeic-700.html"><div class="fz__v"><img src="assets/courses/feat-toeic.webp" alt="3ヶ月で結果を出すスコアアップ講座 TOEIC L&amp;R 700点突破プログラム。マンツーマントレーニング、オンラインライブ型クラス" loading="lazy"></div>
<div class="fz__b"><p class="fz__k"><span>特集 2</span>TOEIC L&amp;R 700点突破プログラム</p>
<h3 class="fz__t">苦手を得意に変える、<wbr>3か月で自信の持てる英語力を。</h3>
<p class="fz__d">海外経験豊富な英語コーチとのマンツーマントレーニングで、TOEIC® L&amp;R 700点以上を目指します。オンラインライブ型のクラスで、文法・リスニング・リーディング・英会話をバランスよく強化します。</p>
<ul class="fz__facts">{toeic_facts}</ul>
<span class="fz__go">詳しくはこちら{ARROW}</span></div></a>
</div></div></section>'''

TIER_ROWS = [('ベーシック', 'まず触ってみたい方に。1〜2週間で、基礎とミニ成果物1つ。'), ('プロ', '仕事で使える「1本」を、3か月で仕上げる。'), ('プレミア', '1on1コーチングで、転職・副業・独立へつなげる。')]
def ck(name, val, label, n=None):
    return f'<label class="fchk"><input type="checkbox" name="{name}" value="{val}"><span>{label}</span>' + (f'<small>{n}</small>' if n is not None else '') + '</label>'
tier_n = {t: sum(1 for c in C if c[7] == t) for t, _ in TIER_ROWS}
cat_n = {k: sum(1 for c in C if c[2] == k) for k in CAT}
side = ('<aside class="cside" id="side" aria-label="絞り込み"><div class="cside__in">'
        '<div class="cside__top"><p class="cside__h">絞り込み</p><button type="button" class="cside__x" id="sideClose" aria-label="閉じる">×</button></div>'
        '<div class="fgrp"><p>コースの種類</p>' + ''.join(ck('tier', t, t, tier_n[t]) for t, _ in TIER_ROWS) + '</div>'
        '<div class="fgrp"><p>カテゴリ</p>' + ''.join(ck('cat', k, v[0], cat_n[k]) for k, v in CAT.items()) + '</div>'
        '<div class="fgrp"><p>価格</p>' + ck('price', 'a', '〜3,000円') + ck('price', 'b', '3,000〜10,000円') + ck('price', 'c', '10,000円〜') + '</div>'
        '<div class="cside__foot"><button type="button" class="cside__clear" id="clear">すべてクリア</button><button type="button" class="cside__ok" id="sideOk">結果を見る</button></div>'
        '</div></aside>')
rows_html = ''
for t, sub in TIER_ROWS:
    cc = ''.join(card(i, c) for i, c in enumerate(C) if c[7] == t)
    rows_html += (f'<div class="crow"><div class="crow__h"><div><h3>{t}</h3><p>{sub}</p></div>'
                  f'<button type="button" class="crow__all" data-tier="{t}">すべて見る（{tier_n[t]}件）{ARROW}</button></div>'
                  f'<div class="popular cgrid crow__track">{cc}</div></div>')

listing = f'''<section class="clist" id="list" aria-labelledby="list-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">ALL COURSES</p><h2 class="sec-title" id="list-title">コース一覧</h2><p class="sec-lead">目的やコースの種類から絞り込んで、<wbr>期間・価格を比べられます。</p></div></header>
<div class="goalbar" role="group" aria-label="目的で絞り込む">{goal_btns}</div>
<div class="clay">
{side}
<div class="cmain">
<div class="cbar"><p class="ccount" id="count" aria-live="polite"><b>{len(C)}</b>件のコース</p>
<div class="cbar__r"><button type="button" class="cbar__mode" id="modeBtn">すべてを一覧で見る</button>
<label class="csel"><span>並び替え</span><select id="f-sort"><option value="rec">おすすめ順</option><option value="low">価格が安い順</option><option value="high">価格が高い順</option></select></label></div></div>
<div class="crows" id="rows">{rows_html}</div>
<div id="gridWrap" hidden><div class="popular cgrid" id="grid">{cards}</div>
<div class="cmore" id="more"><p id="moreInfo"></p><button type="button" id="moreBtn">もっと見る</button></div></div>
<div class="cempty" id="empty" hidden><p>条件に合うコースが見つかりませんでした。</p><button type="button" id="reset">絞り込みをリセット</button></div>
<p class="cnote">※一部の価格は現行サイトの掲載価格です。「¥—」は価格の確定待ち、期間・コースの種類は仮の表示です。</p>
</div></div>
<button type="button" class="cfab" id="fab">絞り込む<span id="fabN"></span></button>
<div class="cdim" id="dim" hidden></div>
</div></section>'''

LINE_IC = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5c5 0 9 3.2 9 7.2 0 3.9-3.8 7.1-8.6 7.2-.5.4-2.7 2.3-4.2 2.6-.4.1-.4-.3-.3-.6l.5-2.4C5.3 16.3 3 13.7 3 10.7 3 6.7 7 3.5 12 3.5z" fill="currentColor"/></svg>'
line_band = f'''<section class="cline" aria-label="公式LINE"><div class="wrap"><div class="cline__band">
<span class="cline__ic">{LINE_IC}</span>
<div class="cline__t"><p class="cline__k">公式LINE限定</p><b>LINE登録で、全コース<em>500円OFF</em></b><p>新しいコース情報や限定イベントの案内もお届けします。</p></div>
<a class="cline__btn" href="beginners.html#line">LINEを追加する{ARROW}</a>
</div></div></section>'''

nx2 = (nx.replace('<section class="next nxC" id="next"', '<section class="next nxC cnext" id="next"')
         .replace('<p class="sec-num">07</p>', '')
         .replace('迷っていても、大丈夫。', '迷ったら、ここから。')
         )
nx2 = re.sub(r'<p class="sec-lead">キャリアの悩み.*?</p>', '<p class="sec-lead">相談したら必ず受講、<wbr>ではありません。<wbr>どちらも無料です。</p>', nx2, count=1, flags=re.S)

CMP_IDS = ['chatgpt-basic', 'sns-marketing', 'toeic-700']
CMP_EXTRA = {  # 一覧のデータにない項目（形式・講師のフィードバック・成果物）。仮の値は※で示す
  'chatgpt-basic': ('動画', False, 'AIプロンプト集※'),
  'sns-marketing': ('動画＋演習', False, 'SNSキャンペーン企画書'),
  'toeic-700': ('マンツーマン（ライブ）', True, '英語で話す力（スコア）'),
}
def cmp_rows():
    cs = [next(c for c in C if c[0] == k) for k in CMP_IDS]
    v = lambda x: x if x else '<span class="cmp__q">確認中</span>'
    pr = lambda c: f'¥{c[4]:,}<small>LINEクーポンで ¥{c[4] - 500:,}</small>' if c[4] else '<span class="cmp__q">価格の確定待ち</span>'
    fb = lambda k: '<b class="cmp__o">○</b> 対応' if CMP_EXTRA[k][1] else '<span class="cmp__n">—</span> 対象外'
    rows = [('カテゴリ', [CAT[c[2]][0] for c in cs]), ('コースの種類', [c[7] for c in cs]), ('期間', [v(c[5]) for c in cs]), ('週の学習時間', [v(c[6]) for c in cs]),
            ('形式', [CMP_EXTRA[c[0]][0] for c in cs]), ('残せる成果', [CMP_EXTRA[c[0]][2] for c in cs]), ('価格', [pr(c) for c in cs])]
    return cs, rows
_cs, _rows = cmp_rows()
_href = lambda c: chref(c[0])
cmp_table = ('<div class="cmp__tw"><table class="cmp__t"><caption class="sr-only">3コースの比較</caption><thead><tr><th scope="col"><span class="sr-only">項目</span></th>'
             + ''.join(f'<th scope="col"><span class="cat" style="--cc:{CAT[c[2]][1]};--cb:{CAT[c[2]][2]}">{CAT[c[2]][0]}</span><b>{c[1]}</b></th>' for c in _cs) + '</tr></thead><tbody>'
             + ''.join(f'<tr><th scope="row">{h}</th>' + ''.join(f'<td>{x}</td>' for x in xs) + '</tr>' for h, xs in _rows[1:])
             + '<tr class="cmp__go"><th scope="row"><span class="sr-only">詳細</span></th>' + ''.join(f'<td><a href="{_href(c)}">詳しく見る{ARROW}</a></td>' for c in _cs) + '</tr></tbody></table></div>')
cmp_cards = '<div class="cmp__cards">' + ''.join(
    f'<article class="cmp__card"><span class="cat" style="--cc:{CAT[c[2]][1]};--cb:{CAT[c[2]][2]}">{CAT[c[2]][0]}</span><h3>{c[1]}</h3><dl>'
    + ''.join(f'<div><dt>{h}</dt><dd>{xs[i]}</dd></div>' for h, xs in _rows[1:]) + f'</dl><a href="{_href(c)}">詳しく見る{ARROW}</a></article>' for i, c in enumerate(_cs)) + '</div>'
compare = f'''<section class="ccmp" id="compare" aria-labelledby="cmp-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">COMPARE</p><h2 class="sec-title" id="cmp-title">コースを比べる</h2><p class="sec-lead">コースの種類ごとに、期間・学習時間・形式・価格の違いを並べました。</p></div></header>
{cmp_table}{cmp_cards}
<p class="cnote">※「確認中」「※」の項目は仮の表示です。LINEクーポンは公式LINEの友だち限定で、カートでコードを入力すると適用されます。</p>
</div></section>'''

# ── コース診断（FV-009／PRC-005）＋結果から相談へ引き継ぐ（CTA-005）
DQ = [
  ('いちばん近い目的は？', [('it', '仕事を効率化したい', 'IT・デジタル／ビジネス'), ('mk', '発信を強みにしたい', 'マーケティング・クリエイティブ'), ('en', '英語で選択肢を広げたい', '英語・TOEIC'), ('all', 'まだ決まっていない', 'いくつか見て決めたい')]),
  ('1週間に、学習に使える時間は？', [('1', '週1〜2時間', 'すきま時間で少しずつ'), ('2', '週2〜3時間', '平日夜＋週末に'), ('4', '週4時間以上', 'しっかり取り組みたい'), ('0', 'まだわからない', '相談して決めたい')]),
  ('どこまで進めたい？', [('ベーシック', 'まず基礎を試したい', '1〜2週間で、基礎とミニ成果物'), ('プロ', '仕事で使える1本を仕上げたい', '3か月で成果物を完成'), ('プレミア', 'コーチと一緒に結果を出したい', '1on1のコーチング付き')]),
]
diag_q = ''.join(f'<fieldset class="dq" data-q="{qi}"{"" if qi == 0 else " hidden"}><legend class="dq__t">{q}</legend><div class="dq__o">'
                 + ''.join(f'<button type="button" class="dq__op" data-v="{v}"><span>{t}</span><small>{sub}</small></button>' for v, t, sub in os) + '</div></fieldset>' for qi, (q, os) in enumerate(DQ))
diag = f'''<section class="cdiag" id="diagnosis" aria-labelledby="diag-title"><div class="wrap">
<header class="sec-head cdiag__head"><div><p class="sec-kicker">COURSE FINDER</p><h2 class="sec-title" id="diag-title">3つの質問で、<wbr>あなたに合うコースがわかる</h2><p class="sec-lead">30秒で終わります。答えは保存されません。</p></div></header>
<div class="cdiag__box" id="diagBox">
<div class="dq__pg" aria-hidden="true"><span id="diagN">Q1 / 3</span><i><b id="diagBar" style="width:33.3%"></b></i></div>
{diag_q}
<div class="dq__ft"><button type="button" class="dq__back" id="diagBack" hidden>← 前の質問に戻る</button><a class="dq__skip" href="#list">診断せずに全コースを見る →</a></div>
</div>
<div class="cdiag__res" id="diagRes" hidden aria-live="polite"></div>
</div></section>'''

pagehead = f'''<section class="phead" aria-labelledby="page-title"><div class="wrap">
<nav class="crumb" aria-label="パンくずリスト"><a href="lp-design.html">トップ</a><span aria-hidden="true">/</span><span aria-current="page">コースを探す</span></nav>
<h1 class="phead__t" id="page-title">コースを探す</h1>
<p class="phead__lead">目的やカテゴリから、<wbr>あなたに合うコースを選べます。</p>
<ul class="phead__jump"><li><a href="#featured">特集</a></li><li><a href="#diagnosis">コース診断</a></li><li><a href="#list">コース一覧</a></li><li><a href="#compare">比べる</a></li><li><a href="#next">迷ったら</a></li></ul>
</div></section>'''

css = '''
  /* 価格：通常 → LINEクーポン適用後（PRC-009） */
  .cpr { margin-top: 12px; padding-top: 10px; border-top: 1px dashed var(--line); }
  .cpr__o { color: var(--ts-mid); font-size: 12px; } .cpr__o { font-variant-numeric: tabular-nums; }
  .cpr__n { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 8px; margin: 2px 0 0; }
  .cpr__n small { display: inline-flex; align-items: center; gap: 3px; padding: 2px 8px; border-radius: 99px; background: #E7F8EE; color: #06A04A; font-size: 11px; font-weight: 700; }
  .cpr__n small svg { width: 12px; height: 12px; } .cpr__n b { color: #06A04A; font-size: 20px; font-weight: 800; font-variant-numeric: tabular-nums; }
  .cpr__c { display: block; margin-top: 2px; color: var(--ts-mid); font-size: 10.5px; font-style: normal; line-height: 1.5; }
  .course .foot .p:empty { display: none; } .course .foot:has(.p:empty) { justify-content: flex-end; }
  /* コースを比べる（TBL-002／PCは表・スマホはカード TBL-008） */
  .ccmp { padding: clamp(56px, 6vw, 88px) 0; background: #fff; }
  .cmp__lg { margin: 0 0 12px; color: var(--ts-mid); font-size: 13px; } .cmp__o { color: var(--ts-primary); } .cmp__n { color: #B5B7C8; } .cmp__q { color: var(--ts-mid); font-size: 12.5px; }
  .cmp__tw { overflow: hidden; border-radius: 20px; box-shadow: 0 0 0 1px var(--line); background: #fff; }
  .cmp__t { width: 100%; border-collapse: collapse; font-size: 14px; line-height: 1.6; }
  .cmp__t th, .cmp__t td { padding: 14px 18px; border-top: 1px solid var(--line); text-align: left; vertical-align: top; }
  .cmp__t thead th { border-top: 0; background: #F4F7FE; } .cmp__t thead b { display: block; margin-top: 6px; color: var(--ink); font-size: 16px; }
  .cmp__t tbody th { width: 190px; background: #FAFBFD; color: var(--ts-mid); font-size: 13px; font-weight: 700; }
  .cmp__t td small { display: block; color: #06A04A; font-size: 12px; font-weight: 700; }
  .cmp__go td a, .cmp__card > a { display: inline-flex; align-items: center; gap: 6px; color: var(--ts-primary); font-size: 14px; font-weight: 700; text-decoration: none; } .cmp__go svg, .cmp__card > a svg { width: 15px; height: 15px; }
  .cmp__cards { display: none; }
  .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
  @media (max-width: 760px) {
    .cmp__tw { display: none; } .cmp__lg { display: none; }
    .cmp__cards { display: grid; gap: 12px; }
    .cmp__card { padding: 18px 18px 16px; border-radius: 18px; background: #fff; box-shadow: 0 0 0 1px var(--line); }
    .cmp__card h3 { margin: 8px 0 6px; font-size: 17px; }
    .cmp__card dl { margin: 0 0 10px; } .cmp__card dl div { display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 8px; padding: 9px 0; border-top: 1px solid var(--line); font-size: 13.5px; }
    .cmp__card dt { color: var(--ts-mid); font-size: 12.5px; font-weight: 700; } .cmp__card dd { margin: 0; } .cmp__card dd small { display: block; color: #06A04A; font-size: 12px; font-weight: 700; }
  }
  /* コース診断（FV-009／PRC-005） */
  .cdiag { padding: clamp(56px, 6vw, 88px) 0; background: var(--bg-gray, #F7F8FB); }
  .cdiag__head { justify-content: center; text-align: center; } .cdiag__head .sec-lead { margin-left: auto; margin-right: auto; }
  .cdiag__box, .cdiag__res { max-width: 880px; margin: 0 auto; padding: clamp(22px, 3vw, 34px); border-radius: 24px; background: #fff; box-shadow: 0 0 0 1px var(--line); }
  .dq__pg { display: flex; align-items: center; gap: 12px; color: var(--ts-primary); font-size: 13px; font-weight: 800; } .dq__pg i { flex: 1; height: 6px; border-radius: 99px; background: #E6EBF5; overflow: hidden; } .dq__pg b { display: block; height: 100%; background: var(--ts-primary); transition: width .2s; }
  .dq { margin: 0; padding: 0; border: 0; min-width: 0; } .dq__t { margin: 18px 0 0; padding: 0; font-size: clamp(19px, 2.2vw, 24px); font-weight: 800; color: var(--ink); }
  .dq__o { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; margin-top: 16px; }
  .dq__op { display: grid; gap: 2px; padding: 16px 18px; border: 0; border-radius: 14px; background: #fff; box-shadow: inset 0 0 0 1.5px var(--line); color: var(--ink); text-align: left; font: inherit; cursor: pointer; }
  .dq__op span { font-size: 15.5px; font-weight: 800; } .dq__op small { color: var(--ts-mid); font-size: 12.5px; } .dq__op:hover, .dq__op[aria-pressed="true"] { box-shadow: inset 0 0 0 2px var(--ts-primary); background: #F4F7FE; }
  .dq__ft { display: flex; justify-content: space-between; gap: 12px; margin-top: 16px; font-size: 13.5px; } .dq__back { padding: 0; border: 0; background: none; color: var(--ts-mid); font: inherit; font-weight: 700; cursor: pointer; } .dq__skip { margin-left: auto; color: var(--ts-primary); font-weight: 700; text-decoration: none; }
  .dr { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 28px; }
  .dr__b { display: inline-block; padding: 4px 12px; border-radius: 99px; background: var(--ts-primary); color: #fff; font-size: 12px; font-weight: 800; }
  .dr__n { margin: 10px 0 0; color: var(--ts-primary); font-size: clamp(22px, 2.6vw, 28px); font-weight: 800; } .dr__m { margin: 4px 0 0; color: var(--ts-mid); font-size: 13.5px; }
  .dr__h { margin: 18px 0 0; color: var(--ts-mid); font-size: 13px; font-weight: 800; } .dr ul { margin: 8px 0 0; padding: 0; list-style: none; display: grid; gap: 6px; font-size: 14.5px; line-height: 1.7; } .dr li { display: flex; gap: 6px; word-break: normal; line-break: strict; } .dr li::before { content: "✓"; flex: none; color: var(--ts-primary); font-weight: 800; }
  .dr__bt { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; } .dr__bt a { min-width: 0; padding: 0 22px; }
  .dr__note { margin: 8px 0 0; color: var(--ts-mid); font-size: 12px; }
  .dr__s { padding-left: 24px; border-left: 1px solid var(--line); } .dr__c { display: grid; gap: 2px; margin-top: 10px; padding: 14px 16px; border-radius: 12px; background: var(--bg-gray, #F7F8FB); color: var(--ink); text-decoration: none; } .dr__c small { color: var(--ts-mid); }
  .dr__ans { margin: 16px 0 6px; color: var(--ts-mid); font-size: 12.5px; line-height: 1.7; } .dr__re { padding: 0; border: 0; background: none; color: var(--ts-primary); font: inherit; font-size: 13.5px; font-weight: 700; cursor: pointer; }
  @media (max-width: 760px) { .dq__o { grid-template-columns: minmax(0, 1fr); } .dr { grid-template-columns: minmax(0, 1fr); } .dr__s { padding: 18px 0 0; border-left: 0; border-top: 1px solid var(--line); } .dr__bt a { width: 100%; } }
  /* ══ コースを探す（/courses）══════════════════ */
  .phead { padding: clamp(40px, 5vw, 64px) 0 clamp(32px, 4vw, 48px); background: var(--bg-gray, #F7F8FB); }
  .crumb { display: flex; flex-wrap: wrap; gap: 8px; color: var(--ts-mid); font-size: 12px; }
  .crumb a { color: var(--ts-mid); text-decoration: none; } .crumb a:hover { color: var(--ts-primary); }
  .crumb [aria-current] { color: var(--ink); font-weight: 700; }
  .phead__t { margin: 18px 0 0; color: var(--ink); font-size: clamp(32px, 4vw, 44px); font-weight: 700; letter-spacing: .02em; }
  .phead__lead { margin: 10px 0 0; color: var(--ts-mid); font-size: 15px; line-height: 1.8; word-break: keep-all; overflow-wrap: anywhere; }
  .phead__jump { display: flex; flex-wrap: wrap; gap: 8px; margin: 22px 0 0; padding: 0; list-style: none; }
  .phead__jump a { display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: 99px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); color: var(--ink); font-size: 13px; font-weight: 700; text-decoration: none; }
  .phead__jump a::after { content: "↓"; color: var(--ts-primary); }
  .phead__jump a:hover { box-shadow: inset 0 0 0 1.5px var(--ts-primary); color: var(--ts-primary); }

  /* 特集 */
  .cfeat { padding: clamp(64px, 7vw, 96px) 0; background: #fff; }
  .cfeat__grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
  .fz { display: flex; flex-direction: column; border-radius: 24px; background: #fff; box-shadow: 0 0 0 1px var(--line); color: inherit; text-decoration: none; overflow: hidden; transition: box-shadow .2s, transform .2s; }
  .fz:hover { transform: translateY(-2px); box-shadow: 0 0 0 1.5px var(--ts-primary), var(--shadow-soft); }
  .fz__v { position: relative; aspect-ratio: 16 / 10; background: linear-gradient(160deg, #F4F7FE, #E3EAFB); overflow: hidden; }
  .fz__v img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .fz__b { display: flex; flex-direction: column; flex: 1; padding: 26px 28px 28px; }
  .fz__k { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 10px; margin: 0; color: var(--ink); font-size: 13px; font-weight: 700; }
  .fz__k span { padding: 3px 10px; border-radius: 99px; background: var(--ts-primary); color: #fff; font-size: 11.5px; letter-spacing: .06em; }
  .fz__catch { margin: 16px 0 0; color: var(--ts-primary); font-size: 14px; font-weight: 700; }
  .fz__t { margin: 14px 0 0; color: var(--ink); font-size: 22px; font-weight: 700; line-height: 1.5; word-break: keep-all; overflow-wrap: anywhere; }
  .fz__d { margin: 10px 0 0; color: var(--ts-mid); font-size: 14px; line-height: 1.85; }
  .fz__tags { display: flex; flex-wrap: wrap; gap: 6px; margin: 16px 0 0; padding: 0; list-style: none; }
  .fz__tags li { padding: 4px 12px; border-radius: 99px; background: var(--tint-08); color: var(--ts-primary); font-size: 12px; font-weight: 700; }
  .fz__facts { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; margin: 16px 0 0; padding: 0; list-style: none; }
  .fz__facts li { display: grid; justify-items: center; gap: 2px; padding: 10px 4px; border-radius: 12px; background: var(--bg-gray, #F7F8FB); }
  .fz__facts b { color: var(--ts-primary); font-size: 17px; white-space: nowrap; } .fz__facts span { color: var(--ts-mid); font-size: 11px; line-height: 1.4; text-align: center; }
  .fz__v--white { background: #fff; border-bottom: 1px solid var(--line); } .fz__v--white img { object-fit: contain; padding: 8px 12px; }
  .fz__go { display: inline-flex; align-items: center; gap: 6px; margin-top: auto; padding-top: 20px; color: var(--ts-primary); font-size: 14px; font-weight: 700; }
  .fz__go .ico { width: 16px; height: 16px; transition: transform .2s; } .fz:hover .fz__go .ico { transform: translateX(3px); }
  /* 特集1：Slackの画面イメージ */
  .fz__v--slack { display: grid; place-items: center; padding: 24px; }
  .fz-slack { display: grid; grid-template-columns: 30% 1fr; width: 100%; max-width: 440px; height: 100%; border-radius: 12px; background: #fff; box-shadow: 0 14px 30px rgba(15,27,69,.14); overflow: hidden; font-size: 11px; }
  .fz-slack__side { display: grid; align-content: start; gap: 6px; padding: 12px 10px; background: #3F0E40; color: rgba(255,255,255,.7); }
  .fz-slack__side b { margin-bottom: 4px; color: #fff; font-size: 11.5px; }
  .fz-slack__side .on { margin: 0 -4px; padding: 2px 4px; border-radius: 4px; background: #1164A3; color: #fff; }
  .fz-slack__main { display: grid; align-content: start; gap: 8px; min-width: 0; padding: 10px 12px; }
  .fz-slack__ch { margin: 0 -12px; padding: 0 12px 8px; border-bottom: 1px solid var(--line); color: var(--ink); font-weight: 700; }
  .fz-msg { display: flex; gap: 8px; } .fz-msg b { color: var(--ink); } .fz-msg small { margin-left: 6px; color: var(--ts-mid); font-size: 9.5px; }
  .fz-msg p { margin: 2px 0 0; color: #333; line-height: 1.5; } .fz-msg em { font-style: normal; font-weight: 700; color: var(--ts-primary); }
  .fz-av { display: grid; place-items: center; flex: none; width: 24px; height: 24px; border-radius: 6px; background: var(--a); color: #fff; font-weight: 800; }
  .fz-gantt { display: grid; gap: 5px; padding: 8px 10px; border-radius: 8px; background: var(--bg-gray, #F7F8FB); }
  .fz-gantt p { margin: 0 0 2px; color: var(--ts-mid); font-size: 9.5px; font-weight: 700; }
  .fz-gantt i { display: block; height: 7px; margin-left: var(--s); width: var(--w); border-radius: 99px; background: #6F97F7; } .fz-gantt i.late { background: #F29A57; }

  /* コース一覧 */
  .clist { padding: clamp(64px, 7vw, 96px) 0; background: var(--bg-gray, #F7F8FB); scroll-margin-top: 96px; }
  .cfilter { display: grid; gap: 16px; margin-bottom: 28px; }
  .goalbar { display: flex; flex-wrap: wrap; gap: 8px; }
  .goalf { display: inline-flex; align-items: center; gap: 8px; height: 44px; padding: 0 18px 0 8px; border: 0; border-radius: 99px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); color: var(--ink); font: 700 13.5px/1 var(--font); cursor: pointer; transition: background-color .15s, box-shadow .15s, color .15s; }
  .goalf:first-child { padding-left: 18px; }
  .goalf__i { display: grid; place-items: center; width: 30px; height: 30px; border-radius: 50%; background: var(--tint-08); color: var(--ts-primary); }
  .goalf__i svg { width: 16px; height: 16px; }
  .goalf:hover { box-shadow: inset 0 0 0 1.5px var(--ts-primary); }
  .goalf[aria-pressed="true"] { background: var(--ts-primary); box-shadow: none; color: #fff; }
  .goalf[aria-pressed="true"] .goalf__i { background: rgba(255,255,255,.2); color: #fff; }
  .goalf:focus-visible, .csel select:focus-visible { outline: 2px solid var(--ts-primary); outline-offset: 2px; }
  .cfilter__row { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; }
  .csel { display: inline-flex; align-items: center; gap: 8px; color: var(--ts-mid); font-size: 12.5px; font-weight: 700; }
  .csel select { height: 40px; padding: 0 34px 0 14px; border: 0; border-radius: 10px; background: #fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 9l6 6 6-6' fill='none' stroke='%230F1B45' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") no-repeat right 10px center / 14px; box-shadow: inset 0 0 0 1px var(--line); color: var(--ink); font: 700 13px/1 var(--font); appearance: none; -webkit-appearance: none; cursor: pointer; }
  .ccount { margin: 0 0 0 auto; color: var(--ts-mid); font-size: 13px; } .ccount b { margin-right: 2px; color: var(--ink); font-size: 18px; font-variant-numeric: tabular-nums; }
  .cgrid.popular { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; padding: 0; background: none; overflow: visible; }
  .cgrid .course[hidden] { display: none; }
  .cgrid .thumb { aspect-ratio: 16 / 10; }
  .cgrid .cv { position: relative; width: 100%; height: 100%; }
  .cgrid .cv--img img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
  .cv--g { display: grid; place-items: center; align-content: center; gap: 8px; background: var(--cb); color: var(--cc); overflow: hidden; }
  .cv__dots { position: absolute; inset: 0; background: radial-gradient(circle, var(--cc) 1px, transparent 1.4px) 0 0 / 14px 14px; opacity: .12; }
  .cv__ic { position: relative; display: grid; place-items: center; width: 52px; height: 52px; border-radius: 16px; background: #fff; box-shadow: 0 6px 16px rgba(15,27,69,.08); }
  .cv__ic svg { width: 26px; height: 26px; }
  .cv--g b { position: relative; font-size: 12px; letter-spacing: .06em; }
  .cgrid .cat { background: var(--cb) !important; color: var(--cc) !important; }
  .cempty { display: grid; justify-items: center; gap: 12px; padding: 48px 16px; border-radius: 20px; background: #fff; color: var(--ts-mid); text-align: center; }
  .cempty[hidden], .cgrid .course[hidden] { display: none; }
  .cempty p { margin: 0; } .cempty button { height: 40px; padding: 0 18px; border: 0; border-radius: 99px; background: var(--ts-primary); color: #fff; font: 700 13px/1 var(--font); cursor: pointer; }
  .cnote { margin: 20px 0 0; color: var(--ts-mid); font-size: 12px; }

  /* 一覧：左に絞り込み（PC）／最初は種類ごとの3段、絞り込むとグリッド */
  .goalbar { margin-bottom: 24px; }
  .clay { display: grid; grid-template-columns: 232px minmax(0, 1fr); gap: 28px; align-items: start; }
  .cside { position: sticky; top: 24px; }
  .cside__in { display: grid; gap: 16px; padding: 20px; border-radius: 18px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); }
  .cside__top { display: flex; align-items: center; justify-content: space-between; }
  .cside__h { margin: 0; color: var(--ink); font-size: 15px; font-weight: 700; }
  .cside__x { display: none; }
  .fgrp { display: grid; gap: 8px; padding-top: 14px; border-top: 1px solid var(--line); }
  .fgrp > p { margin: 0 0 2px; color: var(--ts-mid); font-size: 12px; font-weight: 700; }
  .fchk { display: flex; align-items: center; gap: 8px; color: var(--ink); font-size: 13.5px; cursor: pointer; }
  .fchk input { width: 16px; height: 16px; margin: 0; accent-color: var(--ts-primary); }
  .fchk small { margin-left: auto; color: var(--ts-mid); font-size: 12px; font-variant-numeric: tabular-nums; }
  .cside__foot { display: flex; gap: 8px; padding-top: 14px; border-top: 1px solid var(--line); }
  .cside__clear { height: 36px; padding: 0 14px; border: 0; border-radius: 99px; background: transparent; box-shadow: inset 0 0 0 1px var(--line); color: var(--ink); font: 700 12.5px/1 var(--font); cursor: pointer; }
  .cside__ok { display: none; }
  .cmain { min-width: 0; }
  .cbar { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px 14px; margin-bottom: 18px; }
  .cbar .ccount { margin: 0; }
  .cbar__r { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; }
  .cbar__mode { height: 40px; padding: 0 16px; border: 0; border-radius: 10px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); color: var(--ts-primary); font: 700 13px/1 var(--font); cursor: pointer; }
  .cbar__mode:hover, .cside__clear:hover { box-shadow: inset 0 0 0 1.5px var(--ts-primary); }
  .crows { display: grid; gap: 32px; }
  .crows[hidden], #gridWrap[hidden], .cmore[hidden], .cdim[hidden] { display: none; }
  .crow__h { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; margin-bottom: 14px; }
  .crow__h h3 { margin: 0; color: var(--ink); font-size: 20px; }
  .crow__h p { margin: 4px 0 0; color: var(--ts-mid); font-size: 13px; }
  .crow__all { display: inline-flex; flex: none; align-items: center; gap: 6px; padding: 0; border: 0; background: none; color: var(--ts-primary); font: 700 13.5px/1.4 var(--font); cursor: pointer; }
  .crow__all .ico { width: 15px; height: 15px; }
  .cgrid.popular.crow__track { grid-auto-flow: column; grid-template-columns: none; grid-auto-columns: calc((100% - 40px) / 3.2); overflow-x: auto; padding-bottom: 10px; scroll-snap-type: x mandatory; scrollbar-width: thin; }
  .crow__track .course { scroll-snap-align: start; }
  .crow__track .desc { display: none; }
  .clist #grid.cgrid.popular { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .cmore { display: grid; justify-items: center; gap: 10px; margin-top: 28px; color: var(--ts-mid); font-size: 12.5px; }
  .cmore p { margin: 0; }
  .cmore button { height: 48px; padding: 0 32px; border: 0; border-radius: 99px; background: #fff; box-shadow: inset 0 0 0 1.5px var(--ts-primary); color: var(--ts-primary); font: 700 14px/1 var(--font); cursor: pointer; }
  .cmore button:hover { background: var(--ts-primary); color: #fff; }
  .cfab { display: none; }
  .cdim { position: fixed; inset: 0; z-index: 60; background: rgba(15,27,69,.4); }
  @media (max-width: 900px) {
    .clay { grid-template-columns: minmax(0, 1fr); }
    .cside { position: fixed; left: 0; right: 0; bottom: 0; top: auto; z-index: 70; transform: translateY(105%); visibility: hidden; transition: transform .25s, visibility .25s; }
    .cside.is-open { transform: none; visibility: visible; }
    .cside__in { max-height: 80svh; overflow-y: auto; padding: 20px 20px calc(20px + env(safe-area-inset-bottom, 0px)); border-radius: 20px 20px 0 0; box-shadow: 0 -10px 30px rgba(15,27,69,.2); }
    .cside__x { display: grid; place-items: center; width: 36px; height: 36px; border: 0; border-radius: 50%; background: var(--bg-gray, #F7F8FB); color: var(--ink); font-size: 20px; cursor: pointer; }
    .cside__ok { display: block; flex: 1; height: 44px; border: 0; border-radius: 99px; background: var(--ts-primary); color: #fff; font: 700 14px/1 var(--font); cursor: pointer; }
    .cside__clear { height: 44px; }
    .cfab { display: inline-flex; align-items: center; justify-content: center; position: sticky; bottom: calc(16px + env(safe-area-inset-bottom, 0px)); z-index: 50; margin: 24px auto 0; height: 48px; padding: 0 26px; border: 0; border-radius: 99px; background: var(--ink); color: #fff; font: 700 14px/1 var(--font); box-shadow: 0 10px 24px rgba(15,27,69,.3); cursor: pointer; }
    .clist .wrap { display: flex; flex-direction: column; }
    .cfab { align-self: center; }
    .clist #grid.cgrid.popular { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .cgrid.popular.crow__track { grid-auto-columns: calc((100% - 20px) / 2.3); }
  }
  @media (max-width: 640px) {
    .clist #grid.cgrid.popular { grid-template-columns: minmax(0, 1fr); }
    .cgrid.popular.crow__track { grid-auto-columns: 64%; }
    .cgrid.crow__track .course { flex-direction: column; }
    .cgrid.crow__track .thumb { width: auto; aspect-ratio: 16 / 10; border-right: 0; border-bottom: 1px solid var(--line); }
    .cgrid.crow__track .cv--g b { display: block; }
    .cbar__r { width: 100%; }
    .crow__h { flex-direction: column; align-items: flex-start; gap: 6px; }
    .cbar__mode { flex: 1; white-space: nowrap; }
  }
  @media (prefers-reduced-motion: reduce) { .cside { transition: none; } }

  /* LINE帯（一覧の下） */
  .cline { padding: 0 0 clamp(56px, 6vw, 80px); background: var(--bg-gray, #F7F8FB); }
  .cline__band { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; align-items: center; gap: 16px 22px; padding: 22px 28px; border-radius: 20px; background: #fff; box-shadow: inset 0 0 0 1.5px #06C755; }
  .cline__ic { display: grid; place-items: center; width: 52px; height: 52px; border-radius: 16px; background: #06C755; color: #fff; } .cline__ic svg { width: 28px; height: 28px; }
  .cline__k { margin: 0; color: #06A847; font-size: 12px; font-weight: 700; letter-spacing: .06em; }
  .cline__t b { display: block; margin-top: 2px; color: var(--ink); font-size: 18px; } .cline__t em { font-style: normal; color: #06A847; }
  .cline__t p:last-child { margin: 4px 0 0; color: var(--ts-mid); font-size: 13px; }
  .cline__btn { display: inline-flex; align-items: center; gap: 8px; height: 48px; padding: 0 22px; border-radius: 99px; background: #06C755; color: #fff; font-size: 14px; font-weight: 700; text-decoration: none; white-space: nowrap; }
  .cline__btn:hover { background: #05B04B; } .cline__btn .ico { width: 16px; height: 16px; }
  .cnext { background: #fff; }

  @media (max-width: 1100px) { .cgrid.popular { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
  @media (max-width: 900px) {
    .cfeat__grid { grid-template-columns: minmax(0, 1fr); }
    .cgrid.popular { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .ccount { width: 100%; margin: 0; }
  }
  @media (max-width: 640px) {
    .goalbar { flex-wrap: nowrap; margin: 0 calc(var(--gutter) * -1); padding: 2px var(--gutter); overflow-x: auto; scrollbar-width: none; }
    .goalf { flex: none; }
    .csel { flex: 1 1 calc(50% - 8px); } .csel select { flex: 1; min-width: 0; }
    .cgrid.popular { grid-template-columns: minmax(0, 1fr); }
    .cgrid .course { flex-direction: row; }
    .cgrid .thumb { flex: none; width: 116px; aspect-ratio: auto; border-bottom: 0; border-right: 1px solid var(--line); }
    .cgrid .cv__ic { width: 40px; height: 40px; border-radius: 12px; } .cgrid .cv__ic svg { width: 20px; height: 20px; } .cgrid .cv--g b { display: none; }
    .cgrid .desc { display: none; }
    .fz__b { padding: 22px 20px 24px; } .fz__t { font-size: 19px; } .fz__facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .fz-slack__side { display: none; } .fz-slack { grid-template-columns: 1fr; }
    .cline__band { grid-template-columns: auto minmax(0, 1fr); padding: 20px; } .cline__btn { grid-column: 1 / -1; justify-content: center; }
  }
'''

GOALMAP = {k: cats for k, t, cats, _ in GOALS if cats}
DIAG_DATA = json.dumps([{'slug': c[0], 'title': c[1].replace('&amp;', '&'), 'cat': c[2], 'catName': CAT[c[2]][0], 'price': c[4], 'dur': c[5], 'time': c[6], 'lv': c[7], 'href': chref(c[0])} for c in C], ensure_ascii=False)
DIAG_GOALS = json.dumps({'it': ['it', 'biz'], 'mk': ['mk', 'cr'], 'en': ['en'], 'all': list(CAT.keys())})
script = '''<script>
  // コース診断：3問の答えから、合うコースを原則1つ提案する（FV-009／PRC-005）。相談には答えを引き継ぐ（CTA-005）
  (() => {
    const box = document.getElementById('diagBox'), res = document.getElementById('diagRes'); if (!box) return;
    const D = ''' + DIAG_DATA + ''', G = ''' + DIAG_GOALS + ''';
    const qs = [...box.querySelectorAll('.dq')], back = document.getElementById('diagBack'), bar = document.getElementById('diagBar'), num = document.getElementById('diagN');
    const LV = ['ベーシック', 'プロ', 'プレミア']; let ans = [], q = 0;
    const label = (qi, v) => qs[qi].querySelector(`[data-v="${v}"] span`).textContent;
    const show = i => { q = i; qs.forEach((f, k) => f.hidden = k !== i); back.hidden = i === 0; bar.style.width = ((i + 1) / 3 * 100) + '%'; num.textContent = `Q${i + 1} / 3`;
      qs[i].querySelectorAll('.dq__op').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.v === ans[i]))); };
    const esc = t => String(t).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const result = () => {
      const pool = D.filter(c => G[ans[0]].includes(c.cat));
      const want = LV.indexOf(ans[2]);
      const TM = { '1': /1〜2|週1|週2時間/, '2': /2〜3|週2/, '4': /週[4-9]|週2回/, '0': /$^/ };
      const score = c => Math.abs(LV.indexOf(c.lv) - want) * 10 + (c.time && TM[ans[1]].test(c.time) ? 0 : 3) + (c.price ? 0 : 1);
      const ranked = pool.slice().sort((a, b) => score(a) - score(b));
      const top = ranked[0], alt = ranked.slice(1, 2);
      const why = [ans[0] === 'all' ? '目的がまだ決まっていなくても、始めやすいコースです' : `目的「${label(0, ans[0])}」に合う「${top.catName}」のコースです`,
        top.lv === ans[2] ? `「${label(2, ans[2])}」に合う「${top.lv}」のコースです` : `いちばん近い種類は「${top.lv}」です`,
        top.time ? `学習時間の目安は「${top.time}」です（あなたの答え：${label(1, ans[1])}）` : `学習時間はご都合に合わせて相談できます（あなたの答え：${label(1, ans[1])}）`];
      const q2 = new URLSearchParams({ course: top.title, goal: label(0, ans[0]), time: label(1, ans[1]), level: label(2, ans[2]) });
      res.innerHTML = `<div class="dr"><div><span class="dr__b">いちばん合うコース</span><p class="dr__n">${esc(top.title)}</p>
        <p class="dr__m">${esc(top.catName)}・${esc(top.lv)}${top.dur ? '・' + esc(top.dur) : ''}${top.price ? '・¥' + top.price.toLocaleString() : ''}</p>
        <p class="dr__h">おすすめの理由</p><ul>${why.map(w => `<li>${esc(w)}</li>`).join('')}</ul>
        <div class="dr__bt"><a class="btn btn--primary" href="${top.href}">コースの詳細を見る</a><a class="btn btn--white" href="contact.html?${q2}">この結果で無料相談する</a></div>
        <p class="dr__note">相談のフォームには、診断の答えが入った状態で進みます。</p></div>
        <div class="dr__s"><p class="dr__h" style="margin-top:0">ほかの候補</p>${alt.map(c => `<a class="dr__c" href="${c.href}"><b>${esc(c.title)}</b><small>${esc(c.catName)}・${esc(c.lv)}${c.price ? '・¥' + c.price.toLocaleString() : ''}</small></a>`).join('') || '<p class="dr__ans">ほかの候補はありません。</p>'}
        <p class="dr__ans">あなたの答え：${ans.map((v, i) => esc(label(i, v))).join('／')}</p><button type="button" class="dr__re" id="diagRe">答えを選び直す</button></div></div>`;
      box.hidden = true; res.hidden = false; res.scrollIntoView({ block: 'nearest' });
      document.getElementById('diagRe').addEventListener('click', () => { ans = []; res.hidden = true; box.hidden = false; show(0); });
    };
    box.addEventListener('click', e => { const b = e.target.closest('.dq__op'); if (!b) return; ans[q] = b.dataset.v; ans.length = q + 1; q < 2 ? show(q + 1) : result(); });
    back.addEventListener('click', () => show(Math.max(0, q - 1)));
  })();

  // コース一覧：最初は「コースの種類ごとの3段（横スライド）」、絞り込み・すべて見るで「グリッド（9件ずつ）」に切り替え
  // LP 01のカードからは ?goal=it（本番）または #goal-it（このデザイン確認用）、フッターのカテゴリは ?c=it / #c-it で着地
  (() => {
    const GOALS = ''' + json.dumps(GOALMAP) + ''';
    const PAGE = 9;
    const $ = id => document.getElementById(id);
    const grid = $('grid'), cards = [...grid.querySelectorAll('.course')];
    const rows = $('rows'), gridWrap = $('gridWrap'), empty = $('empty'), count = $('count');
    const sort = $('f-sort'), modeBtn = $('modeBtn'), side = $('side'), dim = $('dim'), fab = $('fab'), fabN = $('fabN');
    const goalBtns = [...document.querySelectorAll('.goalf')];
    const boxes = name => [...side.querySelectorAll(`input[name="${name}"]`)];
    const checked = name => boxes(name).filter(b => b.checked).map(b => b.value);
    let goal = 'all', forceGrid = false, shown = PAGE;
    const priceBand = p => p === null ? null : p < 3000 ? 'a' : p < 10000 ? 'b' : 'c';
    const active = () => goal !== 'all' || checked('tier').length || checked('cat').length || checked('price').length;

    function render() {
      const tiers = checked('tier'), cats = checked('cat'), prices = checked('price');
      const gc = GOALS[goal] || null;
      const nF = (goal !== 'all') + tiers.length + cats.length + prices.length;
      fabN.textContent = nF ? `（${nF}）` : '';
      const gridMode = forceGrid || active() || sort.value !== 'rec';
      rows.hidden = gridMode; gridWrap.hidden = !gridMode;
      modeBtn.textContent = gridMode ? '種類ごとの表示に戻す' : 'すべてを一覧で見る';
      if (!gridMode) { count.innerHTML = '<b>' + cards.length + '</b>件のコース'; empty.hidden = true; return; }
      const val = c => c.dataset.price ? +c.dataset.price : null;
      const ok = cards.filter(c => (!gc || gc.includes(c.dataset.cat)) && (!tiers.length || tiers.includes(c.dataset.level))
        && (!cats.length || cats.includes(c.dataset.cat)) && (!prices.length || prices.includes(priceBand(val(c)))));
      ok.sort((a, b) => {
        if (sort.value === 'rec') return a.dataset.order - b.dataset.order;
        const x = val(a), y = val(b);
        if (x === null && y === null) return a.dataset.order - b.dataset.order;
        if (x === null) return 1; if (y === null) return -1;             // 価格未定は最後に
        return sort.value === 'low' ? x - y : y - x;
      });
      cards.forEach(c => { c.hidden = true; });
      ok.forEach((c, i) => { grid.appendChild(c); c.hidden = i >= shown; });
      count.innerHTML = '<b>' + ok.length + '</b>件のコース';
      empty.hidden = ok.length > 0;
      $('more').hidden = ok.length <= shown;
      $('moreInfo').textContent = `${Math.min(shown, ok.length)}件 / ${ok.length}件を表示中`;
      $('moreBtn').textContent = `もっと見る（残り${Math.max(0, ok.length - shown)}件）`;
    }
    const update = () => { shown = PAGE; render(); };
    function setGoal(g) {
      goal = GOALS[g] ? g : 'all';
      goalBtns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.goal === goal)));
      update();
    }
    function clearAll() { ['tier', 'cat', 'price'].forEach(n => boxes(n).forEach(b => { b.checked = false; })); sort.value = 'rec'; forceGrid = false; setGoal('all'); }
    goalBtns.forEach(b => b.addEventListener('click', () => setGoal(b.dataset.goal)));
    side.addEventListener('change', update);
    sort.addEventListener('change', update);
    $('moreBtn').addEventListener('click', () => { shown += PAGE; render(); });
    $('clear').addEventListener('click', clearAll);
    $('reset').addEventListener('click', clearAll);
    modeBtn.addEventListener('click', () => { if (rows.hidden) clearAll(); else { forceGrid = true; update(); } });
    document.querySelectorAll('.crow__all').forEach(b => b.addEventListener('click', () => {
      boxes('tier').forEach(x => { x.checked = x.value === b.dataset.tier; });
      update(); $('list').scrollIntoView({ block: 'start', behavior: 'smooth' });
    }));
    // スマホ：絞り込みを下から出す
    const openSide = o => { side.classList.toggle('is-open', o); dim.hidden = !o; document.body.style.overflow = o ? 'hidden' : ''; };
    fab.addEventListener('click', () => openSide(true));
    [dim, $('sideClose'), $('sideOk')].forEach(el => el.addEventListener('click', () => openSide(false)));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') openSide(false); });

    function land(first) {
      const q = first ? new URLSearchParams(location.search) : new URLSearchParams();
      const h = (location.hash || '').slice(1);
      const g = q.get('goal') || (h.startsWith('goal-') ? h.slice(5) : '');
      const c = q.get('c') || (h.startsWith('c-') ? h.slice(2) : '');
      if (!g && !c) { if (first) render(); return; }
      boxes('cat').forEach(b => { b.checked = b.value === c; });
      setGoal(g);
      $('list').scrollIntoView({ block: 'start' });
    }
    land(true);
    window.addEventListener('hashchange', () => land(false));
  })();
</script>
'''

html = head + css + between.replace('<a href="courses.html">コースを探す</a>', '<a href="courses.html" aria-current="page">コースを探す</a>') \
       .replace('<a class="brand" href="/"', '<a class="brand" href="lp-design.html"') \
       + '<main>\n' + pagehead + feature + diag + listing + compare + line_band + nx2 + '\n' + footer_on.replace('</body>', script + '</body>')
html = html.replace('<title>', '<title>', 1)
html = re.sub(r'<title>[^<]*</title>', '<title>コースを探す | The Academy</title>', html, count=1)
open(OUT, 'w').write(html)
print('ok', len(html))
