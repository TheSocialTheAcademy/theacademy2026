from common import *
import os
PH = os.path.dirname(os.path.abspath(__file__)) + '/ph/'
K = {'IT・デジタル': 'it', 'マーケティング': 'mk', '英語・TOEIC': 'en', 'ビジネス': 'biz', 'クリエイティブ': 'cr', 'キャリア・学び方': 'ca'}
ACC = {'it': '#1E9E62', 'mk': '#E46A1F', 'en': '#3E78FE', 'biz': '#8A70E8', 'cr': '#E8608F', 'ca': '#3E78FE'}  # 濃紺の地でも読める差し色
# 記事：カテゴリ, タイトル, 見出し（[]が強調）, アイコン, 写真, 写真の位置, 要点3つ, 数字
ART = [('キャリア・学び方', '働きながら学びを続けるための、週2時間のつくり方', '[週2時間]で<br>学びを続ける', 'clock', 'weekly', '25% 60%', ['スキマ時間を見つける', '30分×4回に分ける', '週末に振り返る'], '2h'),
       ('IT・デジタル', 'ChatGPTを仕事の相棒にする、最初の5つの使い方', 'ChatGPTを<br>仕事の[相棒]に', 'spark', 'chatgpt', '50% 50%', ['議事録の要約', 'メールの下書き', '企画のたたき台'], '5'),
       ('マーケティング', '顧客理解から始めるSNSキャンペーン設計', 'SNSは<br>[顧客理解]から', 'mega', 'sns', '60% 50%', ['誰に届けるか', '何を伝えるか', 'なぜ今か'], '3'),
       ('英語・TOEIC', '会議で使える、短い英語フレーズ20', '会議で使える<br>英語フレーズ[20]', 'chat', 'english', '50% 55%', ['相づち', '確認する', '提案する'], '20'),
       ('キャリア・学び方', '未経験から実績をつくる、ポートフォリオの育て方', '未経験から<br>[実績]をつくる', 'user', 'portfolio', '40% 50%', ['小さくつくる', '過程を残す', '公開する'], '3'),
       ('ビジネス', '小さなイベントを成功させる、当日の進行表のつくり方', '当日の[進行表]<br>のつくり方', 'calendar', 'event', '50% 50%', ['目的から逆算', 'キューを決める', '役割を分ける'], '3')]
hl = lambda s, tag='em': s.replace('[', f'<{tag}>').replace(']', f'</{tag}>')
# N-1 濃紺＋大見出し＋切り抜いた写真（経済メディア風）
def n1(a):
    c, t, h, icn, ph, pos, pts, num = a; k = K[c]; nm, col, bg = CAT[k]
    return (f'<div class="ey n1" style="--ac:{ACC[k]}"><div class="n1-ph"><img src="{PH}{ph}.jpg" style="object-position:{pos}" alt=""></div>'
            f'<p class="n1-c">{nm}</p><p class="n1-h">{hl(h)}</p><p class="n1-l">THE ACADEMY ｜ 学びのヒント</p></div>')
# N-2 写真全面＋大見出し（強調語にカテゴリ色の帯）
def n2(a):
    c, t, h, icn, ph, pos, pts, num = a; k = K[c]; nm, col, bg = CAT[k]
    return (f'<div class="ey n2" style="--ac:{col}"><img class="ph" src="{PH}{ph}.jpg" style="object-position:{pos}" alt=""><div class="n2-sh"></div>'
            f'<p class="n2-c">{ic(icn, "n2-i", 1.8)}{nm}</p><p class="n2-h">{hl(h)}</p></div>')
# N-3 要点型（ノート系で人気の「○つのポイント」）
def n3(a):
    c, t, h, icn, ph, pos, pts, num = a; k = K[c]; nm, col, bg = CAT[k]
    li = ''.join(f'<li><b>{i + 1}</b>{p}</li>' for i, p in enumerate(pts))
    return (f'<div class="ey n3" style="--cc:{col};--cb:{bg}"><div class="n3-l"><p class="n3-c">{nm}</p><p class="n3-h">{hl(h)}</p></div>'
            f'<div class="n3-r"><p class="n3-k">{ic(icn, "n3-i", 1.8)}ポイント</p><ol>{li}</ol></div></div>')
# N-4 マーカー型（白地に手書き風の蛍光ペン＋線のアイコン）
def n4(a):
    c, t, h, icn, ph, pos, pts, num = a; k = K[c]; nm, col, bg = CAT[k]
    return (f'<div class="ey n4" style="--cc:{col};--cb:{bg}">{ic(icn, "n4-i", 1.4)}<p class="n4-c">#{nm}</p><p class="n4-h">{hl(h, "mark")}</p>'
            f'<svg class="n4-sq" viewBox="0 0 100 20"><path d="M2 14 C 25 4, 45 18, 70 8 S 95 10, 98 6" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg><p class="n4-l">学びのヒント</p></div>')
