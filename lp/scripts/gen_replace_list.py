# 差し替え箇所の一覧（画像／仮置き／文章）を、確認用ページ（lp/docs/replace-list.html）と CSV（lp/docs/replace-list.csv）に書き出す
# 2026-10-08 時点の lp/*.html を全ページ走査した結果をもとに、ページ・セクション単位でまとめたもの
import os, csv, html
S = os.path.dirname(os.path.abspath(__file__)); DOCS = os.path.join(os.path.dirname(S), 'docs')

# 種類：画像／仮置き／文章　状態：差し替え（仮のもの）／確認（このまま使えるか判断）／確定（このまま使う）
IMG = [
 # (ページ, セクション, 素材, いまの中身, 状態, 対応)
 ('トップ', 'HERO', 'assets/hero.webp', 'AIで作った写真（候補から採用）', '確認', '本番でもこの画像を使うか。人物の写り・権利を確認'),
 ('トップ・コースを探す・受講までの流れ', '人気のコース／コース一覧／流れ', 'assets/photos/sns-phone.webp・ai-laptop.webp・toeic-study.webp', '3枚の写真を12コースのサムネイルに使い回し（sns-phone は10か所）', '差し替え', 'コースごとのサムネイルを用意（Wix ストアの商品画像を使ってもよい）'),
 ('トップ', '04 ポートフォリオ', 'assets/courses/ai.webp・marketing.webp', 'ポートフォリオ画面の中のコース画像', '確認', 'コースのサムネイルを差し替えたら、同じ画像にそろえる'),
 ('コースを探す', '特集', 'assets/courses/feat-slack.webp・feat-toeic.webp', 'Slack×GAS・TOEIC の特集画像', '確認', '本番の画像か確認'),
 ('学び方・受講成果', '4ステップ', 'assets/how/step-01〜04.webp', '学びの4ステップの画面イメージ', '確認', '実際の受講画面に近いか確認'),
 ('学び方・受講成果', '受講成果', 'assets/outcomes/*.webp（6枚）', '見本として作った成果物の画像（企画書・プロンプト・プレゼンなど）', '差し替え', '本人の了承を得た、実際の受講生の成果物に差し替えるか判断'),
 ('コース詳細（SNS）・ポートフォリオ', '成果物／フィード', 'assets/outcomes/sns-design.webp', 'SNS の成果物画像（見本）', '差し替え', '実際の成果物に差し替えるか判断'),
 ('ポートフォリオ・はじめての方へ', '見出し／SHOW／例', 'assets/portfolio/*.webp（12枚）', '実際の画面を匿名化したもの（X風ニックネーム）', '確認', '匿名化の最終確認（名前・顔・社名が残っていないか）'),
 ('はじめての方へ', 'ABOUT／FOR YOU', 'assets/illust/about-community・for-you-1〜3.webp', '作成したイラスト', '確定', 'そのまま使用'),
 ('全ページ', 'NEXT STEP', 'assets/illust/next-zoom.webp', 'オンライン相談の画面とパンフレットのイラスト（17か所で共通）', '確定', 'そのまま使用'),
 ('トップ・学びのヒント', '記事カード', 'assets/journal/ai・career・sns.webp', '記事のアイキャッチ（見本）', '差し替え', '実際の記事のアイキャッチに'),
 ('学びのヒント', 'アクセスの多い記事／評価の高い記事／最新記事', 'assets/outcomes・how・portfolio の画像', '記事のアイキャッチの代わりに、成果物・学び方・ポートフォリオの画像を仮で使用', '差し替え', '実際の記事のアイキャッチに'),
 ('無料相談・資料請求', 'パンフレットのタブ', 'assets/pamphlet/cover.webp', 'パンフレットの表紙', '確認', '最新版のパンフレットの表紙か確認'),
 ('全ページ', 'ヘッダー・フッター', 'assets/academy_logo_blue_trim.png', 'ロゴ', '確定', 'そのまま使用（Wix では SVG があれば SVG）'),
 ('コース詳細（SNS 以外の12ページ）', '成果物の画像', '（画像なし・CSS で描いた仮画像）', 'カテゴリ色の仮画像＋「成果物の画像（準備中）」', '差し替え', '各コースの成果物の画像を用意'),
 ('お役立ち資料', '新着／一覧', '（画像なし・CSS で描いた表紙）', '資料名を書いた色違いの仮の表紙', '差し替え', '実際の資料の表紙に'),
 ('記事ページ（見本）', '冒頭・著者', '（画像なし・「写真」の枠）', '著者・監修者の写真の枠', '差し替え', '著者の写真を用意（なければ枠ごと外す）'),
 ('数字の根拠', '自由回答', 'assets/avatars/*.svg（3種）', '用意いただいたアイコン', '確定', 'そのまま使用'),
 ('数字の根拠', '満足度・コース数', '（SVG で描いたグラフ）', 'レーダーチャートとカテゴリ別の棒グラフ', '確認', '本番の数字に変えたら作り直す'),
 ('全ページ', 'SNS で共有したときの画像', '（なし）', 'OGP 画像がない', '差し替え', '1200×630 の画像を新しく作る'),
]

