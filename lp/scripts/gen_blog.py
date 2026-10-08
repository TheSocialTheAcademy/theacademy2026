# 学びのヒント（/blog）ページを、LPの共通部品と「コースを探す」の下層ページ共通スタイルから組み立てる
# 流れ（プロトタイプ準拠）：見出し → アクセスの多い記事（今週／今月）→ 評価の高い記事 → 最新記事（カテゴリ絞り込み・並び替え）→ お役立ち資料・LINE
import os, tempfile
S = os.path.dirname(os.path.abspath(__file__))          # このスクリプトのフォルダ（lp/scripts）
LPDIR = os.path.dirname(S)                              # 出力先（lp）
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')  # 共通部品を取り出すときの捨て出力
import os, re, json
os.environ['TA_COURSES_OUT'] = TMP_COURSES
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)
head, between, footer_on, ARROW, lp, line_band = g['head'], g['between'], g['footer_on'], g['ARROW'], g['s'], g['line_band']
base_css = g['css']
OUT = os.path.join(LPDIR, 'blog.html')

def ic(d, w=1.9): return f'<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{d}</g></svg>'
CLOCK = ic('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>', 2)
THUMB = ic('<path d="M7 11v9H4v-9zM7 11l4-7a2 2 0 0 1 3 2l-1 4h5a2 2 0 0 1 2 2.3l-1.2 6A2 2 0 0 1 16.8 20H7"/>', 2)
DOC = ic('<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h5"/>')
TPL = ic('<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 10h16M10 10v10"/>')
NEW = ic('<path d="M20 12a8 8 0 1 1-2.3-5.6M20 4v4h-4"/>')
DOWN = ic('<path d="m6 9 6 6 6-6"/>', 2.2)

# カテゴリの色（コースを探すと同じ）
CAT = {'IT・デジタル': ('#1E9E62', '#E9F7F0'), 'マーケティング': ('#E46A1F', '#FFF1E7'), '英語・TOEIC': ('#0141D4', '#EAF0FF'),
       'ビジネス': ('#6B4FD8', '#F0ECFF'), 'クリエイティブ': ('#D9467A', '#FDECF2'), 'キャリア・学び方': ('#0F1B45', '#EEF1F6')}
def tag(c): fg, bg = CAT[c]; return f'<span class="bl-tag" style="--cc:{fg};--cb:{bg}">{c}</span>'

