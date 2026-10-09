# 新しく作るページ：無料相談・資料請求（contact）／よくある質問（faq）／記事の見本（article）／コース詳細の見本（course）
# 共通部品（ヘッダー・フッター・CSS・NEXT STEP）は gen_courses.py 経由で lp-design.html から流用する
import os, tempfile
S = os.path.dirname(os.path.abspath(__file__))          # このスクリプトのフォルダ（lp/scripts）
LPDIR = os.path.dirname(S)                              # 出力先（lp）
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')  # 共通部品を取り出すときの捨て出力
import os, re, json
os.environ['TA_COURSES_OUT'] = TMP_COURSES
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)
head, between, footer_on, ARROW, nx2, base_css = g['head'], g['between'], g['footer_on'], g['ARROW'], g['nx2'], g['css']
LP = LPDIR + '/'
def ic(d, w=1.9): return f'<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{d}</g></svg>'
LN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3C6.5 3 2 6.6 2 11c0 3.9 3.5 7.2 8.3 7.9.3.1.8.2.9.5.1.3.1.7 0 1l-.1.9c0 .3-.2 1 .9.5s5.9-3.5 8-6C21.4 14.3 22 12.7 22 11c0-4.4-4.5-8-10-8z"/></svg>'
CHK = ic('<path d="m5 12 5 5 9-10"/>', 2.6)
def crumb(*items):
    parts = ['<a href="lp-design.html">トップ</a>'] + [f'<a href="{h}">{t}</a>' if h else f'<span aria-current="page">{t}</span>' for t, h in items]
    return '<nav class="crumb" aria-label="パンくずリスト">' + '<span aria-hidden="true">/</span>'.join(parts) + '</nav>'
def page(fname, title, css, body, script='', nav=None):
    b = between
    if nav: b = b.replace(f'<a href="{nav}">', f'<a href="{nav}" aria-current="page">')
    html = head + base_css + css + b + '<main>\n' + body + '\n' + footer_on.replace('</body>', script + '</body>')
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title} | The Academy</title>', html, count=1)
    html = html.replace('href="/beginners', 'href="beginners.html')
    open(LP + fname, 'w').write(html); print('ok', fname, len(html))

common_css = '''
  .x-sec { padding: clamp(48px, 6vw, 80px) 0; } .x-sec--g { background: var(--bg-gray, #F7F8FB); } .x-sec--w { background: #fff; }
  .x-todo { display: inline-block; padding: 1px 8px; border-radius: 6px; background: #FFF1E7; color: #E46A1F; font-size: 11.5px; font-weight: 700; vertical-align: middle; }
  .x-card { border-radius: 22px; background: #fff; box-shadow: 0 0 0 1px var(--line); }
  .x-btn { display: inline-flex; align-items: center; justify-content: center; gap: 6px; min-height: 50px; padding: 0 24px; border: 0; border-radius: 12px; background: var(--ts-primary); color: #fff; font: inherit; font-size: 15px; font-weight: 700; text-decoration: none; cursor: pointer; }
  .x-btn svg { width: 16px; height: 16px; } .x-btn--w { background: #fff; color: var(--ink); box-shadow: inset 0 0 0 1px rgba(15,27,69,.18); } .x-btn--g { background: #06C755; } .x-btn[disabled] { opacity: .45; cursor: not-allowed; }
  .x-note { margin: 10px 0 0; color: var(--ts-mid); font-size: 12px; line-height: 1.7; }
  .cform [hidden], .x-sec [hidden] { display: none !important; }
  .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
'''

# ═════════ 無料相談・資料請求（FORM-009 → FORM-002/004 → FORM-005 → FORM-006、FORM-007、FORM-001） ═════════
FAQ_SIDE = [('相談したら、必ず受講しないといけませんか？', 'いいえ。相談だけでも大丈夫です。受講するかは、あとで決められます。'),
            ('何を準備すればいいですか？', '特にありません。気になっていることや、迷っていることをお聞かせください。'),
            ('顔を出さないといけませんか？', 'カメラはオフでも参加できます。<span class="x-todo">要確認</span>')]
faq_side = ('<aside class="ct-side" aria-label="相談の前によくある質問"><p class="ct-side__h">よくある質問</p>'
            + ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ_SIDE))
            + f'<a class="ct-side__more" href="faq.html">よくある質問をすべて見る{ARROW}</a></aside>')
