# 学び方・受講成果（/how-to-learn）ページを、LPの共通部品と「コースを探す」の部品（ページ見出し・迷ったら）から組み立てる
import os, tempfile
S = os.path.dirname(os.path.abspath(__file__))          # このスクリプトのフォルダ（lp/scripts）
LPDIR = os.path.dirname(S)                              # 出力先（lp）
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')  # 共通部品を取り出すときの捨て出力
import os, re, sys
os.environ['TA_COURSES_OUT'] = TMP_COURSES
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)       # 共通部品を取り出す（出力は一時ファイル）
head, between, footer_on, nx2, ARROW, lp = g['head'], g['between'], g['footer_on'], g['nx2'], g['ARROW'], g['s']
base_css = g['css']                                # .phead・.cnext など「コースを探す」で作った下層ページ共通のスタイル
OUT = os.path.join(LPDIR, 'how-to-learn.html')

def ic(d, w=1.9): return f'<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{d}</g></svg>'
avatars = re.findall(r'<svg class="avt".*?</svg>', lp, re.S)   # LP 05 のキャラクターのアイコン
av = lambda i, size=30: re.sub(r'width="\d+" height="\d+"', f'width="{size}" height="{size}"', avatars[i % len(avatars)], count=1)

# ── ① LEARNING OUTCOMES：成果物6つ（各カードに成果物の画面イメージ）
M = {
 'strategy': '''<div class="om om--sheet"><p class="om__t">マーケティング戦略シート</p><div class="om__g2"><div><b>市場</b><i></i><i class="s"></i></div><div><b>顧客</b><i></i><i class="s"></i></div><div><b>競合</b><i></i><i class="s"></i></div><div class="on"><b>戦略</b><i></i><i class="s"></i></div></div></div>''',
 'sns': '''<div class="om om--sns"><span style="--c:#F7A072">春の<br>キャンペーン</span><span style="--c:#6F97F7">新メニュー<br>登場</span><span style="--c:#7CC49A">お客様の<br>声</span><span style="--c:#FFD66B">週末<br>イベント</span></div>''',
 'prompt': '''<div class="om om--prompt"><p class="om__t">議事録まとめ用プロンプト<span>テンプレート</span></p><p class="om__pl"><b>#役割</b> あなたは営業チームの書記です。</p><p class="om__pl"><b>#入力</b> <em>{会議メモ}</em> を貼り付け</p><p class="om__pl"><b>#出力</b> 決定事項・宿題・期限を表に</p><div class="om__ai"><i>AI</i><span>決定事項3件・宿題4件を整理しました</span></div></div>''',
 'brand': '''<div class="om om--brand"><div class="om__logo">Hana<small>coffee</small></div><div class="om__sw"><i style="--c:#3B2A22"></i><i style="--c:#E9D8C4"></i><i style="--c:#7CC49A"></i></div><p>「毎朝の、小さなご褒美。」</p></div>''',
 'event': '''<div class="om om--event"><p class="om__t">当日の進行表</p><ol><li><time>13:00</time>受付・オープニング</li><li><time>13:20</time>ワークショップ</li><li class="on"><time>14:30</time>交流タイム</li><li><time>15:30</time>クロージング</li></ol></div>''',
 'eng': '''<div class="om om--slide"><div class="om__slide"><p>My Work in 5 Minutes</p><i></i><i class="s"></i><span>01 / 05</span></div><div class="om__time">05:00</div></div>''',
}
OUTS = [
 ('strategy', 'マーケティング', '#E46A1F', '#FFF1E7', 'マーケティング戦略', '市場分析から戦略立案までを、一枚の戦略シートに。'),
 ('sns', 'クリエイティブ', '#D9467A', '#FDECF2', 'CanvaでSNS投稿デザイン', '伝えたいことが届く、SNS投稿のデザインセット。'),
 ('prompt', 'IT・デジタル', '#1E9E62', '#E9F7F0', 'AIプロンプト', '毎日の業務で繰り返し使える、<wbr>AIへの指示のテンプレート集。'),
 ('brand', 'マーケティング', '#E46A1F', '#FFF1E7', 'ブランドコンセプト設計', '顧客に選ばれる理由を、言葉とビジュアルに。'),
 ('event', 'ビジネス', '#6B4FD8', '#F0ECFF', 'イベント運営計画', '目的から当日の進行までをつなぐ実施計画。'),
 ('eng', '英語・TOEIC', '#0141D4', '#EAF0FF', '英語プレゼンテーション', '自分の仕事を英語で伝える、5分間のプレゼン。'),
]
IMG = {'strategy': ('assets/outcomes/marketing-strategy.webp', 'マーケティング戦略の資料（重点顧客と提供価値、SNSを起点とした顧客獲得の設計）'),
       'sns': ('assets/outcomes/sns-design.webp', 'カフェのInstagramカルーセル投稿。4枚の写真と帯がつながるデザイン'),
       'prompt': ('assets/outcomes/ai-prompt.webp', '議事録まとめ用プロンプトと、AIが会議メモから整理した決定事項・宿題の表'),
       'brand': ('assets/outcomes/brand-concept.webp', '架空の家具ブランドのコンセプト設計。ブランドの土台、写真とタグライン、配色、書体、トーン'),
       'event': ('assets/outcomes/event-plan.webp', '架空イベントの運営計画。開催までの準備工程表と、当日の進行・キューシート'),
       'eng': ('assets/outcomes/english-presentation.webp', 'イベントプロデューサーとしての仕事を紹介する、5分間の英語プレゼン資料3枚')}