# 記事（タイトル・日付・読了時間・評価は仮）。画像は記事のアイキャッチ（gen_eyecatch.py で作る N-2：写真＋大見出し）
A = {
 'weekly2h':  ('キャリア・学び方', '2026.09.08', 5, '働きながら学びを続けるための、<wbr>週2時間のつくり方', '忙しい平日でも学びを止めないために。スキマ時間の見つけ方と、無理なく続く習慣づくりのコツをまとめました。', 'assets/journal/weekly2h.webp', 142),
 'chatgpt5':  ('IT・デジタル', '2026.08.26', 4, 'ChatGPTを<wbr>仕事の相棒にする、<wbr>最初の5つの使い方', '最初のひと言の書き方から、議事録・メール・企画のたたき台づくりまで。', 'assets/journal/chatgpt5.webp', 118),
 'snscamp':   ('マーケティング', '2026.08.12', 6, '顧客理解から始める<wbr>SNSキャンペーン設計', '「誰に・何を・なぜ」を先に決めると、投稿の反応が変わります。', 'assets/journal/snscamp.webp', 101),
 'restart':   ('キャリア・学び方', '2026.08.01', 5, '独学が続かなかった人のための、<wbr>学び直しの始め方', '三日坊主で終わった経験がある人ほど、最初の設計が大切です。', 'assets/journal/restart.webp', 77),
 'phrase20':  ('英語・TOEIC', '2026.07.20', 3, '会議で使える、<wbr>短い英語フレーズ20', '相づち・確認・提案。覚えておくと会議で困らない短い表現を集めました。', 'assets/journal/phrase20.webp', 64),
 'portfolio': ('キャリア・学び方', '2026.07.08', 6, '未経験から実績をつくる、<wbr>ポートフォリオの育て方', '「載せるものがない」から始める人のための、実績の残し方。', 'assets/journal/portfolio.webp', 128),
 'aimemo':    ('IT・デジタル', '2026.06.24', 5, '会議メモをAIで要約する、<wbr>実務の手順', 'プロンプトの型と、要約を確認するときのポイント。', 'assets/journal/aimemo.webp', 96),
 'insta1':    ('マーケティング', '2026.06.10', 4, 'Instagramの投稿企画を、<wbr>1枚のシートで考える', '目的・ターゲット・投稿の型を1枚に整理する方法。', 'assets/journal/insta1.webp', 84),
 'event':     ('ビジネス', '2026.05.28', 5, '小さなイベントを成功させる、<wbr>当日の進行表のつくり方', '目的から逆算して、当日の流れとキューを決めます。', 'assets/journal/event.webp', 52),
 'canva':     ('クリエイティブ', '2026.05.14', 4, 'Canvaで伝わる投稿をつくる、<wbr>3つの基本', '余白・文字の大きさ・色の数。この3つで見違えます。', 'assets/journal/canva.webp', 71),
 'brand':     ('ビジネス', '2026.04.30', 6, '選ばれる理由を言葉にする、<wbr>ブランドコンセプトの考え方', 'お客様が感じている価値を、短い言葉にまとめる手順。', 'assets/journal/brand.webp', 45),
 'present':   ('英語・TOEIC', '2026.04.16', 5, '5分で伝わる、<wbr>英語プレゼンの組み立て方', '結論から話す型と、緊張しても崩れない準備のしかた。', 'assets/journal/present.webp', 58),
}
def small(k): return A[k][5].replace('assets/journal/', 'assets/photos/articles/')  # 小さい画像は見出しが読めないため、文字なしの写真
def href(k): return 'article.html' if k == 'weekly2h' else f'/blog/{k}'  # 記事ページは見本の1本だけ
def meta(k):
    c, d, m = A[k][0], A[k][1], A[k][2]
    return f'<p class="bl-meta">{tag(c)}<time>{d}</time><span class="bl-min">{CLOCK}{m}分で読める</span></p>'

# ── ① ページ見出し
cats = list(CAT)
pagehead = f'''<section class="phead" aria-labelledby="page-title"><div class="wrap">
<nav class="crumb" aria-label="パンくずリスト"><a href="lp-design.html">トップ</a><span aria-hidden="true">/</span><span aria-current="page">学びのヒント</span></nav>
<h1 class="phead__t" id="page-title">学びを続けるヒント</h1>
<p class="phead__lead">キャリア、生成AI、マーケティングなど、<wbr>働きながら学ぶためのヒントを届けます。</p>
<ul class="phead__jump"><li><a href="#popular">アクセスの多い記事</a></li><li><a href="#rated">評価の高い記事</a></li><li><a href="#latest">最新記事</a></li><li><a href="#resources">お役立ち資料</a></li></ul>
</div></section>'''