TOPICS = ['コースの選び方', '続けられるか不安', 'キャリアの相談', '料金・お支払い', 'その他']
steps = '<ol class="ct-steps" id="ctSteps">' + ''.join(f'<li data-s="{i}"><b>{i + 1}</b>{t}</li>' for i, t in enumerate(['日時を選ぶ', 'お名前・連絡先', '内容の確認'])) + '</ol>'
contact_body = f'''<section class="phead" aria-labelledby="page-title"><div class="wrap">
{crumb(('無料相談・資料請求', None))}
<h1 class="phead__t" id="page-title">無料相談・資料請求</h1>
<p class="phead__lead">あなたに合った方法で、<wbr>最初の一歩を選べます。<wbr>相談したら必ず受講、<wbr>ではありません。</p>
</div></section>
<section class="x-sec x-sec--g cform" id="consult" aria-label="お申し込み"><div class="wrap">
<div class="ct-tabs" role="tablist" aria-label="申し込みの種類"><button type="button" role="tab" id="tab-consult" aria-controls="p-consult" aria-selected="true">30分の無料相談を予約</button><button type="button" role="tab" id="tab-pamphlet" aria-controls="p-pamphlet" aria-selected="false">パンフレットを受け取る</button></div>
<div class="ct-grid">
<div>
<div class="x-card ct-box" id="p-consult" role="tabpanel" aria-labelledby="tab-consult">
{steps}
<div class="ct-step" data-step="0">
<p class="ct-h">ご都合のよい日時を選んでください<small>オンライン・30分</small></p>
<div class="ct-cal" id="ctCal"></div>
<p class="x-note">○ 予約できます　× 埋まっています　<span class="x-todo">空き状況は表示例。予約システムとつなぐ</span></p>
<div class="ct-sel"><span id="ctSelTxt">日時を選んでください</span><button type="button" class="x-btn" id="ctNext0" disabled>次へ（お名前・連絡先）{ARROW}</button></div>
</div>
<div class="ct-step" data-step="1" hidden>
<div class="ct-sel ct-sel--top"><span>予約する日時：<b id="ctSelTxt2"></b></span><button type="button" class="ct-link" data-go="0">変更する</button></div>
<div class="ct-carry" id="ctCarry" hidden><p><b>コース診断の結果（引き継ぎ）</b><span id="ctCarryTxt"></span></p><button type="button" class="ct-link" id="ctCarryX">外す</button></div>
<div class="ct-fm">
<label class="ct-f"><span>お名前<em>必須</em></span><input type="text" id="fName" autocomplete="name" placeholder="例：山田 花子"><small class="ct-err" id="eName" hidden>お名前を入力してください</small></label>
<label class="ct-f"><span>メールアドレス<em>必須</em></span><input type="email" id="fMail" autocomplete="email" inputmode="email" placeholder="例：name@example.com"><small class="ct-err" id="eMail" hidden>メールアドレスの形式で入力してください（例：name@example.com）</small></label>
<fieldset class="ct-f"><legend>相談したいこと（いくつでも）</legend><div class="ct-chips">{''.join(f'<label><input type="checkbox" name="topic" value="{t}"><span>{t}</span></label>' for t in TOPICS)}</div></fieldset>
<label class="ct-f"><span>事前に伝えておきたいこと（任意）</span><textarea id="fMemo" rows="3" placeholder="例：仕事と両立できるか知りたい"></textarea></label>
</div>
<div class="ct-nav"><button type="button" class="x-btn x-btn--w" data-go="0">← 日時に戻る</button><button type="button" class="x-btn" id="ctNext1">内容を確認する{ARROW}</button></div>
</div>
<div class="ct-step" data-step="2" hidden>
<p class="ct-h">この内容で予約します</p>
<dl class="ct-conf" id="ctConf"></dl>
<p class="x-note">送信すると、確認のメールをお送りします。<wbr>相談したら必ず受講、ではありません。</p>
<div class="ct-nav"><button type="button" class="x-btn x-btn--w" data-go="1">← 入力に戻る</button><button type="button" class="x-btn" id="ctSend">この内容で予約する{ARROW}</button></div>
</div>
<div class="ct-done" data-step="3" hidden tabindex="-1">
<span class="ct-done__ok">{ic('<path d="m5 12 5 5 9-10"/>', 2.4)}</span>
<p class="ct-done__h">ご予約を受け付けました</p><p class="ct-done__d" id="ctDoneDate"></p>
<ol class="ct-done__f"><li><b>すぐに</b>確認のメールをお送りします</li><li><b>前日</b>参加のURLと、当日の流れをお送りします</li><li><b>当日</b>URLから参加します（カメラはオフでもOK）</li></ol>
<div class="ct-done__m"><b>確認のメールが届かないときは</b>迷惑メールのフォルダをご確認ください。<wbr>10分たっても届かない場合は、<a href="#form">お問い合わせ</a>からご連絡ください。</div>
<div class="ct-done__b"><a class="x-btn x-btn--g" href="beginners.html#line">{LN}公式LINEも追加しておく</a><a class="x-btn x-btn--w" href="courses.html">コースを見ておく</a></div>
<p class="x-note">※このページは見本です。実際には送信されません。</p>
</div>
</div>
<div class="x-card ct-box ct-pf" id="p-pamphlet" role="tabpanel" aria-labelledby="tab-pamphlet" hidden>
<div class="ct-pf__v"><img src="assets/pamphlet/cover.webp" alt="The Academy パンフレットの表紙" width="520" height="735" loading="lazy"></div>
<div class="ct-pf__f" id="pfForm">
<p class="ct-h">30秒で登録、すぐにダウンロード</p><p class="x-note" style="margin:0 0 14px">送信すると、この画面にダウンロードのボタンが出ます。<wbr>同じものをメールでもお送りします。</p>
<div class="ct-fm">
<label class="ct-f"><span>お名前<em>必須</em></span><input type="text" id="pName" autocomplete="name" placeholder="例：山田 花子"><small class="ct-err" id="epName" hidden>お名前を入力してください</small></label>
<label class="ct-f"><span>メールアドレス<em>必須</em></span><input type="email" id="pMail" autocomplete="email" inputmode="email" placeholder="例：name@example.com"><small class="ct-err" id="epMail" hidden>メールアドレスの形式で入力してください（例：name@example.com）</small></label>
<fieldset class="ct-f"><legend>いまの状況（任意）</legend><div class="ct-chips">{''.join(f'<label><input type="radio" name="st" value="{t}"><span>{t}</span></label>' for t in ['会社員', 'フリーランス', '学生', 'その他'])}</div></fieldset>
</div>
<button type="button" class="x-btn ct-pf__go" id="pfSend">送信してダウンロードする</button>
</div>
<div class="ct-pf__done" id="pfDone" hidden tabindex="-1"><span class="ct-done__ok">{ic('<path d="m5 12 5 5 9-10"/>', 2.4)}</span><p class="ct-done__h">ダウンロードの準備ができました</p>
<a class="x-btn" href="#" data-todo="PDFのURL">パンフレット（PDF）をダウンロード</a><p class="x-note">同じリンクをメールでもお送りしました。<wbr>届かないときは迷惑メールのフォルダをご確認ください。</p><p class="x-note">※このページは見本です。実際には送信されません。</p></div>
</div>
</div>
{faq_side}
</div></div></section>
<section class="x-sec x-sec--w" id="form" aria-labelledby="form-title"><div class="wrap ct-other">
<div><p class="sec-kicker">CONTACT</p><h2 class="sec-title" id="form-title">法人のお客様・<wbr>その他のお問い合わせ</h2><p class="sec-lead">研修のご相談や取材など、<wbr>上記以外はこちらからお送りください。</p></div>
<div class="x-card ct-box"><div class="ct-fm">
<label class="ct-f"><span>お名前<em>必須</em></span><input type="text" autocomplete="name"></label>
<label class="ct-f"><span>会社名（任意）</span><input type="text" autocomplete="organization"></label>
<label class="ct-f"><span>メールアドレス<em>必須</em></span><input type="email" autocomplete="email"></label>
<label class="ct-f"><span>お問い合わせ内容<em>必須</em></span><textarea rows="4"></textarea></label></div>
<button type="button" class="x-btn" style="margin-top:16px" disabled title="見本のため送信できません">送信する（見本）</button></div>
</div></section>'''
contact_css = common_css + '''
  .ct-tabs { display: inline-flex; flex-wrap: wrap; gap: 4px; padding: 5px; border-radius: 14px; background: #fff; box-shadow: 0 0 0 1px var(--line); }
  .ct-tabs button { padding: 11px 18px; border: 0; border-radius: 10px; background: none; color: var(--ts-mid); font: inherit; font-size: 14px; font-weight: 800; cursor: pointer; }
  .ct-tabs button[aria-selected="true"] { background: var(--ts-primary); color: #fff; }
  .ct-grid { display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: 24px; margin-top: 18px; align-items: start; }
  .ct-box { padding: clamp(20px, 3vw, 30px); }
  .ct-steps { display: flex; gap: 6px; margin: 0 0 20px; padding: 0; list-style: none; }
  .ct-steps li { flex: 1; display: flex; align-items: center; gap: 8px; padding: 10px 12px; border-radius: 10px; background: var(--bg-gray, #F7F8FB); color: var(--ts-mid); font-size: 13px; font-weight: 700; }
  .ct-steps b { display: grid; place-items: center; flex: none; width: 22px; height: 22px; border-radius: 50%; background: #D9DCE6; color: #fff; font-size: 12px; }
  .ct-steps li.is-done b, .ct-steps li.is-cur b { background: var(--ts-primary); } .ct-steps li.is-cur { background: #EAF0FF; color: var(--ts-primary); }
  .ct-h { margin: 0 0 10px; color: var(--ink); font-size: 17px; font-weight: 800; } .ct-h small { margin-left: 8px; color: var(--ts-mid); font-size: 12.5px; font-weight: 700; }
  .ct-cal { overflow-x: auto; } .ct-cal table { width: 100%; min-width: 520px; border-collapse: separate; border-spacing: 6px; text-align: center; font-size: 13.5px; }
  .ct-cal th { color: var(--ts-mid); font-size: 12.5px; font-weight: 700; }
  .ct-cal button { width: 100%; height: 42px; border: 0; border-radius: 10px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); color: var(--ts-primary); font: inherit; font-weight: 800; cursor: pointer; }
  .ct-cal button:hover { box-shadow: inset 0 0 0 1.5px var(--ts-primary); } .ct-cal button[aria-pressed="true"] { background: var(--ts-primary); color: #fff; box-shadow: none; font-size: 12px; }
  .ct-cal button:disabled { background: #F2F3F7; color: #B5B7C8; box-shadow: none; cursor: not-allowed; }
  .ct-sel { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; margin-top: 16px; padding: 14px 16px; border-radius: 12px; background: #EAF0FF; font-size: 14px; } .ct-sel b { color: var(--ts-primary); }
  .ct-sel--top { margin: 0 0 18px; }
  .ct-link { padding: 0; border: 0; background: none; color: var(--ts-primary); font: inherit; font-size: 13.5px; font-weight: 700; cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }
  .ct-carry { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin: -6px 0 18px; padding: 12px 16px; border-radius: 12px; background: #F2FBF6; box-shadow: inset 0 0 0 1px #BFE8CF; font-size: 13.5px; } .ct-carry p { margin: 0; } .ct-carry b { display: block; color: #06A04A; font-size: 12.5px; }
  .ct-fm { display: grid; gap: 16px; } .ct-f { display: grid; gap: 6px; margin: 0; padding: 0; border: 0; min-width: 0; font-size: 14px; font-weight: 700; color: var(--ink); }
  .ct-f legend { padding: 0; margin-bottom: 6px; } .ct-f em { margin-left: 8px; padding: 1px 6px; border-radius: 4px; background: #FFF1E7; color: #E46A1F; font-size: 11px; font-style: normal; }
  .ct-f input, .ct-f textarea { width: 100%; min-height: 48px; padding: 10px 14px; border: 0; border-radius: 10px; background: #fff; box-shadow: inset 0 0 0 1px rgba(15,27,69,.2); font: inherit; font-size: 16px; font-weight: 400; color: var(--ink); }
  .ct-f input:focus, .ct-f textarea:focus { outline: 0; box-shadow: inset 0 0 0 2px var(--ts-primary); }
  .ct-f input.is-ok { box-shadow: inset 0 0 0 1.5px #06A04A; } .ct-f input.is-ng { box-shadow: inset 0 0 0 1.5px #E5484D; }
  .ct-err { color: #E5484D; font-size: 12.5px; font-weight: 700; }
  .ct-chips { display: flex; flex-wrap: wrap; gap: 8px; } .ct-chips label { position: relative; cursor: pointer; } .ct-chips input { position: absolute; opacity: 0; width: 1px; height: 1px; }
  .ct-chips span { display: inline-block; padding: 9px 14px; border-radius: 99px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); font-size: 13.5px; font-weight: 700; }
  .ct-chips input:checked + span { background: #EAF0FF; box-shadow: inset 0 0 0 1.5px var(--ts-primary); color: var(--ts-primary); } .ct-chips input:focus-visible + span { outline: 3px solid var(--ts-light-blue); outline-offset: 2px; }
  .ct-nav { display: flex; justify-content: space-between; gap: 10px; margin-top: 22px; flex-wrap: wrap; }
  .ct-conf { display: grid; margin: 0; } .ct-conf div { display: grid; grid-template-columns: 160px minmax(0, 1fr); gap: 12px; padding: 12px 0; border-top: 1px solid var(--line); font-size: 14px; } .ct-conf dt { color: var(--ts-mid); font-weight: 700; } .ct-conf dd { margin: 0; white-space: pre-wrap; }
  .ct-done, .ct-pf__done { text-align: center; padding: 10px 0; } .ct-done:focus, .ct-pf__done:focus { outline: 0; }
  .ct-done__ok { display: inline-grid; place-items: center; width: 64px; height: 64px; border-radius: 50%; background: #E7F8EE; color: #06A04A; } .ct-done__ok svg { width: 32px; height: 32px; }
  .ct-done__h { margin: 14px 0 0; color: var(--ink); font-size: 24px; font-weight: 800; } .ct-done__d { margin: 6px 0 0; color: var(--ts-primary); font-weight: 800; }
  .ct-done__f { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin: 22px 0 0; padding: 0; list-style: none; text-align: left; }
  .ct-done__f li { padding: 14px; border-radius: 12px; background: var(--bg-gray, #F7F8FB); font-size: 13.5px; line-height: 1.6; } .ct-done__f b { display: block; color: var(--ts-primary); }
  .ct-done__m { margin-top: 14px; padding: 14px 16px; border-radius: 12px; background: #FFF8EF; text-align: left; color: var(--ts-mid); font-size: 13px; line-height: 1.7; } .ct-done__m b { display: block; color: var(--ink); } .ct-done__m a { color: var(--ts-primary); font-weight: 700; }
  .ct-done__b { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 20px; } .ct-done__b .x-btn svg { width: 18px; height: 18px; }
  .ct-pf { display: grid; grid-template-columns: 200px minmax(0, 1fr); gap: 28px; align-items: start; }
  .ct-pf__v img { display: block; width: 100%; height: auto; border-radius: 10px; box-shadow: 0 14px 30px rgba(15,27,69,.16); } .ct-pf__go { width: 100%; margin-top: 18px; }
  .ct-pf__done { grid-column: 2; } .ct-pf__done .x-btn { margin-top: 16px; }
  .ct-side { position: sticky; top: 96px; padding: 22px; border-radius: 20px; background: #fff; box-shadow: 0 0 0 1px var(--line); }
  .ct-side__h { margin: 0 0 6px; color: var(--ink); font-weight: 800; }
  .ct-side details { padding: 12px 0; border-top: 1px solid var(--line); } .ct-side summary { color: var(--ink); font-size: 13.5px; font-weight: 700; line-height: 1.6; cursor: pointer; }
  .ct-side details p { margin: 6px 0 0; color: var(--ts-mid); font-size: 13px; line-height: 1.7; }
  .ct-side__more { display: inline-flex; align-items: center; gap: 4px; margin-top: 8px; color: var(--ts-primary); font-size: 13px; font-weight: 700; text-decoration: none; } .ct-side__more svg { width: 14px; height: 14px; }
  .ct-other { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr); gap: 32px; align-items: start; }
  @media (max-width: 960px) { .ct-grid, .ct-other { grid-template-columns: minmax(0, 1fr); } .ct-side { position: static; } }
  @media (max-width: 640px) { .ct-steps li { font-size: 0; justify-content: center; } .ct-steps li.is-cur { flex: 2.6; font-size: 12px; white-space: nowrap; } .ct-conf div { grid-template-columns: minmax(0, 1fr); gap: 2px; }
    .ct-done__f { grid-template-columns: minmax(0, 1fr); } .ct-pf { grid-template-columns: minmax(0, 1fr); } .ct-pf__v { max-width: 160px; margin: 0 auto; } .ct-pf__done { grid-column: auto; } .ct-nav .x-btn, .ct-sel .x-btn { width: 100%; } }
'''
contact_js = '''<script>
(() => {
  // タブ：#pamphlet で開いたらパンフレットを表示
  const tabs = [...document.querySelectorAll('.ct-tabs [role="tab"]')];
  const pick = id => tabs.forEach(t => { const on = t.id === id; t.setAttribute('aria-selected', String(on)); document.getElementById(t.getAttribute('aria-controls')).hidden = !on; });
  tabs.forEach(t => t.addEventListener('click', () => pick(t.id)));
  if (location.hash === '#pamphlet') pick('tab-pamphlet');
  // 日時：今日から6日分（日曜を除く）。空きは見本のため決まった並びで作る（本番は予約システムの空き状況）
  const cal = document.getElementById('ctCal'), W = '日月火水木金土', T = ['10:00', '13:00', '16:00', '19:00', '20:30'];
  const days = []; for (let d = new Date(), i = 0; days.length < 6 && i < 14; i++) { d = new Date(Date.now() + (i + 1) * 864e5); if (d.getDay() !== 0) days.push(d); }
  const fmt = d => `${d.getMonth() + 1}/${d.getDate()}(${W[d.getDay()]})`, full = d => `${d.getMonth() + 1}月${d.getDate()}日（${W[d.getDay()]}）`;
  cal.innerHTML = '<table><thead><tr><th><span class="sr-only">時間</span></th>' + days.map(d => `<th scope="col">${fmt(d)}</th>`).join('') + '</tr></thead><tbody>'
    + T.map((t, ti) => `<tr><th scope="row">${t}</th>` + days.map((d, di) => { const full_ = (di * 7 + ti * 3) % 5 === 0; return `<td><button type="button" data-d="${di}" data-t="${ti}" ${full_ ? 'disabled aria-label="埋まっています"' : `aria-label="${full(d)} ${t}"`} aria-pressed="false">${full_ ? '×' : '○'}</button></td>`; }).join('') + '</tr>').join('') + '</tbody></table>';
  let pickD = null, pickT = null; const selTxt = document.getElementById('ctSelTxt'), next0 = document.getElementById('ctNext0');
  const slot = () => `${full(days[pickD])} ${T[pickT]}〜（30分）`;
  cal.addEventListener('click', e => { const b = e.target.closest('button:not(:disabled)'); if (!b) return;
    cal.querySelectorAll('button[aria-pressed="true"]').forEach(x => { x.setAttribute('aria-pressed', 'false'); x.textContent = '○'; });
    b.setAttribute('aria-pressed', 'true'); b.textContent = '選択中'; pickD = +b.dataset.d; pickT = +b.dataset.t;
    selTxt.innerHTML = '選択中：<b>' + slot() + '</b>'; next0.disabled = false; });
  // ステップの切り替え
  const steps = [...document.querySelectorAll('[data-step]')], marks = [...document.querySelectorAll('#ctSteps li')];
  const go = n => { steps.forEach(s => s.hidden = +s.dataset.step !== n); marks.forEach((m, i) => { m.classList.toggle('is-cur', i === n); m.classList.toggle('is-done', i < n); });
    document.getElementById('ctSteps').hidden = n === 3; const cur = steps.find(s => +s.dataset.step === n); (n === 3 ? cur : cur.querySelector('input, button'))?.focus({ preventScroll: true });
    document.getElementById('p-consult').scrollIntoView({ block: 'start', behavior: 'smooth' }); };
  marks[0].classList.add('is-cur');
  document.querySelectorAll('[data-go]').forEach(b => b.addEventListener('click', () => go(+b.dataset.go)));
  next0.addEventListener('click', () => { document.getElementById('ctSelTxt2').textContent = slot(); go(1); });
  // コース診断からの引き継ぎ（?course=…&goal=…）
  const q = new URLSearchParams(location.search), carry = document.getElementById('ctCarry');
  if (q.get('course')) { document.getElementById('ctCarryTxt').textContent = `${q.get('course')}（${[q.get('goal'), q.get('time'), q.get('level')].filter(Boolean).join('／')}）`; carry.hidden = false;
    document.querySelector('input[name="topic"][value="コースの選び方"]').checked = true; }
  document.getElementById('ctCarryX').addEventListener('click', () => carry.hidden = true);
  // その場のエラー表示（FORM-004）
  const mailOk = v => /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(v);
  const check = (inp, err, ok) => { const v = inp.value.trim(), good = ok(v); inp.classList.toggle('is-ok', good); inp.classList.toggle('is-ng', !good); document.getElementById(err).hidden = good; inp.setAttribute('aria-invalid', String(!good)); return good; };
  const rules = [['fName', 'eName', v => v.length > 0], ['fMail', 'eMail', mailOk], ['pName', 'epName', v => v.length > 0], ['pMail', 'epMail', mailOk]];
  rules.forEach(([i, e, ok]) => { const inp = document.getElementById(i); inp.addEventListener('blur', () => { if (inp.value) check(inp, e, ok); }); inp.addEventListener('input', () => { if (inp.classList.contains('is-ng')) check(inp, e, ok); }); });
  const valid = ids => ids.map(([i, e, ok]) => check(document.getElementById(i), e, ok)).every(Boolean);
  document.getElementById('ctNext1').addEventListener('click', () => { if (!valid(rules.slice(0, 2))) { document.querySelector('.is-ng')?.focus(); return; }
    const topics = [...document.querySelectorAll('input[name="topic"]:checked')].map(x => x.value).join('、') || '（なし）';
    const rows = [['日時', slot() + '・オンライン'], ['お名前', document.getElementById('fName').value], ['メールアドレス', document.getElementById('fMail').value], ['相談したいこと', topics]];
    if (!carry.hidden) rows.push(['診断の結果', document.getElementById('ctCarryTxt').textContent]);
    if (document.getElementById('fMemo').value.trim()) rows.push(['伝えておきたいこと', document.getElementById('fMemo').value.trim()]);
    const esc = t => t.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    document.getElementById('ctConf').innerHTML = rows.map(([k, v]) => `<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join(''); go(2); });
  document.getElementById('ctSend').addEventListener('click', () => { document.getElementById('ctDoneDate').textContent = slot() + '　オンライン'; go(3); });
  // パンフレット：送信後すぐダウンロード（FORM-001）
  document.getElementById('pfSend').addEventListener('click', () => { if (!valid(rules.slice(2))) { document.querySelector('#pfForm .is-ng')?.focus(); return; }
    document.getElementById('pfForm').hidden = true; const d = document.getElementById('pfDone'); d.hidden = false; d.focus(); });
})();
</script>'''
page('contact.html', '無料相談・資料請求', contact_css, contact_body, contact_js)

