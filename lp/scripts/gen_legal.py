# 法務ページ：特定商取引法に基づく表記（tokushoho）／プライバシーポリシー（privacy）／利用規約（terms）
# 共通部品は gen_extra.py と同じく gen_courses.py 経由で lp-design.html から流用する
# 文面は The Academy の事業（買い切りのオンラインコース・無料相談・ポートフォリオ・公式LINE）に合わせた案。
# 事業者情報など未確定の箇所は .x-todo（要確認）で示す。公開前に専門家の確認を受ける前提。
import os, tempfile
S = os.path.dirname(os.path.abspath(__file__))          # このスクリプトのフォルダ（lp/scripts）
LPDIR = os.path.dirname(S)                              # 出力先（lp）
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')  # 共通部品を取り出すときの捨て出力
import os, re
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)
head, between, footer_on, base_css = g['head'], g['between'], g['footer_on'], g['css']
LP = LPDIR + '/'
UPDATED = '2026年◯月◯日'

def T(s='要確認'): return f'<span class="x-todo">{s}</span>'

css = '''
  .x-todo { display: inline-block; padding: 1px 8px; border-radius: 6px; background: #FFF1E7; color: #E46A1F; font-size: 11.5px; font-weight: 700; vertical-align: middle; }
  .lg-tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 22px 0 0; padding: 0; list-style: none; }
  .lg-tabs a { display: inline-flex; align-items: center; padding: 7px 14px; border-radius: 99px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); color: var(--ink); font-size: 13px; font-weight: 700; text-decoration: none; }
  .lg-tabs a:hover { color: var(--ts-primary); box-shadow: inset 0 0 0 1.5px var(--ts-primary); }
  .lg-tabs a[aria-current] { background: var(--ink); box-shadow: none; color: #fff; }
  .lg-meta { margin: 14px 0 0; color: var(--ts-mid); font-size: 12.5px; }
  .lg { padding: clamp(40px, 5vw, 72px) 0 clamp(56px, 7vw, 96px); background: #fff; }
  .lg-grid { display: grid; grid-template-columns: 1fr; gap: 32px; }
  @media (min-width: 1024px) { .lg-grid { grid-template-columns: 232px minmax(0, 1fr); gap: 56px; } .lg-toc { position: sticky; top: 96px; align-self: start; } }
  .lg-toc { font-size: 13px; }
  .lg-toc summary { margin: 0 0 10px; color: var(--ts-mid); font-size: 12px; font-weight: 700; letter-spacing: .08em; cursor: pointer; }
  @media (min-width: 1024px) { .lg-toc summary { pointer-events: none; list-style: none; } .lg-toc summary::-webkit-details-marker { display: none; } .lg-grid--one { grid-template-columns: minmax(0, 1fr); } }
  @media (max-width: 1023px) { .lg-toc summary { margin: 0; color: var(--ink); font-size: 14px; } .lg-toc details[open] summary { margin-bottom: 10px; } }
  .lg-toc ol { margin: 0; padding: 0; list-style: none; border-left: 1px solid var(--line); }
  .lg-toc a { display: block; padding: 6px 0 6px 14px; margin-left: -1px; border-left: 2px solid transparent; color: var(--ts-mid); line-height: 1.5; text-decoration: none; }
  .lg-toc a:hover, .lg-toc a.is-on { border-left-color: var(--ts-primary); color: var(--ink); }
  @media (max-width: 1023px) { .lg-toc { padding: 16px 18px; border-radius: 16px; background: var(--bg-gray, #F7F8FB); } .lg-toc ol { columns: 2; column-gap: 20px; border: 0; } .lg-toc a { padding-left: 0; border: 0; break-inside: avoid; } }
  @media (max-width: 600px) { .lg-toc ol { columns: 1; } }
  .lg-body { max-width: 760px; color: var(--ink); font-size: 15px; line-height: 1.95; overflow-wrap: anywhere; }
  .lg-body > p:first-child { margin-top: 0; }
  .lg-body h2 { margin: 48px 0 12px; padding-top: 8px; font-size: 19px; line-height: 1.5; scroll-margin-top: 96px; }
  .lg-body h2:first-of-type { margin-top: 8px; }
  .lg-body ol, .lg-body ul { margin: 8px 0; padding-left: 1.5em; }
  .lg-body li { margin: 4px 0; }
  .lg-body ol ol { list-style: lower-roman; }
  .lg-body a { color: var(--ts-primary); }
  .lg-note { margin: 0 0 32px; padding: 14px 18px; border-left: 3px solid #E46A1F; border-radius: 0 12px 12px 0; background: #FFF8F2; color: var(--ink); font-size: 13px; line-height: 1.8; }
  .lg-tbl { width: 100%; margin: 8px 0 0; border-collapse: collapse; font-size: 14.5px; }
  .lg-tbl th, .lg-tbl td { padding: 16px 0; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; line-height: 1.85; }
  .lg-tbl th { width: 30%; padding-right: 24px; font-weight: 700; }
  .lg-tbl tr:first-child th, .lg-tbl tr:first-child td { border-top: 1px solid var(--ink); }
  @media (max-width: 600px) { .lg-tbl th, .lg-tbl td { display: block; width: auto; padding: 0; border: 0; } .lg-tbl th { padding-top: 16px; } .lg-tbl td { padding: 4px 0 16px; border-bottom: 1px solid var(--line); } .lg-tbl tr:first-child th { border-top: 1px solid var(--ink); } .lg-tbl tr:first-child td { border-top: 0; } }
  .lg-end { margin: 40px 0 0; color: var(--ts-mid); font-size: 13px; text-align: right; }
'''