# ── ② アクセスの多い記事（今週／今月）
RANK = {'week': ['weekly2h', 'chatgpt5', 'snscamp', 'restart', 'phrase20'], 'month': ['portfolio', 'weekly2h', 'aimemo', 'chatgpt5', 'insta1']}
def rank_html(key, hidden):
    ks = RANK[key]; top = ks[0]
    lst = ''.join(f'<li><a class="rk" href="{href(k)}"><span class="rk__n">{i + 2}</span><span class="rk__ph"><img src="{small(k)}" alt="" loading="lazy"></span><span class="rk__b">{meta(k)}<b>{A[k][3]}</b></span></a></li>' for i, k in enumerate(ks[1:]))
    return f'''<div class="rk-panel" data-period="{key}"{" hidden" if hidden else ""}>
<a class="rk-top" href="{href(top)}"><span class="rk-top__ph"><img src="{A[top][5]}" alt="" loading="lazy"><span class="rk__n rk__n--1">1</span></span><span class="rk-top__b">{meta(top)}<b>{A[top][3]}</b><span class="rk-top__ex">{A[top][4]}</span></span></a>
<ol class="rk-list">{lst}</ol></div>'''
popular = f'''<section class="bl-pop" id="popular" aria-labelledby="pop-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">POPULAR</p><h2 class="sec-title" id="pop-title">アクセスの多い記事</h2></div>
<div class="bl-seg" role="tablist" aria-label="期間"><button type="button" role="tab" aria-selected="true" data-period="week">今週</button><button type="button" role="tab" aria-selected="false" data-period="month">今月</button></div></header>
{rank_html('week', False)}{rank_html('month', True)}
</div></section>'''

# ── ③ 評価の高い記事
rated_keys = sorted(A, key=lambda k: -A[k][6])[:3]
rated = f'''<section class="bl-rated" id="rated" aria-labelledby="rated-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">TOP RATED</p><h2 class="sec-title" id="rated-title">評価の高い記事</h2>
<p class="sec-lead">読んだ人の「役に立った」が多い記事です。</p></div></header>
<ol class="rt">{''.join(f'<li><a class="rt__c" href="{href(k)}"><span class="rt__ph"><img src="{A[k][5]}" alt="" loading="lazy"><span class="rt__badge">{THUMB}役に立った <b>{A[k][6]}</b></span></span><span class="rt__b">{meta(k)}<b>{A[k][3]}</b><span class="rt__ex">{A[k][4]}</span></span></a></li>' for k in rated_keys)}</ol>
</div></section>'''

# ── ④ 最新記事（カテゴリ絞り込み・並び替え・もっと見る）
latest_items = ''.join(f'<li class="lt" data-cat="{A[k][0]}" data-date="{A[k][1]}"><a href="{href(k)}"><span class="lt__ph"><img src="{small(k)}" alt="" loading="lazy"></span><span class="lt__b">{meta(k)}<b>{A[k][3]}</b><span class="lt__ex">{A[k][4]}</span></span></a></li>' for k in sorted(A, key=lambda k: A[k][1], reverse=True))
chips = '<button type="button" class="bl-chip" aria-pressed="true" data-cat="">すべて</button>' + ''.join(f'<button type="button" class="bl-chip" aria-pressed="false" data-cat="{c}">{c}</button>' for c in cats)
latest = f'''<section class="bl-latest" id="latest" aria-labelledby="latest-title"><div class="wrap">
<header class="sec-head"><div><p class="sec-kicker">LATEST</p><h2 class="sec-title" id="latest-title">最新記事</h2></div>
<label class="bl-sort"><span>並び替え</span><select id="ltSort"><option value="desc">新しい順</option><option value="asc">古い順</option></select>{DOWN}</label></header>
<div class="bl-chips" role="group" aria-label="カテゴリで絞り込む">{chips}</div>
<ol class="lt-list" id="ltList">{latest_items}</ol>
<div class="lt-empty" id="ltEmpty" hidden><div class="lte__l"><p class="lte__t">「<span id="ltEmptyCat"></span>」の記事は準備中です</p><p class="lte__s">公開したら公式LINEでお知らせします。<wbr>ほかのカテゴリや、よく読まれている記事もどうぞ。</p>
<div class="lte__b"><a class="lte__line" href="beginners.html#line">新着をLINEで受け取る</a><button type="button" class="lte__all" id="ltEmptyAll">すべての記事を見る</button></div></div>
<div class="lte__r"><p class="lte__k">よく読まれている記事</p><ol>{''.join(f'<li><a href="{href(k)}"><span>{i + 1}</span>{A[k][3]}</a></li>' for i, k in enumerate(['weekly2h', 'chatgpt5', 'portfolio']))}</ol></div></div>
<div class="lt-more"><button type="button" class="btn btn--white" id="ltMore">もっと見る{DOWN}</button></div>
<p class="hl-note">※記事タイトル・日付・評価の数は仮です。</p>
</div></section>'''

