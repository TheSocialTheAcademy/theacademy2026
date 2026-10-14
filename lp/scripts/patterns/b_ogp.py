from common import *
A = '/home/user/theacademy2026/lp/assets/'
LOGO = A + 'academy_logo_blue_trim.png'
CATCH = '学んで、つくって、<br>次のキャリアへ。'
SUB = '働きながら学べるオンラインスクール'
TH = ['sns-marketing', 'ai-efficiency', 'toeic-700', 'event-design', 'canva-basic', 'instagram']
def o1():  # 青の地＋キャッチ
    return f'<div class="og o1"><svg class="bgs" viewBox="0 0 1200 630"><circle cx="1080" cy="80" r="260" fill="#fff" opacity=".07"/><circle cx="1150" cy="560" r="200" fill="#3E78FE" opacity=".35"/><path d="M-50 520 C 300 420, 600 640, 1250 470 L1250 700 L-50 700Z" fill="#fff" opacity=".06"/></svg><img class="lg lg--w" src="{LOGO}" alt=""><p class="o-c">{CATCH}</p><p class="o-s">{SUB}</p><p class="o-u">theacademyjapan.org</p></div>'
def o2():  # メイン写真＋白いパネル
    return f'<div class="og o2"><img class="ph" src="{A}hero.webp" alt=""><div class="o2-p"><img class="lg" src="{LOGO}" alt=""><p class="o-c o-c--ink">{CATCH}</p><p class="o-s o-s--sub">{SUB}</p></div></div>'
def o3():  # 白地＋コースのサムネイルを並べる
    tiles = ''.join(f'<img src="{A}thumbs/{t}.webp" alt="">' for t in TH)
    return f'<div class="og o3"><div class="o3-l"><img class="lg" src="{LOGO}" alt=""><p class="o-c o-c--ink">{CATCH}</p><p class="o-s o-s--sub">{SUB}</p><span class="o3-b">実践コース 10+　平均満足度 4.2</span></div><div class="o3-r">{tiles}</div></div>'
def o4():  # 白地＋大きなキャッチ＋カテゴリ色の帯
    bars = ''.join(f'<i style="background:{CAT[k][1]}"></i>' for k in ('it', 'mk', 'en', 'biz', 'cr'))
    return f'<div class="og o4"><img class="lg" src="{LOGO}" alt=""><p class="o-c o-c--ink o4-c">学んで、<em>つくって</em>、<br>次のキャリアへ。</p><p class="o-s o-s--sub">{SUB}</p><div class="o4-bar">{bars}</div></div>'
# ページ別の自動OGP（コース＝サムネイル、記事＝アイキャッチ）
def pg_course():
    return f'<div class="og o5" style="background:#0F1B45"><img class="o5-img" src="{A}thumbs/canva-basic.webp" alt=""><div class="o5-f"><img class="lg lg--w" src="{LOGO}" alt=""><span>コース｜Canva初級</span></div></div>'
def pg_article():
    return f'<div class="og o5" style="background:#0F1B45"><img class="o5-img" src="{A}journal/weekly2h.webp" alt=""><div class="o5-f"><img class="lg lg--w" src="{LOGO}" alt=""><span>学びのヒント</span></div></div>'
def sns(img_html, title, desc):  # SNSでの見え方（X・Facebook風の汎用カード）
    return f'<div class="sns"><div class="sns-i">{img_html}</div><div class="sns-b"><small>theacademyjapan.org</small><b>{title}</b><p>{desc}</p></div></div>'
css = '''.og{position:relative;width:1200px;height:630px;overflow:hidden;color:#0F1B45;transform-origin:0 0;isolation:isolate}.wrapog{width:600px;height:315px;overflow:hidden;border-radius:10px;box-shadow:0 0 0 1px #E1E5EE}.wrapog .og{transform:scale(.5)}
.bgs{position:absolute;inset:0;width:100%;height:100%;z-index:-1}.ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 30%}
.lg{height:44px;display:block}.lg--w{filter:brightness(0) invert(1)}
.o-c{font-size:66px;font-weight:900;line-height:1.35;letter-spacing:.01em}.o-c--ink{color:#0F1B45}.o-s{font-size:26px;font-weight:700;margin-top:18px;opacity:.9}.o-s--sub{color:#4A4E6A}
.o1{background:#0141D4;color:#fff;padding:70px 80px}.o1 .o-c{margin-top:70px}.o-u{position:absolute;right:80px;bottom:56px;font-size:22px;font-weight:700;opacity:.75}
.o2-p{position:absolute;left:56px;top:56px;bottom:56px;width:590px;background:rgba(255,255,255,.95);border-radius:24px;padding:52px 52px}.o2-p .o-c{font-size:54px;margin-top:56px}.o2-p .o-s{font-size:22px}
.o3{background:#fff;display:grid;grid-template-columns:560px 1fr}.o3-l{padding:70px 0 0 72px}.o3-l .o-c{font-size:52px;margin-top:60px}.o3-l .o-s{font-size:22px}
.o3-b{display:inline-block;margin-top:34px;background:#EAF0FF;color:#0141D4;font-size:22px;font-weight:800;padding:10px 22px;border-radius:999px}
.o3-r{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:40px 40px 0 0;transform:rotate(-6deg) translate(20px,-30px);align-content:start}.o3-r img{width:100%;border-radius:14px;box-shadow:0 10px 24px rgba(15,27,69,.14)}
.o4{background:#fff;padding:72px 84px}.o4-c{font-size:80px;margin-top:64px}.o4-c em{font-style:normal;color:#0141D4;background:linear-gradient(transparent 62%,#EAF0FF 62%)}.o4-bar{position:absolute;left:0;right:0;bottom:0;height:22px;display:flex}.o4-bar i{flex:1}
.o5-img{position:absolute;left:0;top:24px;width:1200px;height:500px;object-fit:contain}.o5-f{position:absolute;left:0;right:0;bottom:0;height:90px;display:flex;align-items:center;justify-content:space-between;padding:0 48px;color:#fff;font-size:24px;font-weight:800}.o5-f .lg{height:36px}
.row2{display:grid;grid-template-columns:600px 1fr;gap:36px;align-items:start}.row2+.row2{margin-top:28px}.note{font-size:14px;color:#4A4E6A;line-height:1.8}.note b{color:#0F1B45}
.sns{width:520px;border:1px solid #DDE2EA;border-radius:16px;overflow:hidden;background:#fff}.sns-i{width:520px;height:273px;overflow:hidden}.sns-i .og{transform:scale(.4333)}.sns-b{padding:12px 16px 14px}.sns-b small{color:#676688;font-size:12px}.sns-b b{display:block;font-size:15px;margin:2px 0}.sns-b p{font-size:13px;color:#4A4E6A}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}.pair p.lbl{margin-bottom:8px}'''
def blk(code, name, desc, pros, html, rec=False, note=''):
    return pat(code, name, desc, pros, f'<div class="row2"><div><p class="lbl">1200×630（縮小表示）</p><div class="wrapog">{html}</div></div><div><p class="lbl">SNS に貼ったときの見え方（例）</p>{sns(html, "The Academy｜働きながら学べるオンラインスクール", "学んで、つくって、次のキャリアへ。成果物をつくり、ポートフォリオに残す学び方。")}</div></div>', rec)