CUR = ' aria-current="page"'
TABS = [('terms.html', '利用規約'), ('privacy.html', 'プライバシーポリシー'), ('tokushoho.html', '特定商取引法に基づく表記')]
NOTE = ('<p class="lg-note"><b>公開前の確認事項</b>：この文面は The Academy の事業内容に合わせて作った案です。'
        f'{T()} の箇所を埋め、現行の規約・FAQ（返金・受講期間）と内容をそろえたうえで、弁護士などの専門家の確認を受けてから公開してください。</p>')

script = '''<script>
(() => {
  const d = document.getElementById('lgToc'); if (d && matchMedia('(min-width: 1024px)').matches) d.open = true;
  const links = [...document.querySelectorAll('.lg-toc a')];
  if (!links.length || !('IntersectionObserver' in window)) return;
  const map = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { links.forEach(a => a.classList.remove('is-on')); map.get(e.target.id)?.classList.add('is-on'); }
  }), { rootMargin: '-96px 0px -70% 0px' });
  map.forEach((a, id) => { const el = document.getElementById(id); if (el) io.observe(el); });
})();
</script>'''

def legal(fname, title, lead, sections, intro='', end=''):
    """sections: [(id, 見出し, 本文HTML)]"""
    tabs = '<ul class="lg-tabs" aria-label="規約・ポリシー">' + ''.join(
        f'<li><a href="{h}"{CUR if h == fname else ""}>{t}</a></li>' for h, t in TABS) + '</ul>'
    toc = ('' if len(sections) == 1 else '<nav class="lg-toc" aria-label="目次"><details id="lgToc"><summary>目次</summary><ol>'
           + ''.join(f'<li><a href="#{i}">{h}</a></li>' for i, h, _ in sections) + '</ol></details></nav>')
    body = ''.join(f'<h2 id="{i}">{h}</h2>\n{b}\n' for i, h, b in sections)
    main = f'''<section class="phead" aria-labelledby="page-title"><div class="wrap">
<nav class="crumb" aria-label="パンくずリスト"><a href="lp-design.html">トップ</a><span aria-hidden="true">/</span><span aria-current="page">{title}</span></nav>
<h1 class="phead__t" id="page-title">{title}</h1>
<p class="phead__lead">{lead}</p>
{tabs}
</div></section>
<section class="lg" aria-label="{title}の本文"><div class="wrap"><div class="lg-grid{'' if toc else ' lg-grid--one'}">
{toc}
<div class="lg-body">
{intro}
{body}
<p class="lg-end">{end or f"制定日：{UPDATED}<br>最終更新日：{UPDATED}"}</p>
</div></div></div></section>'''
    html = head + base_css + css + between + '<main>\n' + main + '\n' + footer_on.replace('</body>', script + '</body>')
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title} | The Academy</title>', html, count=1)
    html = html.replace('href="/beginners', 'href="beginners.html')
    if os.environ.get('LEGAL_SITE'): open(LP + fname, 'w').write(html); print('ok', fname, len(html))

