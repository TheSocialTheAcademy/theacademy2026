# 数字の根拠（evidence）：トップのヒーローにある3つの数字（平均満足度4.2・実践コース10+・週2h〜）の調べ方と時点（E1：レーダー型）
# アンケートの値・回答数・期間・自由回答は 2026年8月の受講生アンケート（2026-10-08 に確定版を反映）
# 受講生の声のアイコンは lp/assets/avatars/ の SVG をそのまま埋め込む（色はブランドの青）
import os, re, math, tempfile
S = os.path.dirname(os.path.abspath(__file__))          # このスクリプトのフォルダ（lp/scripts）
LPDIR = os.path.dirname(S)                              # 出力先（lp）
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')  # 共通部品を取り出すときの捨て出力
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)
head, between, footer_on, base_css = g['head'], g['between'], g['footer_on'], g['css']

def load(name):
    t = open(os.path.join(LPDIR, 'assets', 'avatars', name)).read()
    t = re.sub(r'<title>.*?</title>', '', t)
    t = re.sub(r' id="[^"]*"', '', t).replace(' xmlns="http://www.w3.org/2000/svg" d=', ' d=')
    return t.replace('width="512" height="512" ', 'aria-hidden="true" focusable="false" ')
SVGS = {'young_f': load('youthful-female.svg'), 'young_m': load('youthful-male.svg'), 'mature_f': load('mature-female.svg')}
def avatar(kind): return f'<span class="ev-av">{SVGS[kind]}</span>'

TODO = lambda t='仮の数字': f'<span class="x-todo">{t}</span>'
# ── 満足度アンケート（2026年8月） ──
ITEMS = [  # (項目, 質問文, 平均)
 ('内容の分かりやすさ', '動画や教材の説明は分かりやすかったですか？', 4.3),
 ('実務で使える', '学んだことを、仕事や活動で使えそうですか？', 4.4),
 ('続けやすさ', '忙しい中でも、無理なく続けられましたか？', 4.0),
 ('成果物づくり', '自分の成果物（ポートフォリオ）をつくれましたか？', 3.9),
 ('サポート', 'スタッフの案内や質問への対応に満足しましたか？', 4.0),
]
TOTAL = 4.2

def radar(items, size=440):
    cx = cy = size / 2; R = size / 2 - 78; n = len(items)
    ang = [-math.pi / 2 + 2 * math.pi * i / n for i in range(n)]
    pt = lambda a, r: (cx + r * math.cos(a), cy + r * math.sin(a))
    g = ''
    for lv in range(1, 6):  # 1〜5 の目盛り（中心は 0）
        pts = ' '.join('%.1f,%.1f' % pt(a, R * lv / 5) for a in ang)
        g += f'<polygon points="{pts}" class="rd-grid{" rd-grid--o" if lv == 5 else ""}"/>'
    for a in ang:
        x, y = pt(a, R); g += f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" class="rd-axis"/>'
    for lv in (1, 2, 3, 4, 5):
        x, y = pt(ang[0], R * lv / 5); g += f'<text x="{x + 6:.1f}" y="{y + 4:.1f}" class="rd-tick">{lv}</text>'
    pts = ' '.join('%.1f,%.1f' % pt(a, R * v / 5) for a, (_, _, v) in zip(ang, items))
    g += f'<polygon points="{pts}" class="rd-area"/>'
    for a, (lab, _, v) in zip(ang, items):
        x, y = pt(a, R * v / 5); g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" class="rd-dot"/>'
        lx, ly = pt(a, R + 34); anc = 'middle' if abs(math.cos(a)) < .3 else ('start' if math.cos(a) > 0 else 'end')
        g += f'<text x="{lx:.1f}" y="{ly - 4:.1f}" text-anchor="{anc}" class="rd-lab">{lab}</text><text x="{lx:.1f}" y="{ly + 15:.1f}" text-anchor="{anc}" class="rd-val">{v:.1f}</text>'
    return f'<svg viewBox="0 0 {size} {size}" class="rd" role="img" aria-label="満足度の項目別平均（5段階）：' + '、'.join(f'{l} {v}' for l, _, v in items) + f'">{g}</svg>'