# ═════════ よくある質問（FAQ-004 検索 ＋ FAQ-003 カテゴリ ＋ FAQ-006 回答の評価） ═════════
TODO = lambda t='現行FAQから回答を移す': f'<span class="x-todo">{t}</span>'
FQ = [
 ('お申し込み', 'q-consult', '無料相談は必ず受けないといけませんか？', 'いいえ。希望する方のみです。コースのページから直接お申し込みいただけます。', '相談 必須 申し込み'),
 ('お申し込み', 'q-howto', 'どうやって申し込みますか？', 'コースのページで内容と価格を確かめ、カートに入れてクレジットカードで決済します。新規登録・ログイン後、ダッシュボードから受講を始められます。', '申し込み方法 カート 登録'),
 ('お申し込み', 'q-coupon', 'クーポンはどう使いますか？', '公式LINEの友だちに配信している「全コース500円OFF」のクーポンを、カートの「クーポンコードを入力」欄に入力してください。', 'クーポン 割引 LINE 500円'),
 ('お支払い', 'q-pay', '支払い方法は何がありますか？', 'クレジットカード（VISA・Mastercard・AMEX・JCB・Diners・DISCOVER）に対応しています。', '支払い カード 決済'),
 ('お支払い', 'q-monthly', '月額の費用はかかりますか？', 'コースはコースごとの買い切りで、月額費用はかかりません。今後、コミュニティやポートフォリオなどで、月額制などの継続課金のサービスを始める準備をしています。始める際は、料金・内容・契約期間・更新と解約の方法を、本サービス上でお知らせします。', '月額 費用 料金 買い切り'),
 ('返金', 'q-refund', '返金はできますか？', 'コースはデジタルコンテンツのため、決済の完了後の返金はお受けしていません。ただし、当社の責任によりコースを受講できない場合は、個別に対応します。詳しくは<a href="terms.html#a8">利用規約 第8条</a>をご覧ください。', '返金 キャンセル'),
 ('返金', 'q-cancel', '申し込みを取り消したいときは？', '決済の完了後は、申し込みの取り消し（キャンセル）はできません。購入前に、コースのページで内容と価格をご確認ください。当社の責任で受講できない場合は、<a href="contact.html#form">お問い合わせ</a>からご連絡ください。', '取り消し キャンセル 解約'),
 ('視聴関連', 'q-period', '受講できる期間はありますか？', 'ありません。アカウントがある限り、サービスを提供している間は期間の制限なく受講できます。コースのページにある「8週間」などは学習の目安です。退会すると、購入したコースは受講できなくなります。', '期間 視聴 いつまで'),
 ('視聴関連', 'q-pc', 'パソコンがなくても受講できますか？', 'はい。スマートフォン・タブレットでも動画を受講できます。スライド資料も含まれるため、できるだけ大きな画面での再生をおすすめします。課題の作成など一部の学習は、パソコンのほうが進めやすい場合があります。</p><p><b>推奨ブラウザ</b><br>Google Chrome・Safari・Firefox・Microsoft Edge（いずれも最新版）</p><p><b>課題・制作におすすめのパソコン</b><br>MacBook Air / MacBook Pro（Apple シリコン搭載モデル）、または同等以上の性能の Windows パソコン。メモリ 16GB 以上（動画編集をする場合は 32GB 以上）、ストレージ 256〜512GB 以上（外付けストレージでの増設も可）。</p><p>動作環境を満たさない場合、本サービスを正常にご利用いただけないことがあります。', 'スマホ パソコン 端末'),
 ('機能・操作', 'q-anon', 'ポートフォリオは匿名で公開できますか？', 'はい。表示名はニックネームにできます。ほとんどの会員の方が、ニックネームで登録しています。作品ごとに「自分だけ」「会員のみ」「全体に公開」から公開範囲を選べ、投稿した直後は「自分だけ」です。', 'ポートフォリオ 匿名 公開'),
 ('機能・操作', 'q-others', 'ほかの人のポートフォリオは見られますか？', '無料登録すると、「会員のみ」「全体に公開」に設定された作品や、フォロー中の人のフィードを見られます。資格・認定、学びの歩み、ビジョン、人柄、強みなども、会員登録をすると見られます。', 'ポートフォリオ フォロー フィード'),
 ('サービス', 'q-busy', '忙しくて続けられるか不安です', '週2時間から進められる学習設計です。学び方の詳細は<a href="how-to-learn.html">「学び方・受講成果」</a>で紹介しています。', '忙しい 続けられる 時間'),
]
CATS = ['お申し込み', 'お支払い', '返金', '視聴関連', '機能・操作', 'サービス']
CID = {c: f'fc-{i + 1}' for i, c in enumerate(CATS)}
def fq_item(c, qid, q, a, k):
    return f"""<details class="fq2" id="{qid}" data-cat="{c}" data-k="{k}"><summary><i aria-hidden="true">Q</i><span class="fq2__q">{q}</span></summary>
<div class="fq2__a"><p>{a}</p><div class="fq2__fb" data-fb><span>この回答で解決しましたか？</span><button type="button" data-v="yes">はい</button><button type="button" data-v="no">いいえ</button></div></div></details>"""
faq_groups = ''.join(f'<div class="fq3-g" id="{CID[c]}" data-g><h2 class="fq3-g__h">{c}</h2><div class="x-card fq3-g__l">' + ''.join(fq_item(*x) for x in FQ if x[0] == c) + '</div></div>' for c in CATS)
faq_nav = ('<nav class="fq3-nav" aria-label="カテゴリ"><p class="fq3-nav__h">カテゴリ</p><ul>'
           + ''.join(f'<li><a href="#{CID[c]}" data-n="{CID[c]}">{c}<small>{sum(1 for x in FQ if x[0] == c)}</small></a></li>' for c in CATS) + '</ul></nav>')