# ═════════ 特定商取引法に基づく表記 ═════════
DISCLOSE = '請求があった場合には、遅滞なく開示します。ご希望の方は、下記のメールアドレスまでご連絡ください。'
MAIL = 'info@thesocialjapan.com'
ROWS = [
    ('販売事業者', 'The Social株式会社'),
    ('運営統括責任者', DISCLOSE),
    ('所在地', DISCLOSE),
    ('電話番号', DISCLOSE),
    ('メールアドレス', f'{MAIL}<br>お問い合わせは、<a href="contact.html#form">お問い合わせフォーム</a>からも受け付けています。'),
    ('サービス名', 'The Academy（オンライン学習サービス）'),
    ('販売価格', '各コースのページに、税込価格で表示しています。'),
    ('商品代金以外の必要料金', 'サービスの利用に必要なインターネット接続料金・通信料金は、お客様のご負担となります。'),
    ('お支払い方法', 'クレジットカード（VISA・Mastercard・American Express・JCB・Diners Club・DISCOVER）'),
    ('お支払い時期', 'ご注文の確定時に決済します。実際の引き落とし日は、各カード会社の規定によります。'),
    ('提供時期', '決済の完了後、すぐに受講を始められます。'),
    ('受講期間', 'アカウントがある限り、本サービスを提供している間は、期間の制限なく受講できます。退会してアカウントを削除すると、購入したコースは受講できなくなります。コースの内容は改訂することがあり、改訂後は新しい内容での受講となります。各コースのページにある「〇週間」などの期間は学習の目安で、受講できる期間ではありません。'),
    ('割引・クーポン', '公式LINEなどで配布するクーポンは、カートでの決済時にのみ使えます。決済後にさかのぼっての適用や、他のクーポンとの併用はできません。'),
    ('返品・キャンセル', f'デジタルコンテンツという商品の性質上、決済の完了後のキャンセル・返金はお受けしていません。ただし、当社の責任によりコースを受講できない場合は、個別に対応します。'),
    ('動作環境', '''<b>受講できる端末</b><br>パソコン・スマートフォン・タブレットなど、インターネットに接続できる端末で動画を受講・視聴できます。スライド資料も含まれるため、できるだけ大きな画面での再生をおすすめします。課題の作成など一部の学習は、パソコンのほうが進めやすい場合があります。<br><br>
<b>推奨ブラウザ</b><br>Google Chrome・Safari・Firefox・Microsoft Edge（いずれも最新版）<br><br>
<b>課題・制作におすすめのパソコン</b><br>MacBook Air / MacBook Pro（Apple シリコン搭載モデル）、または同等以上の性能の Windows パソコン。メモリ 16GB 以上（動画編集をする場合は 32GB 以上）、ストレージ 256〜512GB 以上（外付けストレージでの増設も可）。<br><br>
動作環境を満たさない場合、本サービスを正常にご利用いただけないことがあります。'''),
    ('無料相談について', '無料相談・資料請求は無償です。相談をしたことで、受講の申し込みが必要になることはありません。'),
]
tbl = '<table class="lg-tbl"><tbody>' + ''.join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in ROWS) + '</tbody></table>'
legal('tokushoho.html', '特定商取引法に基づく表記',
      'The Academy でのコースのご購入に関する表記です。',
      [('t-info', '表記事項', tbl)],
      end=f'最終更新日：{UPDATED}')