def card(fn, a, title=True):
    nm, col, bg = CAT[K[a[0]]]
    return f'<div class="cd"><div class="th">{fn(a)}</div><div class="bd"><p class="mt"><span class="chip" style="--cc:{col};--cb:{bg}">{nm}</span>5分で読める</p>' + (f'<h3>{a[1]}</h3>' if title else '') + '</div></div>'
row = lambda fn: '<div class="grid g3">' + ''.join(card(fn, a) for a in ART) + '</div>'
css = '''.g3{grid-template-columns:repeat(3,1fr);gap:22px}.cd{background:#fff;border-radius:14px;box-shadow:0 0 0 1px #E6E9F0;overflow:hidden}.th{aspect-ratio:16/9}
.bd{padding:14px 18px 18px}.chip{display:inline-block;background:var(--cb);color:var(--cc);font-size:11.5px;font-weight:700;padding:2px 10px;border-radius:999px;margin-right:8px}.bd h3{font-size:16px;margin:8px 0 4px;line-height:1.5}.mt{font-size:12.5px;color:#676688}
.ey{position:relative;width:100%;height:100%;overflow:hidden;color:#0F1B45;word-break:keep-all;overflow-wrap:anywhere}.ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.n1{background:#0F1B45;color:#fff}.n1-ph{position:absolute;right:-30px;top:0;bottom:0;width:52%;clip-path:polygon(22% 0,100% 0,100% 100%,0 100%)}.n1-ph img{width:100%;height:100%;object-fit:cover;filter:saturate(.85)}
.n1-c{position:absolute;left:20px;top:16px;font-size:11px;font-weight:800;letter-spacing:.06em;color:var(--ac)}.n1-h{position:absolute;left:20px;top:50%;transform:translateY(-50%);width:60%;font-size:25px;font-weight:900;line-height:1.35}
.n1-h em{font-style:normal;color:#fff;background:linear-gradient(transparent 58%,var(--ac) 58%)}.n1-l{position:absolute;left:20px;bottom:14px;font-size:9.5px;font-weight:700;letter-spacing:.1em;opacity:.7}
.n2-sh{position:absolute;inset:0;background:linear-gradient(90deg,rgba(15,27,69,.82) 0%,rgba(15,27,69,.55) 55%,rgba(15,27,69,.1) 100%)}.n2{color:#fff}
.n2-c{position:absolute;left:20px;top:16px;display:flex;align-items:center;gap:6px;font-size:11.5px;font-weight:800}.n2-i{width:16px;height:16px}.n2-h{position:absolute;left:20px;bottom:20px;font-size:27px;font-weight:900;line-height:1.4}
.n2-h em{font-style:normal;background:var(--ac);padding:0 6px;border-radius:4px}
.n3{display:grid;grid-template-columns:55% 45%;background:#fff}.n3-l{padding:18px 10px 16px 20px;display:flex;flex-direction:column;justify-content:center;gap:8px}.n3-c{font-size:11px;font-weight:800;color:var(--cc)}
.n3-h{font-size:22px;font-weight:900;line-height:1.4}.n3-h em{font-style:normal;color:var(--cc)}.n3-r{background:var(--cb);padding:16px 16px;display:flex;flex-direction:column;justify-content:center}
.n3-k{display:flex;align-items:center;gap:5px;font-size:11px;font-weight:900;color:var(--cc);margin-bottom:8px}.n3-i{width:16px;height:16px}.n3 ol{list-style:none;display:grid;gap:6px}
.n3 li{display:flex;align-items:center;gap:8px;background:#fff;border-radius:8px;padding:6px 9px;font-size:12px;font-weight:800}.n3 li b{display:grid;place-items:center;width:18px;height:18px;border-radius:5px;background:var(--cc);color:#fff;font-size:10.5px;flex:none}
.n4{background:#FDFCF8}.n4-i{position:absolute;right:22px;top:20px;width:58px;height:58px;color:var(--cc);opacity:.9}.n4-c{position:absolute;left:22px;top:18px;font-size:11.5px;font-weight:800;color:var(--cc)}
.n4-h{position:absolute;left:22px;top:50%;transform:translateY(-46%);font-size:27px;font-weight:900;line-height:1.45}.n4-h mark{background:linear-gradient(transparent 55%,var(--cb) 55%,var(--cb) 92%,transparent 92%);color:inherit;box-shadow:0 0 0 0}
.n4 mark{background:linear-gradient(transparent 52%,color-mix(in srgb,var(--cc) 28%,#fff) 52%,color-mix(in srgb,var(--cc) 28%,#fff) 90%,transparent 90%)}
.n4-sq{position:absolute;left:22px;bottom:34px;width:70px;height:14px;color:var(--cc)}.n4-l{position:absolute;right:22px;bottom:16px;font-size:10px;font-weight:900;letter-spacing:.14em;color:#676688}
.cmp{width:100%;border-collapse:collapse;font-size:14px}.cmp th,.cmp td{border-bottom:1px solid #E6E9F0;padding:10px 12px;text-align:left}.cmp th{background:#F7F8FB;font-weight:700}
.alt{display:grid;grid-template-columns:1fr 1fr;gap:22px}.alt p.lbl{margin-bottom:8px}'''
pats = [
 pat('N-1', '濃紺＋大見出し＋写真（経済メディア風）', '濃紺の地に、記事の要点を2行の大見出しで。強調したい言葉にカテゴリ色の下線を引き、右側に斜めに切った写真を置きます。読み物としての「格」が出ます。',
     [('◎', '一覧で強く目立つ'), ('◎', 'コース（明るい色）とはっきり違う'), ('△', '濃紺が多いとページが重くなる')], row(n1)),
 pat('N-2', '写真全面＋大見出し', '写真を全面に敷き、左を暗くして白い大見出し。強調語にカテゴリ色の帯を敷きます。写真の雰囲気と見出しの両方が伝わります。',
     [('◎', '写真が主役で華やか'), ('○', '見出しが読みやすい'), ('△', '写真の明るさで印象が変わる')], row(n2)),
 pat('N-3', '要点型（○つのポイント）', '左に見出し、右に要点3つ。ノート系の記事で人気の「この記事で分かること」を1枚にした型です。写真がいらず、中身が一番具体的に伝わります。',
     [('◎', '中身が一番具体的'), ('◎', '写真なしで作れる（自動生成も可）'), ('△', '情報量が多く、スマホでは文字が小さい')], row(n3), True),
 pat('N-4', 'マーカー型（白地＋蛍光ペン）', '白地に大見出し、強調語にカテゴリ色の蛍光ペン、右上に線のアイコン。手書きノートのような親しみやすさで、個人の発信でよく見る表紙です。',
     [('○', '親しみやすい・軽い'), ('◎', '写真なしで作れる'), ('△', '一覧で目立つ力は弱め')], row(n4)),
]
alt = ('<section class="pat"><h2>見出しを画像に入れるときの注意</h2><p class="d">この型は画像の中に見出しを入れるので、カードの下のタイトルと内容が重なります。ノートなどと同じく「画像は短い見出し・カードは正式なタイトル」と役割を分ければ自然です。重なりが気になる場合は、カードのタイトルを外して画像だけで見せる方法もあります。</p>'
       '<div class="alt"><div><p class="lbl">カードのタイトルあり（いまの作り）</p>' + card(n3, ART[1]) + '</div><div><p class="lbl">カードのタイトルなし（画像だけで見せる）</p>' + card(n3, ART[1], False) + '</div></div></section>')