faq_body = f"""<section class="phead" aria-labelledby="page-title"><div class="wrap">
{crumb(('よくある質問', None))}
<h1 class="phead__t" id="page-title">よくある質問</h1>
<p class="phead__lead">知りたいことのカテゴリを選ぶか、<wbr>キーワードで探せます。</p>
<label class="fq2-s"><span class="sr-only">キーワードで探す</span>{ic('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', 2.2)}<input type="search" id="fqQ" placeholder="キーワードで探す（例：返金、スマホ、支払い）" autocomplete="off"></label>
</div></section>
<section class="x-sec x-sec--g" id="faq-list" aria-label="質問の一覧"><div class="wrap fq3">
{faq_nav}
<div class="fq3-main">
<p class="fq2-n" id="fqN" aria-live="polite" hidden></p>
<div id="fqL">{faq_groups}</div>
<div class="x-card fq2-0" id="fq0" hidden><p class="fq2-0__t">「<span id="fq0q"></span>」に合う質問が見つかりませんでした</p><p class="x-note" style="margin-top:4px">言葉を短くするか、ひらがな・カタカナを変えて探してみてください。</p>
<div class="fq2-0__b"><span>よく見られている質問：</span><a href="#q-consult">相談は必須？</a><a href="#q-pay">支払い方法</a><a href="#q-busy">続けられるか不安</a></div>
<a class="x-btn" href="contact.html#form">お問い合わせする</a></div>
</div>
</div></section>
<section class="x-sec x-sec--w" id="faq-more" aria-labelledby="fq-more"><div class="wrap fq2-more"><div><h2 class="sec-title" id="fq-more" style="font-size:clamp(22px,2.6vw,28px)">解決しないときは</h2><p class="sec-lead">内容を確認して、<wbr>担当スタッフがお答えします。</p></div>
<div class="fq2-more__b"><a class="x-btn" href="contact.html#form">お問い合わせ{ARROW}</a><a class="x-btn x-btn--w" href="contact.html">30分の無料相談</a></div></div></section>"""
faq_css = common_css + """
  .phead .fq2-s { max-width: 640px; margin-top: 22px; }
  .fq2-s { display: flex; align-items: center; gap: 10px; height: 58px; padding: 0 18px; border-radius: 16px; background: #fff; box-shadow: 0 0 0 1.5px var(--ts-primary), 0 8px 22px rgba(1,65,212,.08); }
  .fq2-s svg { width: 20px; height: 20px; color: var(--ts-primary); flex: none; } .fq2-s input { flex: 1; min-width: 0; height: 100%; border: 0; background: none; font: inherit; font-size: 16px; color: var(--ink); } .fq2-s input:focus { outline: 0; }
  .fq2-s:focus-within { box-shadow: 0 0 0 2.5px var(--ts-primary), 0 8px 22px rgba(1,65,212,.12); }
  .fq3 { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 48px; align-items: start; }
  .fq3-nav { position: sticky; top: 96px; } .fq3-nav__h { margin: 0 0 8px; color: var(--ts-mid); font-size: 12px; font-weight: 700; letter-spacing: .08em; }
  .fq3-nav ul { display: flex; flex-direction: column; gap: 2px; margin: 0; padding: 0; list-style: none; }
  .fq3-nav a { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; border-radius: 10px; color: var(--ink); font-size: 14px; font-weight: 700; text-decoration: none; }
  .fq3-nav a small { color: var(--ts-mid); font-weight: 500; } .fq3-nav a:hover { color: var(--ts-primary); }
  .fq3-nav a.is-on { background: #fff; box-shadow: inset 0 0 0 1px var(--line); color: var(--ts-primary); }
  .fq3-nav a.is-off { opacity: .4; pointer-events: none; }
  .fq3-main { min-width: 0; } #fqL { display: flex; flex-direction: column; gap: 32px; }
  .fq3-g { scroll-margin-top: 96px; } .fq3-g[hidden] { display: none; }
  .fq3-g__h { margin: 0 0 10px; color: var(--ink); font-size: 18px; font-weight: 800; }
  .fq3-g__l { padding: 4px clamp(16px, 3vw, 28px); }
  .fq2-n { margin: 0 0 16px; color: var(--ts-mid); font-size: 13px; }
  .fq2 { border-top: 1px solid var(--line); scroll-margin-top: 120px; } .fq2:first-child { border-top: 0; } .fq2[hidden] { display: none; }
  .fq2 summary { position: relative; display: flex; gap: 12px; align-items: baseline; padding: 18px 34px 18px 0; color: var(--ink); font-size: 15.5px; font-weight: 800; line-height: 1.6; list-style: none; cursor: pointer; }
  .fq2 summary::-webkit-details-marker { display: none; }
  .fq2 summary::after { content: ""; position: absolute; right: 6px; top: 26px; width: 9px; height: 9px; border-right: 2px solid var(--ts-mid); border-bottom: 2px solid var(--ts-mid); transform: rotate(45deg); }
  .fq2[open] summary::after { transform: rotate(-135deg); top: 30px; }
  .fq2 summary i { flex: none; color: var(--ts-primary); font: 800 17px/1.4 'Helvetica Neue', Arial, sans-serif; font-style: normal; }
  .fq2 mark { background: #FFE9A8; color: inherit; border-radius: 3px; padding: 0 2px; }
  .fq2__a { padding: 0 0 18px 28px; } .fq2__a > p + p { margin-top: 10px !important; } .fq2__a > p { margin: 0; color: var(--ts-mid); font-size: 14.5px; line-height: 1.85; } .fq2__a a { color: var(--ts-primary); font-weight: 700; }
  .fq2__fb { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-top: 14px; color: var(--ts-mid); font-size: 13px; }
  .fq2__fb button { padding: 6px 16px; border: 0; border-radius: 99px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); color: var(--ink); font: inherit; font-size: 13px; font-weight: 700; cursor: pointer; }
  .fq2__no { display: grid; gap: 10px; margin-top: 12px; padding: 14px 16px; border-radius: 12px; background: var(--bg-gray, #F7F8FB); font-size: 13px; color: var(--ts-mid); }
  .fq2__no p { margin: 0; } .fq2__no .rs { display: flex; flex-wrap: wrap; gap: 8px; } .fq2__no .rs button { padding: 7px 12px; border: 0; border-radius: 99px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); font: inherit; font-size: 12.5px; font-weight: 700; color: var(--ink); cursor: pointer; }
  .fq2__no .rs button[aria-pressed="true"] { background: #EAF0FF; box-shadow: inset 0 0 0 1.5px var(--ts-primary); color: var(--ts-primary); }
  .fq2-0 { padding: 28px; text-align: center; } .fq2-0__t { margin: 0; color: var(--ink); font-size: 17px; font-weight: 800; }
  .fq2-0__b { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px 14px; margin: 14px 0 18px; font-size: 13.5px; color: var(--ts-mid); } .fq2-0__b a { color: var(--ts-primary); font-weight: 700; }
  .fq2-more { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 20px; } .fq2-more__b { display: flex; flex-wrap: wrap; gap: 10px; }
  @media (max-width: 1023px) { .fq3 { grid-template-columns: minmax(0, 1fr); gap: 20px; } .fq3-nav { position: static; } .fq3-nav__h { display: none; }
    .fq3-nav ul { flex-direction: row; flex-wrap: wrap; gap: 8px; } .fq3-nav a { gap: 6px; padding: 7px 13px; border-radius: 99px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); font-size: 13px; } .fq3-nav a.is-on { box-shadow: inset 0 0 0 1px var(--line); color: var(--ink); } }
  @media (max-width: 640px) { .fq2__a { padding-left: 0; } .fq2-more__b, .fq2-more__b .x-btn { width: 100%; } }
"""
faq_js = """<script>
(() => {
  const items = [...document.querySelectorAll('.fq2')], groups = [...document.querySelectorAll('[data-g]')], qIn = document.getElementById('fqQ');
  const nav = [...document.querySelectorAll('.fq3-nav a')], n = document.getElementById('fqN'), none = document.getElementById('fq0'), list = document.getElementById('fqL');
  items.forEach(it => { const s = it.querySelector('.fq2__q'); s.dataset.raw = s.textContent; });
  const esc = t => t.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  // 検索：質問・回答・キーワードで絞り込み、該当がないカテゴリは見出しごと隠す
  const run = () => { const q = qIn.value.trim(); let hit = 0;
    items.forEach(it => { const s = it.querySelector('.fq2__q'), txt = (s.dataset.raw + ' ' + it.querySelector('.fq2__a').textContent + ' ' + it.dataset.k).toLowerCase();
      const ok = !q || q.toLowerCase().split(/\\s+/).every(w => txt.includes(w));
      it.hidden = !ok; if (ok) hit++;
      s.innerHTML = q ? esc(s.dataset.raw).split(esc(q)).join('<mark>' + esc(q) + '</mark>') : esc(s.dataset.raw); });
    groups.forEach(g => { const c = g.querySelectorAll('.fq2:not([hidden])').length; g.hidden = c === 0; const a = nav.find(x => x.dataset.n === g.id); a.classList.toggle('is-off', c === 0); a.querySelector('small').textContent = c; });
    n.hidden = !q; n.textContent = `「${q}」で ${hit}件の質問`; none.hidden = hit > 0; list.hidden = hit === 0; document.getElementById('fq0q').textContent = q; };
  qIn.addEventListener('input', run);
  // いま読んでいるカテゴリを左の一覧で示す
  if ('IntersectionObserver' in window) { const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) nav.forEach(a => a.classList.toggle('is-on', a.dataset.n === e.target.id)); }), { rootMargin: '-120px 0px -60% 0px' }); groups.forEach(g => io.observe(g)); }
  // #q-… で開いたら、その質問を開く
  const open = () => { const t = location.hash && document.querySelector(location.hash + '.fq2'); if (t) { qIn.value = ''; run(); t.open = true; t.scrollIntoView({ block: 'center' }); } };
  window.addEventListener('hashchange', open); run(); open();
  // 回答の評価：「いいえ」なら理由・関連の質問・問い合わせへ（FAQ-006）
  document.querySelectorAll('[data-fb]').forEach(fb => fb.addEventListener('click', e => { const b = e.target.closest('button[data-v]'); if (!b) return;
    if (b.dataset.v === 'yes') { fb.innerHTML = '<span>ありがとうございます。参考にします。</span>'; return; }
    const it = fb.closest('.fq2'), rel = items.filter(x => x !== it && x.dataset.cat === it.dataset.cat).slice(0, 2);
    fb.outerHTML = `<div class="fq2__no"><p>よろしければ、理由を教えてください（任意）</p><div class="rs">${['知りたいことが書かれていない', '説明がわかりにくい', '自分の場合に当てはまるか分からない'].map(r => `<button type="button" aria-pressed="false">${r}</button>`).join('')}</div>
      <p>${rel.length ? '関連する質問：' + rel.map(x => `<a href="#${x.id}">${x.querySelector('.fq2__q').dataset.raw}</a>`).join('　') + '　' : ''}解決しない場合は <a href="contact.html#form">お問い合わせ</a></p></div>`;
    it.querySelectorAll('.rs button').forEach(r => r.addEventListener('click', () => r.setAttribute('aria-pressed', String(r.getAttribute('aria-pressed') !== 'true')))); }));
})();
</script>"""
page('faq.html', 'よくある質問', faq_css, faq_body, faq_js)