# ═════════ プライバシーポリシー ═════════
P = [
 ('p1', '基本方針', '<p>The Social株式会社（以下「当社」）は、オンライン学習サービス「The Academy」（以下「本サービス」）でお預かりする個人情報を、個人情報の保護に関する法律その他の関係法令にしたがって、適切に取り扱います。</p>'),
 ('p2', '取得する情報', '''<p>当社は、本サービスの提供にあたり、次の情報を取得します。</p>
<ol>
<li><b>登録情報</b>：お名前（ニックネームを含む）、メールアドレス、パスワード</li>
<li><b>購入情報</b>：購入したコース、金額、日時、利用したクーポン。クレジットカード番号は決済代行会社が管理し、当社は保有しません。</li>
<li><b>受講情報</b>：受講の進み具合、課題の提出状況、アンケートの回答</li>
<li><b>ポートフォリオ情報</b>：投稿した作品、プロフィール、フォローなどの利用状況</li>
<li><b>相談・お問い合わせ情報</b>：無料相談の予約内容、資料請求の送付先、お問い合わせの内容</li>
<li><b>公式LINEの情報</b>：友だち追加の有無、LINE上でのやりとり</li>
<li><b>端末・利用状況の情報</b>：IPアドレス、ブラウザの種類、Cookie などの識別子、閲覧履歴</li>
</ol>'''),
 ('p3', '利用目的', '''<p>取得した情報は、次の目的に利用します。</p>
<ol>
<li>会員登録・本人確認・ログインのため</li>
<li>コースの販売・決済・受講機能の提供のため</li>
<li>ポートフォリオの表示・公開など、本サービスの機能を提供するため</li>
<li>無料相談の実施、資料の送付、お問い合わせへの回答のため</li>
<li>受講状況に合わせた学習のご案内のため</li>
<li>新しいコース・キャンペーン・クーポンのお知らせのため（配信は停止できます）</li>
<li>アンケートや利用状況の分析による、本サービスの改善・新サービスの開発のため</li>
<li>利用規約に違反する行為・不正利用の防止と対応のため</li>
<li>上記に付随する目的のため</li>
</ol>'''),
 ('p4', 'ポートフォリオで公開される情報', '''<p>ポートフォリオに投稿した作品は、作品ごとに、会員が次の3つから公開範囲を選べます。投稿したときは「自分だけ」に設定され、会員が変更しない限りほかの人には表示されません。</p>
<ol>
<li><b>自分だけ</b>：本人だけが見られます。</li>
<li><b>会員のみ</b>：The Academy にログインしている会員が見られます。</li>
<li><b>全体に公開</b>：会員以外の人も見られます。検索エンジンの検索結果に表示されることがあります。</li>
</ol>
<p>プロフィールに表示する名前は、ニックネームにできます。公開した情報は、第三者に閲覧・保存される可能性があります。ご本人や他人を特定できる情報、仕事で扱った非公開の情報は載せないでください。</p>'''),
 ('p5', '第三者への提供', '''<p>当社は、次の場合を除き、ご本人の同意なく個人情報を第三者に提供しません。</p>
<ol>
<li>法令に基づく場合</li>
<li>人の生命・身体・財産の保護に必要で、ご本人の同意を得ることが難しい場合</li>
<li>国や地方公共団体などの事務に協力する必要があり、同意を得ることでその遂行に支障が出るおそれがある場合</li>
<li>合併・事業譲渡などで事業が承継される場合</li>
</ol>'''),
 ('p6', '業務の委託', '<p>当社は、決済・メール配信・予約管理・サーバー運用などの業務を外部に委託することがあります。その際は、委託先を適切に選び、契約などにより必要な監督を行います。</p>'),
 ('p7', 'Cookie・外部への情報送信', '''<p>本サービスでは、利用状況を把握するため、Cookie などを使って、次の事業者へ利用者の情報を送信することがあります。ブラウザの設定で Cookie を無効にできますが、一部の機能が使えなくなる場合があります。</p>
<table class="lg-tbl"><tbody>
<tr><th scope="row">送信先</th><td>Google LLC（Google アナリティクス）<br>Google による情報の取り扱いは、<a href="https://policies.google.com/technologies/partner-sites?hl=ja" target="_blank" rel="noopener">Google のサービスを使用するサイトやアプリから収集した情報の Google による使用</a>をご覧ください。Google アナリティクスによる収集を止めたい場合は、<a href="https://tools.google.com/dlpage/gaoptout?hl=ja" target="_blank" rel="noopener">Google アナリティクス オプトアウト アドオン</a>を利用できます。</td></tr>
<tr><th scope="row">送信する情報</th><td>閲覧したページ、端末・ブラウザの情報、Cookie の識別子など</td></tr>
<tr><th scope="row">利用目的</th><td>アクセス状況の分析、サービスの改善</td></tr>
</tbody></table>'''),
 ('p8', '安全管理', '<p>当社は、個人情報の漏えい・滅失・き損を防ぐため、アクセス権限の管理、通信の暗号化、従業者への教育など、必要かつ適切な安全管理措置を講じます。</p>'),
 ('p9', '開示・訂正・利用停止などのご請求', '<p>ご本人から、個人情報の開示・訂正・追加・削除・利用停止・第三者提供の停止のご請求があった場合は、ご本人であることを確認したうえで、法令にしたがって遅滞なく対応します。ご請求は、下記の窓口までご連絡ください。登録情報の一部は、マイページから変更できます。</p>'),
 ('p10', '未成年の方の利用', '<p>未成年の方は、保護者の同意を得たうえで本サービスをご利用ください。</p>'),
 ('p11', 'このポリシーの変更', '<p>当社は、法令の改正やサービス内容の変更に合わせて、このポリシーを変更することがあります。重要な変更をする場合は、本サービス上でお知らせします。</p>'),
 ('p12', 'お問い合わせ窓口', f'<p>The Social株式会社　個人情報のお問い合わせ窓口<br>メールアドレス：{MAIL}<br><a href="contact.html#form">お問い合わせフォーム</a><br>当社の住所・代表者の氏名は、ご請求があった場合に遅滞なくお知らせします。</p>'),
]
legal('privacy.html', 'プライバシーポリシー', 'The Academy でお預かりする個人情報の取り扱いについて定めています。', P)

