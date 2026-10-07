# ═════════ コース詳細（K2 成果物から見せる型）：全コース分を同じ型で作る ═════════
C, CAT, chref = g['C'], g['CAT'], g['chref']
TODO_S = lambda t='仮': f'<span class="x-todo">{t}</span>'
DELIV = {'sns-marketing': 'SNSキャンペーン企画書', 'ai-efficiency': '業務を自動化する仕組み', 'toeic-700': '英語で伝える5分間プレゼン', 'event-design': 'イベント運営計画書',
         'marketing-basic': 'マーケティング戦略シート', 'instagram': 'Instagramの投稿企画シート', 'automation': '業務自動化ツール', 'chatgpt-basic': '仕事で使えるプロンプト集',
         'line-official': '公式LINEの予約・資料請求の仕組み', 'business-english': 'ビジネスメールの定型文集', 'project-management': 'プロジェクト計画書', 'canva-basic': 'SNS投稿のデザインセット',
         'slack-gas-task': 'Slackで完結するタスク管理'}
FOR_CAT = {'it': ['毎日の作業に、時間を取られすぎている', 'ツールを使いこなして、仕事を楽にしたい', '社内のデジタル化を任された'],
           'mk': ['発信や集客を任されたが、何から始めればいいか分からない', '投稿はしているが、反応や成果につながらない', '企画から振り返りまで、一通り経験しておきたい'],
           'en': ['英語を使う仕事に、自信を持って臨みたい', '独学が続かず、伸び悩んでいる', 'スコアや実務で、目に見える成果を出したい'],
           'biz': ['仕事の進め方を、体系的に身につけたい', 'チームをまとめる役割を任された', '計画から振り返りまで、型を持っておきたい'],
           'cr': ['伝わるデザインを、自分でつくれるようになりたい', 'SNSや資料の見た目に自信がない', '仕事で使えるデザインの基本を知りたい']}
SNS_CAN = ['顧客を理解し、届けたい相手と内容を決められる', 'キャンペーンを企画書にまとめられる', '数字を見て、次の改善を決められる']
SNS_WEEKS = [('顧客理解とペルソナ', '誰に届けるかを決める'), ('競合・トレンドの調べ方', '伸びている投稿を分析'), ('目的と数値目標', 'キャンペーンのゴールを決める'), ('企画の設計', '投稿の流れを組み立てる'),
             ('投稿の制作', 'Canvaで画像と文章をつくる'), ('運用と予約投稿', '続けられる運用の型'), ('数字の見方と改善', '反応から次の一手を決める'), ('企画書にまとめる', '成果物を完成・公開する')]
