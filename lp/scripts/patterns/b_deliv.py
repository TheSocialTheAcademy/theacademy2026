from common import *; from mock import mock, MOCK_CSS
SEL = [C[0], C[2], C[7]]
badge = '<span class="sk">作例</span>'
def da(c):
    s, n, k, i, lv, f, d, kind, items = c; nm, col, bg = CAT[k]
    pk = 'phone' if kind != 'phone' else 'doc'
    return f'<div class="dv da" style="background:{bg}">{badge}<div class="da-pc"><p class="da-top"><span></span><span></span><span></span></p><div class="da-sc">{mock("slide" if kind == "phone" else kind, items, col, d)}</div></div><div class="da-ph">{mock("phone", items, col, d)}</div><p class="dv-n">{d}</p></div>'
def db(c):
    s, n, k, i, lv, f, d, kind, items = c; nm, col, bg = CAT[k]
    return f'<div class="dv db" style="background:{bg}">{badge}<div class="db-m">{mock(kind, items, col, d)}</div><div class="db-t"><span class="kk" style="color:{col}">{nm}</span><p>{d}</p><small>{n}でつくる</small></div></div>'
def dc(c):
    s, n, k, i, lv, f, d, kind, items = c; nm, col, bg = CAT[k]
    memo = ''.join(f'<span style="transform:rotate({r}deg)">{t}？</span>' for t, r in zip(items[:3], (-4, 3, -2)))
    return f'<div class="dv dc" style="background:#F7F8FB">{badge}<div class="dc-b"><p class="dc-l">受講前</p><div class="dc-memo">{memo}</div></div><span class="dc-a" style="color:{col}">→</span><div class="dc-a2" style="background:{bg}"><p class="dc-l" style="color:{col}">受講後</p><div class="dc-m">{mock(kind, items, col, d)}</div></div></div>'
def dd(c):
    s, n, k, i, lv, f, d, kind, items = c; nm, col, bg = CAT[k]
    its = ''.join(f'<li><b style="color:{col}">{j + 1:02d}</b>{t}</li>' for j, t in enumerate(items[:4]))
    return f'<div class="dv dd" style="background:{bg};--cc:{col}">{badge}<span class="kk" style="color:{col}">完成する成果物</span><p class="dd-n">{d}</p><ol>{its}</ol>{ic(i, "dd-i", 1.2)}</div>'