pats = [
 '<section class="pat"><h2>OGP 画像の決め方</h2><p class="d">OGP 画像は、X・Facebook・LINE・Slack などに URL を貼ったときに出る画像です（1200×630）。サイト全体で使う「共通の1枚」と、コース・記事ページで使う「ページごとの画像」に分けると、少ない手間で全ページに画像が出ます。</p><div class="why" style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">'
 '<div style="background:#F7F8FB;border-radius:12px;padding:14px 16px;font-size:13.5px;line-height:1.7"><b>① 共通の1枚</b><br>トップ・はじめての方へ・よくある質問など、ほとんどのページ。下の O-1〜O-4 から選ぶ</div>'
 '<div style="background:#F7F8FB;border-radius:12px;padding:14px 16px;font-size:13.5px;line-height:1.7"><b>② コース詳細</b><br>コースのサムネイルをそのまま使う（作り直し不要）</div>'
 '<div style="background:#F7F8FB;border-radius:12px;padding:14px 16px;font-size:13.5px;line-height:1.7"><b>③ 記事</b><br>記事のアイキャッチをそのまま使う（作り直し不要）</div></div></section>',
 blk('O-1', '青の地＋キャッチ', 'ブランドの青に、白いロゴとキャッチ「学んで、つくって、次のキャリアへ。」。どの SNS でも目立ち、文字がはっきり読めます。', [('◎', '一番目立つ・読みやすい'), ('○', '作りがシンプル'), ('△', '中身（何のサービスか）は文字だけ')], o1()),
 blk('O-2', 'メイン写真＋白いパネル', 'トップのメイン写真に、白いパネルでロゴとキャッチを重ねます。サイトを開いたときの印象とそろいます。', [('◎', 'サイトの第一印象とそろう'), ('○', '人の温かさが伝わる'), ('△', '小さく表示されると写真が細かく見える')], o2()),
 blk('O-3', 'キャッチ＋コースのサムネイル', '左にロゴとキャッチと実績、右にコースのサムネイルを並べます。「いろいろなコースがあるオンラインスクール」だとひと目で分かります。', [('◎', '何のサービスか一番伝わる'), ('◎', '実績（10+・4.2）も入る'), ('○', '今あるサムネイルで作れる')], o3(), True),
 blk('O-4', '白地＋大きなキャッチ', '白地に大きなキャッチ、下にカテゴリ5色の帯。すっきりしていて、ロゴとコピーが主役です。', [('○', '上品・シンプル'), ('△', 'SNS の白い画面の中では目立ちにくい')], o4()),
 '<section class="pat"><h2>ページごとの OGP（自動）</h2><p class="d">コース詳細と記事は、すでにある画像を切らずに置き、下の帯（ロゴ＋ページの種類）を足して使います。コースや記事を足すと、同じ作り方で自動で用意できます。</p><div class="pair">'
 f'<div><p class="lbl">コース詳細（サムネイル＋帯）</p><div class="wrapog">{pg_course()}</div></div><div><p class="lbl">記事（アイキャッチ＋帯）</p><div class="wrapog">{pg_article()}</div></div></div></section>',
 '<section class="pat"><h2>おすすめ</h2><p class="d">共通の1枚は <b>O-3（キャッチ＋コースのサムネイル）</b>。URL を受け取った人に「どんなサービスか」が画像だけで伝わり、実績の数字も入れられます。目立ちやすさを優先するなら O-1 です。コース詳細と記事は、ページごとの画像（自動）を使うのがおすすめです。</p></section>',
]
open('ogp.html', 'w').write(board('OGP 画像（SNS で共有したときの画像）　デザイン候補', 'サイト共通の1枚の候補4つと、コース・記事ページごとの画像の作り方です。', pats, css))
