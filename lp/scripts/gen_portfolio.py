# ポートフォリオ（/portfolio）ページを、LPの共通部品と「コースを探す」の下層ページ共通スタイルから組み立てる
# 流れ（プロトタイプ準拠）：見出し → WHY（VS比較）→ 伝えられること → ひとりじゃない → 公開ポートフォリオの例 → はじめかた・FAQ → 行動
import os, tempfile
S = os.path.dirname(os.path.abspath(__file__))          # このスクリプトのフォルダ（lp/scripts）
LPDIR = os.path.dirname(S)                              # 出力先（lp）
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')  # 共通部品を取り出すときの捨て出力
import os, re
os.environ['TA_COURSES_OUT'] = TMP_COURSES
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)
head, between, footer_on, ARROW, lp = g['head'], g['between'], g['footer_on'], g['ARROW'], g['s']
base_css = g['css']
OUT = os.path.join(LPDIR, 'portfolio.html')

def ic(d, w=1.9): return f'<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{d}</g></svg>'
avatars = re.findall(r'<svg class="avt".*?</svg>', lp, re.S)
av = lambda i, size=36: re.sub(r'width="\d+" height="\d+"', f'width="{size}" height="{size}"', avatars[i % len(avatars)], count=1)
HEART = ic('<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>', 2)
CHAT = ic('<path d="M20 12a8 8 0 0 1-11.6 7.1L4 20l1-4.2A8 8 0 1 1 20 12z"/>', 2)
I = {
 'cert': ic('<circle cx="12" cy="9" r="5"/><path d="M9 13.5 8 21l4-2 4 2-1-7.5"/>'),
 'score': ic('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'),
 'ai': ic('<rect x="5" y="7" width="14" height="12" rx="3"/><path d="M12 3v4M9 12h.01M15 12h.01M9 16h6"/>'),
 'path': ic('<circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="6" r="2.2"/><path d="M8 17c6 0 2-10 8-10"/>'),
 'bulb': ic('<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.2h5c0-.9.4-1.6 1.1-2.2A6 6 0 0 0 12 3z"/>'),
 'star': ic('<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>'),
 'flag': ic('<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>'),
 'person': ic('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
 'brief': ic('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>'),
 'book': ic('<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/>'),
 'eye': ic('<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'),
 'user+': ic('<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0M19 8v6M16 11h6"/>'),
 'feed': ic('<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 9h8M8 13h8M8 17h5"/>'),
 'down': ic('<path d="M12 5v14M6 13l6 6 6-6"/>', 2.2),
 'lock': ic('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>'),
 'off': ic('<path d="M3 3l18 18M10.6 6.1A10 10 0 0 1 12 6c6.4 0 10 6 10 6a17 17 0 0 1-3 3.6M6.6 6.6C3.9 8.3 2 12 2 12s3.6 7 10 7a9.6 9.6 0 0 0 4.4-1"/>'),
 'globe': ic('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'),
 'grid': ic('<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/></g>'),
}
I['grid'] = I['grid'].replace('</g></g>', '</g>')

# ── 共通：公開ポートフォリオの画面パーツ
def prof(size='m', fol=True):
    return f'''<div class="pp-prof pp-prof--{size}"><span class="pp-av">匿名</span><div><b>匿名ユーザー</b><small>営業企画 × データ分析を学習中</small></div>{'<span class="pp-fol">フォローする</span>' if fol else ''}</div>'''
STATS = '<ul class="pp-stats"><li><b>3</b>実績</li><li><b>2</b>資格</li><li><b>42</b>学びの記録</li></ul>'

# ── ① ページ見出し（ヒーロー型）
hero_vis = '''<div class="pv" aria-hidden="true">
  <div class="pq pv__prof"><img src="assets/portfolio/hero-profile.webp" alt=""></div>
  <div class="pq pv__feat"><img src="assets/portfolio/hero-featured-work.webp" alt=""></div>
  <div class="pq pv__cert"><img src="assets/portfolio/hero-certification.webp" alt=""></div>
  <div class="pq pv__road"><img src="assets/portfolio/hero-roadmap.webp" alt=""></div>
  <span class="pv__lab pv__l1">代表実績</span><span class="pv__lab pv__l2">資格・認定</span><span class="pv__lab pv__lab--o pv__l3">目指す未来</span>
</div>'''
pagehead = f'''<section class="phead pp-head" aria-labelledby="page-title"><div class="wrap pp-head__grid">
<div class="pp-head__copy">
<nav class="crumb" aria-label="パンくずリスト"><a href="lp-design.html">トップ</a><span aria-hidden="true">/</span><span aria-current="page">ポートフォリオ</span></nav>
<p class="sec-kicker pp-head__k">LEARNING PORTFOLIO</p>
<h1 class="phead__t" id="page-title">積み重ねた努力を、<wbr>見える形に。</h1>
<p class="phead__lead">資格やスコアだけでは、<wbr>そこまでの努力は伝わりません。<wbr>学びの過程と成果を1ページにまとめて公開し、<wbr>次の仕事やチャンスにつなげましょう。</p>
<div class="pp-cta"><a class="btn btn--primary" href="#start">無料で登録する</a><a class="btn btn--white" href="#sample">ポートフォリオの例を見る<span class="pp-cta__ic">{I['down']}</span></a></div>
<p class="pp-note">{I['lock']}匿名で始められます。登録は無料です。</p>
</div>
{hero_vis}
</div></section>'''

# ── ② WHY：VS比較
# 目盛りは物差し全体の幅に対して 1/60 ずつ。10・30・50 番目が「これまで／今／これから」のピンの位置（1/6・1/2・5/6）と一致する
TICKS = ''.join(f'<i class="{"p on" if n == 50 else "p" if n in (10, 30) else "l" if n % 5 == 0 else ""}" style="left:{n * 100 / 60:.4f}%"></i>' for n in range(1, 60))
def items(keys): return ''.join(f'<li><span>{I[k]}</span>{t}</li>' for k, t in keys)
def vsl(items): return ''.join(f'<li><span>{I[k]}</span>{t}</li>' for k, t in items)
why = f'''<section class="pp-why" id="why" aria-labelledby="why-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">WHY PORTFOLIO</p><h2 class="sec-title" id="why-title">結果だけでは、<wbr>頑張りは伝わらない。</h2>
<p class="sec-lead">評価の物差しが変わりつつある今、<wbr>「過程」を伝える手段が必要です。</p></div></header>
<div class="r1">
<div class="r1__ruler" aria-hidden="true"><div class="r1__ticks">{TICKS}</div><span class="r1__name">評価の物差し</span>
 <span class="r1__pin" style="left:16.6667%">これまで</span><span class="r1__pin" style="left:50%">今</span><span class="r1__pin r1__pin--on" style="left:83.3333%">これから</span></div>
<ol class="r1__cols">
 <li><p class="r1__k">PAST<span>これまで</span></p><h3>結果を<br>持っているか</h3><ul>{items([('cert','資格の有無'),('score','スコアや点数')])}</ul></li>
 <li><p class="r1__k">NOW<span>今</span></p><h3>結果を<br>すぐ比べられる</h3><ul>{items([('ai','AIによるスキル判定')])}</ul><p class="r1__n">結果だけでは、<wbr>差がつきにくくなった</p></li>
 <li class="on"><p class="r1__k">NEXT<span>これから</span></p><h3>過程で<br>選ばれる</h3><ul>{items([('path','学びを続けてきた過程'),('bulb','試行錯誤の工夫'),('star','その人らしい強み')])}</ul>
  <p class="r1__warn"><span>{I['off']}</span>でも、まだ誰にも見えていない</p></li>
</ol></div>
<p class="vs__so"><span>だから</span>見えていないものを、<wbr>公開ポートフォリオで自分から伝える。</p>
<div class="pfor"><p class="pfor__h">こんな方に</p>
  <div class="pfor__c">{av(0, 44)}<div><h3>「学んできたことで、<wbr>次の仕事をつかみたい」</h3><p>身につけたことを実績として見せ、<wbr>転職や独立、<wbr>新しい役割につなげたい方に。</p></div></div>
  <div class="pfor__c">{av(1, 44)}<div><h3>「今度こそ、<wbr>形に残したい」</h3><p>途中で止まった学びも、<wbr>自分のペースで少しずつ積み重ねたい方に。</p></div></div>
</div>
</div></section>'''

# ── ③ 伝えられること（2段のジグザグ）
show_v1 = f'''<div class="pw sh-v1" aria-hidden="true">
  <div class="pw__bar"><i></i><i></i><i></i><span>実績</span></div>
  <div class="sh-v1__in">
    <img src="assets/outcomes/marketing-strategy.webp" alt="">
    <div><span class="sh-pill">実績</span><p class="sh-v1__t">重点顧客の再設計と、<br>SNSを起点にした集客計画</p>
    <dl><div><dt>背景・課題</dt><dd>来店のきっかけが分からない</dd></div><div><dt>担当範囲</dt><dd>顧客分析・戦略シート作成</dd></div><div><dt>制作プロセス</dt><dd>分析 → 仮説 → 店長と検証</dd></div><div class="on"><dt>成果</dt><dd>新規来店の導線ができた</dd></div></dl></div>
  </div>
  <div class="sh-v1__foot"><span>{I['cert']}資格・認定 2</span><span>{I['path']}学びの歩み 42件</span></div>
</div>'''
show_v2 = f'''<div class="pw sh-v2" aria-hidden="true">
  <div class="pw__bar"><i></i><i></i><i></i><span>プロフィール</span></div>
  <div class="sh-v2__in">{prof('m')}
    <p class="sh-lab">ビジョン</p><p class="sh-v2__vis">「感覚とデータの両方から、<br>選ばれる体験をつくりたい。」</p>
    <div class="sh-v2__g">
      <div><p class="sh-lab">人物像診断</p><div class="sh-bar"><span>計画</span><i style="--w:78%"></i></div><div class="sh-bar"><span>共感</span><i style="--w:64%"></i></div><div class="sh-bar"><span>挑戦</span><i style="--w:52%"></i></div></div>
      <div><p class="sh-lab">強み・働き方</p><div class="pp-tags"><span>顧客理解</span><span>仮説づくり</span><span>週3リモート</span></div>
      <p class="sh-lab" style="margin-top:12px">役立った本・サービス</p><p class="sh-v2__bk">{I['book']}『顧客体験の教科書』</p></div>
    </div>
  </div>
</div>'''
def li3(items): return ''.join(f'<li><span class="sh-ic">{I[k]}</span><div><b>{t}</b><p>{d}</p></div></li>' for k, t, d in items)
def tile(img, name, desc, cls=''):
    return f'<div class="g2__t{cls}"><div class="g2__img"><img src="assets/portfolio/{img}.webp" alt="" loading="lazy"></div><p class="g2__cap">{name}<small>{desc}</small></p></div>'
show = f'''<section class="pp-show" id="show" aria-labelledby="show-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">WHAT YOU CAN SHOW</p><h2 class="sec-title" id="show-title">公開ポートフォリオで、<wbr>伝えられること。</h2></div></header>
<h3 class="g2__h"><span>01</span>学びを、<wbr>そのまま実績に</h3>
<div class="g2__grid g2__grid--a">
 {tile('show-featured-work', '実績', '背景・課題 → 担当範囲 → 制作プロセス → 成果を、<wbr>ひとつのストーリーに。', ' g2__t--big')}
 {tile('show-certification', '資格・認定', 'スキルを裏付ける資格と認定を載せられます。')}
 {tile('show-timeline', '学びの歩み', '学び始めから現在まで、<wbr>積み重ねを時系列で。')}
</div>
<h3 class="g2__h"><span>02</span>数字だけでは見えない、<wbr>あなたらしさ</h3>
<div class="g2__grid g2__grid--b">
 {tile('show-vision', 'ビジョン', '実現したいこと')}
 {tile('show-persona', '人柄', '自分らしさを、<wbr>自分の言葉で記入')}
 {tile('show-strengths', '強み・働き方', '得意なこと・今の仕事')}
 {tile('show-books', '書籍・サービス', '役立ったもの', ' g2__t--fit')}
</div>
<p class="hl-note">※画面はイメージです。</p>
</div></section>'''

# ── ④ ひとりじゃない：実際のフィード画面（3カラム）を横幅いっぱいに
HEART2=ic('<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',2)
BOOK=ic('<path d="M6 3h12v18l-6-4-6 4z"/>',2); SHARE=ic('<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 11l7.6-4M8.2 13l7.6 4"/>',2)
SEARCH=ic('<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',2); PLUS=ic('<path d="M12 5v14M5 12h14"/>',2.2)
LAY=ic('<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',2); BELL=ic('<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 20a2 2 0 0 0 4 0"/>',2)
POSTS=[(1,'@saki_mkt','マーケティング職','制作実績を共有しました','2時間前','#個人の学び','カフェのSNSキャンペーン企画をまとめました。背景から結果まで、ポートフォリオに残しています。','assets/outcomes/sns-design.webp',24),
       (2,'@ryo_analytics','データ分析を学習中','学びを共有しました','昨日','#週2時間の学び','今週は平日夜に30分ずつ進めた📊 グラフの見せ方が少し分かってきた。',None,12)]
def post(p,img=True):
    a,h,role,act,t,tag,body,src_,lk=p
    im=f'<div class="fx-img"><img src="{src_}" alt=""></div>' if (src_ and img) else ''
    return f'''<div class="fx-post"><div class="fx-av">{av(a, 40)}<i>+</i></div><div class="fx-pb"><b class="fx-h">{h}</b><small class="fx-role">{role}</small><small class="fx-act">{act}・{t}</small><span class="fx-tag">{tag}</span><p>{body}</p>{im}<div class="fx-acts"><span>{HEART2}{lk}</span><span>{BOOK}保存</span><span>{SHARE}シェア</span></div></div></div>'''
TOP=f'''<div class="fx-top"><div class="fx-search">{SEARCH}投稿やユーザーを検索</div><span class="fx-new">{PLUS}新規投稿</span></div>
<ul class="fx-tabs"><li class="on">{LAY}フィード</li><li>{HEART2}いいね</li><li>{BOOK}保存</li><li>{BELL}通知</li></ul>'''
TREND=f'''<div class="fx-card fx-trend"><p class="fx-ch">トレンドのキーワード</p><ol>{''.join(f'<li><small>{i+1}・The Academyで注目</small><b>{k}</b><em>{n}件の投稿</em></li>' for i,(k,n) in enumerate([('制作実績',10),('SNSマーケティング',8),('データ分析',8),('Canva',6),('生成AI',4)]))}</ol></div>'''
FOLLOW=f'''<div class="fx-card fx-follow"><p class="fx-ch">フォローのおすすめ</p>{''.join(f'<div class="fx-u">{av(a, 34)}<div><b>{h}</b><small>{r}</small></div>{"<span class=fx-on>✓ フォロー中</span>" if on else "<span class=fx-plus>"+PLUS+"</span>"}</div>' for a,h,r,on in [(4,'@kento_side','データ分析で副業を開始',False),(0,'@mio_design','営業 → デザイナーへ',True),(5,'@taku_eng','英語で海外案件に挑戦',False)])}</div>'''
feed_v = f'''<div class="fx h2" aria-hidden="true"><div class="h1__win"><div class="fx-bar">フィード<span class="fx-lv">Level 4<i></i></span></div>
<div class="h2__g">{TREND}<div class="fx-main">{TOP}{post(POSTS[0])}</div><div class="h2__r">{FOLLOW}<div class="fx-card h2__mini">{post(POSTS[1],False)}</div></div></div></div>
<span class="h2__lab h2__l1">ロールモデルが見つかる</span><span class="h2__lab h2__l2">学びのフィード</span><span class="h2__lab h2__l3">フォローでつながる</span></div>'''
alone = f'''<section class="pp-alone" id="alone" aria-labelledby="alone-title"><div class="wrap pp-alone__grid">
<div class="pp-alone__copy"><header class="sec-head"><div><p class="sec-kicker">YOU ARE NOT ALONE</p><h2 class="sec-title" id="alone-title">ひとりじゃないから、<wbr>続けられる。</h2>
<p class="sec-lead">「自分にもできる？」<wbr>「同じような人はいる？」。<wbr>その答えは、<wbr>先を歩く人の中にあります。</p></div></header>
<ol class="al-list">
  <li><span class="sh-ic">{I['eye']}</span><div><b>ロールモデルが見つかる</b><p>関連するユーザーのポートフォリオから、<wbr>なりたい姿に近い人が見つかります。</p></div></li>
  <li><span class="sh-ic">{I['user+']}</span><div><b>フォローでつながる</b><p>SNSのように気になる人をフォローして、<wbr>歩みを追いかけられます。</p></div></li>
  <li><span class="sh-ic">{I['feed']}</span><div><b>学びのフィード</b><p>フォローしている人の学びのシェアが届き、<wbr>勉強の進め方のヒントとモチベーションに。</p></div></li>
</ol></div>
{feed_v}
</div></section>'''

# ── ⑤ 公開ポートフォリオの例
sample = f'''<section class="pp-sample" id="sample" aria-labelledby="sample-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">SAMPLE</p><h2 class="sec-title" id="sample-title">公開ポートフォリオの例</h2>
<p class="sec-lead">こんなページが、<wbr>あなたの学びからできあがります。</p></div></header>
<div class="i3">
<div class="pw i3__win"><div class="pw__bar"><i></i><i></i><i></i><span>theacademy.jp/portfolio/u/anonymous</span></div><div class="i3__shot"><img src="assets/portfolio/sample-page.webp" alt="公開ポートフォリオの画面例。プロフィール、スコア、ビジョン、代表実績" loading="lazy">
<span class="i3__n" style="left:45%;top:31%">1</span><span class="i3__n" style="left:26.5%;top:61%">2</span><span class="i3__n" style="left:45%;top:77%">3</span><span class="i3__n" style="left:95%;top:19%">4</span></div></div>
<ol class="i3__list"><li><span class="i3__nn">1</span><div><b>プロフィール</b><p>肩書き・ひとこと紹介。<wbr>匿名でも公開できます</p></div></li><li><span class="i3__nn">2</span><div><b>スコア</b><p>実績・学びの活動・<wbr>フォロワーの数</p></div></li><li><span class="i3__nn">3</span><div><b>ビジョン</b><p>何年後に、<wbr>何を実現したいか</p></div></li><li><span class="i3__nn">4</span><div><b>代表実績</b><p>いちばん見てほしい成果を大きく</p></div></li></ol>
</div>
<p class="hl-note">※画面・内容はイメージです。<wbr>ほかのユーザーのポートフォリオやフィードは、<wbr>無料登録後に見られます。</p>
</div></section>'''

# ── ⑥ はじめかた＋よくある質問
faq = [('匿名で公開できますか？', 'はい。表示名はニックネームにできます。作品ごとに「自分だけ」「会員のみ」「全体に公開」から公開範囲を選べ、投稿した直後は「自分だけ」です。'),
       ('費用はかかりますか？', 'ポートフォリオの登録は無料です。'),
       ('ほかの人のポートフォリオは見られますか？', '無料登録すると、公開ポートフォリオやフォロー中の人のフィードを見られます。'),
       ('受講前でも作れますか？', 'はい。無料登録だけで、受講前からポートフォリオを作れます。これまでの仕事や活動の実績、学びたいことを先にまとめておくと、受講後に成果物を足すだけで「受講前からの成長」が伝わるポートフォリオになります。'),
       ('企業の人事担当者も見られますか？', '公開範囲を「全体に公開」にした実績は、The Academy に登録していない方（企業の人事担当者を含む）も、URL から見られます。「自分だけ」「会員のみ」にした実績は見られません。')]
faq_html = ''.join(f'<details class="fq"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faq))
# ── ⑥ はじめかた：大きな番号を線でつなぎ、各ステップに操作の画面
def ic2(d,w=2): return f'<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{d}</g></svg>'
LOCK=ic2('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>'); PLUS3=ic2('<path d="M12 5v14M5 12h14"/>',2.2)
HEART3=ic2('<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>'); SHARE3=ic2('<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 11l7.6-4M8.2 13l7.6 4"/>')
GLOBE=ic2('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'); CHECK=ic2('<path d="m5 12 5 5 9-10"/>',2.6)
STEPS=[('01','登録する','匿名で始められます。'),('02','ポートフォリオを育てる','学びや実績を、<wbr>少しずつ記録。'),('03','PRする・つながる','フォローやフィードで、<wbr>学びを共有。')]
UI1=f'''<div class="ui ui1"><p class="ui__t">無料で登録</p><div class="ui__f"><small>ニックネーム</small><span>@saki_mkt</span></div><div class="ui__f"><small>メールアドレス</small><span>name@example.com</span></div>
<div class="ui__sw"><span class="ui__tg"><i></i></span><b>{LOCK}匿名で公開する</b></div><span class="ui__btn">はじめる</span></div>'''
UI2=f'''<div class="ui ui2"><p class="ui__t">記録を追加</p><div class="ui__opt on"><span>{PLUS3}</span><div><b>実績</b><small>背景から成果まで</small></div></div><div class="ui__opt"><span>{PLUS3}</span><div><b>学びの記録</b><small>今日の気づき</small></div></div><div class="ui__opt"><span>{PLUS3}</span><div><b>資格・認定</b><small>取得した資格</small></div></div></div>'''
UI3=f'''<div class="ui ui3"><div class="ui__ph">{av(1,30)}<div><b>@saki_mkt</b><small>制作実績を共有しました</small></div></div><p class="ui__body">カフェのSNS企画をポートフォリオに公開しました。</p>
<div class="ui__acts"><span class="r">{HEART3}24</span><span>{SHARE3}シェア</span></div><div class="ui__notif">{av(4,22)}<small><b>@kento_side</b> がフォローしました</small></div></div>'''
UIS=[UI1,UI2,UI3]
start = f'''<section class="pp-start" id="start" aria-labelledby="start-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">HOW TO START</p><h2 class="sec-title" id="start-title">はじめかた</h2>
<p class="sec-lead">3ステップで、<wbr>今日から始められます。</p></div></header>
<ol class="j2">{''.join(f'<li><span class="j2__dot">{n}</span><h3>{t}</h3><p class="j2__d">{d}</p><div class="j2__v" aria-hidden="true">{UIS[i]}</div></li>' for i, (n, t, d) in enumerate(STEPS))}</ol>
<div class="fqw"><h3 class="fqw__h">よくある質問</h3><div class="fqw__l">{faq_html}</div></div>
</div></section>'''

# ── ⑦ 行動：3つの入口
doors = [('まずは見てみたい方', 'ポートフォリオの例を見る', 'どんなページになるか、<wbr>例で確かめられます。', '#sample', '見てみる', 'btn--white'),
         ('自分の歩みを残したい方', 'ポートフォリオを作る', '匿名でもOK。<wbr>学びの記録から始められます。', '#start', '無料で登録する', 'btn--primary'),
         ('載せる実績をつくりたい方', 'コースを探す', '仕事で使える成果物を、<wbr>コースで完成させます。', 'courses.html', 'コースを探す', 'btn--white')]
door_html = ''.join(f'<li class="dr{" dr--main" if c == "btn--primary" else ""}"><p class="dr__who">{w}</p><h3>{t}</h3><p>{d}</p><a class="btn {c}" href="{h}">{b}</a></li>' for w, t, d, h, b, c in doors)
act = f'''<section class="pp-act" id="next" aria-labelledby="act-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">YOUR FIRST STEP</p><h2 class="sec-title" id="act-title">あなたの努力を、<wbr>見える形に。</h2>
<p class="sec-lead">まずは例を見るところから。<wbr>次に、<wbr>あなた自身の歩みを残していきましょう。</p></div></header>
<ul class="drs">{door_html}</ul>
</div></section>'''

css = r'''
  /* ══ ポートフォリオ（/portfolio）══════════════ */
  .pp-why, .pp-alone, .pp-start { padding: clamp(64px, 7vw, 96px) 0; background: #fff; }
  .pp-show, .pp-act { padding: clamp(64px, 7vw, 96px) 0; background: var(--bg-gray, #F7F8FB); }
  .pp-sample { padding: clamp(64px, 7vw, 96px) 0; background: #EEF3FC; }
  .hl-note { margin: 18px 0 0; color: var(--ts-mid); font-size: 12px; }
  .pp-head .sec-kicker, .pp-head .phead__lead, .sec-lead { word-break: keep-all; overflow-wrap: anywhere; }
  .pp-why .sec-title, .pp-show .sec-title, .pp-alone .sec-title, .pp-sample .sec-title, .pp-start .sec-title, .pp-act .sec-title, .pp-head .phead__t { word-break: keep-all; overflow-wrap: anywhere; }
  /* 共通の画面（ウィンドウ）とプロフィール */
  .pw { position: relative; border-radius: 16px; background: #fff; box-shadow: 0 1px 2px rgba(15,27,69,.05), 0 24px 56px rgba(15,27,69,.12); color: var(--ink); overflow: hidden; }
  .pw__bar { display: flex; align-items: center; gap: 6px; height: 34px; padding: 0 14px; border-bottom: 1px solid #EEF0F5; color: var(--ts-mid); font-size: 11.5px; }
  .pw__bar i { width: 9px; height: 9px; border-radius: 50%; background: #E3E7EF; } .pw__bar span { margin-left: 8px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
  .pp-prof { display: flex; align-items: center; gap: 10px; }
  .pp-prof b { display: block; font-size: 14px; } .pp-prof small { display: block; color: var(--ts-mid); font-size: 11.5px; }
  .pp-av { display: grid; place-items: center; flex: none; width: 42px; height: 42px; border-radius: 50%; background: linear-gradient(135deg, #6F97F7, #0141D4); color: #fff; font-size: 11px; font-weight: 700; }
  .pp-prof--l .pp-av { width: 52px; height: 52px; font-size: 12px; } .pp-prof--l b { font-size: 16px; }
  .pp-fol { margin-left: auto; padding: 5px 12px; border-radius: 99px; background: var(--ts-primary); color: #fff; font-size: 11.5px; font-weight: 700; white-space: nowrap; }
  .pp-fol--s { padding: 3px 9px; background: #EAF0FF; color: var(--ts-primary); font-size: 10.5px; }
  .pp-tags { display: flex; flex-wrap: wrap; gap: 6px; } .pp-tags span { padding: 3px 10px; border-radius: 99px; background: #F1F4FA; color: var(--ink); font-size: 11.5px; font-weight: 700; }
  .pp-stats { display: grid; grid-template-columns: repeat(3, 1fr); margin: 18px 0 0; padding: 14px 0 0; border-top: 1px solid #EEF0F5; list-style: none; text-align: center; color: var(--ts-mid); font-size: 11.5px; }
  .pp-stats b { display: block; color: var(--ink); font-size: 20px; }
  .sh-lab { margin: 16px 0 6px; color: var(--ts-mid); font-size: 11px; font-weight: 700; letter-spacing: .1em; }
  .sh-ic { display: grid; place-items: center; flex: none; width: 44px; height: 44px; border-radius: 12px; background: #EAF0FF; color: var(--ts-primary); }
  .sh-ic svg, .vs li span svg, .pp-note svg, .pp-cta__ic svg, .sh-v1__foot svg, .sh-v2__bk svg, .fd-post__r svg, .pv__w small svg, .pv__badge span svg { width: 22px; height: 22px; }
  /* ① 見出し */
  .pp-head { padding-bottom: clamp(48px, 6vw, 80px); overflow: hidden; }
  .pp-head__grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr); gap: clamp(32px, 5vw, 72px); align-items: center; }
  .pp-head__k { margin: 22px 0 0; }
  .pp-head .phead__t { margin-top: 8px; font-size: clamp(32px, 4.2vw, 48px); line-height: 1.3; }
  .pp-cta { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; } .pp-cta .btn { min-width: 0; padding: 0 26px; }
  .pp-cta__ic { display: inline-grid; } .pp-cta__ic svg { width: 18px; height: 18px; }
  .pp-note { display: flex; align-items: center; gap: 6px; margin: 14px 0 0; color: var(--ts-mid); font-size: 13px; } .pp-note svg { width: 16px; height: 16px; }
  /* 実際の公開ポートフォリオ画面の部品を浮かべる */
  .pv { position: relative; height: 480px; }
  .pq { position: absolute; border-radius: 12px; background: #fff; overflow: hidden; box-shadow: 0 1px 2px rgba(15,27,69,.05), 0 20px 48px rgba(15,27,69,.14); }
  .pq img { display: block; width: 100%; height: auto; }
  .pv__prof { left: 0; top: 70px; width: 64%; z-index: 2; padding: 6px 4px 2px; }
  .pv__feat { right: 0; top: 0; width: 42%; z-index: 3; }
  .pv__cert { right: 0; bottom: 0; width: 46%; z-index: 4; }
  .pv__road { left: 6%; bottom: 10px; width: 40%; z-index: 3; padding: 4px 6px; }
  .pv__lab { position: absolute; z-index: 5; padding: 4px 11px; border-radius: 99px; background: var(--ts-primary); color: #fff; font-size: 11.5px; font-weight: 700; white-space: nowrap; box-shadow: 0 6px 14px rgba(1,65,212,.25); }
  .pv__lab--o { background: #E46A1F; box-shadow: 0 6px 14px rgba(228,106,31,.25); }
  .pv__l1 { right: 30%; top: -8px; } .pv__l2 { right: 4%; bottom: 128px; } .pv__l3 { left: 2%; bottom: 112px; }
  /* ② WHY */
  .vs { display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); align-items: stretch; gap: 0; }
  .vs__p { padding: 28px 32px; border-radius: 24px; }
  .vs__p--now { background: #F4F5F8; } .vs__p--hide { background: #EAF0FF; box-shadow: inset 0 0 0 2px var(--ts-primary); }
  .vs__h { margin: 0 0 16px; font-size: 18px; font-weight: 700; } .vs__p--now .vs__h { color: var(--ts-mid); } .vs__p--hide .vs__h { color: var(--ts-primary); }
  .vs ul { display: grid; gap: 12px; margin: 0; padding: 0; list-style: none; }
  .vs li { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border-radius: 14px; background: #fff; font-size: 16px; font-weight: 700; }
  .vs li span { display: grid; place-items: center; width: 38px; height: 38px; border-radius: 10px; background: #F1F3F7; color: var(--ts-mid); }
  .vs__p--now li { color: var(--ts-mid); } .vs__p--hide li span { background: #EAF0FF; color: var(--ts-primary); }
  .vs__mid { align-self: center; z-index: 1; display: grid; place-items: center; width: 64px; height: 64px; margin: 0 -14px; border-radius: 50%; background: var(--ink); color: #fff; font: 800 18px/1 'Helvetica Neue', Arial, sans-serif; letter-spacing: .04em; box-shadow: 0 0 0 6px #fff; }
  /* WHY：評価の物差し（目盛り＋3つの時代）*/
  .r1__ruler { position: relative; height: 92px; margin: 34px 0 18px; }
  .r1__ticks { position: absolute; left: 0; right: 0; bottom: 0; height: 58px; overflow: hidden; border-radius: 14px; background: linear-gradient(90deg, #EEF1F6 0%, #DCE6FD 55%, #C9D8FB 100%); box-shadow: inset 0 0 0 1px #D8E0F0; }
  .r1__ticks i { position: absolute; bottom: 10px; width: 1.5px; height: 12px; background: #A9B6D3; transform: translateX(-50%); } .r1__ticks i.l { height: 24px; background: #7F8DB0; }
  .r1__ticks i.p { bottom: 0; width: 2px; height: 58px; background: #9AA8C8; } .r1__ticks i.on { width: 3px; background: var(--ts-primary); }
  .r1__name { position: absolute; left: 16px; bottom: 34px; color: var(--ts-mid); font-size: 11px; font-weight: 700; letter-spacing: .14em; }
  .r1__pin { position: absolute; top: 0; transform: translateX(-50%); padding: 5px 14px; border-radius: 99px; background: #fff; color: var(--ts-mid); font-size: 13px; font-weight: 800; letter-spacing: .1em; box-shadow: 0 6px 16px rgba(15,27,69,.1); }
  .r1__pin::after { content: ""; position: absolute; left: 50%; top: 100%; width: 2px; height: 10px; background: #9AA8C8; transform: translateX(-50%); }
  .r1__pin--on { background: var(--ts-primary); color: #fff; box-shadow: 0 8px 18px rgba(1,65,212,.3); } .r1__pin--on::after { background: var(--ts-primary); width: 3px; }
  .r1__cols { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin: 0; padding: 0; list-style: none; }
  .r1__cols > li { position: relative; padding: 24px; border-radius: 22px; background: #fff; box-shadow: 0 0 0 1px #fff, 0 2px 4px rgba(15,27,69,.04), 0 12px 32px rgba(15,27,69,.08); }
  .r1__cols > li.on { background: #fff; box-shadow: 0 0 0 2px var(--ts-primary), 0 24px 48px rgba(1,65,212,.14); }
  .r1__cols > li:not(:last-child)::after { content: ""; position: absolute; right: -16px; top: 54px; z-index: 1; width: 13px; height: 13px; border-top: 4px solid #7F8DB0; border-right: 4px solid #7F8DB0; border-radius: 2px; transform: rotate(45deg); }
  .r1__k { margin: 0; color: #9AA8C8; font: 800 12px/1 'Helvetica Neue', Arial, sans-serif; letter-spacing: .2em; } .on .r1__k { color: var(--ts-primary); }
  .r1__cols h3 { margin: 8px 0 16px; color: var(--ts-mid); font-size: 21px; line-height: 1.4; } .on h3 { color: var(--ink); }
  .r1__cols ul { display: grid; gap: 8px; margin: 0; padding: 0; list-style: none; }
  .r1__cols ul li { display: flex; align-items: center; gap: 10px; padding: 11px 13px; border-radius: 13px; background: #F4F6FA; color: var(--ts-mid); font-size: 15px; font-weight: 700; }
  .r1__cols ul li span { display: grid; place-items: center; width: 32px; height: 32px; border-radius: 9px; background: #fff; } .r1__cols svg { width: 18px; height: 18px; }
  .on ul li { background: #F3F6FE; color: var(--ink); } .on ul li span { background: #fff; color: var(--ts-primary); }
  .r1__n { margin: 16px 0 0; color: var(--ts-mid); font-size: 13.5px; font-weight: 700; line-height: 1.7; }
  .r1__warn { display: flex; align-items: center; gap: 8px; margin: 14px 0 0; padding: 9px 12px; border-radius: 12px; background: #FFF1E7; color: #E46A1F; font-size: 13.5px; font-weight: 700; } .r1__warn span { display: inline-grid; } .r1__warn svg { width: 18px; height: 18px; }

  .r1__k span { display: none; }
  .vs__so { display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 4px 12px; margin: 28px 0 0; padding: 18px 24px; border-radius: 99px; background: var(--ts-primary); color: #fff; font-size: 18px; font-weight: 700; text-align: center; }
  .vs__so span { padding: 2px 12px; border-radius: 99px; background: rgba(255,255,255,.18); font-size: 13px; }
  .pfor { display: grid; grid-template-columns: auto 1fr 1fr; gap: 20px; align-items: stretch; margin-top: clamp(40px, 5vw, 56px); }
  .pfor__h { align-self: center; margin: 0; padding-right: 8px; color: var(--ink); font-size: 18px; font-weight: 700; writing-mode: horizontal-tb; }
  .pfor__c { display: flex; gap: 16px; align-items: flex-start; padding: 22px 24px; border-radius: 20px; box-shadow: 0 0 0 1px var(--line); }
  .pfor__c .avt { flex: none; } .pfor__c h3 { margin: 0; color: var(--ink); font-size: 17px; word-break: keep-all; overflow-wrap: anywhere; } .pfor__c p { margin: 6px 0 0; color: var(--ts-mid); font-size: 13.5px; line-height: 1.8; word-break: keep-all; overflow-wrap: anywhere; }
  /* ③ 伝えられること：実画面のタイル */
  .g2__h { display: flex; align-items: baseline; gap: 12px; margin: 0 0 16px; color: var(--ink); font-size: 22px; font-weight: 700; word-break: keep-all; overflow-wrap: anywhere; }
  .g2__h span { color: var(--ts-primary); font: 800 15px/1 'Helvetica Neue', Arial, sans-serif; letter-spacing: .14em; }
  .g2__grid { display: grid; gap: 18px; } .g2__grid--a { margin-bottom: 48px; grid-template-columns: 1fr 1.25fr; } .g2__t--big { grid-row: span 2; }
  .g2__grid--b { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .g2__t { padding: 16px 16px 20px; border-radius: 20px; background: #fff; box-shadow: 0 0 0 1px var(--line); }
  .g2__img { display: grid; place-items: center; height: 170px; padding: 12px; border-radius: 12px; background: linear-gradient(160deg, #F4F7FE, #E3EAFB); overflow: hidden; }
  .g2__img img { display: block; max-width: 100%; max-height: 100%; width: auto; height: auto; border-radius: 6px; box-shadow: 0 8px 20px rgba(15,27,69,.1); }
  .g2__grid--b .g2__img img { width: 100%; max-height: none; } .g2__grid--b .g2__t--fit .g2__img img { width: auto; max-height: 100%; }
  .g2__t--big .g2__img { height: 420px; }
  .g2__cap { margin: 12px 0 0; color: var(--ink); font-size: 16px; font-weight: 700; } .g2__cap small { display: block; margin-top: 2px; color: var(--ts-mid); font-size: 13.5px; font-weight: 500; line-height: 1.7; word-break: keep-all; overflow-wrap: anywhere; }
  /* ④ ひとりじゃない：文章を上、フィード画面を横幅いっぱいに */
  .pp-alone__grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: 40px; }
  .pp-alone .sec-head { margin-bottom: 28px; }
  .al-list { display: grid; gap: 14px; margin: 0; padding: 0; list-style: none; }
  .al-list li { display: flex; gap: 14px; padding: 18px 20px; border-radius: 18px; background: var(--bg-gray, #F7F8FB); }
  .al-list b { display: block; font-size: 16px; } .al-list p { margin: 3px 0 0; color: var(--ts-mid); font-size: 14px; line-height: 1.75; word-break: keep-all; overflow-wrap: anywhere; }
  .pp-alone .al-list { grid-template-columns: repeat(3, minmax(0, 1fr)); }

  .fx { position: relative; color: var(--ink); font-size: 12px; }
  .fx b, .fx p { margin: 0; }
  .fx-card { border-radius: 12px; background: #fff; box-shadow: 0 0 0 1px #E3E7EF; padding: 14px 16px; }
  .fx-ch { font-size: 13px; font-weight: 700; margin-bottom: 8px !important; }
  .fx-trend ol { margin: 0; padding: 0; list-style: none; } .fx-trend li { display: grid; grid-template-columns: 1fr auto; padding: 6px 0; } .fx-trend small { grid-column: 1 / -1; color: var(--ts-mid); font-size: 10.5px; } .fx-trend b { font-size: 12px; } .fx-trend em { font-style: normal; color: var(--ts-mid); font-size: 11px; }
  .fx-u { display: flex; align-items: center; gap: 8px; padding: 6px 0; } .fx-u b { display: block; font-size: 12.5px; } .fx-u small { display: block; color: var(--ts-mid); font-size: 10.5px; }
  .fx-u .fx-plus, .fx-u .fx-on { margin-left: auto; } .fx-plus { display: grid; place-items: center; width: 22px; height: 16px; border-radius: 99px; box-shadow: inset 0 0 0 1.5px var(--ts-primary); color: var(--ts-primary); } .fx-plus svg { width: 11px; height: 11px; } .fx-on { color: var(--ts-mid); font-size: 10.5px; }
  .fx-main { border-radius: 12px; background: #fff; box-shadow: 0 0 0 1px #E3E7EF; overflow: hidden; }
  .fx-top { display: flex; gap: 8px; padding: 12px 12px 0; } .fx-search { flex: 1; display: flex; align-items: center; gap: 8px; padding: 9px 12px; border-radius: 8px; background: #F4F6FA; box-shadow: inset 0 0 0 1px #E3E7EF; color: #8C97B5; font-size: 12px; } .fx-search svg { width: 15px; height: 15px; }
  .fx-new { display: inline-flex; align-items: center; gap: 4px; padding: 0 14px; border-radius: 8px; background: var(--ts-primary); color: #fff; font-size: 12px; font-weight: 700; } .fx-new svg { width: 13px; height: 13px; }
  .fx-tabs { display: grid; grid-template-columns: repeat(4, 1fr); margin: 10px 0 0; padding: 0 6px; list-style: none; border-bottom: 1px solid #E3E7EF; }
  .fx-tabs li { display: flex; align-items: center; justify-content: center; gap: 5px; padding: 10px 0; color: var(--ink); font-size: 12px; font-weight: 700; } .fx-tabs li.on { color: var(--ts-primary); background: #F4F7FE; border-radius: 8px 8px 0 0; } .fx-tabs svg { width: 14px; height: 14px; }
  .fx-post { display: grid; grid-template-columns: 44px 1fr; gap: 10px; padding: 14px; border-bottom: 1px solid #EEF0F5; } .fx-post:last-child { border-bottom: 0; }
  .fx-av { position: relative; width: 40px; height: 40px; } .fx-av .avt { width: 40px; height: 40px; } .fx-av i { position: absolute; right: -3px; bottom: -3px; display: grid; place-items: center; width: 16px; height: 16px; border-radius: 50%; background: #fff; box-shadow: 0 0 0 1px #C9D1E3; font-style: normal; font-size: 11px; line-height: 1; }
  .fx-h { display: block; font-size: 14px; text-decoration: underline; text-underline-offset: 2px; } .fx-role { display: block; color: var(--ink); font-size: 12px; } .fx-act { display: block; color: var(--ts-mid); font-size: 11px; }
  .fx-tag { display: inline-block; margin: 6px 0; padding: 2px 8px; border-radius: 6px; background: #F1F3F7; font-size: 11px; font-weight: 700; }
  .fx-pb p { font-size: 12.5px; line-height: 1.6; }
  .fx-img { margin-top: 8px; border-radius: 8px; overflow: hidden; box-shadow: 0 0 0 1px #E3E7EF; } .fx-img img { display: block; width: 100%; height: 130px; object-fit: cover; }
  .fx-acts { display: flex; gap: 16px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #EEF0F5; color: var(--ink); font-size: 11.5px; font-weight: 700; } .fx-acts span { display: inline-flex; align-items: center; gap: 4px; } .fx-acts svg { width: 14px; height: 14px; }
  .fx-bar { display: flex; align-items: center; justify-content: space-between; height: 40px; padding: 0 16px; border-bottom: 1px solid #EEF0F5; background: #fff; font-size: 14px; font-weight: 700; }
  .fx-lv { display: flex; align-items: center; gap: 10px; color: var(--ts-primary); font-size: 12px; } .fx-lv i { width: 120px; height: 5px; border-radius: 99px; background: linear-gradient(90deg, var(--ts-primary) 25%, #E6EBF5 25%); }

  .h1__win { width: 100%; border-radius: 16px; background: #F7F8FB; overflow: hidden; box-shadow: 0 1px 2px rgba(15,27,69,.05), 0 24px 56px rgba(15,27,69,.14); }
  .h2__g { display: grid; grid-template-columns: 0.8fr 1.4fr 0.95fr; gap: 14px; align-items: start; padding: 16px; } .h2__r { display: grid; gap: 14px; } .h2__mini { padding: 0; overflow: hidden; } .h2__mini .fx-post { padding: 12px; }
  .fx-img img { height: 200px; }
  .h2__lab { position: absolute; z-index: 3; padding: 5px 12px; border-radius: 99px; background: var(--ts-primary); color: #fff; font-size: 12px; font-weight: 700; box-shadow: 0 6px 14px rgba(1,65,212,.25); }
  .h2__l1 { right: 3%; top: 34px; } .h2__l2 { left: 32%; top: 34px; } .h2__l3 { right: 3%; top: 282px; }

  /* ⑤ 例 */
  .smp { border-radius: 24px; }
  .smp__grid { display: grid; grid-template-columns: 300px minmax(0, 1fr); }
  .smp__side { padding: 28px; border-right: 1px solid #EEF0F5; } .smp__vis { margin: 0; font-size: 14px; font-weight: 700; line-height: 1.7; }
  .smp__side .sh-lab:first-of-type { margin-top: 22px; }
  .smp__main { padding: 28px 32px; }
  .smp__fol { display: block; margin: 18px 0 0; padding: 10px; border-radius: 10px; text-align: center; font-size: 13px; }
  .pp-sample .todo, .pp-start .todo { display: inline-block; margin-left: 4px; padding: 1px 8px; border-radius: 6px; background: #FFF1E7; color: #E46A1F; font-size: 12px; font-weight: 700; }
  .smp__work { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.1fr); gap: 24px; align-items: start; }
  .smp__work h3 { margin: 0 0 12px; color: var(--ink); font-size: 18px; }
  .smp__story div { grid-template-columns: 96px 1fr; padding: 9px 12px; font-size: 13px; }
  .smp__dash { padding: 14px; border-radius: 14px; background: #0F1B45; color: #fff; }
  .smp__dash p { margin: 0 0 10px; font-size: 12px; font-weight: 700; }
  .smp__kpi { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; } .smp__kpi span { padding: 8px; border-radius: 8px; background: rgba(255,255,255,.08); }
  .smp__kpi small { display: block; color: #A9B6DA; font-size: 10px; } .smp__kpi b { display: block; font-size: 14px; } .smp__kpi em { font-style: normal; color: #7EE2A8; font-size: 10.5px; font-weight: 700; }
  .smp__chart { display: flex; align-items: flex-end; gap: 6px; height: 110px; margin-top: 12px; padding: 0 2px; border-bottom: 1px solid rgba(255,255,255,.2); }
  .smp__chart i { flex: 1; height: var(--h); border-radius: 4px 4px 0 0; background: linear-gradient(#6F97F7, #3E78FE); } .smp__chart i:last-child { background: linear-gradient(#FFB27E, #F76B38); }
  .smp__tl { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 0; padding: 0; list-style: none; }
  .smp__tl li { position: relative; padding: 14px; border-radius: 14px; background: #F6F8FB; font-size: 13px; font-weight: 700; line-height: 1.5; }
  .smp__tl li.now { background: #FFF6EF; box-shadow: inset 0 0 0 1.5px #F4B48A; }
  .smp__tl time { display: block; margin-bottom: 6px; color: var(--ts-mid); font-size: 11.5px; }
  .tg { display: inline-block; margin-right: 6px; padding: 1px 7px; border-radius: 6px; background: #EAF0FF; color: var(--ts-primary); font-size: 10.5px; vertical-align: 1px; }
  .tg--c { background: #E9F7F0; color: #1E9E62; } .tg--w { background: #FFF1E7; color: #E46A1F; }
  /* ⑤ 例：実画面に番号の注釈 */
  .i3 { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 40px; align-items: center; }
  .i3__win { border-radius: 16px; } .i3__shot { position: relative; } .i3__shot img { display: block; width: 100%; height: auto; }
  .i3__n, .i3__nn { display: grid; place-items: center; width: 30px; height: 30px; border-radius: 50%; background: #E46A1F; color: #fff; font: 800 14px/1 'Helvetica Neue', Arial, sans-serif; box-shadow: 0 0 0 4px rgba(228,106,31,.2); }
  .i3__n { position: absolute; z-index: 2; transform: translate(-50%, -50%); }
  .i3__list { display: grid; gap: 14px; margin: 0; padding: 0; list-style: none; }
  .i3__list li { display: flex; gap: 12px; padding: 16px; border-radius: 16px; background: #fff; box-shadow: 0 0 0 1px var(--line); } .i3__nn { flex: none; }
  .i3__list b { display: block; font-size: 16px; } .i3__list p { margin: 3px 0 0; color: var(--ts-mid); font-size: 13.5px; line-height: 1.7; word-break: keep-all; overflow-wrap: anywhere; }
  /* ⑥ はじめかた・FAQ */
  /* はじめかた：大きな番号を線でつなぐ */
  .ui { padding: 14px 16px; border-radius: 14px; background: #fff; box-shadow: 0 1px 2px rgba(15,27,69,.05), 0 14px 32px rgba(15,27,69,.12); font-size: 12px; color: var(--ink); }
  .ui svg { width: 14px; height: 14px; } .ui b, .ui p { margin: 0; }
  .ui__t { margin-bottom: 10px !important; font-size: 13px; font-weight: 700; }
  .ui__f { margin-bottom: 8px; } .ui__f small { display: block; color: var(--ts-mid); font-size: 10.5px; } .ui__f span { display: block; margin-top: 3px; padding: 7px 10px; border-radius: 8px; box-shadow: inset 0 0 0 1px #DDE3EE; }
  .ui__sw { display: flex; align-items: center; gap: 8px; margin: 10px 0; } .ui__sw b { display: inline-flex; align-items: center; gap: 4px; font-size: 12px; }
  .ui__tg { position: relative; width: 32px; height: 18px; border-radius: 99px; background: var(--ts-primary); } .ui__tg i { position: absolute; right: 2px; top: 2px; width: 14px; height: 14px; border-radius: 50%; background: #fff; }
  .ui__btn { display: block; padding: 8px; border-radius: 8px; background: var(--ts-primary); color: #fff; font-weight: 700; text-align: center; }
  .ui__opt { display: flex; align-items: center; gap: 10px; margin-top: 6px; padding: 8px 10px; border-radius: 10px; box-shadow: inset 0 0 0 1px #E3E7EF; } .ui__opt.on { box-shadow: inset 0 0 0 2px var(--ts-primary); background: #F4F7FE; }
  .ui__opt span { display: grid; place-items: center; width: 26px; height: 26px; border-radius: 8px; background: #EAF0FF; color: var(--ts-primary); } .ui__opt b { display: block; font-size: 12.5px; } .ui__opt small { display: block; color: var(--ts-mid); font-size: 10.5px; }
  .ui__ph { display: flex; align-items: center; gap: 8px; } .ui__ph b { display: block; font-size: 12.5px; } .ui__ph small { display: block; color: var(--ts-mid); font-size: 10.5px; }
  .ui__body { margin: 8px 0 !important; line-height: 1.6; }
  .ui__acts { display: flex; gap: 14px; padding-top: 8px; border-top: 1px solid #EEF0F5; font-weight: 700; } .ui__acts span { display: inline-flex; align-items: center; gap: 4px; } .ui__acts .r { color: #E5486B; }
  .ui__notif { display: flex; align-items: center; gap: 6px; margin-top: 10px; padding: 7px 9px; border-radius: 10px; background: #FFF6EF; } .ui__notif small { font-size: 11px; }

  .j2 { position: relative; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 40px; margin: 0; padding: 0; list-style: none; }
  .j2::before { content: ""; position: absolute; left: 32px; right: calc(33.3% - 32px); top: 31px; height: 3px; background: repeating-linear-gradient(90deg, var(--ts-primary) 0 10px, transparent 10px 18px); }
  .j2 li { position: relative; }
  .j2__dot { position: relative; z-index: 1; display: grid; place-items: center; width: 64px; height: 64px; border-radius: 50%; background: var(--ts-primary); color: #fff; font: 800 22px/1 'Helvetica Neue', Arial, sans-serif; box-shadow: 0 0 0 8px #fff, 0 10px 24px rgba(1,65,212,.3); }
  li:last-child .j2__dot { background: #E46A1F; box-shadow: 0 0 0 8px #fff, 0 10px 24px rgba(228,106,31,.3); }
  .j2 h3 { margin: 20px 0 0; color: var(--ink); font-size: 22px; } .j2__d { margin: 4px 0 16px; color: var(--ts-mid); font-size: 14.5px; }
  .j2__v { padding: 18px; border-radius: 18px; background: #F4F6FA; }

  .st3 { position: relative; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin: 0; padding: 0; list-style: none; counter-reset: s; }
  .st3 li { position: relative; padding: 26px 26px 28px; border-radius: 22px; background: var(--bg-gray, #F7F8FB); }
  .st3 li:not(:last-child)::after { content: ""; position: absolute; right: -16px; top: 50%; z-index: 1; width: 12px; height: 12px; border-top: 2.5px solid var(--ts-primary); border-right: 2.5px solid var(--ts-primary); transform: translateY(-50%) rotate(45deg); }
  .st3__n { position: absolute; right: 22px; top: 18px; margin: 0; color: #D6DEEF; font: 800 44px/1 'Helvetica Neue', Arial, sans-serif; }
  .st3 h3 { margin: 16px 0 0; color: var(--ink); font-size: 19px; } .st3 li > p:last-child { margin: 6px 0 0; color: var(--ts-mid); font-size: 14px; line-height: 1.75; }
  .fqw { display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 32px; margin-top: clamp(48px, 6vw, 72px); padding-top: clamp(40px, 5vw, 56px); border-top: 1px solid var(--line); }
  .fqw__h { margin: 0; color: var(--ink); font-size: 22px; }
  .fq { border-bottom: 1px solid var(--line); } .fq:first-child { border-top: 1px solid var(--line); }
  .fq summary { position: relative; padding: 18px 40px 18px 34px; color: var(--ink); font-size: 15.5px; font-weight: 700; cursor: pointer; list-style: none; }
  .fq summary::-webkit-details-marker { display: none; }
  .fq summary::before { content: "Q"; position: absolute; left: 0; top: 17px; color: var(--ts-primary); font: 800 17px/1.3 'Helvetica Neue', Arial, sans-serif; }
  .fq summary::after { content: ""; position: absolute; right: 8px; top: 50%; width: 9px; height: 9px; border-right: 2px solid var(--ts-mid); border-bottom: 2px solid var(--ts-mid); transform: translateY(-70%) rotate(45deg); transition: transform .2s; }
  .fq[open] summary::after { transform: translateY(-30%) rotate(-135deg); }
  .fq p { margin: 0; padding: 0 0 20px 34px; color: var(--ts-mid); font-size: 14.5px; line-height: 1.8; }
  /* ⑦ 行動 */
  .drs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin: 0; padding: 0; list-style: none; }
  .dr { display: flex; flex-direction: column; padding: 28px; border-radius: 22px; background: #fff; box-shadow: 0 0 0 1px var(--line); }
  .dr--main { box-shadow: 0 0 0 2px var(--ts-primary), 0 18px 40px rgba(1,65,212,.12); }
  .dr__who { margin: 0; color: var(--ts-primary); font-size: 12.5px; font-weight: 700; }
  .dr h3 { margin: 8px 0 0; color: var(--ink); font-size: 20px; } .dr h3 + p { flex: 1; margin: 8px 0 20px; color: var(--ts-mid); font-size: 14px; line-height: 1.8; }
  .dr .btn { min-width: 0; width: 100%; } .dr .btn--white { box-shadow: 0 0 0 1.5px var(--ts-primary); color: var(--ts-primary); }
  /* レスポンシブ */
  @media (max-width: 1100px) {
    .pp-head__grid, .pp-alone__grid { grid-template-columns: minmax(0, 1fr); }
    .pv { max-width: 640px; }
    .pp-alone .al-list { grid-template-columns: minmax(0, 1fr); } .j2 { gap: 24px; } .j2 h3 { font-size: 19px; } .h2__g { grid-template-columns: 1.4fr 1fr; } .h2__g > .fx-trend { display: none; } .h2__lab { display: none; }
    .g2__grid--a { grid-template-columns: minmax(0, 1fr); } .g2__t--big { grid-row: auto; } .g2__t--big .g2__img { height: auto; }
    .i3 { grid-template-columns: minmax(0, 1fr); gap: 24px; } .i3__list { grid-template-columns: 1fr 1fr; }
    .pfor { grid-template-columns: 1fr 1fr; } .pfor__h { grid-column: 1 / -1; }
    .r1__cols h3 { font-size: 19px; }
  }
  @media (max-width: 760px) {
    .vs { grid-template-columns: minmax(0, 1fr); } .vs__mid { justify-self: center; margin: -14px 0; }
    .r1__ruler { display: none; } .r1__cols { grid-template-columns: minmax(0, 1fr); gap: 28px; } .r1__cols > li:not(:last-child)::after { right: 50%; top: auto; bottom: -20px; transform: translateX(50%) rotate(135deg); }
    .r1__k span { display: inline; margin-left: 8px; font-family: inherit; letter-spacing: .1em; } .r1__cols h3 br { display: none; }
    .vs__p { padding: 22px; } .vs__so { border-radius: 20px; font-size: 16px; }
    .pfor { grid-template-columns: minmax(0, 1fr); }
    .i3__list { grid-template-columns: minmax(0, 1fr); gap: 10px; } .i3__list li { padding: 12px 14px; } .i3__n { width: 22px; height: 22px; font-size: 11px; box-shadow: 0 0 0 3px rgba(228,106,31,.2); }
    .j2 { grid-template-columns: minmax(0, 1fr); gap: 36px; } .j2::before { display: none; } .j2 li:not(:last-child)::after { content: ""; position: absolute; left: 31px; top: 72px; bottom: -28px; width: 3px; background: repeating-linear-gradient(180deg, var(--ts-primary) 0 10px, transparent 10px 18px); } .j2 li { padding-left: 84px; } .j2__dot { position: absolute; left: 0; top: 0; } .j2 h3 { margin-top: 14px; }
    .st3, .drs { grid-template-columns: minmax(0, 1fr); } .st3 li:not(:last-child)::after { right: 50%; top: auto; bottom: -16px; transform: translateX(50%) rotate(135deg); }
    .fqw { grid-template-columns: minmax(0, 1fr); gap: 16px; }
    .g2__grid--b { grid-template-columns: minmax(0, 1fr); } .g2__img { height: auto; min-height: 110px; } .g2__h { font-size: 19px; }
    .pv { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; height: auto; } .pq { position: relative; left: auto; right: auto; top: auto; bottom: auto; width: auto; } .pv__prof { grid-column: 1 / -1; } .pv__feat, .pv__cert { align-self: start; } .pv__road, .pv__lab { display: none; }
    .al-list p { word-break: normal; line-break: strict; }
    .h2__g { grid-template-columns: minmax(0, 1fr); padding: 10px; } .h2__r .fx-follow { display: none; } .fx-img img { height: 150px; }
    .pp-cta .btn { width: 100%; }
  }
'''

html = (head + base_css + css
        + between.replace('<a href="portfolio.html">ポートフォリオ</a>', '<a href="portfolio.html" aria-current="page">ポートフォリオ</a>')
        + '<main>\n' + pagehead + why + show + alone + sample + start + act + '\n' + footer_on)
html = re.sub(r'<title>[^<]*</title>', '<title>ポートフォリオ | The Academy</title>', html, count=1)
open(OUT, 'w').write(html)
print('ok', len(html))