row = lambda fn, cs=SEL: '<div class="grid g3">' + ''.join(f'<div>{fn(c)}<p class="cap">{c[1]}</p></div>' for c in cs) + '</div>'
css = MOCK_CSS + '''.g3{grid-template-columns:repeat(3,1fr)}.g4{grid-template-columns:repeat(4,1fr);gap:14px}.dv{position:relative;aspect-ratio:1.9/1;border-radius:10px;overflow:hidden;word-break:keep-all;overflow-wrap:anywhere}
.sk{position:absolute;right:10px;top:8px;z-index:3;background:rgba(15,27,69,.78);color:#fff;font-size:10.5px;font-weight:700;padding:2px 9px;border-radius:4px;letter-spacing:.06em}
.kk{font-size:11px;font-weight:700}.dv-n{position:absolute;left:14px;bottom:10px;font-size:12px;font-weight:900;background:#fff;padding:3px 10px;border-radius:999px}
.da-pc{position:absolute;left:7%;top:12%;width:66%;height:78%;background:#fff;border:2px solid #0F1B45;border-radius:8px;overflow:hidden}.da-top{height:16px;background:#0F1B45;display:flex;gap:4px;align-items:center;padding:0 7px}.da-top span{width:5px;height:5px;border-radius:50%;background:#fff;opacity:.6}
.da-sc{position:absolute;inset:16px 0 0;--mk:6.4px}.da-sc .mk-pg{inset:4% 6%;box-shadow:none}.da-sc .mk-pg2{display:none}.da-ph{position:absolute;right:6%;top:18%;width:24%;height:76%;--mk:5.6px}.da-ph .mk-phone{width:100%;height:100%}
.db{display:grid;grid-template-columns:58% 42%}.db-m{position:relative;--mk:7.6px}.db-t{padding:20px 18px 18px 4px;display:flex;flex-direction:column;justify-content:center}.db-t p{font-size:17px;font-weight:900;line-height:1.4;margin:4px 0 6px}.db-t small{font-size:11px;color:#676688}
.dc{display:grid;grid-template-columns:38% 8% 54%;align-items:center;padding:0 0 0 14px}.dc-l{font-size:11px;font-weight:900;color:#676688;margin-bottom:6px}.dc-memo{display:flex;flex-direction:column;gap:7px}
.dc-memo span{background:#FFF8D6;border:1px solid #EFE3A2;font-size:11.5px;font-weight:700;padding:6px 9px;width:max-content;max-width:100%;box-shadow:0 2px 4px rgba(0,0,0,.06)}.dc-a{font-size:26px;font-weight:900;text-align:center}
.dc-a2{height:100%;padding:28px 0 0 10px;position:relative}.dc-a2 .dc-l{position:absolute;left:12px;top:10px}.dc-m{position:absolute;inset:26px 0 0 0;--mk:6.6px}
.dd{padding:30px 22px 16px}.dd-n{font-size:18px;font-weight:900;line-height:1.35;margin:2px 0 10px;max-width:78%}.dd ol{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:6px 8px;max-width:84%}
.dd li{background:#fff;border-radius:6px;padding:6px 9px;font-size:12px;font-weight:700;display:flex;gap:6px;white-space:nowrap}.dd-i{position:absolute;right:-14px;bottom:-14px;width:110px;height:110px;color:var(--cc);opacity:.22}
.flow{display:flex;gap:10px;align-items:center;font-size:14px;margin-top:18px;flex-wrap:wrap}.flow span{background:#F7F8FB;border-radius:999px;padding:8px 14px}.flow b{color:#0141D4}'''
pats = [
 pat('D-A', '端末の枠＋実物の画面', 'パソコンとスマホの枠に、実際の成果物の画面（スクリーンショット）を入れます。図は枠の見本で、中身は実物に差し替えます。',
     [('◎', '本物なので信頼感が高い'), ('×', '実際の成果物（受講生の許可・スタッフ作成の見本）が必要'), ('△', '画面の中の文字は小さくなる')], row(da)),
 pat('D-B', '成果物の模型（書類・画面を重ねる）', '成果物を「企画書・スマホ画面・表・チャット・スライド」の5種類の模型で描き、名前と見出しを入れます。コース一覧のデータ（成果物名・見出し）から作れるので、実物がそろうまでの標準に向きます。サムネイル T-C と同じ模型です。',
     [('◎', 'データから自動で作れる・全コースそろう'), ('○', '何をつくるかが分かる'), ('△', '実物ではない（「作例」と明記）')], row(db), True),
 pat('D-C', '受講前 → 受講後', '左に受講前の「バラバラのメモ・疑問」、右に完成した成果物。変化が伝わりますが、横に広い場所でないと読みにくくなります。',
     [('○', '学ぶ意味が伝わる'), ('△', 'スマホでは小さい'), ('△', '受講前の言葉を毎回考える必要')], row(dc)),
 pat('D-D', '中身の見取り図（文字だけ）', '成果物の名前と、中に入る項目を番号つきで並べます。画像を作らずに済み、Wix のテキストでも組めます。',
     [('◎', '一番かんたん・更新しやすい'), ('○', '中身が具体的に分かる'), ('△', '見た目の印象は弱い')], row(dd)),
]
allc = '<section class="pat"><h2><em class="rec">D-B</em>全13コースに当てはめた例</h2><p class="d">成果物名と中身は、今のサイトの章立て（カリキュラム）から仮に付けています。実物ができたコースから D-A（実物の画面）に差し替える運用がおすすめです。</p><div class="grid g3">' + ''.join(f'<div>{db(c)}<p class="cap">{c[1]}</p></div>' for c in C) + '</div><div class="flow"><b>運用</b><span>① いまは D-B の模型（作例と表示）</span>→<span>② 実物ができたら D-A に差し替え</span>→<span>③ 受講生の作品は許可を取ってポートフォリオと共有</span></div></section>'
open('deliv.html', 'w').write(board('コースの成果物画像　4つの型', 'コース詳細ページの大きな画像（完成する成果物）に使う画像の型です。すべてに「作例」と表示します。表示はCanva初級・イベントデザイン・自動化ツール開発の3コース分の例です。', pats + [allc], css))
