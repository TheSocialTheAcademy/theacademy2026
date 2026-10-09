from common import *
import os
PH = os.path.dirname(os.path.abspath(__file__)) + '/ph/'
T = '/home/user/theacademy2026/lp/assets/thumbs/'
K = {'IT・デジタル': 'it', 'マーケティング': 'mk', '英語・TOEIC': 'en', 'ビジネス': 'biz', 'クリエイティブ': 'cr', 'キャリア・学び方': 'ca'}
CHK = '<svg viewBox="0 0 24 24" class="ck"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
HEART = '<svg viewBox="0 0 24 24" class="hs"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" fill="currentColor"/></svg>'
# 記事：カテゴリ, タイトル, ひと言, 補足, アイコン, 写真, 写真の位置, 内容カードの種類, 中身
ART = [
 ('キャリア・学び方', '働きながら学びを続けるための、週2時間のつくり方', '週2時間', 'のつくり方', 'clock', 'weekly', '30% 60%', 'cal', [('月', '30分'), ('水', '30分'), ('土', '60分')]),
 ('IT・デジタル', 'ChatGPTを仕事の相棒にする、最初の5つの使い方', '5つ', 'ChatGPTの使い方', 'spark', 'chatgpt', '50% 50%', 'chat', ['会議メモを要約して', '決定事項は3つです。①…']),
 ('マーケティング', '顧客理解から始めるSNSキャンペーン設計', '顧客理解', 'から始めるSNS設計', 'mega', 'sns', '60% 50%', 'post', ['ペルソナ：30代・会社員', '平日の朝、通勤中に見る']),
 ('英語・TOEIC', '会議で使える、短い英語フレーズ20', '20', '会議の英語フレーズ', 'chat', 'english', '50% 60%', 'talk', ['Could you clarify that?', 'That makes sense.']),
 ('キャリア・学び方', '未経験から実績をつくる、ポートフォリオの育て方', '実績', 'をつくるポートフォリオ', 'user', 'portfolio', '40% 50%', 'prof', ['制作実績', '3件']),
 ('ビジネス', '小さなイベントを成功させる、当日の進行表のつくり方', '進行表', '当日のつくり方', 'calendar', 'event', '50% 50%', 'time', [('13:00', '受付'), ('13:30', '開会'), ('14:00', 'ワーク')]),
]
def mini(a):  # 内容カード（記事の中身を小さな画面で見せる）
    c, t, kw, sub, icn, ph, pos, kind, it = a; nm, col, bg = CAT[K[c]]
    head = lambda s: f'<p class="mc-h">{ic(icn, "mc-i", 1.8)}{s}</p>'
    if kind == 'cal':
        rows = ''.join(f'<li><b>{d}</b><span class="bar" style="width:{int(m[:-1]) * 1.1}px"></span><small>{m}</small></li>' for d, m in it)
        return f'<div class="mc" style="--cc:{col}">{head("今週の学習")}<ul class="mc-cal">{rows}</ul><p class="mc-f">{CHK}合計 2時間</p></div>'
    if kind == 'chat':
        return f'<div class="mc" style="--cc:{col}">{head("AIに頼む")}<p class="mc-me">{it[0]}</p><p class="mc-ai">{it[1]}</p></div>'
    if kind == 'post':
        return f'<div class="mc" style="--cc:{col}">{head("届けたい相手")}<p class="mc-b">{it[0]}</p><p class="mc-s">{it[1]}</p><p class="mc-like">{HEART}128　保存 42</p></div>'
    if kind == 'talk':
        return f'<div class="mc mc--talk" style="--cc:{col}"><p class="mc-q">{it[0]}</p><p class="mc-a">{it[1]}</p></div>'
    if kind == 'prof':
        return f'<div class="mc" style="--cc:{col}"><div class="mc-pf"><span class="av">{ic("user", "", 1.8)}</span><div><b>マーケティング職</b><small>ポートフォリオ</small></div></div><p class="mc-n"><small>{it[0]}</small>{it[1]}</p></div>'
    rows = ''.join(f'<li><b>{tm}</b><span>{x}</span></li>' for tm, x in it)
    return f'<div class="mc" style="--cc:{col}">{head("当日の進行表")}<ul class="mc-tl">{rows}</ul></div>'