SURVEY = [  # 調査の概要（項目と仮の値）
 ('調査名', 'The Academy 受講生アンケート'),
 ('実施期間', '2026年8月1日〜8月31日'),
 ('対象', '受講を始めて4週間以上たった受講生（修了した人を含む）'),
 ('方法', 'オンラインアンケート（匿名・任意回答）'),
 ('回答数', '48名（回答率 62％）'),
 ('評価の方法', '5段階（5：とても満足 〜 1：不満）。平均値は小数第2位を四捨五入'),
 ('「平均満足度4.2」', '「総合的に、The Academy に満足していますか？」への回答の平均'),
 ('調査・集計', 'The Academy 運営事務局（The Social株式会社）'),
 ('次回の更新', '半年ごと（次回は2027年2月の予定）'),
]
COURSES = [('IT・デジタル', 4), ('マーケティング', 3), ('英語・TOEIC', 2), ('ビジネス', 2), ('クリエイティブ', 1)]
COUNT = [
 ('時点', '2026年10月1日'),
 ('数えるもの', '販売中の有料コース（コースを探すに掲載しているもの）'),
 ('数えないもの', '無料の講座・セミナー、販売を終えたコース、業務ツール（Slack×GAS タスク管理システムなど）'),
]
WEEK = [
 ('意味', 'コースの学習の目安で、いちばん少ない週の時間が「週2時間」'),
 ('根拠', '各コースのページにある「週の時間」（例：生成AI 業務改善 週2時間、イベントデザイン 週2時間、SNSマーケティング実践 週2〜3時間）'),
 ('注意', 'かかる時間は、学ぶ人の経験や進め方によって変わります'),
]
def dl(rows): return '<table class="ev-t"><tbody>' + ''.join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows) + '</tbody></table>'
mx = max(n for _, n in COURSES)
bars = ''.join(f'<li><span class="ev-b__l">{c}</span><span class="ev-b__t"><i style="width:{n / mx * 100:.0f}%"></i></span><b>{n}</b></li>' for c, n in COURSES)
rows = ''.join(f'<tr><th scope="row">{l}</th><td>{q}</td><td class="num">{v:.1f}</td></tr>' for l, q, v in ITEMS)
VOICES = [('young_f', '@mio', '受講3か月', '動画のあとに手を動かす課題があるので、仕事でそのまま使えました。'),
          ('young_m', '@kento', '受講2か月', '週2時間でも進められる量に分かれていて、途中でやめずに済みました。'),
          ('mature_f', '@yuko', '受講4か月', '子育てと両立しながら、ポートフォリオに載せられる形まで仕上げられました。')]
voices = ''.join(f'<figure class="ev-v">{avatar(c)}<blockquote>{t}</blockquote><figcaption><b>{n}</b>{m}</figcaption></figure>' for c, n, m, t in VOICES)

PAGE = f'''<section class="phead" aria-labelledby="page-title"><div class="wrap"><nav class="crumb" aria-label="パンくずリスト"><a href="lp-design.html">トップ</a><span aria-hidden="true">/</span><span aria-current="page">数字の根拠</span></nav>
<h1 class="phead__t" id="page-title">数字の根拠</h1><p class="phead__lead">トップページに載せている3つの数字について、<wbr>調べ方と時点をまとめています。</p>
<ul class="ev-jump" aria-label="数字ごとの説明へ移動"><li><a href="#sat"><b>4.2</b>平均満足度</a></li><li><a href="#course"><b>10+</b>実践コース</a></li><li><a href="#week"><b>週2h〜</b>続けやすい設計</a></li></ul></div></section>

<section class="ev-sec ev-sec--w" id="sat"><div class="wrap">
<p class="ev-k">SATISFACTION</p><h2 class="ev-h">平均満足度 4.2 の根拠</h2>
<div class="ev-sat">
<div class="ev-sat__l"><p class="ev-big"><b>{TOTAL}</b><span>/ 5.0</span></p><p class="ev-cap">総合満足度の平均</p>
<ul class="ev-meta"><li><span>実施期間</span>2026年8月</li><li><span>回答数</span>48名</li><li><span>評価</span>5段階</li></ul>
<p class="ev-note">右のチャートは、総合満足度とは別に聞いた5つの項目の平均です。中心が0、外側の線が5です。</p></div>
<div class="ev-sat__r">{radar(ITEMS)}</div>
</div>
<h3 class="ev-h3">項目ごとの質問と平均</h3>
<div class="ev-tw"><table class="ev-q"><thead><tr><th>項目</th><th>質問</th><th class="num">平均</th></tr></thead><tbody>{rows}<tr class="ev-q__total"><th scope="row">総合満足度</th><td>総合的に、The Academy に満足していますか？</td><td class="num">{TOTAL:.1f}</td></tr></tbody></table></div>
<h3 class="ev-h3">調査の概要</h3>{dl(SURVEY)}
<h3 class="ev-h3">自由回答から（抜粋）</h3><div class="ev-vs">{voices}</div>
<p class="ev-note">名前は、本人の了承を得たニックネームです。</p>
</div></section>

<section class="ev-sec" id="course"><div class="wrap ev-two">
<div><p class="ev-k">COURSES</p><h2 class="ev-h">実践コース 10+ の数え方</h2><p class="ev-lead">2026年10月1日時点で、<b>12コース</b>を販売しています。</p>{dl(COUNT)}</div>
<div class="ev-card"><p class="ev-card__t">カテゴリ別のコース数</p><ul class="ev-b">{bars}</ul><p class="ev-note">合計12コース（2026年10月1日時点）</p></div>
</div></section>

<section class="ev-sec ev-sec--w" id="week"><div class="wrap">
<p class="ev-k">TIME</p><h2 class="ev-h">週2h〜 の意味</h2>{dl(WEEK)}
<p class="ev-upd">最終更新：2026年10月1日　数字は定期的に見直します。</p>
</div></section>'''

