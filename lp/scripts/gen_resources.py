# お役立ち資料（resources）：R3 の構成（新着1点＋一覧＋LINE）に、お名前・メールアドレスを入れてすぐダウンロードする受け取り方を組み合わせる
# 資料は随時入れ替わる前提。RES は見本データで、PDF の URL と送信先は未設定（.x-todo）
import os, tempfile
S = os.path.dirname(os.path.abspath(__file__))          # このスクリプトのフォルダ（lp/scripts）
LPDIR = os.path.dirname(S)                              # 出力先（lp）
TMP_COURSES = os.path.join(tempfile.gettempdir(), 'ta_courses_tmp.html')  # 共通部品を取り出すときの捨て出力
import os, re
g = {'__file__': os.path.join(S, 'gen_courses.py')}
os.environ['TA_COURSES_OUT'] = TMP_COURSES
exec(open(os.path.join(S, 'gen_courses.py')).read(), g)
head, between, footer_on, base_css, ARROW = g['head'], g['between'], g['footer_on'], g['css'], g['ARROW']
LP = LPDIR + '/'

def ic(d, w=2): return f'<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{d}</g></svg>'
DL = ic('<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>', 2.2)
X = ic('<path d="M6 6l12 12M18 6 6 18"/>', 2.2)
OK = ic('<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>', 2.2)
LN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3C6.5 3 2 6.6 2 11c0 3.9 3.5 7.2 8.3 7.9.3.1.8.2.9.5.1.3.1.7 0 1l-.1.9c0 .3-.2 1 .9.5s5.9-3.5 8-6C21.4 14.3 22 12.7 22 11c0-4.4-4.5-8-10-8z"/></svg>'
TODO = lambda t: f'<span class="x-todo">{t}</span>'

# (id, カテゴリ, 資料名, 説明, 形式, 表紙の色, PDFのURL)
RES = [
 ('sns-plan', 'SNS・マーケ', 'SNS投稿 企画シート', '投稿のねらい・ターゲット・内容を1枚に整理できるシートです。投稿を始める前に、何を誰に届けるかを決めておくと、迷わず続けられます。', 'PDF・4ページ', '#0141D4', ''),
 ('gpt-prompt', 'AI・IT', 'ChatGPT 指示文の型 20選', '仕事でそのまま使える指示文を、目的別にまとめました。', 'PDF・18ページ', '#0F1B45', ''),
 ('pf-check', 'キャリア', 'ポートフォリオ作成チェックリスト', '採用担当に伝わる作品の見せ方を、10項目で確認できます。', 'PDF・6ページ', '#E46A1F', ''),
 ('toeic-plan', '英語', 'TOEIC 8週間 学習スケジュール表', '週2時間から始められる、書き込み式の計画表です。', 'PDF・3ページ', '#2F6BFF', ''),
 ('ig-insight', 'SNS・マーケ', 'Instagram 分析の見方ガイド', 'インサイトのどの数字を見ればいいかを解説します。', 'PDF・12ページ', '#0141D4', ''),
 ('sheet-func', 'AI・IT', 'Googleスプレッドシート 時短関数まとめ', 'よく使う関数を、使う場面ごとに整理しました。', 'PDF・10ページ', '#0F1B45', ''),
]

def cover(t, col, cls=''):
    return f'<div class="rs-cv {cls}" style="--c:{col}" aria-hidden="true"><span>THE ACADEMY</span><b>{t}</b></div>'
def btn(r, label, cls='x-btn'):
    return f'<button type="button" class="{cls}" data-dl="{r[0]}" data-title="{r[2]}" data-pdf="{r[6]}">{DL}{label}</button>'

f0 = RES[0]
rows = ''.join(f'''<li class="rs-r"><span class="rs-dot" style="--c:{r[5]}" aria-hidden="true"></span><div class="rs-r__b"><p class="rs-tag">{r[1]}</p><h3>{r[2]}</h3><p class="rs-d">{r[3]}</p></div><span class="rs-m">{r[4]}</span>{btn(r, 'ダウンロード', 'rs-r__btn')}</li>''' for r in RES[1:])

