from common import *
LOGO = '/home/user/theacademy2026/lp/assets/academy_logo_blue_trim.png'
# 今のサイトの資料4点（/whitepaper）＋見本2点：カテゴリ, 資料名（[]が強調）, 形式, アイコン, 中身3つ
WP = [('it', 'ChatGPTを使いこなす！<br>ビジネスメール作成の<br>[効率化術]', 'PDF・プロンプト例つき', 'mail', ['依頼内容の伝え方', '役割を設定する', 'プロンプト例4つ']),
      ('biz', 'ロジックツリーと<br>ピラミッドストラクチャーで<br>学ぶ[論理的思考]', 'PDF・初心者向け', 'gantt', ['ロジックツリー', 'ピラミッドストラクチャー', '使い方の例']),
      ('ca', 'キャリア実現のための<br>[タイムトラッキング<br>シート]', 'シート・社会人／大学生', 'clock', ['時間を記録する', '理想の配分と比べる', '行動計画を立てる']),
      ('biz', 'SMART×WOOPで<br>[達成率アップ]の<br>目標設定術', 'PDF・ワークつき', 'chart', ['SMART', 'WOOP', '組み合わせ方']),
      ('mk', 'SNS投稿<br>[企画シート]', 'シート・1枚', 'mega', ['ねらい', 'ターゲット', '投稿の内容']),
      ('cr', 'ポートフォリオ作成<br>[チェックリスト]', 'PDF・10項目', 'user', ['作品の選び方', '背景の書き方', '見せ方'])]
hl = lambda s, tag='em': s.replace('[', f'<{tag}>').replace(']', f'</{tag}>')
plain = lambda s: s.replace('<br>', '').replace('[', '').replace(']', '')
# W-1 今の型を整える（青＋中央の見出し＋黄色の強調＋線のイラスト）
def w1(r):
    k, t, f, icn, pts = r
    return (f'<div class="cv w1"><img class="lg lg--w" src="{LOGO}" alt=""><span class="w1-tag">お役立ち資料</span><p class="w1-t">{hl(t)}</p>'
            f'<div class="w1-ill">{ic(icn, "w1-i", 1.2)}</div><p class="w1-f">学校でもない、職場でもない、学びのサードプレイス</p></div>')
# W-2 資料の表紙（縦長の冊子を置いた見た目）
def w2(r):
    k, t, f, icn, pts = r; nm, col, bg = CAT[k]
    return (f'<div class="cv w2" style="background:{bg};--cc:{col}"><div class="w2-bk"><span class="w2-band"></span><img class="lg" src="{LOGO}" alt=""><p class="w2-k">WHITE PAPER</p>'
            f'<p class="w2-t">{hl(t)}</p>{ic(icn, "w2-i", 1.4)}<p class="w2-f">{f}</p></div><div class="w2-bk w2-bk--2"></div></div>')
# W-3 表紙＋中身のページ（何が入っているかを見せる）
def w3(r):
    k, t, f, icn, pts = r; nm, col, bg = CAT[k]
    li = ''.join(f'<li><b>{i + 1:02d}</b>{p}</li>' for i, p in enumerate(pts))
    return (f'<div class="cv w3" style="background:{bg};--cc:{col}"><div class="w3-l"><span class="w3-tag">{f}</span><p class="w3-t">{hl(t)}</p></div>'
            f'<div class="w3-pg"><p class="w3-h">{ic(icn, "w3-i", 1.8)}もくじ</p><ol>{li}</ol><i></i><i></i><i class="s"></i></div></div>')
# W-4 カテゴリ色のグラデーション＋形（コースのサムネイルと同じ家族）
GR = {'it': ('#1E9E62', '#2FAE73'), 'mk': ('#E46A1F', '#F29A50'), 'en': ('#0141D4', '#3E78FE'), 'biz': ('#6B4FD8', '#8A70E8'), 'cr': ('#D9467A', '#E8608F'), 'ca': ('#0F1B45', '#3A4A80')}
def w4(r):
    k, t, f, icn, pts = r; a, b = GR[k]
    return (f'<div class="cv w4" style="background:linear-gradient(135deg,{a},{b})"><svg class="bgs" viewBox="0 0 480 300"><circle cx="420" cy="40" r="120" fill="#fff" opacity=".12"/><rect x="300" y="170" width="160" height="160" rx="34" fill="#fff" opacity=".1" transform="rotate(18 380 250)"/></svg>'
            f'<span class="w4-tag">{ic("book", "w4-bi", 1.8)}無料資料</span><p class="w4-t">{hl(t)}</p><p class="w4-f">{f}</p></div>')