TMP = [
 # (分類, ページ, 箇所, いまの表示, 必要なもの)
 ('数字', 'トップ', 'HERO の実績', '「2026年◯月時点 要確認」「受講生アンケート・回答◯名 要確認」', '数字の根拠ページと同じ値にそろえる（いまは食い違っている）'),
 ('数字', '数字の根拠', '平均満足度', '総合4.2・5項目の平均・実施期間 2026年8月・回答128名（回答率42％）＝すべて仮', 'アンケートの実際の集計'),
 ('数字', '数字の根拠', 'コース数', '12コース（Slack×GAS は数えない）', 'Slack×GAS を含めるかの判断'),
 ('数字', '学びのヒント', '記事カード', 'いいね・役に立ったの数（142／128／118 など）、日付', '実際の数字（出さない選択も可）'),
 ('数字', 'コースを探す', 'コースを比べる', '「確認中」「※」の項目', '各コースの実際の値'),
 ('価格', 'トップ・コースを探す・コース詳細', 'SNSマーケティング実践・生成AI 業務改善・TOEIC 700点・Slack×GAS', '「¥—」（価格の確定待ち）', '税込価格。ほかの9コースは今のサイトの価格を表示中（変わるなら連絡）'),
 ('コース', 'コース詳細（12ページ）', '成果物', '成果物の名前（例）と仮画像', '各コースで完成する成果物の名前と画像'),
 ('コース', 'コース詳細（13ページ）', '学習の流れ', 'SNS は8週の見本、ほかは共通の4ステップ、Slack×GAS は導入の手順（「内容は仮」）', '各コースの実際の流れ'),
 ('コース', 'コース詳細・コースを探す（8コース）', '学習の目安', '期間・週の時間が空欄（マーケティング戦略基礎・インスタグラム・自動化ツール開発・初級編 ChatGPT・公式LINE運用・ビジネス英語初級・プロジェクトマネジメント・Canva初級）', '各コースの期間と週の時間'),
 ('リンク', '全ページ', 'ヘッダーの「ログイン」', '/login（行き先なし）', 'ログインの URL'),
 ('リンク', 'コース詳細（13ページ）', '「このコースを受講する」・スマホの固定バー', '#（行き先なし）', 'カート（ストアの商品）の URL'),
 ('リンク', '全ページ', 'フッターの SNS アイコン8つ', '#（行き先なし）', '各 SNS の URL。使っていないものは外す'),
 ('リンク', '全ページ', '公式LINE のボタン・浮かぶボタン', 'はじめての方への LINE 欄に移動するだけ', '友だち追加の URL'),
 ('リンク', '無料相談・資料請求', '「パンフレット（PDF）をダウンロード」', '#（行き先なし）', 'パンフレットの PDF'),
 ('リンク', 'ポートフォリオ', '「無料で登録する」（2か所）', '同じページの「はじめかた」に移動するだけ', '登録ページの URL'),
 ('リンク', 'トップ・学びのヒント・記事', '記事11本', '/blog/〜（行き先なし）', '今の Wix ブログの記事 URL'),
 ('リンク', 'お役立ち資料', 'ダウンロード', 'PDF の URL なし', '各資料の PDF'),
 ('機能', '無料相談・資料請求', '日時の表', '空き状況は表示例', '予約の仕組み（Wix ブッキングなど）と予約枠'),
 ('機能', '無料相談・資料請求', 'パンフレット・お問い合わせのフォーム', '送信されない見本（「※このページは見本です」）', '受信先と自動メール'),
 ('機能', 'お役立ち資料', '受け取りのフォーム', '送信先なし', '受け取り方式と送信先（エンジニアと相談）'),
 ('確認', '無料相談・資料請求', '「顔を出さないといけませんか？」', '「カメラはオフでも参加できます」に要確認の印', 'カメラオフで参加できるか'),
 ('法務', '特商法・プライバシー・利用規約', '末尾', '制定日・最終更新日「2026年◯月◯日」', '公開日'),
 ('見本', '学びのヒント', '記事一覧', '記事タイトル・日付・評価は見本', '実際の記事'),
 ('見本', '記事ページ', '本文・著者', '本文は見本、著者名・監修者名・紹介文は仮', '実際の記事と著者'),
 ('見本', 'お役立ち資料', '資料6件', '資料名・説明・ページ数は見本', '実際の資料'),
 ('見本', '数字の根拠', '自由回答3件', '声とニックネームは見本', '本人の了承を得た実際の回答'),
]