body = f'''<section class="phead" aria-labelledby="page-title"><div class="wrap">
<nav class="crumb" aria-label="パンくずリスト"><a href="lp-design.html">トップ</a><span aria-hidden="true">/</span><span aria-current="page">お役立ち資料</span></nav>
<h1 class="phead__t" id="page-title">お役立ち資料</h1>
<p class="phead__lead">学びや仕事に役立つ資料を、<wbr>無料で配布しています。<wbr>内容は随時更新します。</p>
</div></section>
<section class="x-sec x-sec--w" id="featured" aria-labelledby="rs-new"><div class="wrap rs-f">
{cover(f0[2], f0[5], 'rs-cv--b')}
<div class="rs-f__b"><p class="rs-tag">新着の資料<em>{f0[1]}</em></p><h2 class="rs-f__t" id="rs-new">{f0[2]}</h2><p class="rs-f__d">{f0[3]}</p><p class="rs-m">{f0[4]}</p>
{btn(f0, '無料でダウンロード')}
<p class="x-note">お名前とメールアドレスを入力すると、すぐにダウンロードできます。 {TODO('資料は見本')}</p></div>
</div></section>
<section class="x-sec x-sec--g" id="list" aria-labelledby="rs-list"><div class="wrap">
<h2 class="rs-h2" id="rs-list">資料の一覧</h2>
<ul class="rs-l">{rows}</ul>
</div></section>
<section class="rs-line" aria-labelledby="rs-line"><div class="wrap rs-line__in"><div><p class="rs-line__t" id="rs-line">新しい資料のお知らせは、公式LINEで</p><p class="rs-line__d">資料が増えたときにお知らせします。<wbr>全コース500円OFFのクーポンもお届けします。</p></div>
<a class="x-btn x-btn--g" href="beginners.html#line">{LN}友だち追加する</a></div></section>
<dialog class="rs-dlg" id="rsDlg" aria-labelledby="rsDlgT">
<button type="button" class="rs-dlg__x" id="rsX" aria-label="閉じる">{X}</button>
<form id="rsForm" novalidate>
<p class="rs-dlg__k">無料でダウンロード</p><h2 class="rs-dlg__t" id="rsDlgT"></h2>
<label class="rs-fl" for="rsName">お名前<input id="rsName" name="name" autocomplete="name" placeholder="例：山田 花子" required></label>
<label class="rs-fl" for="rsMail">メールアドレス<input id="rsMail" name="email" type="email" autocomplete="email" inputmode="email" placeholder="例：hanako@example.com" required></label>
<p class="rs-err" id="rsErr" role="alert" hidden></p>
<label class="rs-ck" for="rsNews"><input type="checkbox" id="rsNews" name="news" checked>新しい資料やコースのお知らせを受け取る</label>
<button type="submit" class="x-btn rs-sub">{DL}ダウンロードする</button>
<p class="x-note"><a href="privacy.html">プライバシーポリシー</a>に同意のうえ、送信してください。 {TODO('送信先（フォームの保存先）を設定')}</p>
</form>
<div class="rs-done" id="rsDone" hidden>
<span class="rs-done__ic">{OK}</span><p class="rs-dlg__t">ダウンロードを開始しました</p>
<p class="rs-done__d">始まらないときは、下のボタンからダウンロードしてください。<wbr>次回からは入力なしでダウンロードできます。</p>
<a class="x-btn" id="rsAgain" download>{DL}もう一度ダウンロード</a>
<p class="x-note" id="rsNoPdf" hidden>{TODO('PDFのURLを設定')}（見本のため、ファイルはまだありません）</p>
</div>
</dialog>'''

