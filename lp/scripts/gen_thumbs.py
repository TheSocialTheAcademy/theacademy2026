# コースのサムネイル（T-B：淡い地色＋線アイコン）を、コース一覧のデータから画像で書き出す
# 出力：lp/assets/thumbs/<slug>.webp（1280×800）。コースを足したら ICON に1行足して、このスクリプトを実行する
#   python3 lp/scripts/gen_thumbs.py && NODE_PATH=$(npm root -g) node lp/scripts/gen_thumbs.js
import os, html, tempfile, json
S = os.path.dirname(os.path.abspath(__file__)); LPDIR = os.path.dirname(S)
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)
CAT, C, cur_meta = g['CAT'], g['C'], g['cur_meta']
P = {  # 線アイコン（24×24）
 'palette': '<path d="M12 3a9 9 0 0 0 0 18c1.2 0 1.8-.9 1.4-1.9-.4-1 .3-2.1 1.4-2.1H17a4 4 0 0 0 4-4 9 9 0 0 0-9-10z"/><circle cx="7.5" cy="11" r="1.2"/><circle cx="10.5" cy="7" r="1.2"/><circle cx="15" cy="7.5" r="1.2"/>',
 'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1 7 17M17 7l2.1-2.1"/>',
 'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="m12 13 1 2 2 .3-1.5 1.4.4 2.1-1.9-1-1.9 1 .4-2.1L9 15.3l2-.3z"/>',
 'camera': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'chart': '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/><path d="M15 8h4v4"/>',
 'chat': '<path d="M12 3.5c5 0 9 3.2 9 7.2s-4 7.2-9 7.2c-.7 0-1.4-.1-2-.2L6 20l.6-3.6C4.4 15 3 13 3 10.7 3 6.7 7 3.5 12 3.5z"/><path d="M8 10h8M8 13h5"/>',
 'code': '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
 'mega': '<path d="M4 11v3a1 1 0 0 0 1 1h2l6 4V6L7 10H5a1 1 0 0 0-1 1z"/><path d="M17 9a4 4 0 0 1 0 6M19.5 6.5a8 8 0 0 1 0 11"/>',
 'spark': '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
 'head': '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>',
 'gantt': '<path d="M3 4v16h18"/><path d="M7 7h6M9 11h8M12 15h7"/>',
}
# コースごとのアイコンと、サムネイルでの改行位置（<wbr>）
ICON = {'sns-marketing': ('mega', 'SNSマーケティング<wbr>実践'), 'ai-efficiency': ('spark', '生成AI<wbr> 業務改善'), 'toeic-700': ('head', 'TOEIC L&R<wbr> 700点突破'),
        'event-design': ('calendar', None), 'marketing-basic': ('chart', 'マーケティング<wbr>戦略基礎'), 'instagram': ('camera', None), 'automation': ('code', '自動化ツール<wbr>開発'),
        'chatgpt-basic': ('spark', '初級編<wbr> ChatGPT'), 'line-official': ('chat', '公式LINE<wbr>運用'), 'business-english': ('mail', 'ビジネス英語<wbr>初級'),
        'project-management': ('gantt', 'プロジェクト<wbr>マネジメント'), 'canva-basic': ('palette', None), 'slack-gas-task': ('gear', 'Slack×GAS<wbr> スマート管理ツール')}
rows = [(c[0], html.unescape(c[1]), c[2], c[7], c[5], c[6]) for c in C] + [('slack-gas-task', 'Slack×GAS スマート管理ツール', 'it', 'ツール', '仕様書つき', None)]
def tile(slug, title, cat, lv, dur, time):
    name, col, bg, _ = CAT[cat]; icon, disp = ICON[slug]
    if not dur: dur, time = cur_meta(slug)
    meta = '・'.join(x for x in (lv, dur, time) if x)
    svg = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{P[icon]}</svg>'
    return (f'<div class="th" id="t-{slug}" style="background:{bg};--cc:{col}"><span class="k">{name}</span>{svg}'
            f'<p class="n">{disp or html.escape(title)}</p><p class="f">{meta}</p><p class="l">THE ACADEMY</p></div>')
CSS = '''*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Noto Sans JP',sans-serif;background:#fff;display:flex;flex-wrap:wrap;gap:20px;padding:20px;width:1400px}
.th{position:relative;width:640px;height:400px;overflow:hidden;color:#0F1B45;word-break:keep-all;overflow-wrap:anywhere}
.k{position:absolute;left:40px;top:38px;background:#fff;color:var(--cc);font-size:19px;font-weight:700;padding:6px 18px;border-radius:999px}
svg{position:absolute;right:40px;top:38px;width:150px;height:150px;color:var(--cc)}
.n{position:absolute;left:40px;right:40px;bottom:86px;font-size:42px;font-weight:900;line-height:1.3;letter-spacing:.01em}
.f{position:absolute;left:40px;bottom:40px;font-size:19px;font-weight:500;color:#4A4E6A}.l{position:absolute;right:40px;bottom:42px;font-size:15px;font-weight:900;letter-spacing:.16em;color:var(--cc);opacity:.85}'''
out = os.path.join(tempfile.gettempdir(), 'ta_thumbs.html')
open(out, 'w').write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(tile(*r) for r in rows)}</body></html>')
json.dump({'html': out, 'dir': os.path.join(LPDIR, 'assets', 'thumbs'), 'slugs': [r[0] for r in rows]}, open(os.path.join(tempfile.gettempdir(), 'ta_thumbs.json'), 'w'))
print('ok thumbs html', len(rows), out)
