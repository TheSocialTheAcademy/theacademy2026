from common import *
import os; A = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets') + '/'
K = {'IT・デジタル': 'it', 'マーケティング': 'mk', '英語・TOEIC': 'en', 'ビジネス': 'biz', 'クリエイティブ': 'cr', 'キャリア・学び方': 'ca'}
# 記事：カテゴリ, タイトル, キーワード（大）, 補足, アイコン, 仮の画像（成果物・学び方・ポートフォリオ）
ART = [
 ('キャリア・学び方', '働きながら学びを続けるための、<wbr>週2時間のつくり方', '週2時間', 'のつくり方', 'clock', 'how/step-01-learn.webp'),
 ('IT・デジタル', 'ChatGPTを仕事の相棒にする、<wbr>最初の5つの使い方', '5つ', 'ChatGPTの使い方', 'spark', 'outcomes/ai-prompt.webp'),
 ('マーケティング', '顧客理解から始める<wbr>SNSキャンペーン設計', '顧客理解', 'から始めるSNS設計', 'mega', 'outcomes/sns-design.webp'),
 ('英語・TOEIC', '会議で使える、<wbr>短い英語フレーズ20', '20', '会議の英語フレーズ', 'chat', 'outcomes/english-presentation.webp'),
 ('キャリア・学び方', '未経験から実績をつくる、<wbr>ポートフォリオの育て方', '実績', 'をつくるポートフォリオ', 'user', 'portfolio/show-featured-work.webp'),
 ('ビジネス', '小さなイベントを成功させる、<wbr>当日の進行表のつくり方', '進行表', '当日のつくり方', 'calendar', 'outcomes/event-plan.webp'),
]
def col(c): k = K[c]; return CAT[k][1], CAT[k][2]
def ea(a):
    c, t, kw, sub, i, img = a; fg, bg = col(c)
    return f'<div class="ey ea" style="background:{bg};--cc:{fg}"><span class="chip">{c}</span><p class="ea-t">{t.replace("<wbr>", "<br>")}</p><p class="lab">学びのヒント</p>{ic(i, "ea-i", 1.2)}</div>'
def eb(a):
    c, t, kw, sub, i, img = a; fg, bg = col(c)
    return f'<div class="ey eb" style="background:{bg};--cc:{fg}"><span class="chip">{c}</span><p class="eb-k" style="color:{fg}">{kw}</p><p class="eb-s">{sub}</p><span class="eb-line" style="background:{fg}"></span><p class="lab">学びのヒント</p></div>'
def ec(a):
    c, t, kw, sub, i, img = a; fg, bg = col(c)
    return f'<div class="ey ec" style="background:{bg};--cc:{fg}"><div class="ec-f"><img src="{A + img}" alt=""></div><span class="chip ec-c">{c}</span><span class="ec-tmp">仮の画像</span></div>'
def ed(a):
    c, t, kw, sub, i, img = a; fg, bg = col(c)
    return f'<div class="ey ed"><div class="ed-p"><img src="{A + img}" alt=""></div><div class="ed-t" style="background:{fg}"><span>{c}</span><b>{kw}</b></div></div>'