css = '''
  .x-todo { display: inline-block; padding: 1px 8px; border-radius: 6px; background: #FFF1E7; color: #E46A1F; font-size: 11.5px; font-weight: 700; vertical-align: middle; }
  .x-sec { padding: clamp(48px, 6vw, 80px) 0; } .x-sec--g { background: var(--bg-gray, #F7F8FB); } .x-sec--w { background: #fff; }
  .x-btn { display: inline-flex; align-items: center; justify-content: center; gap: 6px; min-height: 50px; padding: 0 24px; border: 0; border-radius: 12px; background: var(--ts-primary); color: #fff; font: inherit; font-size: 15px; font-weight: 700; text-decoration: none; cursor: pointer; }
  .x-btn svg { width: 17px; height: 17px; } .x-btn--g { background: #06C755; }
  .x-note { margin: 10px 0 0; color: var(--ts-mid); font-size: 12.5px; line-height: 1.7; } .x-note a { color: var(--ts-primary); }
  .rs-cv { position: relative; display: flex; flex-direction: column; justify-content: space-between; aspect-ratio: 1 / 1.3; padding: 24px; border-radius: 10px; background: var(--c); color: #fff; overflow: hidden; box-shadow: 0 10px 28px rgba(15,27,69,.16); }
  .rs-cv::after { content: ""; position: absolute; right: -30%; bottom: -18%; width: 80%; aspect-ratio: 1; border-radius: 50%; background: rgba(255,255,255,.12); }
  .rs-cv span { font-size: 10px; letter-spacing: .16em; opacity: .8; } .rs-cv b { position: relative; z-index: 1; font-size: 24px; line-height: 1.45; }
  .rs-f { display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: 56px; align-items: center; }
  .rs-tag { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin: 0; color: var(--ts-primary); font-size: 12.5px; font-weight: 700; }
  .rs-tag em { padding: 1px 9px; border-radius: 99px; background: #FFF1E7; color: #E46A1F; font-style: normal; font-size: 11.5px; }
  .rs-f__t { margin: 10px 0 0; color: var(--ink); font-size: clamp(24px, 2.6vw, 30px); line-height: 1.45; }
  .rs-f__d { max-width: 52ch; margin: 12px 0 0; color: var(--ts-mid); font-size: 15px; line-height: 1.85; }
  .rs-m { margin: 8px 0 0; color: var(--ts-mid); font-size: 12.5px; white-space: nowrap; } .rs-f .x-btn { margin-top: 20px; }
  .rs-h2 { margin: 0 0 20px; color: var(--ink); font-size: clamp(20px, 2.2vw, 24px); }
  .rs-l { margin: 0; padding: 0; list-style: none; border-radius: 20px; background: #fff; box-shadow: 0 0 0 1px var(--line); }
  .rs-r { display: grid; grid-template-columns: 10px minmax(0, 1fr) auto auto; gap: 20px; align-items: center; padding: 20px 24px; border-top: 1px solid var(--line); }
  .rs-r:first-child { border-top: 0; } .rs-dot { width: 10px; height: 10px; border-radius: 3px; background: var(--c); }
  .rs-r h3 { margin: 4px 0 0; color: var(--ink); font-size: 16px; line-height: 1.5; } .rs-d { margin: 4px 0 0; color: var(--ts-mid); font-size: 13.5px; line-height: 1.7; } .rs-r .rs-m { margin: 0; }
  .rs-r__btn { display: inline-flex; align-items: center; gap: 6px; height: 42px; padding: 0 16px; border: 0; border-radius: 10px; background: #EEF2FD; color: var(--ts-primary); font: inherit; font-size: 13.5px; font-weight: 700; cursor: pointer; white-space: nowrap; }
  .rs-r__btn svg { width: 15px; height: 15px; } .rs-r__btn:hover { background: var(--ts-primary); color: #fff; }
  .rs-line { padding: 44px 0; background: #E9F9EF; } .rs-line__in { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 20px; }
  .rs-line__t { margin: 0; color: var(--ink); font-size: 20px; font-weight: 800; } .rs-line__d { margin: 6px 0 0; color: var(--ts-mid); font-size: 14px; line-height: 1.7; }
  .rs-dlg { width: min(460px, calc(100% - 32px)); max-height: calc(100% - 32px); padding: 32px; border: 0; border-radius: 22px; color: var(--ink); box-shadow: 0 24px 60px rgba(15,27,69,.25); }
  .rs-dlg::backdrop { background: rgba(15,27,69,.45); }
  .rs-dlg__x { position: absolute; top: 14px; right: 14px; display: grid; place-items: center; width: 36px; height: 36px; border: 0; border-radius: 50%; background: var(--bg-gray, #F7F8FB); color: var(--ink); cursor: pointer; } .rs-dlg__x svg { width: 18px; height: 18px; }
  .rs-dlg form { display: flex; flex-direction: column; gap: 14px; }
  .rs-dlg__k { margin: 0; color: var(--ts-primary); font-size: 12.5px; font-weight: 700; } .rs-dlg__t { margin: 0; padding-right: 36px; font-size: 19px; font-weight: 800; line-height: 1.5; }
  .rs-fl { display: flex; flex-direction: column; gap: 6px; font-size: 13.5px; font-weight: 700; }
  .rs-fl input { height: 48px; padding: 0 14px; border: 1px solid rgba(15,27,69,.2); border-radius: 10px; font: inherit; font-size: 16px; font-weight: 400; color: var(--ink); }
  .rs-fl input:focus { outline: 2px solid var(--ts-primary); outline-offset: 1px; } .rs-fl input[aria-invalid="true"] { border-color: #D93025; }
  .rs-err { margin: -4px 0 0; color: #D93025; font-size: 13px; font-weight: 700; }
  .rs-ck { display: flex; align-items: center; gap: 8px; font-size: 13.5px; } .rs-ck input { width: 18px; height: 18px; accent-color: var(--ts-primary); }
  .rs-sub { width: 100%; margin-top: 4px; } .rs-dlg .x-note { margin: 0; }
  .rs-done { display: flex; flex-direction: column; align-items: center; gap: 12px; text-align: center; } .rs-done .rs-dlg__t { padding: 0; }
  .rs-done__ic { display: grid; place-items: center; width: 56px; height: 56px; border-radius: 50%; background: #E9F9EF; color: #06A04A; } .rs-done__ic svg { width: 30px; height: 30px; }
  .rs-done__d { margin: 0; color: var(--ts-mid); font-size: 14px; line-height: 1.8; } .rs-done .x-btn { width: 100%; } .rs-done .x-btn[aria-disabled="true"] { opacity: .45; pointer-events: none; }
  .rs-dlg [hidden] { display: none !important; }
  @media (max-width: 900px) { .rs-f { grid-template-columns: minmax(0, 1fr); gap: 28px; } .rs-cv--b { max-width: 220px; } .rs-cv--b b { font-size: 20px; }
    .rs-r { grid-template-columns: 10px minmax(0, 1fr); gap: 6px 14px; padding: 18px; } .rs-dot { grid-row: 1 / 4; align-self: start; margin-top: 6px; } .rs-r .rs-m, .rs-r__btn { grid-column: 2; } .rs-r__btn { justify-self: start; margin-top: 6px; }
    .rs-line__in .x-btn { width: 100%; } .rs-f .x-btn { width: 100%; } }
  @media (max-width: 480px) { .rs-dlg { padding: 26px 20px; } }
'''