# ── ⑤ お役立ち資料・LINE
# 資料は随時追加・更新されるため、特定の資料は載せず、資料一覧への入口（1本の帯）だけを置く
LINE_IC = g['LINE_IC']
resources = f'''<section class="bl-res" id="resources" aria-label="お役立ち資料と公式LINE"><div class="wrap"><div class="k2">
<a class="k2__r" href="resources.html"><span class="k2__ic">{DOC}</span><span class="k2__t"><span class="k2__k">お役立ち資料</span><b>仕事や学びに役立つ資料を、<wbr>目的に合わせて選べます</b></span><span class="k2__go">{ARROW}</span></a>
<a class="k2__r k2__r--line" href="beginners.html#line"><span class="k2__ic">{LINE_IC}</span><span class="k2__t"><span class="k2__k">公式LINE限定</span><b>LINE登録で、<wbr>全コース<em>500円OFF</em></b></span><span class="k2__go">{ARROW}</span></a>
</div></div></section>'''

js = r'''<script>
(() => {
  // アクセスの多い記事：今週／今月
  const seg = document.querySelectorAll('.bl-seg button'), panels = document.querySelectorAll('.rk-panel');
  seg.forEach(b => b.addEventListener('click', () => { seg.forEach(x => x.setAttribute('aria-selected', String(x === b))); panels.forEach(p => p.hidden = p.dataset.period !== b.dataset.period); }));
  // 最新記事：カテゴリ・並び替え・もっと見る（6件ずつ）
  const list = document.getElementById('ltList'), items = [...list.children], more = document.getElementById('ltMore'), empty = document.getElementById('ltEmpty'), sort = document.getElementById('ltSort');
  const chips = document.querySelectorAll('.bl-chip'); let cat = '', shown = 6;
  function render() {
    const hit = items.filter(li => !cat || li.dataset.cat === cat).sort((a, b) => sort.value === 'asc' ? a.dataset.date.localeCompare(b.dataset.date) : b.dataset.date.localeCompare(a.dataset.date));
    items.forEach(li => li.hidden = true); hit.forEach((li, i) => { list.appendChild(li); li.hidden = i >= shown; });
    more.hidden = hit.length <= shown; empty.hidden = hit.length > 0;
    const cn = [...chips].find(x => x.getAttribute('aria-pressed') === 'true'); document.getElementById('ltEmptyCat').textContent = cn ? cn.textContent.trim() : '';
  }
  chips.forEach(c => c.addEventListener('click', () => { chips.forEach(x => x.setAttribute('aria-pressed', String(x === c))); cat = c.dataset.cat; shown = 6; render(); }));
  sort.addEventListener('change', render);
  more.addEventListener('click', () => { shown += 6; render(); });
  document.getElementById('ltEmptyAll').addEventListener('click', () => chips[0].click());
  render();
})();
</script>'''