card = lambda fn, a: f'<div>{fn(a)}<p class="cap">{a[1].replace("<wbr>", "")}</p></div>'
row = lambda fn: '<div class="grid g3">' + ''.join(card(fn, a) for a in ART) + '</div>'
css = '''.g3{grid-template-columns:repeat(3,1fr)}.ey{position:relative;aspect-ratio:16/9;border-radius:10px;overflow:hidden;word-break:keep-all;overflow-wrap:anywhere}
.chip{display:inline-block;background:#fff;color:var(--cc);font-size:11px;font-weight:700;padding:3px 10px;border-radius:999px}.lab{position:absolute;right:18px;bottom:14px;font-size:10.5px;font-weight:900;letter-spacing:.12em;color:var(--cc);opacity:.85}
.ea{padding:20px 22px}.ea-t{font-size:21px;font-weight:900;line-height:1.45;margin-top:14px;max-width:84%;position:relative;z-index:1}.ea-i{position:absolute;right:-14px;top:-14px;width:120px;height:120px;color:var(--cc);opacity:.18}
.eb{padding:20px 22px}.eb-k{font-size:52px;font-weight:900;line-height:1.05;margin-top:22px;letter-spacing:.01em}.eb-s{font-size:17px;font-weight:900;margin-top:6px}.eb-line{position:absolute;left:22px;bottom:18px;width:40px;height:4px;border-radius:2px}
.ec{padding:14px}.ec-f{position:absolute;inset:14px 14px 14px 14px;border-radius:7px;overflow:hidden;background:#fff}.ec-f img{width:100%;height:100%;object-fit:cover;display:block}
.ec-c{position:absolute;left:24px;bottom:24px;box-shadow:0 2px 8px rgba(15,27,69,.15)}.ec-tmp{position:absolute;right:24px;top:24px;background:rgba(15,27,69,.78);color:#fff;font-size:10.5px;font-weight:700;padding:2px 9px;border-radius:4px}
.ed{display:grid;grid-template-columns:62% 38%}.ed-p img{width:100%;height:100%;object-fit:cover;display:block}.ed-t{color:#fff;padding:18px 16px;display:flex;flex-direction:column;justify-content:flex-end}.ed-t span{font-size:10.5px;font-weight:700;opacity:.9}.ed-t b{font-size:24px;font-weight:900;line-height:1.25;margin-top:4px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}.pair .card{border:1px solid #E6E9F0;border-radius:12px;overflow:hidden;background:#fff}.pair .card .ey{border-radius:0}.pair .card p.t{font-weight:900;font-size:16px;line-height:1.5;padding:12px 16px 4px}.pair .card p.m{font-size:12px;color:#676688;padding:0 16px 14px}
.flow{display:flex;gap:10px;align-items:center;font-size:14px;margin-top:18px;flex-wrap:wrap}.flow span{background:#F7F8FB;border-radius:999px;padding:8px 14px}.flow b{color:#0141D4}'''
pats = [
 pat('E-A', 'タイトル文字型', 'カテゴリの淡い地色に、記事タイトルをそのまま大きく置きます。カードの下にもタイトルが出るため、同じ文字が2回並びます。',
     [('◎', 'タイトルだけで作れる'), ('△', 'カード下のタイトルと重複'), ('△', '長いタイトルは文字が小さくなる')], row(ea)),
 pat('E-B', 'キーワード型（ひと言を大きく）', '記事の中心になるひと言（「週2時間」「5つ」「20」など）だけを大きく置きます。タイトルはカードの下に出るので重複せず、並べたときに一覧で目に留まります。コースのサムネイル（T-B）と同じ地色・札で統一できます。',
     [('◎', '記事ごとに「ひと言」を決めるだけ'), ('◎', 'タイトルと重複しない'), ('○', 'データから自動で作れる')], row(eb), True),
 pat('E-C', '今ある画像を同じ枠に入れる（仮の運用）', '成果物・学び方・ポートフォリオの画像を、カテゴリ色の余白つきの枠に入れて、左下にカテゴリ札を重ねます。画像の雰囲気がバラバラでも、枠と札がそろうので一覧に統一感が出ます。記事のアイキャッチができるまでの仮として使えます。',
     [('◎', '新しい画像がいらない・すぐ使える'), ('○', '枠と札で統一感が出る'), ('△', '記事の内容と画像が完全には合わない')], row(ec)),
 pat('E-D', '画像＋キーワードの帯', '左に今ある画像、右にカテゴリ色の帯とキーワード。E-B と E-C の中間です。帯の色が強いので、一覧ではにぎやかになります。',
     [('○', '画像と言葉の両方が入る'), ('△', '帯の色が強く、トップでは目立ちすぎる')], row(ed)),
]
ex = lambda fn, a: f'<div class="card">{fn(a)}<p class="t">{a[1].replace("<wbr>", "")}</p><p class="m">{a[0]}・5分で読める</p></div>'
sim = '<section class="pat"><h2>記事カードに入れたときの見え方</h2><p class="d">左：いま（E-C 仮の画像）／右：記事がそろったあと（E-B キーワード）。どちらもカテゴリ札と地色が同じなので、途中で入れ替えても一覧の統一感は保てます。</p><div class="pair">' + ex(ec, ART[0]) + ex(eb, ART[0]) + '</div><div class="flow"><b>運用</b><span>① いまは E-C（今ある画像を枠に入れる・「仮の画像」表示）</span>→<span>② 記事を公開するときに「ひと言」を決めて E-B に差し替え</span></div></section>'
open('eye.html', 'w').write(board('記事のアイキャッチ　4つの型', 'トップ・学びのヒントの記事カードで使う画像の型です。記事がこれから増えるため、記事ごとに画像を探さずに作れるかを基準にしています。表示は6本分の例です。', pats + [sim], css))
