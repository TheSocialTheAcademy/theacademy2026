# OGP 画像（SNS で URL を共有したときの画像、1200×630）を書き出す
#   共通の1枚：O-3（キャッチ＋コースのサムネイル）→ lp/assets/ogp/default.jpg
#   コース詳細：サムネイル＋ロゴの帯 → lp/assets/ogp/course-<slug>.jpg
#   記事：アイキャッチ＋ロゴの帯 → lp/assets/ogp/article-<キー>.jpg
#   python3 lp/scripts/gen_ogp.py && TA_JOB=/tmp/ta_ogp.json NODE_PATH=$(npm root -g) node lp/scripts/gen_ogp.js && python3 lp/scripts/gen_ogp.py save
# 各ページへの <meta property="og:..."> の書き込みは set_ogp.py（build.sh の最後に実行）
import os, sys, json, tempfile, glob
S = os.path.dirname(os.path.abspath(__file__)); LPDIR = os.path.dirname(S); A = os.path.join(LPDIR, 'assets')
OUT = os.path.join(A, 'ogp'); TMP = tempfile.gettempdir()
LOGO = os.path.join(A, 'academy_logo_blue_trim.png')
TH = ['sns-marketing', 'ai-efficiency', 'toeic-700', 'event-design', 'canva-basic', 'instagram']
def slugs_course(): return sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(A, 'thumbs', '*.webp')))
def keys_article(): return sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(A, 'journal', '*.webp')))
COURSE_NAME = {}
for f in glob.glob(os.path.join(LPDIR, 'course-*.html')):
    t = open(f).read(); i = t.find('<title>'); COURSE_NAME[os.path.basename(f)[7:-5]] = t[i + 7:t.find('</title>', i)].split(' | ')[0]
if len(sys.argv) > 1 and sys.argv[1] == 'save':
    from PIL import Image
    J = json.load(open(os.path.join(TMP, 'ta_ogp.json')))
    for s in J['slugs']:
        Image.open(os.path.join(TMP, f'ta_ogp_{s}.png')).convert('RGB').resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, f'{s}.jpg'), quality=86, optimize=True)
    print('ok ogp jpg', len(J['slugs'])); sys.exit()
def default():
    tiles = ''.join(f'<img src="file://{A}/thumbs/{t}.webp" alt="">' for t in TH)
    return (f'<div class="og o3" id="t-default"><div class="o3-l"><img class="lg" src="file://{LOGO}" alt=""><p class="c">学んで、つくって、<br>次のキャリアへ。</p>'
            f'<p class="s">働きながら学べるオンラインスクール</p><span class="b">実践コース 10+　平均満足度 4.2</span></div><div class="o3-r">{tiles}</div></div>')
def band(id_, img, label):
    return f'<div class="og o5" id="t-{id_}"><img class="im" src="file://{img}" alt=""><div class="f"><img class="lg lg--w" src="file://{LOGO}" alt=""><span>{label}</span></div></div>'
tiles = [default()] + [band(f'course-{s}', f'{A}/thumbs/{s}.webp', f'コース｜{COURSE_NAME.get(s, s)}') for s in slugs_course()] + [band(f'article-{k}', f'{A}/journal/{k}.webp', '学びのヒント') for k in keys_article()]
CSS = '''*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Noto Sans JP',sans-serif;background:#fff;width:1240px;padding:20px}
.og{position:relative;width:1200px;height:630px;overflow:hidden;color:#0F1B45;margin-bottom:20px}.lg{height:44px;display:block}.lg--w{filter:brightness(0) invert(1)}
.o3{background:#fff;display:grid;grid-template-columns:560px 1fr}.o3-l{padding:70px 0 0 72px}.c{font-size:52px;font-weight:900;line-height:1.35;margin-top:60px}.s{font-size:22px;font-weight:700;color:#4A4E6A;margin-top:18px}
.b{display:inline-block;margin-top:34px;background:#EAF0FF;color:#0141D4;font-size:22px;font-weight:800;padding:10px 22px;border-radius:999px}
.o3-r{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:40px 40px 0 0;transform:rotate(-6deg) translate(20px,-30px);align-content:start}.o3-r img{width:100%;border-radius:14px;box-shadow:0 10px 24px rgba(15,27,69,.14)}
.o5{background:#0F1B45}.im{position:absolute;left:0;top:24px;width:1200px;height:500px;object-fit:contain}.f{position:absolute;left:0;right:0;bottom:0;height:90px;display:flex;align-items:center;justify-content:space-between;padding:0 48px;color:#fff;font-size:24px;font-weight:800}.f .lg{height:36px}'''
os.makedirs(OUT, exist_ok=True)
html = os.path.join(TMP, 'ta_ogp.html')
open(html, 'w').write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(tiles)}</body></html>')
ids = ['default'] + [f'course-{s}' for s in slugs_course()] + [f'article-{k}' for k in keys_article()]
json.dump({'html': html, 'dir': OUT, 'slugs': ids}, open(os.path.join(TMP, 'ta_ogp.json'), 'w'))
print('ok ogp html', len(ids))