# P-1：写真＋ひと言のカード
def p1(a):
    c, t, kw, sub, icn, ph, pos = a[:7]; nm, col, bg = CAT[K[c]]
    return f'<div class="ey" style="--cc:{col}"><img class="ph" src="{PH}{ph}.jpg" style="object-position:{pos}" alt=""><div class="kc">{ic(icn, "kc-i", 1.8)}<p class="kc-k">{kw}</p><p class="kc-s">{sub}</p></div></div>'
# P-2：淡い色のパネル（ひと言＋アイコン）＋写真
def p2(a):
    c, t, kw, sub, icn, ph, pos = a[:7]; nm, col, bg = CAT[K[c]]
    return f'<div class="ey p2" style="--cc:{col};background:{bg}"><div class="p2-t">{ic(icn, "p2-i", 1.6)}<p class="p2-k">{kw}</p><p class="p2-s">{sub}</p></div><img class="p2-ph" src="{PH}{ph}.jpg" style="object-position:{pos}" alt=""></div>'
# P-3：写真＋内容カード（記事の中身を小さな画面で）
def p3(a):
    c, t, kw, sub, icn, ph, pos = a[:7]; nm, col, bg = CAT[K[c]]
    return f'<div class="ey p3" style="--cc:{col}"><img class="ph" src="{PH}{ph}.jpg" style="object-position:{pos}" alt=""><div class="p3-sh"></div>{mini(a)}</div>'
def card(fn, a):
    nm, col, bg = CAT[K[a[0]]]
    return f'<div class="cd"><div class="th">{fn(a)}</div><div class="bd"><p class="mt"><span class="chip" style="--cc:{col};--cb:{bg}">{nm}</span>5分で読める</p><h3>{a[1]}</h3></div></div>'
row = lambda fn: '<div class="grid g3">' + ''.join(card(fn, a) for a in ART) + '</div>'
def course(slug, name, k, meta):
    nm, col, bg = CAT[k]
    return f'<div class="cd"><div class="th th--c"><img src="{T}{slug}.webp" alt=""></div><div class="bd"><p class="mt"><span class="chip" style="--cc:{col};--cb:{bg}">{nm}</span>{meta}</p><h3>{name}</h3></div></div>'
mix = lambda fn: ('<p class="lbl">コース（いまのサムネイル）</p><div class="grid g3">' + course('sns-marketing', 'SNSマーケティング実践', 'mk', '8週間') + course('ai-efficiency', '生成AI 業務改善', 'it', '6週間') + course('toeic-700', 'TOEIC L&R 700点突破', 'en', '3か月') + '</div>'
                  + '<p class="lbl" style="margin-top:18px">記事（この型）</p><div class="grid g3">' + ''.join(card(fn, a) for a in ART[:3]) + '</div>')
