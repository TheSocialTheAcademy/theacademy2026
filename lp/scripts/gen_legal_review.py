# 法務3ページの文面レビュー用ページ（Artifact）。本文は gen_legal.py のデータをそのまま使う＝確認した文面がそのままサイトに入る
import os, tempfile
S = os.path.dirname(os.path.abspath(__file__))          # このスクリプトのフォルダ（lp/scripts）
LPDIR = os.path.dirname(S)                              # 出力先（lp）
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')  # 共通部品を取り出すときの捨て出力
import os, re
os.environ.pop('LEGAL_SITE', None)
g = {'__file__': os.path.join(S, 'gen_legal.py')}
exec(open(os.path.join(S, 'gen_legal.py')).read(), g)
ROWS, P, A = g['ROWS'], g['P'], g['A']
TODO = re.compile(r'<span class="x-todo">([^<]*)</span>')

def mark(h): return TODO.sub(r'<mark>\1</mark>', h)
def plain(h): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)).strip()

# 要確認の一覧（ページ・項目ID付き）
todos = []
for i, (k, v) in enumerate(ROWS, 1):
    for m in TODO.findall(v): todos.append(('特商法', f'T{i}', k, m))
for i, (_, h, b) in enumerate(P, 1):
    for m in TODO.findall(b): todos.append(('プライバシー', f'P{i}', h, m))
for i, (_, h, b) in enumerate(A, 1):
    for m in TODO.findall(b): todos.append(('利用規約', f'A{i}', h, m))

def item(id_, h, body):
    return f'<article class="it" id="{id_}"><header><span class="id">{id_}</span><h3>{h}</h3></header><div class="tx">{mark(body)}</div></article>'

sec_t = ''.join(item(f'T{i}', k, f'<p>{v}</p>') for i, (k, v) in enumerate(ROWS, 1))
sec_p = ''.join(item(f'P{i}', h, b) for i, (_, h, b) in enumerate(P, 1))
sec_a = ''.join(item(f'A{i}', h, b) for i, (_, h, b) in enumerate(A, 1))
todo_rows = ''.join(f'<tr><td><a href="#{i}">{i}</a></td><td>{pg}</td><td>{h}</td><td>{m}</td></tr>' for pg, i, h, m in todos)

POINTS = [
    ('責任者・所在地・電話番号は「請求があれば開示」と表記', '特商法では原則として表示が必要な項目です。ただし「請求があれば遅滞なく開示する」と書き、実際に請求があれば応じる場合は、表示を省略できます（特商法第11条ただし書）。そのため、空欄ではなくこの一文を入れています（T2〜T4）。請求が来たら、メールで遅滞なく回答してください。'),
    ('受講期間は「サービス提供中は期限なし」', '「無期限」とだけ書くと、サービスを終えるときに約束違反になるおそれがあります。そのため「本サービスを提供している間」と条件をつけ、終了時は事前にお知らせする第13条と組み合わせました。コースページの「8週間」は学習の目安だと明記しています（T12・A6）。'),
    ('個人情報の窓口も同じ扱い', '個人情報保護法でも、住所・代表者の氏名は「求めに応じて遅滞なく回答する」形で足ります。P12 にその一文を入れました。'),
    ('返金は「決済後は原則不可＋当社責任のときは個別対応」', '確定済み。デジタルコンテンツで一般的な書き方です。サイトに反映するときに、FAQ「返金はできますか？」「申し込みを取り消したいときは？」の回答も同じ内容にそろえます（T14・A8）。'),
    ('コースは月額なし、将来の月額プランに備えた一文を追加', '確定済み。コースは買い切りで月額費用なしと明記しました（A5）。コミュニティ・ポートフォリオで月額制を始める可能性に備え、「料金などは提供時に表示し、自ら申し込んだ場合だけかかる」という条項を先に入れています。実際に始めるときは、特商法の表記に「契約期間・自動更新・解約方法」を追加し、申し込み画面の最終確認にも同じ内容を出す必要があります。'),
    ('購入済みコースはアカウントがある限り受講できる', '確定済み。退会するとアカウントが削除され、受講できなくなることを明記しました（T9・A6・A14）。'),
    ('講師フィードバックは約束していない', 'FAQから外した方針に合わせ、規約にもフィードバックの提供は書いていません。'),
    ('ポートフォリオの公開範囲は「自分だけ／会員のみ／全体に公開」の3段階', '確定済み。作品ごとに誰に見せるかを選べ、投稿直後は「自分だけ」です（P4）。ポートフォリオ機能もこの3段階で作ります。'),
    ('外部送信は Google アナリティクスのみ、裁判所は横浜地方裁判所', '確定済み。Google の説明ページとオプトアウトの方法へのリンクを添えました。広告ツールは使っていないので、「広告」の文言は外しています。Meta ピクセルや Google 広告などを入れるときは、P7 に追記が必要です（P7）。会社の登記が神奈川県のため、神奈川県を管轄する横浜地方裁判所にしました（A20）。'),
    ('動作環境は現行の内容を最新版に更新', '「M1 / M2チップ」は「Apple シリコン搭載モデル」に、「Safari 16.1以上」は「最新版」にしました。型番やバージョンを書かないので、新しい機種が出ても直す必要がありません。メモリは、現行の MacBook が16GBからのため「16GB以上」にしています。Windows 利用者向けの一文と、Microsoft Edge を追加しました。Edge で動作確認していない場合は外します（T15）。'),
    ('ポートフォリオは「著作権は投稿者、当社は紹介に使える」', '匿名公開できること、公開範囲を超えて当社が公開しないことを明記しました（P4・A10）。'),
    ('成果は保証しない', '資格・転職・収入を保証しないことを明記しました（A15）。賠償の上限は、消費者契約法に配慮して「故意・重過失を除く」にしています。'),
    ('Cookie の送信先を書く欄を用意', '2023年の電気通信事業法改正（外部送信規律）に対応する欄です。実際に使う解析・広告ツールを教えてください（P7）。'),
]
points = ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in POINTS)