TXT = [
 # (分類, ページ, 箇所, 今のサイト（または以前の案）, 新しいサイト)
 ('変更', 'トップ', 'ヒーローのキャッチ', '自分らしく成長できる学びのサードプレイス', '学んで、つくって、次のキャリアへ。（「サードプレイス」はコミュニティーの説明へ）'),
 ('変更', 'トップ', 'ヒーローのリード文', '講師と仲間に支えられながら', '仲間の歩みを励みにしながら（講師フィードバックを約束しない方針）'),
 ('変更', 'トップ', '実績の表記', '週2〜／満足度4.8・20+（以前の案）', '実践コース 10+・平均満足度 4.2・週2h〜（根拠ページへリンク）'),
 ('変更', 'はじめての方へ', 'お悩み3つ', '入社3〜5年目／副業・独立志望／グローバルキャリア', '「たとえば、こんな想いに。」心の声3つ（属性の呼びかけをやめる）'),
 ('変更', '全ページ', '公式LINE の特典3', '限定コミュニティに参加できる', '限定イベントの情報が届く'),
 ('変更', 'トップ・はじめての方へ', '受講までの流れ', '①無料相談から始まる4ステップ', 'コースを選ぶ → 決済 → 受講 → 残す・飛び込む（相談は希望者のみの一文）'),
 ('変更', 'トップ・無料相談', 'キャリアの3分岐', '無料体験講座／無料相談会／パンフレット', '無料相談（主）とパンフレットの2択。無料体験は廃止'),
 ('変更', 'トップ', '選ばれる理由', '3つ（「5-15万円」の表記あり）', 'WHY・流れ・LINE などに分けて説明。「5-15万円」は今の価格と合わないため要確認'),
 ('変更', '全ページ', 'カテゴリ名', '語学・TOEIC など', 'IT・デジタル／マーケティング／英語・TOEIC／ビジネス／クリエイティブ（記事のみ「キャリア・学び方」を追加）'),
 ('変更', '全ページ', '表記の統一', '—', '「コミュニティー」「3か月」「週2〜3時間」の形'),
 ('変更', 'コース', '新しいコース名', '今の商品名', 'SNSマーケティング実践・生成AI 業務改善・TOEIC L&R 700点突破 は新しい名前（今の商品との対応は要確認）'),
 ('変更', 'コース詳細', '見出し', 'コース名＋説明', '完成する成果物を主語にした1行（例：8週間で、SNSキャンペーン企画書を完成させる）。講師欄なし'),
 ('変更', 'よくある質問', '回答', '今の FAQ（6カテゴリ）', '13問。返金・取り消し・受講期間・月額・スマホ・ポートフォリオ・数字の根拠は規約と同じ内容で確定。講師フィードバックの質問は削除'),
 ('変更', 'コースを探す', '比較表', '講師のフィードバックの行あり（以前の案）', '講師のフィードバックの行を削除'),
 ('新規', '法務3ページ', '全文', '今の文面（あれば）', '確定版の文面に差し替え（特商法・プライバシーポリシー・利用規約）'),
 ('新規', '学び方・ポートフォリオ・はじめての方へ・数字の根拠・お役立ち資料', '全文', '—', '新しく書いた文章（Wix に入力）'),
 ('要確認', 'コース', '「TOEIC L&R 700点突破」', '—', '結果の約束に読めるため、「700点を目指す」などの言い方か注記を検討'),
 ('仮の文章', 'コース詳細（12ページ）', '見出し・説明・こんな方に・できること', '—', '共通の型で作った仮の文章。各コースの実際の内容に書き換え'),
 ('仮の文章', 'コースを探す', 'コース診断', '—', '質問文・結果の理由の文言を確認'),
 ('仮の文章', '学びのヒント・記事ページ', '記事タイトル・抜粋・本文・著者紹介', '—', '実際の記事に差し替え'),
 ('仮の文章', 'お役立ち資料', '資料名・説明', '—', '実際の資料に差し替え'),
 ('仮の文章', '数字の根拠', '自由回答・調査の概要', '—', '実際のアンケートに合わせて書き換え'),
 ('仮の文章', 'ポートフォリオ・トップ05', '画面の中の投稿・トーク', '—', '見本の文章（ニックネームは匿名）。このままでよいか確認'),
]

