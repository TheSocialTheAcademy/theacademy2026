# 記事のアイキャッチ（N-2：写真全面＋大見出し。強調語にカテゴリ色の帯）を書き出す
# 出力：lp/assets/journal/<記事のキー>.webp（1280×720）。写真は lp/assets/photos/articles/<キー>.webp（CC0、出典は assets/photos/CREDITS.md）
# 記事を足したら EYE に1行（カテゴリ・見出し・アイコン・写真の位置）足して、次を実行する
#   python3 lp/scripts/gen_eyecatch.py && TA_JOB=/tmp/ta_eyecatch.json NODE_PATH=$(npm root -g) node lp/scripts/gen_thumbs.js && TA_JOB=/tmp/ta_eyecatch.json python3 lp/scripts/thumbs_webp.py
import os, json, tempfile
S = os.path.dirname(os.path.abspath(__file__)); LPDIR = os.path.dirname(S)
CAT = {'IT・デジタル': '#1E9E62', 'マーケティング': '#E46A1F', '英語・TOEIC': '#0141D4', 'ビジネス': '#6B4FD8', 'クリエイティブ': '#D9467A', 'キャリア・学び方': '#3E78FE'}  # 帯の色（キャリアは濃紺の地で見えるよう明るい青）
P = {
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'spark': '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
 'mega': '<path d="M4 11v3a1 1 0 0 0 1 1h2l6 4V6L7 10H5a1 1 0 0 0-1 1z"/><path d="M17 9a4 4 0 0 1 0 6M19.5 6.5a8 8 0 0 1 0 11"/>',
 'book': '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h7"/>',
 'chat': '<path d="M12 3.5c5 0 9 3.2 9 7.2s-4 7.2-9 7.2c-.7 0-1.4-.1-2-.2L6 20l.6-3.6C4.4 15 3 13 3 10.7 3 6.7 7 3.5 12 3.5z"/><path d="M8 10h8M8 13h5"/>',
 'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 'camera': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8"/>',
 'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 'palette': '<path d="M12 3a9 9 0 0 0 0 18c1.2 0 1.8-.9 1.4-1.9-.4-1 .3-2.1 1.4-2.1H17a4 4 0 0 0 4-4 9 9 0 0 0-9-10z"/><circle cx="7.5" cy="11" r="1.2"/><circle cx="10.5" cy="7" r="1.2"/><circle cx="15" cy="7.5" r="1.2"/>',
 'chart': '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
 'head': '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>',
}
# キー：(カテゴリ, 見出し（[]が強調）, アイコン, 写真の位置)
EYE = {
 'weekly2h':  ('キャリア・学び方', '[週2時間]で<br>学びを続ける', 'clock', '25% 60%'),
 'chatgpt5':  ('IT・デジタル', 'ChatGPTを<br>仕事の[相棒]に', 'spark', '50% 50%'),
 'snscamp':   ('マーケティング', 'SNSは<br>[顧客理解]から', 'mega', '60% 50%'),
 'restart':   ('キャリア・学び方', '独学が続かない人の<br>[学び直し]', 'book', '50% 50%'),
 'phrase20':  ('英語・TOEIC', '会議で使える<br>英語フレーズ[20]', 'chat', '50% 55%'),
 'portfolio': ('キャリア・学び方', '未経験から<br>[実績]をつくる', 'user', '40% 50%'),
 'aimemo':    ('IT・デジタル', '会議メモを<br>[AIで要約]', 'spark', '15% 60%'),
 'insta1':    ('マーケティング', '投稿企画は<br>[1枚のシート]で', 'camera', '60% 50%'),
 'event':     ('ビジネス', '当日の[進行表]<br>のつくり方', 'calendar', '50% 50%'),
 'canva':     ('クリエイティブ', '伝わる投稿の<br>[3つの基本]', 'palette', '50% 50%'),
 'brand':     ('ビジネス', '選ばれる理由を<br>[言葉]にする', 'chart', '70% 50%'),
 'present':   ('英語・TOEIC', '5分で伝わる<br>[英語プレゼン]', 'head', '35% 40%'),
}
def tile(k, cat, h, icn, pos):
    ph = os.path.join(LPDIR, 'assets', 'photos', 'articles', f'{k}.webp')
    svg = f'<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{P[icn]}</svg>'
    return (f'<div class="th" id="t-{k}" style="--ac:{CAT[cat]}"><img class="ph" src="file://{ph}" style="object-position:{pos}" alt=""><div class="sh"></div>'
            f'<p class="c">{svg}{cat}</p><p class="h">{h.replace("[", "<em>").replace("]", "</em>")}</p></div>')
CSS = '''*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Noto Sans JP',sans-serif;background:#fff;display:flex;flex-wrap:wrap;gap:20px;padding:20px;width:1400px}
.th{position:relative;width:640px;height:360px;overflow:hidden;color:#fff;word-break:keep-all}.ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.sh{position:absolute;inset:0;background:linear-gradient(90deg,rgba(15,27,69,.86) 0%,rgba(15,27,69,.64) 55%,rgba(15,27,69,.28) 100%),linear-gradient(0deg,rgba(15,27,69,.35) 0%,rgba(15,27,69,0) 55%)}
.c{position:absolute;left:32px;top:28px;display:flex;align-items:center;gap:9px;font-size:18px;font-weight:800}.i{width:24px;height:24px}
.h{position:absolute;left:32px;bottom:30px;font-size:44px;font-weight:900;line-height:1.42;letter-spacing:.01em}.h em{font-style:normal;background:var(--ac);padding:0 10px;border-radius:6px;margin:0 4px}'''
out = os.path.join(tempfile.gettempdir(), 'ta_eyecatch.html')
open(out, 'w').write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(tile(k, *v) for k, v in EYE.items())}</body></html>')
json.dump({'html': out, 'dir': os.path.join(LPDIR, 'assets', 'journal'), 'slugs': list(EYE), 'prefix': 'ta_eye_'}, open(os.path.join(tempfile.gettempdir(), 'ta_eyecatch.json'), 'w'))
print('ok eyecatch html', len(EYE), out)