css = r'''
  /* ══ 学びのヒント（/blog）══════════════ */
  .bl-pop, .bl-latest { padding: clamp(64px, 7vw, 96px) 0; background: #fff; }
  .bl-rated { padding: clamp(64px, 7vw, 96px) 0; background: var(--bg-gray, #F7F8FB); }
  .bl-res { padding: 0 0 clamp(56px, 6vw, 80px); background: #fff; }
  .hl-note { margin: 18px 0 0; color: var(--ts-mid); font-size: 12px; }
  .bl-pop .sec-title, .bl-rated .sec-title, .bl-latest .sec-title, .sec-lead { word-break: keep-all; overflow-wrap: anywhere; }
  .bl-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; margin: 0; color: var(--ts-mid); font-size: 12px; }
  .bl-tag { padding: 2px 10px; border-radius: 99px; background: var(--cb); color: var(--cc); font-size: 11.5px; font-weight: 700; }
  .bl-min { display: inline-flex; align-items: center; gap: 4px; } .bl-min svg { width: 13px; height: 13px; }
  .bl-pop b, .bl-rated b, .bl-latest b { word-break: keep-all; overflow-wrap: anywhere; }
  /* ② ランキング */
  .bl-seg { display: inline-flex; gap: 4px; padding: 4px; border-radius: 99px; background: #F1F4FA; }
  .bl-seg button { padding: 8px 20px; border: 0; border-radius: 99px; background: none; color: var(--ts-mid); font: inherit; font-size: 14px; font-weight: 700; cursor: pointer; }
  .bl-seg button[aria-selected="true"] { background: #fff; color: var(--ts-primary); box-shadow: 0 2px 8px rgba(15,27,69,.1); }
  .rk-panel { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 32px; align-items: start; } .rk-panel[hidden] { display: none; }
  .rk-top { display: block; color: inherit; text-decoration: none; }
  .rk-top__ph { position: relative; display: block; aspect-ratio: 16 / 9; border-radius: 22px; overflow: hidden; background: #EEF1F6; } .rk-top__ph img { display: block; width: 100%; height: 100%; object-fit: cover; transition: transform .4s; }
  .rk-top:hover img { transform: scale(1.03); }
  .rk-top__b { display: block; padding: 18px 4px 0; } .rk-top__b b { display: block; margin-top: 10px; color: var(--ink); font-size: 24px; line-height: 1.5; } .rk-top__ex { display: block; margin-top: 8px; color: var(--ts-mid); font-size: 14px; line-height: 1.8; }
  .rk__n { display: grid; place-items: center; flex: none; width: 34px; height: 34px; border-radius: 50%; background: #EEF1F6; color: var(--ink); font: 800 15px/1 'Helvetica Neue', Arial, sans-serif; }
  .rk__n--1 { position: absolute; right: 16px; top: 16px; width: 48px; height: 48px; background: var(--ts-primary); color: #fff; font-size: 20px; box-shadow: 0 8px 20px rgba(1,65,212,.35); }
  .rk-list { display: grid; margin: 0; padding: 0; list-style: none; }
  .rk { display: grid; grid-template-columns: 34px 120px minmax(0, 1fr); gap: 16px; align-items: center; padding: 16px 0; border-bottom: 1px solid var(--line); color: inherit; text-decoration: none; }
  li:first-child > .rk { padding-top: 0; }
  .rk:hover b { color: var(--ts-primary); }
  .rk__ph { aspect-ratio: 16 / 9; border-radius: 12px; overflow: hidden; background: #EEF1F6; } .rk__ph img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .rk__b b { display: block; margin-top: 6px; color: var(--ink); font-size: 15.5px; line-height: 1.55; }
  /* ③ 評価の高い記事 */
  .rt { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin: 0; padding: 0; list-style: none; }
  .rt__c { display: flex; flex-direction: column; height: 100%; border-radius: 20px; background: #fff; box-shadow: 0 0 0 1px var(--line); color: inherit; text-decoration: none; overflow: hidden; transition: box-shadow .2s, transform .2s; }
  .rt__c:hover { transform: translateY(-2px); box-shadow: 0 0 0 1px rgba(1,65,212,.25), var(--shadow-soft); }
  .rt__ph { position: relative; display: block; aspect-ratio: 16 / 9; background: #EEF1F6; } .rt__ph img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .rt__badge { position: absolute; right: 12px; top: 12px; display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 99px; background: #fff; color: var(--ts-mid); font-size: 12px; font-weight: 700; box-shadow: 0 6px 16px rgba(15,27,69,.14); }
  .rt__badge svg { width: 15px; height: 15px; color: var(--ts-primary); } .rt__badge b { color: var(--ts-primary); font-size: 15px; }
  .rt__b { display: block; padding: 18px 20px 22px; } .rt__b > b { display: block; margin-top: 10px; color: var(--ink); font-size: 17px; line-height: 1.55; } .rt__ex { display: block; margin-top: 8px; color: var(--ts-mid); font-size: 13.5px; line-height: 1.8; }
  /* ④ 最新記事 */
  .bl-sort { position: relative; display: inline-flex; align-items: center; gap: 10px; color: var(--ts-mid); font-size: 13px; font-weight: 700; }
  .bl-sort select { appearance: none; padding: 10px 38px 10px 14px; border: 0; border-radius: 10px; background: #F1F4FA; color: var(--ink); font: inherit; font-size: 14px; cursor: pointer; }
  .bl-sort svg { position: absolute; right: 12px; width: 16px; height: 16px; pointer-events: none; color: var(--ink); }
  .bl-chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 24px; }
  .bl-chip { padding: 8px 16px; border: 0; border-radius: 99px; background: #fff; color: var(--ink); font: inherit; font-size: 13.5px; font-weight: 700; box-shadow: inset 0 0 0 1px var(--line); cursor: pointer; }
  .bl-chip[aria-pressed="true"] { background: var(--ts-primary); color: #fff; box-shadow: none; }
  .lt-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 40px; margin: 0; padding: 0; list-style: none; }
  .lt[hidden] { display: none; }
  .lt a { display: grid; grid-template-columns: 160px minmax(0, 1fr); gap: 18px; align-items: center; padding: 20px 0; border-bottom: 1px solid var(--line); color: inherit; text-decoration: none; }
  .lt a:hover b { color: var(--ts-primary); }
  .lt__ph { aspect-ratio: 16 / 9; border-radius: 14px; overflow: hidden; background: #EEF1F6; } .lt__ph img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .lt__b b { display: block; margin-top: 8px; color: var(--ink); font-size: 16px; line-height: 1.55; } .lt__ex { display: block; margin-top: 4px; color: var(--ts-mid); font-size: 13px; line-height: 1.7; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  .lt-empty { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: 32px; margin-top: 8px; padding: clamp(22px, 3vw, 32px); border-radius: 22px; background: #fff; box-shadow: 0 0 0 1px var(--line); }
  .lt-empty[hidden] { display: none; }
  .lte__t { margin: 0; color: var(--ink); font-size: 19px; font-weight: 800; } .lte__s { margin: 8px 0 0; color: var(--ts-mid); font-size: 14px; line-height: 1.8; }
  .lte__b { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }
  .lte__line, .lte__all { display: inline-flex; align-items: center; height: 46px; padding: 0 20px; border: 0; border-radius: 12px; font: inherit; font-size: 14px; font-weight: 700; text-decoration: none; cursor: pointer; }
  .lte__line { background: #06C755; color: #fff; } .lte__all { background: #fff; color: var(--ink); box-shadow: inset 0 0 0 1px var(--line); }
  .lte__k { margin: 0; color: var(--ts-mid); font-size: 12.5px; font-weight: 700; } .lte__r ol { margin: 10px 0 0; padding: 0; list-style: none; display: grid; gap: 8px; }
  .lte__r a { display: flex; gap: 10px; align-items: flex-start; padding: 12px 14px; border-radius: 12px; background: var(--bg-gray, #F7F8FB); color: var(--ink); font-size: 13.5px; font-weight: 700; line-height: 1.6; text-decoration: none; }
  .lte__r a span { display: grid; place-items: center; flex: none; width: 24px; height: 24px; border-radius: 50%; background: var(--ts-primary); color: #fff; font-size: 12px; }
  @media (max-width: 760px) { .lt-empty { grid-template-columns: minmax(0, 1fr); } }
  .lt-more { margin-top: 28px; text-align: center; } .lt-more[hidden], #ltMore[hidden] { display: none; }
  .lt-more .btn { min-width: 220px; gap: 6px; box-shadow: inset 0 0 0 1.5px var(--ts-primary); color: var(--ts-primary); } .lt-more svg { width: 16px; height: 16px; }
  /* ⑤ お役立ち資料 */
  /* お役立ち資料と公式LINE：1つの箱を2つに区切る */
  .k2 { display: grid; grid-template-columns: 1fr 1fr; border-radius: 22px; background: var(--bg-gray, #F7F8FB); overflow: hidden; }
  .k2__r { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; align-items: center; gap: 16px; padding: 24px 28px; color: var(--ink); text-decoration: none; }
  .k2__r + .k2__r { border-left: 1px solid #E3E7EF; }
  .k2__ic { display: grid; place-items: center; width: 46px; height: 46px; border-radius: 12px; background: #fff; color: var(--ts-primary); } .k2__ic svg { width: 22px; height: 22px; } .k2__r--line .k2__ic { background: #06C755; color: #fff; }
  .k2__k { display: block; color: var(--ts-primary); font-size: 12px; font-weight: 700; letter-spacing: .08em; } .k2__r--line .k2__k { color: #06A04A; }
  .k2__t b { display: block; margin-top: 2px; font-size: 15.5px; line-height: 1.5; } .k2__t em { font-style: normal; color: #06A04A; }
  .k2__go { display: grid; place-items: center; width: 40px; height: 40px; border-radius: 50%; background: var(--ts-primary); color: #fff; } .k2__go svg { width: 16px; height: 16px; } .k2__r--line .k2__go { background: #06C755; }
  .k2__r:hover b { color: var(--ts-primary); } .k2__r--line:hover b { color: #06A04A; } .k2__t b { word-break: keep-all; overflow-wrap: anywhere; }
  @media (max-width: 1000px) {
    .rk-panel { grid-template-columns: minmax(0, 1fr); } .rt { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); } .rt li:last-child { display: none; }
    .lt-list { grid-template-columns: minmax(0, 1fr); }
  }
  @media (max-width: 640px) {
    .bl-pop .sec-head, .bl-latest .sec-head { gap: 16px; }
    .rk-top__b b { font-size: 19px; } .rk { grid-template-columns: 30px 96px minmax(0, 1fr); gap: 12px; } .rk__b b { font-size: 14px; } .rk__b .bl-min { display: none; }
    .rt { grid-template-columns: minmax(0, 1fr); } .rt li:last-child { display: block; }
    .lt a { grid-template-columns: 112px minmax(0, 1fr); gap: 14px; padding: 16px 0; } .lt__ex { display: none; } .lt__b b { font-size: 14.5px; } .lt .bl-min { display: none; }
    .bl-chips { flex-wrap: nowrap; margin-right: calc(var(--gutter) * -1); padding-right: var(--gutter); overflow-x: auto; scrollbar-width: none; } .bl-chip { flex: none; }
    .k2 { grid-template-columns: minmax(0, 1fr); } .k2__r { gap: 14px; padding: 18px; } .k2__r + .k2__r { border-left: 0; border-top: 1px solid #E3E7EF; } .k2__ic { width: 40px; height: 40px; } .k2__t b { font-size: 14.5px; }
  }
'''

html = (head + base_css + css
        + between.replace('<a href="blog.html">学びのヒント</a>', '<a href="blog.html" aria-current="page">学びのヒント</a>')
        + '<main>\n' + pagehead + popular + rated + latest + resources + '\n' + js + '\n' + footer_on)
html = re.sub(r'<title>[^<]*</title>', '<title>学びのヒント | The Academy</title>', html, count=1)
open(OUT, 'w').write(html)
print('ok', len(html))