html = f'''<title>The Academy 規約文面</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Josefin+Sans:wght@600&display=swap">
<style>
/* レイアウト：左に目次（PC）、右に1カラムの文面。各項目に ID（T1・P3・A8）を振り、修正指示に使えるようにする */
:root {{
  --bg: #FFFFFF; --surface: #F5F6FA; --ink: #0F1B45; --mid: #5E6182; --line: #DFE2EC; --accent: #0141D4; --todo-bg: #FFF1E7; --todo: #C2560F;
  --f-body: "Noto Sans JP", "Hiragino Sans", "Yu Gothic", system-ui, sans-serif; --f-en: "Josefin Sans", "Noto Sans JP", sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg: #0E1430; --surface: #161E40; --ink: #E8EBF7; --mid: #A3A8C8; --line: #2A3462; --accent: #7EA2FF; --todo-bg: #3A2614; --todo: #FFB27A; color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --bg: #0E1430; --surface: #161E40; --ink: #E8EBF7; --mid: #A3A8C8; --line: #2A3462; --accent: #7EA2FF; --todo-bg: #3A2614; --todo: #FFB27A; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--f-body); font-size: 15px; line-height: 1.9; padding-inline: 16px; }}
.wrap {{ max-width: 1080px; margin: 0 auto; padding-block: 40px 80px; }}
.eyebrow {{ margin: 0; color: var(--accent); font-family: var(--f-en); font-size: 12px; letter-spacing: .14em; }}
h1 {{ margin: 6px 0 8px; font-size: clamp(26px, 4vw, 34px); line-height: 1.4; text-wrap: balance; }}
.lead {{ margin: 0; color: var(--mid); max-width: 62ch; }}
h2 {{ margin: 0 0 16px; font-size: 21px; line-height: 1.5; scroll-margin-top: 16px; }}
h2 small {{ display: block; color: var(--mid); font-size: 13px; font-weight: 400; }}
a {{ color: var(--accent); }}
a:focus-visible, button:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
mark {{ padding: 1px 6px; border-radius: 4px; background: var(--todo-bg); color: var(--todo); font-size: 12.5px; font-weight: 700; }}
.grid {{ display: grid; gap: 40px; margin-top: 36px; }}
@media (min-width: 960px) {{ .grid {{ grid-template-columns: 240px minmax(0, 1fr); gap: 56px; }} .toc {{ position: sticky; top: 24px; align-self: start; }} }}
.toc {{ display: flex; flex-direction: column; gap: 2px; font-size: 13.5px; }}
.toc a {{ padding: 6px 12px; border-radius: 8px; color: var(--ink); text-decoration: none; }}
.toc a:hover {{ background: var(--surface); }}
.toc .n {{ color: var(--mid); font-size: 12px; margin-left: 4px; }}
@media (max-width: 959px) {{ .toc {{ flex-direction: row; flex-wrap: wrap; gap: 6px; }} .toc a {{ background: var(--surface); }} }}
main {{ min-width: 0; display: flex; flex-direction: column; gap: 64px; }}
.points {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 1px; background: var(--line); border-block: 1px solid var(--line); }}
.points li {{ display: grid; gap: 2px; padding: 14px 0; background: var(--bg); }}
.points b {{ font-size: 15px; }} .points span {{ color: var(--mid); font-size: 14px; }}
.tbl {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13.5px; }}
th, td {{ padding: 10px 12px 10px 0; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
th {{ color: var(--mid); font-weight: 500; font-size: 12px; }}
td:first-child {{ font-variant-numeric: tabular-nums; font-weight: 700; white-space: nowrap; }}
.it {{ padding: 18px 0; border-top: 1px solid var(--line); scroll-margin-top: 16px; }}
.it:last-child {{ border-bottom: 1px solid var(--line); }}
.it header {{ display: flex; align-items: baseline; gap: 12px; }}
.id {{ flex: none; min-width: 34px; color: var(--accent); font-family: var(--f-en); font-size: 13px; letter-spacing: .04em; font-variant-numeric: tabular-nums; }}
.it h3 {{ margin: 0; font-size: 16px; line-height: 1.6; }}
.tx {{ padding-left: 46px; max-width: 70ch; }}
.tx p {{ margin: 6px 0 0; }} .tx ol, .tx ul {{ margin: 6px 0 0; padding-left: 1.4em; }} .tx li {{ margin: 3px 0; }}
.tx table {{ margin-top: 8px; }} .tx th {{ width: 30%; color: var(--ink); font-weight: 700; font-size: 13.5px; }}
@media (max-width: 600px) {{ .tx {{ padding-left: 0; }} }}
.how {{ padding: 16px 20px; border-radius: 12px; background: var(--surface); font-size: 14px; }}
.how p {{ margin: 0; }} .how code {{ font-family: inherit; font-weight: 700; }}
</style>
<div class="wrap">
<p class="eyebrow">LEGAL DRAFT</p>
<h1>特定商取引法・プライバシーポリシー・利用規約の文面案</h1>
<p class="lead">The Academy の事業（買い切りのオンラインコース、無料相談、ポートフォリオ、公式LINE）に合わせて書いた案です。調整が終わってから、サイトに反映します。</p>

<div class="grid">
<nav class="toc" aria-label="目次">
<a href="#points">作成の方針</a>
<a href="#todo">要確認の一覧<span class="n">{len(todos)}</span></a>
<a href="#tokushoho">特定商取引法に基づく表記<span class="n">{len(ROWS)}</span></a>
<a href="#privacy">プライバシーポリシー<span class="n">{len(P)}</span></a>
<a href="#terms">利用規約<span class="n">{len(A)}</span></a>
</nav>
<main>
<div class="how"><p><b>直し方</b>：各項目の番号で指示してください。例：<code>A8 返金は購入後7日以内なら可</code>、<code>T1 株式会社ザ・ソーシャル</code>。<mark>オレンジ</mark>の箇所は情報が必要なところです。公開前に、弁護士などの専門家の確認を受けてください。</p></div>

<section id="points" aria-labelledby="h-points"><h2 id="h-points">作成の方針<small>判断が分かれそうな点</small></h2><ul class="points">{points}</ul></section>

<section id="todo" aria-labelledby="h-todo"><h2 id="h-todo">要確認の一覧<small>埋める必要がある情報 {len(todos)}件</small></h2>
<div class="tbl"><table><thead><tr><th>番号</th><th>ページ</th><th>項目</th><th>必要な情報</th></tr></thead><tbody>{todo_rows}</tbody></table></div></section>

<section id="tokushoho" aria-labelledby="h-t"><h2 id="h-t">特定商取引法に基づく表記<small>tokushoho.html ／ 項目 T1〜T{len(ROWS)}</small></h2>{sec_t}</section>
<section id="privacy" aria-labelledby="h-p"><h2 id="h-p">プライバシーポリシー<small>privacy.html ／ 項目 P1〜P{len(P)}</small></h2>{sec_p}</section>
<section id="terms" aria-labelledby="h-a"><h2 id="h-a">利用規約<small>terms.html ／ 第1条〜第{len(A)}条（A1〜A{len(A)}）</small></h2>{sec_a}</section>
</main></div></div>'''
html = html.replace('href="contact.html#form"', 'href="#"').replace('href="privacy.html"', 'href="#privacy"')
open(os.path.join(tempfile.gettempdir(), 'legal-draft.html'), 'w').write(html); print('ok', len(html), 'todos', len(todos))