css = """
main{--p:#0141D4;--sub:#676688;--ln:rgba(15,27,69,.10);--bg:#F7F8FB;--or:#E46A1F}
main *{box-sizing:border-box}
.x-todo{display:inline-block;padding:1px 7px;border-radius:6px;background:#FFF1E7;color:var(--or);font-size:11px;font-weight:700;vertical-align:middle}
.ev-jump{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0 0;padding:0;list-style:none}
.ev-jump a{display:flex;align-items:baseline;gap:8px;padding:10px 16px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1px var(--ln);color:var(--sub);font-size:13px;font-weight:700;text-decoration:none}
.ev-jump b{color:var(--ink);font-size:20px;font-family:'Helvetica Neue',Arial,sans-serif}
.ev-sec{padding:clamp(56px,6vw,88px) 0;background:var(--bg)} .ev-sec--w{background:#fff}
.ev-k{margin:0;color:var(--p);font-size:12px;font-weight:700;letter-spacing:.14em} .ev-h{margin:6px 0 0;color:var(--ink);font-size:clamp(22px,2.6vw,28px);line-height:1.45}
.ev-h3{margin:44px 0 12px;color:var(--ink);font-size:17px} .ev-lead{margin:10px 0 0;color:var(--sub);font-size:15px} .ev-lead b{color:var(--ink)}
.ev-note{margin:12px 0 0;color:var(--sub);font-size:12.5px;line-height:1.7}
.ev-sat{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,480px);gap:48px;align-items:center;margin-top:28px;padding:clamp(24px,3vw,40px);border-radius:24px;background:var(--bg)}
.ev-big{display:flex;align-items:baseline;gap:8px;margin:0;color:var(--ink)} .ev-big b{font:800 clamp(64px,8vw,96px)/1 'Helvetica Neue',Arial,sans-serif;color:var(--p)} .ev-big span{color:var(--sub);font-size:20px;font-weight:700}
.ev-cap{margin:8px 0 0;color:var(--ink);font-size:15px;font-weight:700}
.ev-meta{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0;padding:0;list-style:none} .ev-meta li{padding:6px 12px;border-radius:99px;background:#fff;box-shadow:inset 0 0 0 1px var(--ln);color:var(--ink);font-size:13px;font-weight:700} .ev-meta span{margin-right:6px;color:var(--sub);font-weight:500}
.rd{display:block;width:100%;max-width:480px;height:auto;margin:0 auto;overflow:visible}
.rd-grid{fill:none;stroke:rgba(15,27,69,.12);stroke-width:1} .rd-grid--o{stroke:rgba(15,27,69,.28)} .rd-axis{stroke:rgba(15,27,69,.12)}
.rd-area{fill:rgba(1,65,212,.16);stroke:#0141D4;stroke-width:2.5;stroke-linejoin:round} .rd-dot{fill:#fff;stroke:#0141D4;stroke-width:2.5}
.rd-tick{fill:#8A8BA6;font-size:10px} .rd-lab{fill:#0F1B45;font-size:12.5px;font-weight:700} .rd-val{fill:#0141D4;font-size:14px;font-weight:800;font-family:'Helvetica Neue',Arial,sans-serif}
.ev-tw{overflow-x:auto}
.ev-q{width:100%;min-width:520px;border-collapse:collapse;font-size:14px} .ev-q th,.ev-q td{padding:12px 16px 12px 0;border-bottom:1px solid var(--ln);text-align:left;vertical-align:top;line-height:1.7}
.ev-q thead th{color:var(--sub);font-size:12px;font-weight:500} .ev-q tbody th{color:var(--ink);white-space:nowrap} .ev-q td{color:var(--sub)}
.ev-q .num{text-align:right;color:var(--ink);font-weight:800;font-variant-numeric:tabular-nums} .ev-q__total th,.ev-q__total td{border-top:1.5px solid var(--ink)} .ev-q__total .num{color:var(--p)}
.ev-t{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:16px} .ev-t th,.ev-t td{padding:14px 0;border-bottom:1px solid var(--ln);text-align:left;vertical-align:top;line-height:1.8}
.ev-t th{width:26%;padding-right:20px;color:var(--ink);font-weight:700} .ev-t td{color:var(--ink)} .ev-t tr:first-child th,.ev-t tr:first-child td{border-top:1px solid var(--ln)}
.ev-vs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.ev-v{display:flex;flex-direction:column;gap:12px;margin:0;padding:22px;border-radius:18px;background:var(--bg)}
.ev-av{display:block;width:64px;height:64px;border-radius:50%;background:#fff;overflow:hidden} .ev-av svg{width:100%;height:100%;display:block}
.ev-v blockquote{margin:0;color:var(--ink);font-size:14.5px;line-height:1.8} .ev-v figcaption{color:var(--sub);font-size:12.5px} .ev-v figcaption b{margin-right:8px;color:var(--ink)}
.ev-two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,420px);gap:48px;align-items:start}
.ev-card{padding:28px;border-radius:22px;background:#fff;box-shadow:0 0 0 1px var(--ln)} .ev-card__t{margin:0 0 16px;color:var(--ink);font-weight:700}
.ev-b{display:grid;gap:12px;margin:0;padding:0;list-style:none} .ev-b li{display:grid;grid-template-columns:110px minmax(0,1fr) 24px;gap:12px;align-items:center;font-size:13.5px}
.ev-b__l{color:var(--ink);font-weight:700} .ev-b__t{height:12px;border-radius:99px;background:var(--bg);overflow:hidden} .ev-b__t i{display:block;height:100%;border-radius:99px;background:var(--p)} .ev-b b{text-align:right;color:var(--ink);font-variant-numeric:tabular-nums}
.ev-upd{margin:28px 0 0;color:var(--sub);font-size:13px}
@media (max-width:900px){.ev-sat,.ev-two{grid-template-columns:1fr;gap:28px} .ev-vs{grid-template-columns:1fr} .ev-t th{width:auto;display:block;padding-bottom:0;border:0} .ev-t td{display:block;padding-top:4px} .ev-t tr:first-child td{border-top:0}}
@media (max-width:640px){.ev-q{min-width:0}.ev-q thead{display:none}.ev-q tr{display:grid;grid-template-columns:minmax(0,1fr) auto;column-gap:12px;padding:12px 0;border-bottom:1px solid var(--ln)}.ev-q th,.ev-q td{padding:0;border:0!important}.ev-q td:not(.num){grid-column:1/-1;grid-row:2;margin-top:4px;font-size:13px}.ev-q__total{border-top:1.5px solid var(--ink)}}
"""
html = head + base_css + css + between + '<main>\n' + PAGE + '\n' + footer_on
html = re.sub(r'<title>[^<]*</title>', '<title>数字の根拠 | The Academy</title>', html, count=1)
html = html.replace('href="/beginners', 'href="beginners.html')
open(os.path.join(LPDIR, 'evidence.html'), 'w').write(html); print('ok evidence.html', len(html))