def write_csv():
    with open(os.path.join(DOCS, 'replace-list.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['種類', '分類・状態', 'ページ', '箇所', 'いまの中身', '対応・必要なもの'])
        for p, s, src, now, st, todo in IMG: w.writerow(['画像', st, p, s + '｜' + src, now, todo])
        for c, p, s, now, need in TMP: w.writerow(['仮置き', c, p, s, now, need])
        for c, p, s, old, new in TXT: w.writerow(['文章', c, p, s, old, new])

def e(x): return html.escape(x)
PILL = {'差し替え': 'w', '確認': 'c', '確定': 'o', '変更': 'c', '新規': 'o', '要確認': 'w', '仮の文章': 'w'}
def pill(t): return f'<span class="pill pill--{PILL.get(t, "c")}">{e(t)}</span>'

def write_html():
    cnt = lambda rows, k, v: sum(1 for r in rows if r[k] == v)
    img_rows = ''.join(f'<tr data-k="{e(st)}"><td>{pill(st)}</td><th scope="row">{e(p)}<small>{e(s)}</small></th><td><code>{e(src)}</code><p>{e(now)}</p></td><td>{e(todo)}</td></tr>' for p, s, src, now, st, todo in IMG)
    tmp_rows = ''.join(f'<tr><td><span class="tag">{e(c)}</span></td><th scope="row">{e(p)}<small>{e(s)}</small></th><td>{e(now)}</td><td>{e(need)}</td></tr>' for c, p, s, now, need in TMP)
    txt_rows = ''.join(f'<tr><td>{pill(c)}</td><th scope="row">{e(p)}<small>{e(s)}</small></th><td>{e(old)}</td><td>{e(new)}</td></tr>' for c, p, s, old, new in TXT)
    page = f'''<title>The Academy 差し替え箇所リスト</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Josefin+Sans:wght@600&display=swap">
<style>
/* レイアウト：上に要約の数字、下に3つの表（画像／仮置き／文章）。表は横にはみ出すときだけ枠の中でスクロール */
:root {{ --bg:#FFFFFF; --surface:#F5F6FA; --ink:#0F1B45; --mid:#5E6182; --line:#DFE2EC; --accent:#0141D4; --warn-bg:#FFF1E7; --warn:#C2560F; --ok-bg:#E9F9EF; --ok:#13804A; --c-bg:#EAF0FF;
  --f-body:"Noto Sans JP","Hiragino Sans","Yu Gothic",system-ui,sans-serif; --f-en:"Josefin Sans","Noto Sans JP",sans-serif; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#0E1430; --surface:#161E40; --ink:#E8EBF7; --mid:#A3A8C8; --line:#2A3462; --accent:#7EA2FF; --warn-bg:#3A2614; --warn:#FFB27A; --ok-bg:#12301F; --ok:#7BE0A6; --c-bg:#1D2A5C; color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --bg:#0E1430; --surface:#161E40; --ink:#E8EBF7; --mid:#A3A8C8; --line:#2A3462; --accent:#7EA2FF; --warn-bg:#3A2614; --warn:#FFB27A; --ok-bg:#12301F; --ok:#7BE0A6; --c-bg:#1D2A5C; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--f-body); font-size: 15px; line-height: 1.8; padding-inline: 16px; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding-block: 40px 96px; }}
.eyebrow {{ margin: 0; color: var(--accent); font-family: var(--f-en); font-size: 12px; letter-spacing: .14em; }}
h1 {{ margin: 6px 0 8px; font-size: clamp(26px, 4vw, 34px); line-height: 1.4; text-wrap: balance; }}
.lead {{ margin: 0; color: var(--mid); max-width: 70ch; }}
.sum {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin: 28px 0 0; padding: 0; list-style: none; }}
.sum li {{ padding: 18px 20px; border-radius: 14px; background: var(--surface); }}
.sum b {{ display: block; font-size: 28px; line-height: 1.2; font-variant-numeric: tabular-nums; }} .sum span {{ color: var(--mid); font-size: 13px; }}
.key {{ margin-top: 20px; padding: 16px 20px; border-left: 3px solid var(--warn); border-radius: 0 12px 12px 0; background: var(--warn-bg); font-size: 14px; }}
.key p {{ margin: 0; }}
nav.jump {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 28px; }}
nav.jump a {{ padding: 7px 14px; border-radius: 99px; background: var(--surface); color: var(--ink); font-size: 13.5px; font-weight: 700; text-decoration: none; }}
section {{ margin-top: 56px; scroll-margin-top: 16px; }}
h2 {{ margin: 0 0 6px; font-size: 22px; }} h2 + p {{ margin: 0 0 14px; color: var(--mid); font-size: 14px; }}
.tbl {{ overflow-x: auto; }}
table {{ width: 100%; min-width: 760px; border-collapse: collapse; font-size: 13.5px; line-height: 1.7; }}
th, td {{ padding: 12px 14px 12px 0; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
thead th {{ color: var(--mid); font-size: 12px; font-weight: 500; white-space: nowrap; }}
tbody th {{ width: 22%; font-weight: 700; }} tbody th small {{ display: block; color: var(--mid); font-weight: 500; font-size: 12px; }}
td p {{ margin: 4px 0 0; }}
code {{ padding: 1px 6px; border-radius: 5px; background: var(--surface); font-size: 12px; overflow-wrap: anywhere; }}
.pill {{ display: inline-block; padding: 1px 9px; border-radius: 99px; font-size: 11.5px; font-weight: 700; white-space: nowrap; }}
.pill--w {{ background: var(--warn-bg); color: var(--warn); }} .pill--o {{ background: var(--ok-bg); color: var(--ok); }} .pill--c {{ background: var(--c-bg); color: var(--accent); }}
.tag {{ display: inline-block; padding: 1px 9px; border-radius: 6px; background: var(--surface); font-size: 12px; font-weight: 700; white-space: nowrap; }}
a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
</style>
<div class="wrap">
<p class="eyebrow">REPLACEMENT LIST · 2026.10.08</p>
<h1>画像・仮置き・文章の差し替え箇所</h1>
<p class="lead">新しいサイトの全ページ（トップ・下層・コース詳細13・法務3）を走査し、本番までに差し替える・確認するものを一覧にしました。Wix へ移すときのチェックリストとして使えます。同じ内容の CSV（replace-list.csv）もあります。</p>
<ul class="sum">
<li><b>{len(IMG)}</b><span>画像（差し替え {cnt(IMG,4,"差し替え")}・確認 {cnt(IMG,4,"確認")}・確定 {cnt(IMG,4,"確定")}）</span></li>
<li><b>{len(TMP)}</b><span>仮置き（数字・価格・コース・リンク・機能・法務・見本）</span></li>
<li><b>{len(TXT)}</b><span>文章（今のサイトから変更 {cnt(TXT,0,"変更")}・新規 {cnt(TXT,0,"新規")}・仮 {cnt(TXT,0,"仮の文章")}）</span></li>
</ul>
<div class="key"><p><b>先に直したほうがよい食い違い</b>：トップのヒーローの実績が「2026年◯月時点」「回答◯名」のままで、数字の根拠ページ（2026年10月1日時点・回答128名）と合っていません。</p></div>
<nav class="jump" aria-label="表へ移動"><a href="#img">画像</a><a href="#tmp">仮置き</a><a href="#txt">文章</a></nav>

<section id="img" aria-labelledby="h-img"><h2 id="h-img">画像</h2><p>差し替え＝仮のもの、確認＝このまま使えるか判断、確定＝このまま使う。</p>
<div class="tbl"><table><thead><tr><th>状態</th><th>ページ・箇所</th><th>素材と、いまの中身</th><th>対応</th></tr></thead><tbody>{img_rows}</tbody></table></div></section>

<section id="tmp" aria-labelledby="h-tmp"><h2 id="h-tmp">仮置き</h2><p>サイト上でオレンジの印（要確認・仮の数字など）が付いている箇所、行き先のないリンク、送信されない見本のフォームです。</p>
<div class="tbl"><table><thead><tr><th>分類</th><th>ページ・箇所</th><th>いまの表示</th><th>必要なもの</th></tr></thead><tbody>{tmp_rows}</tbody></table></div></section>

<section id="txt" aria-labelledby="h-txt"><h2 id="h-txt">文章</h2><p>今のサイト（theacademyjapan.org）から変えた主な文章、新しく書いた文章、本番前に書き換える仮の文章です。</p>
<div class="tbl"><table><thead><tr><th>分類</th><th>ページ・箇所</th><th>今のサイト（以前の案）</th><th>新しいサイト</th></tr></thead><tbody>{txt_rows}</tbody></table></div></section>
</div>'''
    open(os.path.join(DOCS, 'replace-list.html'), 'w').write(page)

write_csv(); write_html(); print('ok', len(IMG), len(TMP), len(TXT))