def ov(k):
    if k in IMG: return f'<div class="oc__v oc__v--img"><img src="{IMG[k][0]}" alt="作例：{IMG[k][1]}" loading="lazy"><span class="oc__ex">作例</span></div>'
    return f'<div class="oc__v">{M[k]}</div>'
outs = ''.join(f'<li class="oc">{ov(k)}<div class="oc__b"><span class="oc__cat" style="--cc:{col};--cb:{bg}">{cat}</span><h3>{t}</h3><p>{d}</p></div></li>'
               for k, cat, col, bg, t, d in OUTS)
outcomes = f'''<section class="hl-out" id="outcomes" aria-labelledby="out-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">LEARNING OUTCOMES</p><h2 class="sec-title" id="out-title">できるようになったことが、<wbr>自信になる。</h2>
<p class="sec-lead">課題を終えることではなく、<wbr>仕事で使えるものを完成させること。<wbr>コースでつくる成果物の作例をご紹介します。</p></div>
<a class="sec-more" href="courses.html">コースを探す<span class="sec-more__arrow">{ARROW}</span></a></header>
<ul class="ocs">{outs}</ul>
<p class="hl-note">※画像はすべて作例です。実際の成果物はコースによって異なります。</p>
</div></section>'''

# ── ② HOW IT WORKS：知る→試す→形にする→共有する（01〜03が「学ぶ」、04が「残す」）
STEPS = [
 ('知る', '短い講義と事例から、考え方と基本を理解します。', ic('<path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H11v15H5.5A1.5 1.5 0 0 1 4 17.5z"/><path d="M20 5.5A1.5 1.5 0 0 0 18.5 4H13v15h5.5a1.5 1.5 0 0 0 1.5-1.5z"/>'), '<span class="hs__tag">動画・事例</span>'),
 ('試す', '自分の仕事や興味に置き換え、小さく手を動かします。', ic('<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13.5 6.5l4 4"/>'), '<span class="hs__tag">ワーク・課題</span>'),
 ('形にする', 'コースの内容を理解した上で、伝わる形に整えます。', ic('<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5M12 12v9M12 12L4 7.5"/>'), '<span class="hs__tag">資格</span><span class="hs__tag">ポートフォリオ</span><span class="hs__tag">テンプレート</span>'),
 ('共有する', '制作の背景や過程も学習ポートフォリオに残し、人と仕事の機会へつなげます。', ic('<circle cx="18" cy="5.5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="18.5" r="2.5"/><path d="M8.2 10.8l7.6-4M8.2 13.2l7.6 4"/>'), '<a class="hs__link" href="/portfolio">ポートフォリオを見る' + ARROW + '</a>'),
]
steps = ''.join(f'<li class="hs{" hs--share" if i == 3 else ""}"><div class="hs__top"><span class="hs__n">0{i+1}</span><span class="hs__ic">{svg}</span></div><h3>{t}</h3><p>{d}</p><div class="hs__tags">{tags}</div></li>'
                for i, (t, d, svg, tags) in enumerate(STEPS))