# ═════════ 記事ページの見本（AUTH-002 冒頭表記 ＋ SNSシェア ＋ AUTH-001 記事末尾の著者） ═════════
SHARE = [('X', '#111', 'https://x.com/intent/post?url={u}&text={t}'), ('Facebook', '#1877F2', 'https://www.facebook.com/sharer/sharer.php?u={u}'), ('LINE', '#06C755', 'https://social-plugins.line.me/lineit/share?url={u}')]
art_body = f'''<section class="ar-head" id="article-head" aria-labelledby="page-title"><div class="wrap ar-w">
{crumb(('学びのヒント', 'blog.html'), ('記事', None))}
<span class="bl-tag ar-tag">キャリア・学び方</span>
<h1 class="ar-t" id="page-title">働きながら学びを続けるための、<wbr>週2時間のつくり方</h1>
<div class="ar-by"><img class="ar-ph" src="assets/illust/staff.webp" alt="" loading="lazy"><span>著者 <b>The Academy スタッフ</b></span><i aria-hidden="true"></i><span>公開 <time datetime="2026-09-08">2026.09.08</time>／更新 <time datetime="2026-10-01">2026.10.01</time></span><i aria-hidden="true"></i><span>5分で読める</span></div>
</div></section>
<article class="x-sec x-sec--w ar-body" id="article-body"><div class="wrap ar-w">
<img class="ar-img" src="assets/photos/articles/weekly2h.webp" alt="ノートを開いて学習の計画を立てている様子" loading="lazy">
<p class="x-note" style="text-align:right">※本文は見本です</p>
<p>忙しい平日でも学びを止めないために、まずは「週2時間」を確保するところから始めましょう。まとまった時間を探すより、短い時間を決まった場所に置くほうが続きます。</p>
<h2>1. 先に「時間の置き場所」を決める</h2>
<p>平日の夜に30分を2回、週末に1時間。合わせて週2時間です。カレンダーに予定として入れ、ほかの予定と同じように扱います。</p>
<h2>2. 1回で終わる量に分ける</h2>
<p>1回30分で「動画を1本見て、メモを3行書く」のように、終わりが見える単位にすると、次に始めるときの負担が減ります。</p>
<h2>3. 進んだことを、形に残す</h2>
<p>学んだことや作ったものを記録しておくと、続ける理由になります。The Academyでは、学びの記録をポートフォリオに残せます。</p>
<div class="ar-end">
<div class="ar-sh"><p>この記事をシェアする</p><div>{''.join(f'<a href="#" data-share="{tpl}" style="--c:{c}" target="_blank" rel="noopener">{n}</a>' for n, c, tpl in SHARE)}<button type="button" id="arCopy" style="--c:#676688">URLをコピー</button></div></div>
<section class="x-card ar-au" aria-labelledby="au-h"><img class="ar-ph ar-ph--l" src="assets/illust/staff.webp" alt="" loading="lazy"><div><p class="ar-au__k" id="au-h">この記事を書いた人</p><p class="ar-au__n">The Academy スタッフ</p><p class="ar-au__r">The Academy 運営事務局</p>
<p class="ar-au__d">受講生のサポートやキャリア相談で得た気づきをもとに、<wbr>働きながら学ぶためのヒントを発信しています。</p><a class="ar-au__a" href="blog.html">スタッフのほかの記事{ARROW}</a></div></section>
<h2 class="ar-rel__h">関連する記事</h2>
<div class="ar-rel"><a href="/blog/restart">独学が続かなかった人のための、<wbr>学び直しの始め方</a><a href="/blog/portfolio">未経験から実績をつくる、<wbr>ポートフォリオの育て方</a><a href="/blog/aimemo">会議メモをAIで要約する、<wbr>実務の手順</a></div>
</div>
</div></article>'''
art_css = common_css + '''
  .ar-head { padding: clamp(36px, 5vw, 56px) 0 24px; background: var(--bg-gray, #F7F8FB); }
  .ar-w { max-width: 820px; } .ar-tag { display: inline-block; margin-top: 18px; --cc: #0F1B45; --cb: #E6EAF2; padding: 3px 12px; border-radius: 99px; background: var(--cb); color: var(--cc); font-size: 12px; font-weight: 700; }
  .ar-t { margin: 12px 0 0; color: var(--ink); font-size: clamp(26px, 3.4vw, 36px); line-height: 1.45; word-break: keep-all; overflow-wrap: anywhere; }
  .ar-by { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; margin-top: 18px; padding: 12px 16px; border-radius: 14px; background: #fff; box-shadow: 0 0 0 1px var(--line); color: var(--ts-mid); font-size: 13px; }
  .ar-by b { color: var(--ink); } .ar-by i { width: 1px; height: 22px; background: var(--line); }
  .ar-ph { display: block; flex: none; width: 40px; height: 40px; border-radius: 50%; background: #EEF2FC; object-fit: contain; } .ar-ph--l { width: 96px; height: 96px; }
  .ar-body .ar-w { color: var(--ink); font-size: 16px; line-height: 2; } .ar-body h2 { margin: 36px 0 0; font-size: 22px; line-height: 1.5; } .ar-body p { margin: 14px 0 0; }
  .ar-img { display: block; width: 100%; height: auto; border-radius: 18px; }
  .ar-end { margin-top: 48px; padding-top: 32px; border-top: 1px solid var(--line); }
  .ar-sh { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px; padding: 16px 20px; border-radius: 16px; background: var(--bg-gray, #F7F8FB); } .ar-sh p { margin: 0 !important; font-size: 15px; font-weight: 800; }
  .ar-sh div { display: flex; flex-wrap: wrap; gap: 8px; } .ar-sh a, .ar-sh button { display: inline-flex; align-items: center; height: 40px; padding: 0 16px; border: 0; border-radius: 99px; background: var(--c); color: #fff; font: inherit; font-size: 13px; font-weight: 700; line-height: 1; text-decoration: none; cursor: pointer; }
  .ar-au { display: grid; grid-template-columns: 96px minmax(0, 1fr); gap: 22px; margin-top: 16px; padding: 26px; line-height: 1.7; }
  .ar-au__k { margin: 0 !important; color: var(--ts-mid); font-size: 12px !important; font-weight: 800; letter-spacing: .08em; } .ar-au__n { margin: 4px 0 0 !important; font-size: 20px; font-weight: 800; }
  .ar-au__r { margin: 0 !important; color: var(--ts-primary); font-size: 13px !important; font-weight: 700; } .ar-au__d { margin: 8px 0 0 !important; color: var(--ts-mid); font-size: 14px !important; }
  .ar-au__a { display: inline-flex; align-items: center; gap: 4px; margin-top: 8px; color: var(--ts-primary); font-size: 14px; font-weight: 700; text-decoration: none; } .ar-au__a svg { width: 15px; height: 15px; }
  .ar-rel__h { font-size: 17px !important; margin-top: 28px !important; } .ar-rel { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 12px; }
  .ar-rel a { padding: 14px 16px; border-radius: 14px; background: #fff; box-shadow: 0 0 0 1px var(--line); color: var(--ink); font-size: 14px; font-weight: 700; line-height: 1.6; text-decoration: none; } .ar-rel a:hover { box-shadow: 0 0 0 1.5px var(--ts-primary); }
  @media (max-width: 640px) { .ar-by i { display: none; } .ar-au { grid-template-columns: minmax(0, 1fr); } .ar-rel { grid-template-columns: minmax(0, 1fr); } }
'''
art_js = '''<script>
(() => {
  const u = encodeURIComponent(location.href), t = encodeURIComponent(document.title);
  document.querySelectorAll('[data-share]').forEach(a => a.href = a.dataset.share.replace('{u}', u).replace('{t}', t));
  const c = document.getElementById('arCopy');
  c.addEventListener('click', async () => { try { await navigator.clipboard.writeText(location.href); c.textContent = 'コピーしました'; } catch (e) { c.textContent = 'コピーできませんでした'; } setTimeout(() => c.textContent = 'URLをコピー', 2000); });
})();
</script>'''
page('article.html', '働きながら学びを続けるための、週2時間のつくり方', art_css, art_body, art_js, nav='blog.html')

exec(open(os.path.join(S, 'k2block.py')).read())  # コース詳細（K2）は k2block.py・k2.css