# ═════════ 利用規約 ═════════
def ol(*items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'
A = [
 ('a1', '第1条（この規約について）', ol('この規約は、The Social株式会社（以下「当社」）が提供するオンライン学習サービス「The Academy」（以下「本サービス」）の利用条件を定めるものです。',
     '会員登録またはコースの購入をした方は、この規約に同意したものとみなします。',
     '各コースのページや本サービス上の個別の案内は、この規約の一部とします。この規約と個別の案内が異なる場合は、個別の案内を優先します。')),
 ('a2', '第2条（言葉の定義）', ol('「会員」とは、この規約に同意し、当社所定の方法で登録した方をいいます。',
     '「コース」とは、本サービスで販売する動画・教材・課題などの学習コンテンツをいいます。',
     '「投稿コンテンツ」とは、会員がポートフォリオなどに投稿した作品・文章・画像その他の情報をいいます。')),
 ('a3', '第3条（会員登録）', ol('登録を希望する方は、正確な情報を入力して登録を申請してください。',
     '当社は、申請者が過去に規約違反で利用を停止されている場合や、登録内容に虚偽がある場合など、登録が適当でないと判断したときは、登録をお断りすることがあります。',
     '未成年の方は、保護者の同意を得たうえで登録してください。')),
 ('a4', '第4条（アカウントの管理）', ol('会員は、自分の責任でメールアドレスとパスワードを管理してください。',
     'アカウントを第三者に使わせたり、貸与・譲渡したりすることはできません。',
     'アカウントが第三者に使われたことで生じた損害について、当社は、当社に故意または過失がある場合を除き責任を負いません。')),
 ('a5', '第5条（コースの購入と料金）', ol('会員は、各コースのページに表示された価格（税込）を支払うことで、そのコースを受講できます。',
     'お支払いは、当社が指定するクレジットカードで行います。',
     'コースは1コースごとの買い切りで、月額費用はかかりません。',
     '当社は、コミュニティやポートフォリオなどの機能について、月額制などの継続課金のサービス（以下「有料プラン」）を提供することがあります。有料プランの料金・内容・契約期間・更新と解約の方法は、提供を始めるときに本サービス上で表示します。料金は、会員が自ら申し込んだ場合に限りかかります。',
     '受講には、会員ご自身でインターネット環境と端末をご用意ください。通信料金は会員のご負担です。')),
 ('a6', '第6条（受講期間）', ol('会員は、アカウントがある限り、購入したコースを、本サービスを提供している間、期間の制限なく受講できます。',
     '当社は、コースの内容を改訂することがあります。改訂後は、新しい内容での受講となります。',
     '各コースのページに表示する学習期間（「8週間」など）は学習の目安であり、受講できる期間を定めるものではありません。',
     '本サービスを終了する場合は、第13条第3項にしたがってお知らせします。')),
 ('a7', '第7条（クーポン）', ol('当社は、公式LINEなどを通じてクーポンを配布することがあります。',
     'クーポンは、決済時にカートで入力した場合に限り使えます。現金との交換、決済後の適用、他のクーポンとの併用はできません。',
     '有効期限・対象コースなどの条件は、配布時の案内にしたがいます。')),
 ('a8', '第8条（キャンセルと返金）', ol('コースはデジタルコンテンツのため、決済の完了後のキャンセル・返金はお受けしていません。',
     'ただし、当社の責任によりコースを受講できない場合は、個別に対応します。')),
 ('a9', '第9条（無料相談）', '<p>無料相談・資料請求は無償です。相談をしたことで、コースの購入が必要になることはありません。予約の変更・取り消しは、予約時の案内にしたがってご連絡ください。</p>'),
 ('a10', '第10条（投稿コンテンツ）', ol('投稿コンテンツの著作権は、投稿した会員に帰属します。',
     '会員は当社に対し、本サービスの提供・紹介・改善に必要な範囲で、投稿コンテンツを無償で利用（複製・公開・必要な範囲での編集など）することを許諾します。会員がポートフォリオの公開範囲を限定している場合、当社はその範囲を超えて公開しません。',
     '会員は、投稿コンテンツが第三者の著作権・肖像権・プライバシーなどの権利を侵害しないことを保証してください。',
     '当社は、この規約に違反する投稿コンテンツを、事前の通知なく非表示または削除することがあります。')),
 ('a11', '第11条（コースの権利）', ol('コースに関する著作権その他の権利は、当社または正当な権利者に帰属します。',
     '会員は、コースを自分の学習のためにだけ利用できます。録画・複製・転載・配布・販売、第三者への共有はできません。')),
 ('a12', '第12条（禁止事項）', '<p>会員は、次の行為をしてはいけません。</p>' + ol(
     '法令または公序良俗に反する行為', '当社・他の会員・第三者の権利を侵害する行為、または誹謗中傷する行為',
     'アカウントの共有・貸与・譲渡', 'コースの内容を無断で録画・複製・公開・販売する行為',
     '他人の作品を自分の作品として投稿する行為', '本サービスと関係のない営業・勧誘・宣伝',
     '本サービスのサーバーやネットワークに負担をかける行為、不正アクセス', 'その他、当社が不適切と判断する行為')),
 ('a13', '第13条（サービスの変更・中断）', ol('当社は、コースの内容を更新・改訂することがあります。',
     '当社は、システムの保守、障害、天災などの理由により、事前の通知なく本サービスの全部または一部を中断することがあります。',
     '当社は、本サービスを終了する場合、相当の期間をおいて会員にお知らせします。')),
 ('a14', '第14条（利用停止と退会）', ol('当社は、会員がこの規約に違反した場合、事前の通知なく、本サービスの利用停止または登録の抹消を行うことがあります。',
     '会員は、当社所定の方法でいつでも退会できます。退会するとアカウントは削除され、購入したコースは受講できなくなります。有料プランを契約している場合は、退会の前に解約の手続きをしてください。')),
 ('a15', '第15条（保証の否認と免責）', ol('当社は、コースを受講したことによる資格取得・就職・転職・収入の増加などの成果を保証しません。',
     '当社は、本サービスに起因して会員に生じた損害について、当社に故意または過失がある場合を除き、責任を負いません。',
     '当社が責任を負う場合でも、当社に故意または重大な過失がある場合を除き、その賠償額は、損害の原因となったコースについて会員が支払った金額を上限とします。')),
 ('a16', '第16条（個人情報）', '<p>当社は、会員の個人情報を、別に定める<a href="privacy.html">プライバシーポリシー</a>にしたがって取り扱います。</p>'),
 ('a17', '第17条（規約の変更）', '<p>当社は、民法の定型約款の規定に基づき、この規約を変更することがあります。変更する場合は、変更の内容と効力が生じる日を、事前に本サービス上でお知らせします。</p>'),
 ('a18', '第18条（連絡方法）', '<p>当社から会員への連絡は、登録されたメールアドレスへの送信、または本サービス上への掲載によって行います。</p>'),
 ('a19', '第19条（権利・義務の譲渡）', '<p>会員は、当社の書面による同意なく、この規約上の地位や権利・義務を第三者に譲渡できません。</p>'),
 ('a20', '第20条（準拠法と裁判管轄）', '<p>この規約は日本法に準拠します。本サービスに関して紛争が生じた場合は、横浜地方裁判所を第一審の専属的合意管轄裁判所とします。</p>'),
]
legal('terms.html', '利用規約', 'The Academy をご利用いただくうえでの条件を定めています。', A)