how = f'''<section class="hl-how" id="how" aria-labelledby="how-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">HOW IT WORKS</p><h2 class="sec-title" id="how-title">学びを、<wbr>次の機会までつなぐ。</h2>
<p class="sec-lead">4つのステップで、<wbr>学んだことを「使える成果」にして、<wbr>次の機会へつなげます。</p></div></header>
<div class="hsg"><div class="hsg__lab"><span class="hsg__learn">学ぶ</span><span class="hsg__keep">残す</span></div><ol class="hss">{steps}</ol></div>
</div></section>'''

# ── ③ KEEP GOING：続けられる3つの理由（それぞれ画面イメージつき）
week = ''.join(f'<li class="{c}"><b>{d}</b><i></i></li>' for d, c in (('月', ''), ('火', 'on'), ('水', ''), ('木', 'on'), ('金', ''), ('土', 'on2'), ('日', '')))
k1 = f'''<div class="kv kv--week"><p class="kv__t">今週の学習プラン<span>計 2h</span></p><ol>{week}</ol><p class="kv__lg"><i class="on"></i>平日夜 30分<i class="on2"></i>週末 60分</p></div>'''
k2 = '''<div class="kv kv--prog"><p class="kv__t">マイラーニング</p><div class="kv__c"><img src="assets/photos/sns-phone.webp" alt=""><div><b>SNSマーケティング実践</b><small>第4章 運用と数値の見方</small><span><em style="width:62%"></em></span></div><strong>62%</strong></div><p class="kv__go">続きから学ぶ ›</p></div>'''
k3 = f'''<div class="kv kv--feed"><div class="kv__post">{av(0)}<div><b>ゆい</b><small>2時間前</small><p>企画書の構成を見直しました！<br>フィードバックうれしい☺️</p><span class="kv__like">♥ 12</span></div></div><div class="kv__post">{av(3)}<div><b>りょう</b><small>昨日</small><p>今週は平日夜に30分ずつ進めた📷</p></div></div></div>'''
KEEPS = [
 ('忙しくても、続けられる設計', '週2h〜。平日夜と週末に分けて、無理なく進められます。', k1),
 ('進捗が見える', 'マイラーニングで、どこまで進んだか・続きはどこかがひと目で分かります。', k2),
 ('ひとりにしない', 'フォローしている仲間の学習投稿から、勉強の進め方のヒントが見つかります。仲間の歩みが、続けるモチベーションに。', k3),
]
keeps = ''.join(f'<li class="kc"><div class="kc__v">{v}</div><div class="kc__b"><p class="kc__n">0{i+1}</p><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d, v) in enumerate(KEEPS))
keep = f'''<section class="hl-keep" id="keep" aria-labelledby="keep-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">KEEP GOING</p><h2 class="sec-title" id="keep-title">学びを、<wbr>続けられる仕組み。</h2>
<p class="sec-lead">「続けられるか不安」に、<wbr>3つの仕組みで応えます。</p></div></header>
<ul class="kcs">{keeps}</ul>
</div></section>'''


# ── ② 学び方はC案（1つの成果ができるまでを4ステップの画面で追う）。③ 続けられる仕組みはA案（カード3枚）
STORY = [
 ('知る', '短い講義と事例で、考え方と基本をつかむ。', '<img src="assets/how/step-01-learn.webp" alt="オンライン受講の画面。SNSマーケティング入門 第2章「顧客を知る」の講義動画とチャプター一覧" loading="lazy">'),
 ('試す', '自分の仕事に置き換えて、小さく手を動かす。', '<img src="assets/how/step-02-try.webp" alt="顧客理解のワークシート。カフェを例に、誰に・どんな価値・どんな行動につなげるかを書き込む" loading="lazy">'),
 ('形にする', '伝わる形に整えて、使える1本を仕上げる。', '<img src="assets/how/step-03-make.webp" alt="デザインツールの編集画面。カフェのInstagramカルーセル投稿4枚を、写真と帯がつながるように仕上げている" loading="lazy">'),
 ('共有する', '背景や過程もポートフォリオに残し、次の機会へ。', '<img src="assets/how/step-04-share.webp" alt="仕上げたカフェのカルーセル投稿と、ポートフォリオで実績を公開した通知（いいね24件・コメント5件・講師コメントあり）" loading="lazy">'),
]
st = ''.join(f'<li class="hw{" hw--keep" if i == 3 else ""}"><div class="hw__v">{v}</div><p class="hw__n">STEP 0{i+1}</p><h3>{t}</h3><p>{d}</p></li>' for i, (t, d, v) in enumerate(STORY))
how = f"""<section class="hl-how" id="how" aria-labelledby="how-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">HOW IT WORKS</p><h2 class="sec-title" id="how-title">学びを、<wbr>次の機会までつなぐ。</h2>
<p class="sec-lead">例：<wbr>カフェのSNSキャンペーンを<wbr>企画した受講生の3か月。<wbr>知る → 試す → 形にする → 共有する の順に、<wbr>ひとつの成果ができるまで。</p></div></header>
<ol class="hws">{st}</ol></div></section>"""

pagehead = '''<section class="phead" aria-labelledby="page-title"><div class="wrap">
<nav class="crumb" aria-label="パンくずリスト"><a href="lp-design.html">トップ</a><span aria-hidden="true">/</span><span aria-current="page">学び方・受講成果</span></nav>
<h1 class="phead__t" id="page-title">学び方・受講成果</h1>
<p class="phead__lead">忙しくても、仕事で使える成果物を完成させる。<wbr>その成果と、学びの仕組みをご紹介します。</p>
<ul class="phead__jump"><li><a href="#outcomes">受講成果</a></li><li><a href="#how">学び方</a></li><li><a href="#keep">続けられる仕組み</a></li><li><a href="#next">迷ったら</a></li></ul>
</div></section>'''

css = r'''
  /* ══ 学び方・受講成果（/how-to-learn）══════════════ */
  .hl-out, .hl-keep { padding: clamp(64px, 7vw, 96px) 0; background: #fff; }
  .hl-how { padding: clamp(64px, 7vw, 96px) 0; background: var(--bg-gray, #F7F8FB); }
  .hl-note { margin: 18px 0 0; color: var(--ts-mid); font-size: 12px; }
  /* 成果物 */
  .ocs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin: 0; padding: 0; list-style: none; }
  .oc { display: flex; flex-direction: column; border-radius: 20px; background: #fff; box-shadow: 0 0 0 1px var(--line); overflow: hidden; }
  .oc__v { display: grid; place-items: center; height: 200px; padding: 20px; background: linear-gradient(160deg, #F7F9FE 0%, #E6EDFD 100%); overflow: hidden; }
  .oc__b { padding: 20px 22px 22px; }
  .oc__v--img { position: relative; padding: 0; } .oc__ex { position: absolute; right: 10px; top: 10px; padding: 2px 9px; border-radius: 4px; background: rgba(15,27,69,.78); color: #fff; font-size: 11px; font-weight: 700; letter-spacing: .06em; } .oc__v--img img { display: block; width: 100%; height: 100%; object-fit: contain; }
  .oc__cat { display: inline-block; padding: 2px 10px; border-radius: 99px; background: var(--cb); color: var(--cc); font-size: 11.5px; font-weight: 700; }
  .oc h3 { margin: 10px 0 0; color: var(--ink); font-size: 17px; }
  .oc__b p { word-break: keep-all; overflow-wrap: anywhere; margin: 6px 0 0; color: var(--ts-mid); font-size: 13.5px; line-height: 1.75; }
  .om { width: 100%; max-width: 280px; padding: 14px; border-radius: 12px; background: #fff; box-shadow: 0 10px 24px rgba(15,27,69,.10); font-size: 11px; color: var(--ink); }
  .om__t { margin: 0 0 10px; font-weight: 700; font-size: 11.5px; }
  .om i { display: block; height: 5px; margin-top: 5px; border-radius: 99px; background: #DCE3F0; } .om i.s { width: 60%; }
  .om__g2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .om__g2 div { padding: 8px; border-radius: 8px; background: #F4F6FA; } .om__g2 b { font-size: 10.5px; }
  .om__g2 .on { background: #FFF1E7; box-shadow: inset 0 0 0 1.5px #F29A57; } .om__g2 .on b { color: #E46A1F; }
  .om--sns { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; max-width: 220px; padding: 10px; }
  .om--sns span { display: grid; place-items: center; aspect-ratio: 1; border-radius: 8px; background: var(--c); color: #fff; font-weight: 800; font-size: 11px; line-height: 1.35; text-align: center; }
  .om__ch { margin: 0 0 8px; padding-bottom: 6px; border-bottom: 1px solid var(--line); font-weight: 700; }
  .om__msg { display: flex; gap: 6px; align-items: center; margin-top: 6px; } .om__msg span { display: grid; place-items: center; width: 20px; height: 20px; border-radius: 5px; background: var(--a); color: #fff; font-weight: 800; font-size: 10px; } .om__msg p { margin: 0; } .om__msg em { font-style: normal; font-weight: 700; color: var(--ts-primary); }
  .om__gantt { display: grid; gap: 4px; margin-top: 10px; padding: 8px; border-radius: 8px; background: #F4F6FA; } .om__gantt i { height: 6px; margin: 0 0 0 var(--s); width: var(--w); background: #6F97F7; } .om__gantt i.late { background: #F29A57; }
  .om__t span { margin-left: 6px; padding: 1px 6px; border-radius: 4px; background: #E9F7F0; color: #1E9E62; font-size: 9.5px; }
  .om__pl { margin: 5px 0 0; padding: 5px 8px; border-radius: 6px; background: #F4F6FA; font-family: ui-monospace, Menlo, monospace; font-size: 10px; line-height: 1.5; }
  .om__pl b { color: #1E9E62; } .om__pl em { font-style: normal; padding: 0 3px; border-radius: 3px; background: #FFF1E7; color: #E46A1F; }
  .om__ai { display: flex; align-items: center; gap: 6px; margin-top: 8px; padding: 6px 8px; border-radius: 8px; box-shadow: inset 0 0 0 1px #BFE6D0; font-size: 10px; font-weight: 700; }
  .om__ai i { display: grid; place-items: center; width: 18px; height: 18px; border-radius: 5px; background: #1E9E62; color: #fff; font-style: normal; font-size: 8.5px; }
  .om--brand { display: grid; justify-items: center; gap: 10px; text-align: center; }
  .om__logo { font: 800 22px/1 Georgia, serif; color: #3B2A22; } .om__logo small { display: block; margin-top: 3px; font: 700 9px/1 var(--font); letter-spacing: .3em; color: #7A6A5C; }
  .om__sw { display: flex; gap: 6px; } .om__sw i { width: 22px; height: 22px; margin: 0; border-radius: 50%; background: var(--c); box-shadow: 0 0 0 1px var(--line); }
  .om--brand p { margin: 0; font-weight: 700; font-size: 11.5px; }
  .om--event ol { display: grid; gap: 6px; margin: 0; padding: 0; list-style: none; }
  .om--event li { display: flex; gap: 8px; padding: 5px 8px; border-radius: 6px; background: #F4F6FA; } .om--event time { color: var(--ts-mid); font-variant-numeric: tabular-nums; } .om--event li.on { background: #F0ECFF; color: #6B4FD8; font-weight: 700; }
  .om--slide { position: relative; max-width: 250px; padding: 10px; background: #0F1B45; }
  .om__slide { position: relative; aspect-ratio: 16 / 9; padding: 14px; border-radius: 6px; background: #fff; } .om__slide p { margin: 0; font: 800 13px/1.2 'Helvetica Neue', Arial, sans-serif; color: var(--ts-primary); } .om__slide i { width: 70%; } .om__slide span { position: absolute; right: 10px; bottom: 8px; color: var(--ts-mid); font-size: 9px; }
  .om__time { position: absolute; right: -8px; top: -10px; padding: 3px 9px; border-radius: 99px; background: #F29A57; color: #fff; font-weight: 800; font-size: 10.5px; font-variant-numeric: tabular-nums; }
  /* 学び方の4ステップ */
  .hsg__lab { display: grid; grid-template-columns: 3fr 1fr; gap: 16px; margin-bottom: 12px; }
  .hsg__lab span { display: block; padding-bottom: 8px; border-bottom: 2px solid; font-size: 13px; font-weight: 700; letter-spacing: .1em; text-align: center; }
  .hsg__learn { color: var(--ts-primary); border-color: var(--ts-primary) !important; } .hsg__keep { color: #E46A1F; border-color: #F29A57 !important; }
  .hss { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin: 0; padding: 0; list-style: none; counter-reset: s; }
  .hs { position: relative; display: flex; flex-direction: column; padding: 22px 22px 24px; border-radius: 20px; background: #fff; box-shadow: var(--shadow-soft); }
  .hs:not(:last-child)::after { content: ""; position: absolute; right: -13px; top: 42px; z-index: 1; width: 10px; height: 10px; border-top: 2px solid var(--ts-primary); border-right: 2px solid var(--ts-primary); transform: rotate(45deg); }
  .hs__top { display: flex; align-items: center; justify-content: space-between; }
  .hs__n { color: var(--ts-primary); font: 800 28px/1 'Helvetica Neue', Arial, sans-serif; }
  .hs__ic { display: grid; place-items: center; width: 44px; height: 44px; border-radius: 14px; background: var(--tint-08); color: var(--ts-primary); } .hs__ic svg { width: 22px; height: 22px; }
  .hs--share .hs__n { color: #E46A1F; } .hs--share .hs__ic { background: #FFF1E7; color: #E46A1F; }
  .hs h3 { margin: 16px 0 0; color: var(--ink); font-size: 19px; }
  .hs > p { margin: 8px 0 0; color: var(--ts-mid); font-size: 13.5px; line-height: 1.8; }
  .hs__tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: auto; padding-top: 16px; }
  .hs__tag { padding: 3px 10px; border-radius: 99px; background: var(--bg-gray, #F4F6FA); color: var(--ink); font-size: 11.5px; font-weight: 700; }
  .hs__link { display: inline-flex; align-items: center; gap: 6px; color: #E46A1F; font-size: 13.5px; font-weight: 700; text-decoration: none; } .hs__link .ico { width: 15px; height: 15px; }
  /* 続けられる仕組み */
  .kcs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin: 0; padding: 0; list-style: none; }
  .kc { display: flex; flex-direction: column; border-radius: 20px; background: #fff; box-shadow: 0 0 0 1px var(--line); overflow: hidden; }
  .kc__v { display: grid; place-items: center; height: 210px; padding: 20px; background: linear-gradient(160deg, #F7F9FE 0%, #E6EDFD 100%); }
  .kc__b { padding: 20px 24px 24px; }
  .kc__n { margin: 0; color: var(--ts-primary); font-size: 12px; font-weight: 700; letter-spacing: .15em; }
  .kc h3 { margin: 6px 0 0; color: var(--ink); font-size: 18px; }
  .kc__b > p:last-child { margin: 8px 0 0; color: var(--ts-mid); font-size: 13.5px; line-height: 1.8; }
  .kv { width: 100%; max-width: 290px; padding: 14px; border-radius: 14px; background: #fff; box-shadow: 0 10px 24px rgba(15,27,69,.10); font-size: 11px; color: var(--ink); }
  .kv__t { display: flex; justify-content: space-between; margin: 0 0 10px; font-weight: 700; font-size: 12px; } .kv__t span { color: var(--ts-primary); }
  .kv--week ol { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; margin: 0; padding: 0; list-style: none; }
  .kv--week li { display: grid; justify-items: center; gap: 5px; } .kv--week b { color: var(--ts-mid); font-size: 10px; }
  .kv--week li i { width: 100%; height: 44px; border-radius: 6px; background: #F1F3F8; } .kv--week li.on i { background: linear-gradient(#F1F3F8 0 55%, #6F97F7 55%); } .kv--week li.on2 i { background: linear-gradient(#F1F3F8 0 15%, #0141D4 15%); }
  .kv__lg { display: flex; align-items: center; gap: 5px; margin: 10px 0 0; color: var(--ts-mid); font-size: 10px; } .kv__lg i { width: 9px; height: 9px; border-radius: 3px; background: #6F97F7; } .kv__lg i.on2 { margin-left: 8px; background: #0141D4; }
  .kv__c { display: grid; grid-template-columns: 52px minmax(0, 1fr) auto; gap: 10px; align-items: center; padding: 10px; border-radius: 10px; box-shadow: inset 0 0 0 1px var(--line); }
  .kv__c img { width: 52px; height: 40px; border-radius: 6px; object-fit: cover; } .kv__c b { display: block; font-size: 11px; } .kv__c small { color: var(--ts-mid); font-size: 9.5px; }
  .kv__c span { display: block; height: 5px; margin-top: 6px; border-radius: 99px; background: #E6EAF2; } .kv__c em { display: block; height: 100%; border-radius: 99px; background: var(--ts-primary); }
  .kv__c strong { color: var(--ts-primary); font-size: 13px; }
  .kv__go { margin: 10px 0 0; text-align: right; color: var(--ts-primary); font-weight: 700; }
  .kv--feed { display: grid; gap: 10px; }
  .kv__post { display: flex; gap: 8px; } .kv__post .avt { flex: none; } .kv__post b { font-size: 11px; } .kv__post small { margin-left: 6px; color: var(--ts-mid); font-size: 9.5px; }
  .kv__post p { margin: 3px 0 0; padding: 7px 10px; border-radius: 4px 12px 12px 12px; background: #F4F6FA; line-height: 1.5; }
  .kv__like { display: inline-block; margin-top: 4px; color: #E4572E; font-size: 10px; font-weight: 700; }
  .hl-next.next { background: var(--bg-gray, #F7F8FB); }
  /* 学び方：ひとつの成果ができるまで（C案） */
  /* 学び方：上に1本の時間の流れ（線と丸）を通し、4つの画面を並べる */
  .hws { position: relative; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 24px; margin: 0; padding: 44px 0 0; list-style: none; }
  .hws::before { content: ""; position: absolute; left: 12px; right: 12px; top: 11px; height: 2px; background: linear-gradient(90deg, var(--ts-primary) 72%, #E46A1F 80%); }
  .hw { position: relative; }
  .hw::before { content: ""; position: absolute; left: 4px; top: -41px; width: 18px; height: 18px; border-radius: 50%; background: #fff; box-shadow: inset 0 0 0 4px var(--ts-primary); }
  .hw--keep::before { box-shadow: inset 0 0 0 4px #E46A1F; }
  .hw__v { height: 190px; overflow: hidden; border-radius: 16px; } .hw__v img { display: block; width: 100%; height: 100%; object-fit: contain; }
  .hw__n { margin: 16px 0 0; color: var(--ts-primary); font-size: 12px; font-weight: 800; letter-spacing: .12em; } .hw--keep .hw__n { color: #E46A1F; }
  .hw h3 { margin: 4px 0 0; color: var(--ink); font-size: 19px; } .hw > p:last-child { margin: 6px 0 0; color: var(--ts-mid); font-size: 13.5px; line-height: 1.8; }
  .om--video { position: relative; padding: 0 0 12px; overflow: hidden; } .om__play { height: 90px; background: linear-gradient(135deg, #0141D4, #6F97F7); } .om__play::after { content: "▶"; position: absolute; left: 50%; top: 45px; transform: translate(-50%, -50%); display: grid; place-items: center; width: 34px; height: 34px; border-radius: 50%; background: #fff; color: var(--ts-primary); font-size: 12px; }
  .om--video p { margin: 8px 12px 0; font-weight: 700; } .om--video span { display: block; height: 4px; margin: 8px 12px 0; border-radius: 99px; background: #E6EAF2; } .om--video em { display: block; height: 100%; border-radius: 99px; background: var(--ts-primary); } .om--video small { display: block; margin: 4px 12px 0; color: var(--ts-mid); font-size: 9.5px; }
  .om__q { margin-top: 6px; padding: 7px 9px; border-radius: 8px; background: #F4F6FA; } .om__q b { display: block; font-size: 10px; color: var(--ts-mid); } .om__q span { font-weight: 700; }
  .om__pill { display: inline-block; padding: 2px 9px; border-radius: 99px; background: var(--ts-primary); color: #fff; font-size: 10px; font-weight: 700; } .om__pt { margin: 8px 0 0; font-weight: 700; font-size: 12.5px; } .om__react { margin-top: 8px; color: var(--ts-mid); }
  @media (max-width: 900px) { .hws { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 36px; padding-top: 0; } .hws::before, .hw::before { display: none; } }
  @media (max-width: 640px) { .hws { grid-template-columns: minmax(0, 1fr); } .hw__v { height: auto; aspect-ratio: 566 / 400; } }
  .hl-how .sec-title, .hl-keep .sec-title { word-break: keep-all; overflow-wrap: anywhere; }
  @media (max-width: 1100px) { .ocs, .kcs { grid-template-columns: repeat(2, minmax(0, 1fr)); } .hss { grid-template-columns: repeat(2, minmax(0, 1fr)); } .hs:nth-child(2)::after { display: none; } .hsg__lab { display: none; } }
  @media (max-width: 640px) {
    .ocs, .kcs, .hss { grid-template-columns: minmax(0, 1fr); }
    .hs:not(:last-child)::after { right: auto; left: 34px; top: auto; bottom: -13px; transform: rotate(135deg); }
    .hs:nth-child(2)::after { display: block; }
    .oc__v { height: auto; min-height: 180px; }
    .om--sns { max-width: 200px; }
  }
  /* 成果物：画像左・文字右の横長カードを2列（P5） */
  .ocs { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px 24px; }
  .oc { flex-direction: row; } .oc__v { flex: 0 0 52%; height: 210px; } .oc__b { align-self: center; }
  @media (max-width: 1100px) and (min-width: 901px) { .oc { flex-direction: column; } .oc__v { flex: none; height: 200px; } .oc__b { align-self: stretch; } }
  @media (max-width: 900px) { .ocs { grid-template-columns: minmax(0, 1fr); } }
  @media (max-width: 640px) { .oc { flex-direction: column; } .oc__v { flex: none; height: auto; min-height: 0; aspect-ratio: 40 / 21; } .oc__b { align-self: stretch; } }
  /* 続けられる仕組み：淡い青の面に白カード */
  .hl-keep { background: #EEF3FC; }
  .hl-keep .kc { box-shadow: 0 0 0 1px #DCE5F6; }
'''

nx3 = nx2.replace('class="next nxC cnext"', 'class="next nxC cnext hl-next"')
html = (head + base_css + css
        + between.replace('<a href="how-to-learn.html">学び方・受講成果</a>', '<a href="how-to-learn.html" aria-current="page">学び方・受講成果</a>')
        + '<main>\n' + pagehead + outcomes + how + keep + nx3 + '\n' + footer_on)
html = re.sub(r'<title>[^<]*</title>', '<title>学び方・受講成果 | The Academy</title>', html, count=1)
open(OUT, 'w').write(html)
print('ok', len(html))