script = '''<script>
(() => {
  const dlg = document.getElementById('rsDlg'), form = document.getElementById('rsForm'), done = document.getElementById('rsDone');
  const tEl = document.getElementById('rsDlgT'), err = document.getElementById('rsErr'), name = document.getElementById('rsName'), mail = document.getElementById('rsMail');
  const again = document.getElementById('rsAgain'), noPdf = document.getElementById('rsNoPdf');
  const KEY = 'ta-res-lead'; let cur = null;
  const known = () => { try { return !!localStorage.getItem(KEY); } catch (e) { return false; } };
  // ダウンロード：PDF の URL があればすぐに保存を始める（未設定の見本では案内だけ出す）
  const start = r => { const has = !!r.pdf; again.toggleAttribute('hidden', false); noPdf.hidden = has;
    if (has) { again.href = r.pdf; again.removeAttribute('aria-disabled'); again.click(); } else { again.removeAttribute('href'); again.setAttribute('aria-disabled', 'true'); } };
  const showDone = () => { form.hidden = true; done.hidden = false; };
  document.querySelectorAll('[data-dl]').forEach(b => b.addEventListener('click', () => {
    cur = { id: b.dataset.dl, title: b.dataset.title, pdf: b.dataset.pdf };
    tEl.textContent = cur.title; err.hidden = true; [name, mail].forEach(x => x.removeAttribute('aria-invalid'));
    if (known()) { showDone(); dlg.showModal(); start(cur); return; }   // 2回目からは入力なし
    form.hidden = false; done.hidden = true; dlg.showModal(); name.focus(); }));
  form.addEventListener('submit', e => { e.preventDefault();
    const bad = [!name.value.trim() && [name, 'お名前を入力してください'], !/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(mail.value.trim()) && [mail, 'メールアドレスを正しく入力してください（例：hanako@example.com）']].filter(Boolean);
    [name, mail].forEach(x => x.setAttribute('aria-invalid', String(bad.some(([el]) => el === x))));
    if (bad.length) { err.textContent = bad[0][1]; err.hidden = false; bad[0][0].focus(); return; }
    // TODO：送信先（フォームサービス・CRM）へ { name, email, news, resource: cur.id } を送る
    try { localStorage.setItem(KEY, '1'); } catch (e) {}
    showDone(); start(cur); });
  document.getElementById('rsX').addEventListener('click', () => dlg.close());
  dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
})();
</script>'''

html = head + base_css + css + between + '<main>\n' + body + '\n' + footer_on.replace('</body>', script + '</body>')
html = re.sub(r'<title>[^<]*</title>', '<title>お役立ち資料 | The Academy</title>', html, count=1)
html = html.replace('href="/beginners', 'href="beginners.html')
open(LP + 'resources.html', 'w').write(html); print('ok resources.html', len(html))