css = '''.g3{grid-template-columns:repeat(3,1fr);gap:22px}.cd{background:#fff;border-radius:14px;box-shadow:0 0 0 1px #E6E9F0;overflow:hidden}.th{aspect-ratio:16/9}.th--c{aspect-ratio:16/10}.th--c img{width:100%;height:100%;object-fit:cover;display:block}
.bd{padding:14px 18px 18px}.chip{display:inline-block;background:var(--cb);color:var(--cc);font-size:11.5px;font-weight:700;padding:2px 10px;border-radius:999px;margin-right:8px}.bd h3{font-size:16px;margin:8px 0 4px;line-height:1.5}.mt{font-size:12.5px;color:#676688}
.ey{position:relative;width:100%;height:100%;overflow:hidden;color:#0F1B45;word-break:keep-all;overflow-wrap:anywhere}.ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.kc{position:absolute;left:16px;bottom:16px;background:#fff;border-radius:12px;padding:12px 16px 12px;box-shadow:0 10px 26px rgba(15,27,69,.22);min-width:44%}.kc-i{width:20px;height:20px;color:var(--cc);display:block;margin-bottom:4px}.kc-k{font-size:30px;font-weight:900;line-height:1.05;color:var(--cc)}.kc-s{font-size:12.5px;font-weight:800;margin-top:4px}
.p2{display:grid;grid-template-columns:46% 54%}.p2-t{padding:18px 8px 16px 20px;display:flex;flex-direction:column;justify-content:flex-end}.p2-i{width:26px;height:26px;color:var(--cc);margin-bottom:auto}.p2-k{font-size:34px;font-weight:900;line-height:1.05;color:var(--cc)}.p2-s{font-size:12.5px;font-weight:800;margin-top:6px}
.p2-ph{width:calc(100% - 14px);height:calc(100% - 28px);margin:14px 14px 14px 0;object-fit:cover;border-radius:10px}
.p3-sh{position:absolute;inset:0;background:linear-gradient(90deg,rgba(15,27,69,0) 30%,rgba(15,27,69,.35) 100%)}
.mc{position:absolute;right:14px;top:50%;transform:translateY(-50%);width:52%;background:#fff;border-radius:12px;padding:11px 13px;box-shadow:0 12px 28px rgba(15,27,69,.25);font-size:11.5px}
.mc-h{display:flex;align-items:center;gap:6px;font-weight:900;font-size:11.5px;margin-bottom:7px}.mc-i{width:16px;height:16px;color:var(--cc)}
.mc-cal{list-style:none;display:grid;gap:5px}.mc-cal li{display:grid;grid-template-columns:18px 1fr auto;align-items:center;gap:6px}.mc-cal b{font-size:11px}.mc-cal .bar{height:7px;border-radius:4px;background:var(--cc)}.mc-cal small{color:#676688;font-size:10.5px}
.mc-f{display:flex;align-items:center;gap:4px;margin-top:7px;padding-top:6px;border-top:1px solid #EEF0F5;font-weight:800;color:var(--cc)}.ck{width:13px;height:13px}
.mc-me{margin-left:auto;width:max-content;max-width:90%;background:#F1F3F8;border-radius:10px 10px 2px 10px;padding:5px 9px;font-weight:700}.mc-ai{margin-top:6px;width:max-content;max-width:92%;background:var(--cc);color:#fff;border-radius:10px 10px 10px 2px;padding:5px 9px;font-weight:700}
.mc-b{font-weight:900;font-size:12.5px}.mc-s{color:#676688;margin-top:2px}.mc-like{display:flex;align-items:center;gap:4px;margin-top:7px;padding-top:6px;border-top:1px solid #EEF0F5;color:#676688;font-size:10.5px}.hs{width:13px;height:13px;color:#E8608F}
.mc--talk{background:none;box-shadow:none;padding:0;display:grid;gap:6px}.mc-q,.mc-a{background:#fff;border-radius:12px 12px 12px 3px;padding:7px 11px;font-weight:800;font-size:12px;width:max-content;box-shadow:0 8px 20px rgba(15,27,69,.22)}.mc-a{margin-left:auto;background:var(--cc);color:#fff;border-radius:12px 12px 3px 12px}
.mc-pf{display:flex;gap:8px;align-items:center}.av{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#EEF1F6;color:var(--cc)}.av svg{width:17px;height:17px}.mc-pf b{display:block;font-size:12px}.mc-pf small{color:#676688;font-size:10.5px}
.mc-n{margin-top:7px;padding-top:6px;border-top:1px solid #EEF0F5;font-size:22px;font-weight:900;color:var(--cc);line-height:1}.mc-n small{font-size:10.5px;color:#676688;font-weight:700;margin-right:6px}
.mc-tl{list-style:none;display:grid;gap:4px;border-left:2px solid var(--cc);padding-left:8px}.mc-tl li{display:flex;gap:8px}.mc-tl b{font-size:11px;color:var(--cc);font-weight:800}
.cmp{width:100%;border-collapse:collapse;font-size:14px}.cmp th,.cmp td{border-bottom:1px solid #E6E9F0;padding:10px 12px;text-align:left}.cmp th{background:#F7F8FB;font-weight:700}
.note{font-size:12.5px;color:#676688;margin-top:14px;line-height:1.7}'''
pats = [
 pat('P-1', '写真＋ひと言のカード', '記事に関係する写真を全面に敷き、左下に白いカード（アイコン・ひと言・補足）を重ねます。写真だけでは分からない「何の記事か」をカードで補います。',
     [('○', '作りがシンプル'), ('○', '写真の雰囲気が生きる'), ('△', 'カードが写真の一部を隠す')], row(p1)),
 pat('P-2', '淡い色のパネル＋写真', '左はカテゴリの淡い色のパネル（アイコン・ひと言）、右に角丸の写真。写真の明るさがバラバラでも、パネルで一覧の統一感が保てます。',
     [('◎', '一覧の統一感が出る'), ('○', 'ひと言が読みやすい'), ('△', '写真が小さくなる')], row(p2)),
 pat('P-3', '写真＋内容カード（記事の中身を小さな画面で）', '写真の上に、記事の中身を表す小さな画面（学習の予定表・AIとのやりとり・ペルソナ・英語の会話・ポートフォリオ・進行表）を重ねます。写真で場面、カードで中身、アイコンでテーマが伝わります。カードは7種類の型から選び、文字を入れ替えるだけで作れます。',
     [('◎', '記事の中身が一番伝わる'), ('◎', '記事ごとに絵が変わる'), ('○', 'カードは型から選んで文字を入れるだけ')], row(p3), True),
 '<section class="pat"><h2><em class="rec">P-3</em>トップで、コースと記事が並んだとき</h2><p class="d">コースは「色と形」、記事は「写真」。素材が違うので、ひと目で「コース」と「読み物」が分かれます。</p>' + mix(p3) + '</section>',
]
cmp = ('<section class="pat"><h2>比べると</h2><table class="cmp"><tr><th></th><th>P-1 写真＋ひと言</th><th>P-2 パネル＋写真</th><th>P-3 写真＋内容カード</th></tr>' + ''.join('<tr>' + ''.join(f'<{"th" if j == 0 else "td"}>{v}</{"th" if j == 0 else "td"}>' for j, v in enumerate(r)) + '</tr>' for r in [
 ('コースとの見分け', '◎ 写真', '◎ 写真', '◎ 写真'), ('記事の中身が伝わる', '○ ひと言', '○ ひと言', '◎ 中身の画面'), ('一覧の統一感', '△ 写真次第', '◎ パネルでそろう', '○ カードでそろう'),
 ('作る手間', '写真＋ひと言', '写真＋ひと言', '写真＋カードの型と文字')]) + '</table>'
       '<p class="d" style="margin-top:14px">おすすめは <b>P-3</b>。写真（場面）・カード（中身）・アイコン（テーマ）の3つで、タイトルを読む前に記事の内容が想像できます。カードは「予定表・チャット・ペルソナ・会話・プロフィール・進行表・チェックリスト」の7種類から選ぶだけなので、記事が増えても同じ作りで続けられます。</p>'
       '<p class="note">写真はすべて CC0（パブリックドメイン、Openverse 経由の rawpixel・StockSnap）です。ロゴや人の顔がはっきり写るものは避けました。採用する場合は、出典を assets/photos/CREDITS.md に記録します。</p></section>')
open('eye3.html', 'w').write(board('記事のアイキャッチ　写真・カード・アイコンで表す3つの型', '記事に関係する写真（CC0）に、カードとアイコンを組み合わせました。カードの下にタイトルが出るため、画像にはタイトルを書いていません。', pats + [cmp], css))