CD_FAQ = [('q-period', '受講できる期間はありますか？'), ('q-refund', '返金はできますか？'), ('q-pc', 'パソコンがなくても受講できますか？')]
COURSES = list(C) + [('slack-gas-task', 'Slack×GAS タスク管理システム', 'it', 'Slackだけで、タスク・FAQ・ガントチャートを管理できる業務効率化ツールです。', None, None, None, 'ツール', 'assets/courses/feat-slack.webp')]
CD_CSS_FILE = os.path.join(S, 'k2.css')
cd_css = common_css + open(CD_CSS_FILE).read()
def cd_page(c):
    slug, title, cat, desc, price, dur, time, lv, img = c
    name, col, bg, svg = CAT[cat]; d = DELIV[slug]; plain = title.replace('&amp;', '&')
    is_tool = slug == 'slack-gas-task'
    head_t = (f'{dur}で、<br>{d}を<br>1本仕上げる。' if dur else ('Slackだけで、<br>タスク管理を<br>完結させる。' if is_tool else f'{d}を、<br>自分の手で<br>仕上げる。'))
    meta = ''.join(f'<li>{x}</li>' for x in ([dur, time, lv, '動画＋演習'] if not is_tool else ['業務効率化ツール', '仕様書つき']) if x)
    pr = f'¥{price:,}' if price else '¥—'
    pr_note = '' if price else TODO_S('価格の確定待ち')
    cp = f'LINEクーポンで ¥{price - 500:,}' if price else 'LINEクーポンで500円OFF'
    if slug == 'sns-marketing':
        fig = '<img src="assets/outcomes/sns-design.webp" alt="SNSキャンペーン企画書の例（投稿デザインのセット）" loading="lazy">'
        steps = [(f'Week {i + 1}', a, b) for i, (a, b) in enumerate(SNS_WEEKS)]; flow_t = '8週間の流れ'; kick = '8 WEEKS'; can = SNS_CAN
    else:
        fig = f'<div class="k2-ph" style="--cc:{col};--cb:{bg}" role="img" aria-label="{name}の成果物（仮の画像）"><span class="k2-ph__ic">{svg}</span><b>{d}</b><small>成果物の画像（準備中）</small></div>'
        steps = [('STEP 1', '基礎を知る', '短い講義と事例で、考え方をつかむ'), ('STEP 2', '自分の仕事で試す', '小さく手を動かして、使い方を身につける'),
                 ('STEP 3', f'{d}を仕上げる', '仕事で使える形に整える'), ('STEP 4', 'ポートフォリオに公開', '背景や過程も残して、次の機会へ')]
        flow_t = 'ツール導入までの流れ' if is_tool else '受講の流れ'; kick = 'FLOW'
        if is_tool: steps = [('STEP 1', '仕様書を確認する', 'できること・必要な準備をつかむ'), ('STEP 2', 'Slackに設定する', '仕様書どおりにセットアップ'), ('STEP 3', 'チームで使い始める', 'タスク・FAQ・ガントを共有'), ('STEP 4', '運用を整える', '進み具合を見ながら改善')]
        can = [f'{d}を、自分の仕事に合わせて仕上げられる', '学んだ考え方を、ほかの仕事にも応用できる', '成果物をポートフォリオに公開して、伝えられる']
    goal = (f'<p class="k2-goal">{CHK}Slackの中で、チームのタスクが見える状態に</p>' if is_tool else f'<p class="k2-goal">{CHK}{steps[-1][0]}で{d}が完成 → <a href="portfolio.html">ポートフォリオ</a>に公開</p>')
    cap_todo = '' if slug == 'sns-marketing' else TODO_S('成果物の名前・画像は仮')
    rel = [x for x in COURSES if x[2] == cat and x[0] != slug][:3]
    if len(rel) < 3: rel += [x for x in COURSES if x[2] != cat and x[0] != slug and x not in rel][:3 - len(rel)]
    def rc(x):
        n2, c2, b2, s2 = CAT[x[2]]
        p2 = f'<span class="k-rc__p">通常 ¥{x[4]:,}<em>LINEクーポン適用 ¥{x[4] - 500:,}</em></span>' if x[4] else '<span class="k-rc__p">¥—（価格の確定待ち）</span>'
        return f'<a class="k-rc" href="{chref(x[0])}"><span class="k-rc__v" style="--cc:{c2};--cb:{b2}">{s2}</span><b>{x[1]}</b><small>{n2}・{x[7]}</small>{p2}</a>'
    li = lambda xs: ''.join(f'<li>{CHK}{x}</li>' for x in xs)
    tl = ''.join(f'<li><span>{i + 1}</span><p class="k2-tl__w">{w}</p><b>{a}</b><small>{b}</small></li>' for i, (w, a, b) in enumerate(steps))
    how = ''.join(f'<li><b>STEP {i + 1}</b><span>{a}</span><small>{b}</small></li>' for i, (a, b) in enumerate([('知る', '短い講義と事例'), ('試す', '自分の仕事で小さく'), ('形にする', '成果物に仕上げる'), ('共有する', 'ポートフォリオへ')]))
    faqs = ''.join(f'<a href="faq.html#{q}">{t}{ARROW}</a>' for q, t in CD_FAQ)
    note1 = '分かりやすい仕様書つきで、設定も簡単' if is_tool else '動画と演習で、自分のペースで進める'
    buy = (f'<aside class="k-buy" aria-label="価格と申し込み"><p class="k-buy__k">価格（買い切り）</p><p class="k-buy__p">{pr} {pr_note}</p>'
           f'<p class="k-buy__cp">{LN}<span>{cp}<small>公式LINEの友だち限定・カートでコード入力</small></span></p>'
           f'<a class="x-btn" href="#" data-todo="カート">このコースを受講する</a><a class="x-btn x-btn--w" href="contact.html?course={plain}">受講前に無料相談する</a>'
           f'<ul class="k-buy__l"><li>{CHK}{note1}</li><li>{CHK}成果物をポートフォリオに公開できる</li><li>{CHK}クレジットカードで決済</li></ul></aside>')
    body = (f'<section class="k2-hero" id="course-head" aria-labelledby="page-title"><div class="wrap">'
            + crumb(('コースを探す', 'courses.html'), (plain, None))
            + f'<div class="k2-top"><div><span class="k-cat" style="--cc:{col};--cb:{bg}">{name}</span>'
            f'<h1 class="k2-t" id="page-title">{head_t}</h1><p class="k2-name">{title}</p><p class="k2-desc">{desc}</p><ul class="k-meta">{meta}</ul>'
            f'<div class="k2-pr"><p><small>価格（買い切り）</small><b>{pr}</b>{pr_note}</p><p class="k2-cp">{LN}{cp}</p></div>'
            f'<div class="k2-cta"><a class="x-btn" href="#" data-todo="カート">このコースを受講する</a><a class="x-btn x-btn--w" href="contact.html?course={plain}">受講前に無料相談する</a></div></div>'
            f'<figure class="k2-fig">{fig}<figcaption>完成する成果物：{d}（例）{cap_todo}</figcaption></figure></div></div></section>\n'
            f'<section class="x-sec x-sec--w" id="course-flow" aria-labelledby="flow-title"><div class="wrap"><p class="sec-kicker">{kick}</p><h2 class="sec-title" id="flow-title">{flow_t} {TODO_S("内容は仮")}</h2>'
            f'<ol class="k2-tl" style="--n:{len(steps)}">{tl}</ol>{goal}</div></section>\n'
            f'<section class="x-sec x-sec--g" id="course-for" aria-label="こんな方に・できるようになること"><div class="wrap k-2"><div><h2 class="k-h2">こんな方に</h2><ul class="k-ul">{li(FOR_CAT[cat])}</ul></div>'
            f'<div><h2 class="k-h2">できるようになること</h2><ul class="k-ul">{li(can)}</ul></div></div></section>\n'
            f'<section class="x-sec x-sec--w" id="course-how" aria-labelledby="how-title"><div class="wrap"><h2 class="k-h2" id="how-title">学び方</h2><ol class="k-how">{how}</ol>'
            f'<a class="k-a" href="how-to-learn.html#how">学び方をもっと知る{ARROW}</a></div></section>\n'
            f'<section class="x-sec x-sec--g" id="course-faq" aria-labelledby="cfaq-title"><div class="wrap k2-end"><div><h2 class="k-h2" id="cfaq-title">よくある質問</h2><div class="x-card k-faq">{faqs}</div>'
            f'<a class="k-a" href="faq.html">よくある質問をすべて見る{ARROW}</a></div>{buy}</div></section>\n'
            f'<section class="x-sec x-sec--w" id="course-related" aria-labelledby="rel-title"><div class="wrap"><h2 class="k-h2" id="rel-title">関連するコース</h2><div class="k-rel">{"".join(rc(x) for x in rel)}</div></div></section>\n'
            f'<div class="k2-bar" aria-label="価格と申し込み"><div><small>{plain}</small><b>{pr} <em>LINEで500円OFF</em></b></div><a class="x-btn" href="#" data-todo="カート">受講する</a></div>\n'
            + nx2)
    page(chref(slug), plain, cd_css, body, '', nav='courses.html')
for c in COURSES: cd_page(c)
# 以前の見本（course.html）は、SNSマーケティング実践のページへ転送する
open(LP + 'course.html', 'w').write('<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=course-sns-marketing.html"><link rel="canonical" href="course-sns-marketing.html"><title>SNSマーケティング実践 | The Academy</title></head><body><p><a href="course-sns-marketing.html">SNSマーケティング実践のページへ</a></p></body></html>\n')
print('ok course pages', len(COURSES))