def card(fn, r):
    nm, col, bg = CAT[r[0]]
    return f'<div class="cd"><div class="th">{fn(r)}</div><div class="bd"><span class="chip" style="--cc:{col};--cb:{bg}">{nm}</span><h3>{plain(r[1])}</h3><p class="mt">{r[2]}</p></div></div>'
row = lambda fn: '<div class="grid g3">' + ''.join(card(fn, r) for r in WP) + '</div>'
css = '''.g3{grid-template-columns:repeat(3,1fr);gap:22px}.cd{background:#fff;border-radius:14px;box-shadow:0 0 0 1px #E6E9F0;overflow:hidden}.th{aspect-ratio:16/9}
.bd{padding:14px 18px 18px}.chip{display:inline-block;background:var(--cb);color:var(--cc);font-size:11.5px;font-weight:700;padding:2px 10px;border-radius:999px}.bd h3{font-size:15.5px;margin:8px 0 4px;line-height:1.5}.mt{font-size:12.5px;color:#676688}
.cv{position:relative;width:100%;height:100%;overflow:hidden;color:#0F1B45;word-break:keep-all;overflow-wrap:anywhere;isolation:isolate}.bgs{position:absolute;inset:0;width:100%;height:100%;z-index:-1}
.lg{height:16px;display:block}.lg--w{filter:brightness(0) invert(1);position:absolute;left:18px;top:14px}
.w1{background:#1565C8;color:#fff;text-align:center}.w1-tag{position:absolute;right:16px;top:12px;border:1.5px solid #fff;border-radius:4px;font-size:10px;font-weight:700;padding:2px 10px}
.w1-t{position:absolute;left:16px;right:16px;top:44px;font-size:17px;font-weight:900;line-height:1.45}.w1-t em{font-style:normal;color:#FFD54A}
.w1-ill{position:absolute;left:50%;bottom:26px;transform:translateX(-50%);width:70px;height:70px;border-radius:50%;background:rgba(255,255,255,.14);display:grid;place-items:center}.w1-i{width:40px;height:40px;color:#fff}
.w1-f{position:absolute;right:14px;bottom:8px;font-size:7.5px;opacity:.85}
.w2{display:block}.w2-bk{position:absolute;left:50%;top:14px;bottom:-30px;width:46%;transform:translateX(-50%) rotate(-3deg);background:#fff;border-radius:4px 10px 10px 4px;box-shadow:0 14px 30px rgba(15,27,69,.18);padding:18px 14px 0 20px;z-index:2}
.w2-bk--2{transform:translateX(-44%) rotate(4deg);z-index:1;opacity:.6;padding:0}.w2-band{position:absolute;left:0;top:0;bottom:0;width:7px;background:var(--cc);border-radius:4px 0 0 4px}
.w2-k{font-size:8px;font-weight:900;letter-spacing:.16em;color:var(--cc);margin-top:12px}.w2-t{font-size:11.5px;font-weight:900;line-height:1.45;margin-top:4px}.w2-t em{font-style:normal;color:var(--cc)}
.w2-i{width:34px;height:34px;color:var(--cc);margin-top:12px;opacity:.85}.w2-f{font-size:9px;color:#676688;margin-top:6px;font-weight:700}
.w3{display:grid;grid-template-columns:54% 46%}.w3-l{padding:20px 6px 18px 20px;display:flex;flex-direction:column;justify-content:center;gap:10px}.w3-tag{align-self:flex-start;background:#fff;color:var(--cc);font-size:10.5px;font-weight:800;padding:3px 10px;border-radius:999px}
.w3-t{font-size:14.5px;font-weight:900;line-height:1.45}.w3-t em{font-style:normal;color:var(--cc)}
.w3-pg{margin:16px 16px -20px 0;background:#fff;border-radius:10px 10px 0 0;padding:14px 14px;box-shadow:0 10px 24px rgba(15,27,69,.12)}.w3-h{display:flex;align-items:center;gap:5px;font-size:11px;font-weight:900;color:var(--cc);margin-bottom:8px}.w3-i{width:15px;height:15px}
.w3-pg ol{list-style:none;display:grid;gap:5px}.w3-pg li{display:flex;gap:7px;white-space:nowrap;overflow:hidden;font-size:11px;font-weight:700;border-bottom:1px solid #EEF0F5;padding-bottom:5px}.w3-pg li b{color:var(--cc);font-size:10.5px}
.w3-pg i{display:block;height:5px;border-radius:3px;background:#E6E9F0;margin-top:7px}.w3-pg i.s{width:60%}
.w4{color:#fff}.w4-tag{position:absolute;left:18px;top:16px;display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;background:rgba(255,255,255,.18);padding:3px 10px;border-radius:999px}.w4-bi{width:14px;height:14px}
.w4-t{position:absolute;left:18px;right:18px;bottom:36px;font-size:19px;font-weight:900;line-height:1.45}.w4-t em{font-style:normal;background:rgba(255,255,255,.22);padding:0 5px;border-radius:4px}.w4-f{position:absolute;left:18px;bottom:14px;font-size:11px;opacity:.85}
.cmp{width:100%;border-collapse:collapse;font-size:14px}.cmp th,.cmp td{border-bottom:1px solid #E6E9F0;padding:10px 12px;text-align:left}.cmp th{background:#F7F8FB;font-weight:700}
.ref img{height:120px;border-radius:8px;margin-right:10px}'''
ref = '<section class="pat"><h2>参考：今のサイトの資料の表紙（/whitepaper）</h2><p class="d">青の地・中央の見出し・黄色の強調・人物のイラスト・「学びのサードプレイス」の一文。見出しが大きく読みやすい反面、イラストを毎回用意する必要があります。</p><div class="ref">' + ''.join(f'<img src="wp/c{i}.jpg">' for i in range(1, 5)) + '</div></section>'
pats = [ref,
 pat('W-1', '今の型を整える（青＋中央の見出し＋黄色の強調）', '今の表紙の構成はそのままに、人物のイラストを線のアイコンに置き換えて、毎回イラストを用意しなくて済むようにしました。今のサイトから移っても違和感がありません。',
     [('◎', '今の資料と同じ見た目で続けられる'), ('○', 'アイコンなので作りやすい'), ('△', '全部が同じ青になり、資料の違いが出にくい')], row(w1)),
 pat('W-2', '冊子の表紙（資料らしさを出す）', 'カテゴリの淡い地色に、縦長の冊子を置いた見た目。「ダウンロードできる資料」であることが一目で分かります。',
     [('◎', '資料だと分かる'), ('○', 'カテゴリ色で違いが出る'), ('△', '冊子の中の文字は小さい')], row(w2)),
 pat('W-3', '表紙＋もくじ（中身を見せる）', '左に資料名、右に「もくじ」のページ。何が書いてあるかがダウンロード前に分かるので、受け取る理由が伝わります。',
     [('◎', '中身が具体的に分かる'), ('◎', 'もくじ3行を書くだけで作れる'), ('○', 'カテゴリ色で違いが出る')], row(w3), True),
 pat('W-4', 'グラデーション＋形（コースと同じ家族）', 'コースのサムネイルと同じカテゴリ色のグラデーションと形。サイト全体の統一感は一番ですが、コースと見分けにくくなります。',
     [('○', 'サイトの統一感'), ('△', 'コースと混同しやすい')], row(w4)),
]
cmp = ('<section class="pat"><h2>比べると</h2><table class="cmp"><tr><th></th><th>W-1 今の型</th><th>W-2 冊子</th><th>W-3 表紙＋もくじ</th><th>W-4 グラデ＋形</th></tr>' + ''.join('<tr>' + ''.join(f'<{"th" if j == 0 else "td"}>{v}</{"th" if j == 0 else "td"}>' for j, v in enumerate(r)) + '</tr>' for r in [
 ('資料だと分かる', '○', '◎', '◎', '△'), ('中身が伝わる', '○ 見出し', '○ 見出し', '◎ もくじ', '○ 見出し'), ('資料ごとの違い', '△ 同じ青', '○', '○', '○'), ('コース・記事との見分け', '◎', '◎', '◎', '△'), ('今のサイトからの移行', '◎', '○', '○', '△')]) + '</table>'
       '<p class="d" style="margin-top:14px">おすすめは <b>W-3 表紙＋もくじ</b>。資料は「受け取ってもらう」ことが目的なので、中身が先に見えるのが一番効きます。コース（色と形）・記事（写真）とも見た目がはっきり分かれます。今の資料の雰囲気を残したい場合は W-1 です。</p></section>')
open('wp.html', 'w').write(board('お役立ち資料の表紙　4つの型', '今のサイトの資料ページ（theacademyjapan.org/whitepaper）にある4点と見本2点で作りました。資料名は今のサイトのものです。', pats + [cmp], css))