cmp = ('<section class="pat"><h2>比べると（前回の P-3 と並べて）</h2><table class="cmp"><tr><th></th><th>N-1 濃紺＋大見出し</th><th>N-2 写真＋大見出し</th><th>N-3 要点型</th><th>N-4 マーカー型</th><th>前回 P-3 写真＋内容カード</th></tr>' + ''.join('<tr>' + ''.join(f'<{"th" if j == 0 else "td"}>{v}</{"th" if j == 0 else "td"}>' for j, v in enumerate(r)) + '</tr>' for r in [
 ('中身が伝わる', '○ 見出し', '○ 見出し', '◎ 要点3つ', '○ 見出し', '◎ 中身の画面'), ('一覧で目立つ', '◎', '◎', '○', '△', '○'), ('コースとの見分け', '◎', '◎', '◎', '◎', '◎'),
 ('写真', '必要', '必要', 'いらない', 'いらない', '必要'), ('作る手間', '見出し＋写真', '見出し＋写真', '見出し＋要点3つ', '見出し', '写真＋カードの型')]) + '</table>'
       '<p class="d" style="margin-top:14px">おすすめは <b>N-3 要点型</b>。写真を探さずに、見出しと要点3つだけで作れ、記事の中身が一番具体的に伝わります。「この記事で何が分かるか」が先に見えるので、読む前の不安が減ります。目立たせたい特集記事だけ N-1 を使う、という組み合わせもできます。</p></section>')
open('eye4.html', 'w').write(board('記事のアイキャッチ　1枚で表す表紙の4つの型', '経済メディアの記事表紙や、ノートで人気の記事表紙の「表現」（大見出し・強調語・要点・蛍光ペン）を参考に、いまのカテゴリ色で作り直しました。特定のサービスのデザインやロゴは写していません。', pats + [alt, cmp], css))
