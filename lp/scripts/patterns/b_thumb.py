from common import *; from mock import mock, MOCK_CSS
import os; A = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets') + '/'
SEL = [C[0], C[1], C[2], C[3], C[4], C[7]]
PH = {'mk': A + 'photos/sns-phone.webp', 'it': A + 'photos/ai-laptop.webp', 'en': A + 'illust/for-you-1.webp', 'biz': A + 'illust/next-zoom.webp', 'cr': A + 'illust/for-you-2.webp'}
def ta(c):
    s, n, k, i, lv, f = c[:6]; nm, col, bg = CAT[k]
    return f'<div class="th ta" style="background:{col}"><p class="th-l">THE ACADEMY</p><p class="ta-n">{n}</p><p class="ta-c">COURSE</p><span class="ta-p" style="color:{col}">{lv}</span>{ic(i, "ta-i", 1.4)}</div>'
def tb(c):
    s, n, k, i, lv, f = c[:6]; nm, col, bg = CAT[k]
    return f'<div class="th tb" style="background:{bg};--cc:{col}"><span class="tb-k">{nm}</span>{ic(i, "tb-i", 1.3)}<p class="tb-n">{n}</p><p class="tb-f">{lv}・{f}</p><p class="th-l tb-l">THE ACADEMY</p></div>'
def tc(c):
    s, n, k, i, lv, f, d, kind, items = c; nm, col, bg = CAT[k]
    return f'<div class="th tc" style="background:{bg};--cc:{col}"><div class="tc-t"><span class="tb-k">{nm}</span><p class="tc-n">{n}</p><p class="tc-d">つくるもの<b>{d}</b></p></div><div class="tc-m">{mock(kind, items, col, d)}</div></div>'
def td(c):
    s, n, k, i, lv, f = c[:6]; nm, col, bg = CAT[k]
    return f'<div class="th td"><div class="td-p" style="background-image:url({PH[k]})"></div><div class="td-b" style="border-color:{col}"><span style="color:{col}">{nm}</span><p>{n}</p></div></div>'
