# 各ページの <head> に OGP（og:title・og:description・og:image など）を書き込む。build.sh の最後に実行
# 画像：コース詳細＝assets/ogp/course-<slug>.jpg、記事ページ（見本）＝article-weekly2h.jpg、ほか＝default.jpg
# 本番（Wix）では、SEO 設定の「SNS で共有」に同じ画像を登録する。og:image は本来、絶対 URL（https://〜）が必要
import os, re, glob, html as H
S = os.path.dirname(os.path.abspath(__file__)); LPDIR = os.path.dirname(S)
SKIP = {'lp-preview.html', 'why-variants.html', 'course.html'}
n = 0
for f in sorted(glob.glob(os.path.join(LPDIR, '*.html'))):
    name = os.path.basename(f)
    if name in SKIP: continue
    t = open(f).read()
    t = re.sub(r'\n?<meta (?:property="og:[^"]+"|name="twitter:[^"]+")[^>]*>', '', t)
    title = re.search(r'<title>([^<]*)</title>', t).group(1)
    m = re.search(r'<meta name="description" content="([^"]*)"', t); desc = m.group(1) if m else ''
    if name.startswith('course-'): img = f'assets/ogp/course-{name[7:-5]}.jpg'; typ = 'article'
    elif name == 'article.html': img = 'assets/ogp/article-weekly2h.jpg'; typ = 'article'
    else: img = 'assets/ogp/default.jpg'; typ = 'website'
    if not os.path.exists(os.path.join(LPDIR, img)): img = 'assets/ogp/default.jpg'
    tags = (f'\n<meta property="og:type" content="{typ}">\n<meta property="og:site_name" content="The Academy">\n<meta property="og:title" content="{H.escape(title)}">'
            f'\n<meta property="og:description" content="{desc}">\n<meta property="og:image" content="{img}">\n<meta property="og:image:width" content="1200">'
            f'\n<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">')
    t = re.sub(r'(<title>[^<]*</title>)', r'\1' + tags.replace('\\', '\\\\'), t, count=1)
    open(f, 'w').write(t); n += 1
print('ok set_ogp', n)