row = lambda fn, cs=SEL: '<div class="grid g3">' + ''.join(f'<div>{fn(c)}<p class="cap">{c[1]}</p></div>' for c in cs) + '</div>'
css = MOCK_CSS + '''.g3{grid-template-columns:repeat(3,1fr)}.th{word-break:keep-all;overflow-wrap:anywhere;position:relative;aspect-ratio:16/9;border-radius:10px;overflow:hidden}
.th-l{font-size:10px;font-weight:900;letter-spacing:.16em}
.ta{color:#fff;padding:22px 24px}.ta-n{font-size:27px;font-weight:900;line-height:1.25;margin-top:30px;max-width:66%;position:relative;z-index:1}.ta-c{font-size:24px;font-weight:900;letter-spacing:.04em;line-height:1.1;position:relative;z-index:1}
.ta-p{display:inline-block;background:#fff;border-radius:999px;font-size:11px;font-weight:700;padding:3px 12px;margin-top:10px}.ta-i{position:absolute;right:-26px;top:50%;width:170px;height:170px;transform:translateY(-50%);color:rgba(255,255,255,.9)}
.tb{padding:20px 22px;color:#0F1B45}.tb-k,.tc .tb-k{display:inline-block;background:#fff;color:var(--cc);font-size:11px;font-weight:700;padding:3px 10px;border-radius:999px}
.tb-i{position:absolute;right:22px;top:22px;width:96px;height:96px;color:var(--cc)}.tb-n{position:absolute;left:22px;right:120px;bottom:44px;font-size:23px;font-weight:900;line-height:1.3}
.tb-f{position:absolute;left:22px;bottom:20px;font-size:12px;color:#4A4E6A;font-weight:500}.tb-l{position:absolute;right:22px;bottom:20px;color:var(--cc);opacity:.8}
.tc{display:grid;grid-template-columns:52% 48%}.tc-t{padding:18px 0 16px 20px;display:flex;flex-direction:column;align-items:flex-start}.tc-n{font-size:20px;font-weight:900;line-height:1.3;margin-top:10px}
.tc-d{margin-top:auto;font-size:10.5px;color:#676688;font-weight:700}.tc-d b{display:block;color:#0F1B45;font-size:12px;line-height:1.45;margin-top:2px}.tc-m{--mk:7.2px;position:relative}
.td{background:#fff;display:flex;flex-direction:column;border:1px solid #E1E5EE}.td-p{flex:1;background-size:cover;background-position:center}.td-b{border-left:5px solid;padding:9px 14px 10px;background:#fff}
.td-b span{font-size:11px;font-weight:700}.td-b p{font-size:17px;font-weight:900;line-height:1.3}
.spec{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:20px}.spec div{background:#F7F8FB;border-radius:10px;padding:12px 14px;font-size:13px;line-height:1.6;color:#4A4E6A}.spec b{display:block;color:#0F1B45;font-size:13.5px;margin-bottom:2px}
.cmp{width:100%;border-collapse:collapse;font-size:14px;margin-top:6px}.cmp th,.cmp td{border-bottom:1px solid #E6E9F0;padding:10px 12px;text-align:left}.cmp th{background:#F7F8FB;font-weight:700}.cmp td.o{color:#1E9E62;font-weight:700}.cmp td.x{color:#C2410C;font-weight:700}'''
spec = lambda xs: '<div class="spec">' + ''.join(f'<div><b>{a}</b>{b}</div>' for a, b in xs) + '</div>'
pats = [
 pat('T-A', '色ベタ＋大きな線アイコン（今のサイトの型を整理）', '今の theacademyjapan.org のサムネイルと同じ構成（THE ACADEMY・コース名・COURSE・タグ・右の大きなアイコン）。グラデーションと丸バッジをやめ、色はカテゴリ5色に固定します。',
     [('◎', '今のサイトから違和感なく移れる'), ('○', '一覧で目立つ'), ('△', '一覧に並ぶと色が強く、ページの青と競合しやすい')], row(ta) + spec([('入れ替えるもの', 'コース名・タグ・アイコン'), ('固定するもの', '色（カテゴリで決まる）・文字位置・サイズ'), ('作り方', 'Canva / Figma のテンプレ1枚'), ('新コース追加', '5分（文字とアイコンを差し替え）')])),
 pat('T-B', '淡い色＋線アイコン（新サイトの色づかいに合わせる）', '「コースを探す」のカテゴリ色（淡い地色＋濃い線）と同じ配色。白いカテゴリ札・コース名・レベルと時間・右上のアイコンだけで構成します。文字の量が決まっているので、コースが増えても崩れません。',
     [('◎', 'ページ全体の青・白と調和する'), ('◎', '文字とアイコンだけなので自動で作れる'), ('△', '中身（成果物）は伝わらない')], row(tb) + spec([('入れ替えるもの', 'コース名・レベル・時間・アイコン'), ('固定するもの', '地色と線の色（カテゴリ）・配置'), ('作り方', 'テンプレ1枚／コース一覧のデータから自動生成も可'), ('新コース追加', '3分（データ1行を足すだけ）')]), True),
 pat('T-C', '淡い色＋成果物の模型（何をつくるかを見せる）', 'T-B の右半分に、そのコースでつくる成果物の模型（企画書・スマホ画面・表・チャット・スライドの5種類から選ぶ）を置きます。「学んで、つくる」が一覧の段階で伝わります。',
     [('◎', 'つくるものが一目で分かる'), ('○', '模型は5種類の使い回し'), ('△', '小さいサイズでは模型の文字が読めない')], row(tc) + spec([('入れ替えるもの', 'コース名・成果物名・模型の種類と見出し'), ('固定するもの', '模型5種類・配色・配置'), ('作り方', 'テンプレ5枚（模型の種類ごと）'), ('新コース追加', '10分')])),
 pat('T-D', '写真＋カテゴリの帯', '上に写真、下にカテゴリ色の線とコース名。雰囲気は伝わりますが、コースごとに合う写真を毎回探す必要があります（今ある写真は3枚）。',
     [('○', '人や場面が伝わる'), ('×', 'コースが増えるたびに写真選びが必要'), ('×', '写真の明るさや雰囲気がそろいにくい')], row(td)),
]
cmp = '<section class="pat"><h2>比べると</h2><table class="cmp"><tr><th></th><th>T-A 色ベタ</th><th>T-B 淡い色</th><th>T-C 成果物の模型</th><th>T-D 写真</th></tr>' + ''.join(f'<tr><th>{r[0]}</th>' + ''.join(f'<td class="{ "o" if v.startswith("◎") else ("x" if v.startswith("×") else "") }">{v}</td>' for v in r[1:]) + '</tr>' for r in [
 ('統一しやすさ', '◎ 色と配置が固定', '◎ 色と配置が固定', '○ 模型5種類', '× 写真次第'), ('生成のしやすさ', '○ テンプレ差し替え', '◎ データから自動', '○ テンプレ5枚', '× 写真選び'), ('新サイトとの調和', '△ 色が強い', '◎', '◎', '○'),
 ('中身が伝わる', '△', '△', '◎', '○'), ('今のサイトからの移行', '◎ 同じ型', '○', '○', '△')]) + '</table><p class="d" style="margin-top:14px">おすすめは <b>T-B を標準</b>にして、コース詳細の大きな画像やおすすめ枠だけ <b>T-C</b> を使う組み合わせです。どちらも同じ地色・同じカテゴリ札なので、並んでも統一感が保てます。</p></section>'
open('thumb.html', 'w').write(board('コースのサムネイル　4つの型', 'トップ・コースを探す・受講までの流れで使う、コースごとのサムネイル。コースが増えても同じ型で作れるか（統一・生成のしやすさ）を基準に比べています。表示は6コース分の例です。', pats + [cmp], css))
