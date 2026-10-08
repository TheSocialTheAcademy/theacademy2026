# 差し替え箇所の一覧（画像／仮置き／文章）を、チェックリストのページ（lp/docs/replace-list.html）と CSV（lp/docs/replace-list.csv）に書き出す
# 2026-10-08 時点の lp/*.html（同日、画像の決定と今のサイトのコース詳細の反映を追記） を全ページ走査した結果をもとに、ページ・セクション単位でまとめたもの
# 優先度　高＝公開の前に必ず（法律・信頼・購入の導線にかかわる）／中＝公開までに対応を推奨（仮のまま出すと質が下がる）／低＝公開後でもよい
# ページのチェック状態は artifact の db（collection "checks"、ドキュメント ID＝項目 ID）に保存し、見ている全員で共有する
import os, csv, html, json
S = os.path.dirname(os.path.abspath(__file__)); DOCS = os.path.join(os.path.dirname(S), 'docs')

# 画像：(ID, 優先度, ページ, 箇所, 素材, いまの中身, 状態, 対応, 完了の条件)
IMG = [
 ('I01', '高', 'トップ', 'HERO', 'assets/hero.webp', 'AIで作った写真（候補から採用）', '確認', '本番でもこの画像を使うか決める。ほかの案（H-A〜H-D、おすすめは H-B 写真＋成果物カード）を提示済み', '案を決め、写真を使う場合は生成ツールの利用規約と人物の写り（実在の人に見えないか）を確認した'),
 ('I02', '高', 'ポートフォリオ・はじめての方へ', '見出し／SHOW／例', 'assets/portfolio/*.webp（12枚）', '実際の画面を匿名化したもの（X風ニックネーム）', '確定', 'そのまま使用（10/8 に確定）', 'Wix に入れ、表示を確認した'),
 ('I03', '高', 'コース詳細（13ページ）', 'ダイジェスト動画（最初の画面の右側）', 'Vimeo（course_data.json の digest）／表紙 assets/digest/*.webp', '販売中の8コースは今のサイトと同じダイジェスト動画。SNSマーケティング実践・生成AI 業務改善・TOEIC・初級編 ChatGPT・プロジェクトマネジメントの5コースは「準備中」', '差し替え', '5コースのダイジェスト動画を用意して course_data.json に追加（成果物の画像はこの場所では使わない方針に変更）', '13コースすべてで動画が再生でき、「準備中」の表示がない。イベントデザイン・インスタグラムは Vimeo の埋め込み先の制限を確認した'),
 ('I04', '高', '学び方・受講成果', '受講成果', 'assets/outcomes/*.webp（6枚）', '見本として作った成果物の画像（各画像に「作例」と表示）', '確定', 'そのまま使用（10/8 に確定。「作例」と明記済み）', 'Wix に入れ、各画像に「作例」が表示されている'),
 ('I05', '中', 'トップ・コースを探す・受講までの流れ', '人気のコース／コース一覧／流れ／関連するコース', 'assets/thumbs/*.webp（13枚）', 'カテゴリの単色グラデーション＋半透明の形（6種類を並び順で）＋「つくるもの」（成果物の名前）のサムネイル。gen_thumbs.py でコース一覧のデータから作成。成果物の名前が決まったら作り直す（T05）', '確定', 'そのまま使用。Wix ストアの商品画像にも同じ画像を入れる。コースを足したら gen_thumbs.py で作る', 'Wix の商品画像とサイトのサムネイルが同じ画像になっている'),
 ('I06', '中', 'ポートフォリオ', 'フィード', 'assets/outcomes/sns-design.webp', 'SNS の成果物画像（見本）', '確定', '学び方・受講成果と同じ「作例」の扱い（コース詳細では使わなくなった）', 'Wix に入れ、表示を確認した'),
 ('I07', '中', 'コースを探す', '特集', 'assets/courses/feat-slack・feat-toeic.webp', 'Slack×GAS・TOEIC の特集画像', '確定', 'そのまま使用（10/8 に確定）', 'Wix に入れ、表示を確認した'),
 ('I08', '中', 'トップ・学びのヒント', '記事カード', 'assets/journal/ai・career・sns.webp', '記事のアイキャッチ（見本）', '差し替え', 'アイキャッチの型を選ぶ（E-A〜E-D、おすすめは E-B キーワード型）→ 記事ごとに作る', 'トップと学びのヒントに出る記事が、実際の記事のアイキャッチになっている'),
 ('I09', '中', '学びのヒント', 'アクセスの多い記事／評価の高い記事／最新記事', 'assets/outcomes・how・portfolio の画像', '記事のアイキャッチの代わりに、成果物・学び方・ポートフォリオの画像を仮で使用', '差し替え', '当面は E-C（同じ枠に入れて「仮の画像」と表示）、記事を公開するときに I08 の型へ', 'ほかのページの画像を流用しているカードがない'),
 ('I10', '中', '無料相談・資料請求', 'パンフレットのタブ', 'assets/pamphlet/cover.webp', 'パンフレットの表紙', '確認', '最新版のパンフレットの表紙か確認', 'ダウンロードできる PDF と同じ表紙になっている'),
 ('I11', '中', 'お役立ち資料', '新着／一覧', '（CSS で描いた表紙）', '資料名を書いた色違いの仮の表紙', '差し替え', '実際の資料の表紙に', '掲載する資料すべてに実際の表紙が入っている'),
 ('I12', '中', '数字の根拠', '満足度・コース数', '（SVG で描いたグラフ）', 'レーダーチャートとカテゴリ別の棒グラフ', '確認', '本番の数字に変えたら作り直す', 'グラフの値が、表と本文の数字と一致している'),
 ('I13', '中', '全ページ', 'SNS で共有したときの画像', '（なし）', 'OGP 画像がない', '差し替え', '1200×630 の画像を新しく作る', 'トップと主要ページで、SNS に URL を貼ると画像が表示される'),
 ('I14', '低', 'トップ', '04 ポートフォリオ', 'assets/courses/ai・marketing.webp', 'ポートフォリオ画面の中のコース画像', '確認', 'I05 を差し替えたら同じ画像にそろえる', 'コースのサムネイルと同じ画像になっている'),
 ('I15', '低', '学び方・受講成果', '4ステップ', 'assets/how/step-01〜04.webp', '学びの4ステップの画面イメージ', '確認', '実際の受講画面に近いか確認', '実際の画面と大きく違わないと確認した'),
 ('I16', '低', '記事ページ（見本）', '冒頭・著者', '（「写真」の枠）', '著者・監修者の写真の枠', '差し替え', '著者の写真を用意（なければ枠ごと外す）', '写真が入っている、または枠がない'),
 ('I17', '低', 'はじめての方へ', 'ABOUT／FOR YOU', 'assets/illust/about-community・for-you-1〜3.webp', '作成したイラスト', '確定', 'そのまま使用', 'Wix に入れ、表示を確認した'),
 ('I18', '低', '全ページ', 'NEXT STEP', 'assets/illust/next-zoom.webp', 'オンライン相談の画面とパンフレットのイラスト（17か所で共通）', '確定', 'そのまま使用', 'Wix に入れ、表示を確認した'),
 ('I19', '低', '全ページ', 'ヘッダー・フッター', 'assets/academy_logo_blue_trim.png', 'ロゴ', '確定', 'そのまま使用（SVG があれば SVG）', 'Wix に入れ、表示を確認した'),
 ('I20', '低', '数字の根拠', '自由回答', 'assets/avatars/*.svg（3種）', '用意いただいたアイコン', '確定', 'そのまま使用', 'Wix に入れ、表示を確認した'),
]

# 仮置き：(ID, 優先度, 分類, ページ, 箇所, いまの表示, 必要なもの, 完了の条件)
TMP = [
 ('T01', '高', '数字', 'トップ', 'HERO の実績', '「2026年◯月時点 要確認」「受講生アンケート・回答◯名 要確認」', '数字の根拠ページと同じ値にそろえる', 'ヒーローと数字の根拠ページの時点・回答数が一致し、「◯」「要確認」がない'),
 ('T02', '高', '数字', '数字の根拠', '平均満足度', '総合4.2・5項目の平均・期間・回答128名（回答率42％）＝すべて仮', 'アンケートの実際の集計', 'すべて実際の集計値になり、「仮の数字」の印がない'),
 ('T03', '高', '見本', '数字の根拠', '自由回答3件', '声とニックネームは見本', '本人の了承を得た実際の回答（集まらなければセクションごと外す）', '実際の回答に差し替えた、またはセクションがない（見本の声を公開しない）'),
 ('T04', '高', '価格', 'トップ・コースを探す・コース詳細', 'SNSマーケティング実践・生成AI 業務改善・TOEIC 700点', '「¥—」（価格の確定待ち）', '税込価格（ほかの10コースは今のサイトの価格を表示中）', '全コースに税込価格が入り、ストアの商品価格と一致している'),
 ('T05', '高', 'コース', 'コース詳細・サムネイル（13コース）', '成果物の名前', '成果物の名前（例）', '各コースで完成する成果物の名前（見出しとサムネイルの「つくるもの」に出る）', '13コースで成果物の名前が確定し、「（例）」「仮」の印がない'),
 ('T06', '高', 'リンク', '全ページ', 'ヘッダーの「ログイン」', '/login（行き先なし）', 'ログインの URL', '全ページでログインを押すとログイン画面が開く'),
 ('T07', '高', 'リンク', 'コース詳細（13ページ）', '「このコースを受講する」・スマホの固定バー', '#（行き先なし）', 'カート（ストアの商品）の URL', '13ページすべてで、押すと正しい商品のカートに入る'),
 ('T08', '高', 'リンク', '全ページ', '公式LINE のボタン・浮かぶボタン', 'はじめての方への LINE 欄に移動するだけ', '友だち追加の URL', 'LINE のボタンを押すと友だち追加の画面が開く'),
 ('T09', '高', 'リンク', '無料相談・資料請求', '「パンフレット（PDF）をダウンロード」', '#（行き先なし）', 'パンフレットの PDF', '送信後に最新版のパンフレットをダウンロードできる'),
 ('T10', '高', '機能', '無料相談・資料請求', '日時の表', '空き状況は表示例', '予約の仕組み（Wix ブッキングなど）と予約枠', '実際の空き枠から予約でき、確認メールと Zoom の URL が届く'),
 ('T11', '高', '機能', '無料相談・資料請求', 'パンフレット・お問い合わせのフォーム', '送信されない見本（「※このページは見本です」）', '受信先と自動メール', '送信すると連絡先に入り、自動返信と担当者への通知が届く。「見本」の表示がない'),
 ('T12', '高', '法務', '特商法・プライバシー・利用規約', '末尾', '制定日・最終更新日「2026年◯月◯日」', '公開日', '3ページに日付が入っている（専門家の確認も済み）'),
 ('T13', '中', '数字', '数字の根拠', 'コース数', '12コース（Slack×GAS は数えない）', 'Slack×GAS を含めるかの判断', '判断が決まり、ヒーローと根拠ページの数え方が一致している'),
 ('T14', '中', '数字', 'コースを探す', 'コースを比べる', '「確認中」「※」の項目', '各コースの実際の値', '比較表に「確認中」「※」がない'),
 ('T15', '中', 'コース', 'コース詳細（13ページ）', '学習の流れ', '販売中の8コースは今のサイトの章立て（カリキュラム）を表示。SNS は8週の見本、生成AI・TOEIC・初級編 ChatGPT・プロジェクトマネジメントは共通の4ステップ（「内容は仮」）', '残り5コースの実際の流れ', '13コースで流れが確定し、「内容は仮」の印がない'),
 ('T16', '中', 'コース', 'コース詳細・コースを探す（2コース）', '学習の目安', '販売中の8コースは今のサイトの章数・動画時間を表示。初級編 ChatGPT・プロジェクトマネジメントは空欄（今のサイトでは販売停止）', '2コースを続けるか、続けるなら章数と時間', '全コースに学習の目安が入っている'),
 ('T17', '中', 'リンク', '全ページ', 'フッターの SNS アイコン8つ', '#（行き先なし）', '各 SNS の URL。使っていないものは外す', '残したアイコンすべてが正しいアカウントに移動する（Wix の初期リンクがない）'),
 ('T18', '中', 'リンク', 'ポートフォリオ', '「無料で登録する」（2か所）', '同じページの「はじめかた」に移動するだけ', '登録ページの URL', '押すと登録ページが開く'),
 ('T19', '中', 'リンク', 'トップ・学びのヒント・記事', '記事11本', '/blog/〜（行き先なし）', '今の Wix ブログの記事 URL', '記事カードを押すと実際の記事が開く'),
 ('T20', '中', 'リンク', 'お役立ち資料', 'ダウンロード', 'PDF の URL なし', '各資料の PDF', '掲載するすべての資料がダウンロードできる'),
 ('T21', '中', '機能', 'お役立ち資料', '受け取りのフォーム', '送信先なし', '受け取り方式と送信先（エンジニアと相談）', '方式が決まり、送信すると連絡先に入る'),
 ('T22', '中', '見本', '学びのヒント', '記事一覧', '記事タイトル・日付・評価は見本', '実際の記事', '一覧に実際の記事だけが並ぶ'),
 ('T23', '中', '見本', '記事ページ', '本文・著者', '本文は見本、著者名・監修者名・紹介文は仮', '実際の記事と著者', '記事テンプレートに実際の著者情報が入る'),
 ('T24', '中', '見本', 'お役立ち資料', '資料6件', '資料名・説明・ページ数は見本', '実際の資料', '一覧に実際の資料だけが並ぶ'),
 ('T25', '低', '数字', '学びのヒント', '記事カード', 'いいね・役に立ったの数（142／128／118 など）、日付', '実際の数字（出さない選択も可）', '実際の数字になった、または数字を出さない'),
 ('T26', '低', '確認', '無料相談・資料請求', '「顔を出さないといけませんか？」', '「カメラはオフでも参加できます」に要確認の印', 'カメラオフで参加できるか', '回答が確定し、要確認の印がない'),
]

# 文章：(ID, 優先度, 分類, ページ, 箇所, 今のサイト（以前の案）, 新しいサイト, 完了の条件)
TXT = [
 ('W01', '高', '新規', '法務3ページ', '全文', '今の文面（あれば）', '確定版の文面に差し替え（特商法・プライバシーポリシー・利用規約）', '確定版を Wix に入れ、Wix 利用に伴う追記と専門家の確認が済んでいる'),
 ('W02', '高', '仮の文章', 'コース詳細（5ページ）', '見出し・説明・こんな方に・できること', '—', '販売中の8コースは今のサイトの説明・こんな方に・できるようになることを反映済み。残り5コース（SNS・生成AI・TOEIC・初級編 ChatGPT・プロジェクトマネジメント）は仮の文章', '13コースの文章を担当者が確認し、実際のコース内容と合っている'),
 ('W03', '高', '要確認', 'コース', '「TOEIC L&R 700点突破」', '—', '結果の約束に読めるため、「700点を目指す」などの言い方か注記を検討', '表現を決め、根拠のない約束に読める箇所がない'),
 ('W04', '高', '変更', 'トップ', '選ばれる理由', '3つ（「5-15万円」の表記あり）', 'WHY・流れ・LINE などに分けて説明。「5-15万円」は今の価格と合わないため要確認', '「5-15万円」を外した、または正しい根拠を添えた'),
 ('W05', '高', '変更', 'コース', '新しいコース名', '今の商品名', 'SNSマーケティング実践・生成AI 業務改善・TOEIC L&R 700点突破 は新しい名前', '今の商品との対応が決まり、商品名とサイトの表記が一致している'),
 ('W06', '高', '仮の文章', '数字の根拠', '自由回答・調査の概要', '—', '実際のアンケートに合わせて書き換え', '調査の概要が実際の調査と一致している（T02・T03 と同時に）'),
 ('W07', '中', '変更', 'トップ', 'ヒーローのキャッチ', '自分らしく成長できる学びのサードプレイス', '学んで、つくって、次のキャリアへ。（「サードプレイス」はコミュニティーの説明へ）', 'Wix に新しい文言を入れ、旧文言が残っていない'),
 ('W08', '中', '変更', 'トップ', 'ヒーローのリード文', '講師と仲間に支えられながら', '仲間の歩みを励みにしながら（講師フィードバックを約束しない方針）', 'サイト内に「講師のフィードバック」を約束する文言がない'),
 ('W09', '中', '変更', 'トップ', '実績の表記', '週2〜／満足度4.8・20+（以前の案）', '実践コース 10+・平均満足度 4.2・週2h〜（根拠ページへリンク）', '表記が新しい形にそろい、根拠ページにつながる'),
 ('W10', '中', '変更', 'はじめての方へ', 'お悩み3つ', '入社3〜5年目／副業・独立志望／グローバルキャリア', '「たとえば、こんな想いに。」心の声3つ（属性の呼びかけをやめる）', 'Wix に新しい文言を入れ、旧文言が残っていない'),
 ('W11', '中', '変更', '全ページ', '公式LINE の特典3', '限定コミュニティに参加できる', '限定イベントの情報が届く', 'サイトと LINE の実際の配信内容が一致している'),
 ('W12', '中', '変更', 'トップ・はじめての方へ', '受講までの流れ', '①無料相談から始まる4ステップ', 'コースを選ぶ → 決済 → 受講 → 残す・飛び込む（相談は希望者のみの一文）', 'Wix に新しい文言を入れ、旧文言が残っていない'),
 ('W13', '中', '変更', 'トップ・無料相談', 'キャリアの3分岐', '無料体験講座／無料相談会／パンフレット', '無料相談（主）とパンフレットの2択。無料体験は廃止', '無料体験の案内・ページが残っていない（旧 URL は転送）'),
 ('W14', '中', '変更', '全ページ', 'カテゴリ名', '語学・TOEIC など', 'IT・デジタル／マーケティング／英語・TOEIC／ビジネス／クリエイティブ（記事のみ「キャリア・学び方」を追加）', 'ストアの商品カテゴリとサイトの表記が一致している'),
 ('W15', '中', '変更', 'コース詳細', '見出し', 'コース名＋説明', '完成する成果物を主語にした1行。講師欄なし', '13ページの見出しが成果物の名前（T05）と一致している'),
 ('W16', '中', '新規', '学び方・ポートフォリオ・はじめての方へ・数字の根拠・お役立ち資料', '全文', '—', '新しく書いた文章（Wix に入力）', '各ページの文章を担当者が読み、事実と合っている'),
 ('W17', '中', '仮の文章', 'コースを探す', 'コース診断', '—', '質問文・結果の理由の文言を確認', '3問の文言と結果の理由を確認した'),
 ('W18', '中', '仮の文章', '学びのヒント・記事ページ', '記事タイトル・抜粋・本文・著者紹介', '—', '実際の記事に差し替え', '見本の記事が残っていない'),
 ('W19', '中', '仮の文章', 'お役立ち資料', '資料名・説明', '—', '実際の資料に差し替え', '見本の資料が残っていない'),
 ('W20', '低', '変更', '全ページ', '表記の統一', '—', '「コミュニティー」「3か月」「週2〜3時間」の形', '表記ゆれがない'),
 ('W21', '低', '変更', 'よくある質問', '回答', '今の FAQ（6カテゴリ）', '13問。規約と同じ内容で確定済み。講師フィードバックの質問は削除', 'Wix に13問を入れ、規約の内容と食い違いがない'),
 ('W22', '低', '変更', 'コースを探す', '比較表', '講師のフィードバックの行あり（以前の案）', '講師のフィードバックの行を削除', '比較表に講師フィードバックの行がない'),
 ('W23', '低', '仮の文章', 'ポートフォリオ・トップ05', '画面の中の投稿・トーク', '—', '見本の文章（ニックネームは匿名）', 'このまま使ってよいと確認した'),
]

ALL = [('画像', r[0], r[1], r[6], r[2], r[3] + '｜' + r[4], r[5], r[7], r[8]) for r in IMG] + \
      [('仮置き', r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) for r in TMP] + \
      [('文章', r[0], r[1], r[2], r[3], r[4], r[5] + ' → ' + r[6], '', r[7]) for r in TXT]

def write_csv():
    with open(os.path.join(DOCS, 'replace-list.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['ID', '優先度', '種類', '分類・状態', 'ページ', '箇所', 'いまの中身', '対応・必要なもの', '完了の条件', 'チェック', '担当', '期限', 'メモ'])
        for kind, i, pr, cat, page, place, now, todo, done in sorted(ALL, key=lambda r: ('高中低'.index(r[2]), r[1])):
            w.writerow([i, pr, kind, cat, page, place, now, todo, done, '', '', '', ''])

def e(x): return html.escape(x)
PILL = {'差し替え': 'w', '確認': 'c', '確定': 'o', '変更': 'c', '新規': 'o', '要確認': 'w', '仮の文章': 'w'}
def pill(t): return f'<span class="pill pill--{PILL.get(t, "c")}">{e(t)}</span>'
def prio(p): return f'<span class="pr pr--{ {"高": "h", "中": "m", "低": "l"}[p] }">{p}</span>'
def ck(i): return f'<label class="ck" for="c-{i}"><input type="checkbox" id="c-{i}" data-id="{i}" disabled><span class="sr">{i} を完了にする</span></label>'

def write_html():
    rows_i = ''.join(f'<tr data-p="{p}" data-id="{i}"><td>{ck(i)}</td><td class="id">{i}</td><td>{prio(p)}</td><td>{pill(st)}</td><th scope="row">{e(pg)}<small>{e(s)}</small></th><td><code>{e(src)}</code><p>{e(now)}</p></td><td>{e(todo)}</td><td class="done">{e(dn)}</td></tr>' for i, p, pg, s, src, now, st, todo, dn in IMG)
    rows_t = ''.join(f'<tr data-p="{p}" data-id="{i}"><td>{ck(i)}</td><td class="id">{i}</td><td>{prio(p)}</td><td><span class="tag">{e(c)}</span></td><th scope="row">{e(pg)}<small>{e(s)}</small></th><td>{e(now)}</td><td>{e(need)}</td><td class="done">{e(dn)}</td></tr>' for i, p, c, pg, s, now, need, dn in TMP)
    rows_w = ''.join(f'<tr data-p="{p}" data-id="{i}"><td>{ck(i)}</td><td class="id">{i}</td><td>{prio(p)}</td><td>{pill(c)}</td><th scope="row">{e(pg)}<small>{e(s)}</small></th><td>{e(old)}</td><td>{e(new)}</td><td class="done">{e(dn)}</td></tr>' for i, p, c, pg, s, old, new, dn in TXT)
    n = {k: sum(1 for r in ALL if r[2] == k) for k in '高中低'}
    head = '<thead><tr><th><span class="sr">完了</span></th><th>ID</th><th>優先</th><th>{c}</th><th>ページ・箇所</th><th>{a}</th><th>{b}</th><th>完了の条件</th></tr></thead>'
    page = f'''<title>The Academy 差し替え箇所リスト</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Josefin+Sans:wght@600&display=swap">
<style>
/* レイアウト：上に優先度ごとの進み具合、下に3つの表（画像／仮置き／文章）。各行の左端でチェック。表は横にはみ出すときだけ枠の中でスクロール */
:root {{ --bg:#FFFFFF; --surface:#F5F6FA; --ink:#0F1B45; --mid:#5E6182; --line:#DFE2EC; --accent:#0141D4; --warn-bg:#FFF1E7; --warn:#C2560F; --ok-bg:#E9F9EF; --ok:#13804A; --c-bg:#EAF0FF; --hi:#C8321E; --hi-bg:#FDECEA;
  --f-body:"Noto Sans JP","Hiragino Sans","Yu Gothic",system-ui,sans-serif; --f-en:"Josefin Sans","Noto Sans JP",sans-serif; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#0E1430; --surface:#161E40; --ink:#E8EBF7; --mid:#A3A8C8; --line:#2A3462; --accent:#7EA2FF; --warn-bg:#3A2614; --warn:#FFB27A; --ok-bg:#12301F; --ok:#7BE0A6; --c-bg:#1D2A5C; --hi:#FF8F80; --hi-bg:#3A1A18; color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --bg:#0E1430; --surface:#161E40; --ink:#E8EBF7; --mid:#A3A8C8; --line:#2A3462; --accent:#7EA2FF; --warn-bg:#3A2614; --warn:#FFB27A; --ok-bg:#12301F; --ok:#7BE0A6; --c-bg:#1D2A5C; --hi:#FF8F80; --hi-bg:#3A1A18; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--f-body); font-size: 15px; line-height: 1.8; padding-inline: 16px; }}
.wrap {{ max-width: 1240px; margin: 0 auto; padding-block: 40px 96px; }}
.eyebrow {{ margin: 0; color: var(--accent); font-family: var(--f-en); font-size: 12px; letter-spacing: .14em; }}
h1 {{ margin: 6px 0 8px; font-size: clamp(26px, 4vw, 34px); line-height: 1.4; text-wrap: balance; }}
.lead {{ margin: 0; color: var(--mid); max-width: 72ch; }}
.rule {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin: 24px 0 0; padding: 0; list-style: none; }}
.rule li {{ padding: 16px 18px; border-radius: 14px; background: var(--surface); font-size: 13.5px; }}
.rule b {{ display: flex; align-items: center; gap: 8px; margin-bottom: 4px; font-size: 15px; }}
.bar {{ height: 6px; margin-top: 10px; border-radius: 99px; background: var(--line); overflow: hidden; }} .bar i {{ display: block; height: 100%; width: 0; background: var(--ok); transition: width .3s; }}
.cnt {{ margin-top: 4px; color: var(--mid); font-size: 12.5px; font-variant-numeric: tabular-nums; }}
.key {{ margin-top: 16px; padding: 14px 18px; border-left: 3px solid var(--hi); border-radius: 0 12px 12px 0; background: var(--hi-bg); font-size: 14px; }} .key p {{ margin: 0; }}
.bar-tools {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-top: 24px; }}
.bar-tools button {{ padding: 7px 14px; border: 0; border-radius: 99px; background: var(--surface); color: var(--ink); font: inherit; font-size: 13.5px; font-weight: 700; cursor: pointer; }}
.bar-tools button[aria-pressed="true"] {{ background: var(--ink); color: var(--bg); }}
.bar-tools a {{ margin-left: 4px; color: var(--accent); font-size: 13.5px; font-weight: 700; }}
.status {{ margin: 10px 0 0; color: var(--mid); font-size: 12.5px; }}
section {{ margin-top: 48px; scroll-margin-top: 16px; }}
h2 {{ margin: 0 0 6px; font-size: 22px; }} h2 + p {{ margin: 0 0 12px; color: var(--mid); font-size: 14px; }}
.tbl {{ overflow-x: auto; }}
table {{ width: 100%; min-width: 1060px; border-collapse: collapse; font-size: 13px; line-height: 1.7; }}
th, td {{ padding: 12px 12px 12px 0; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
thead th {{ color: var(--mid); font-size: 12px; font-weight: 500; white-space: nowrap; }}
tbody th {{ width: 17%; font-weight: 700; }} tbody th small {{ display: block; color: var(--mid); font-weight: 500; font-size: 12px; }}
td p {{ margin: 4px 0 0; }} td.id {{ color: var(--mid); font-variant-numeric: tabular-nums; white-space: nowrap; }}
td.done {{ width: 20%; color: var(--mid); }}
tr.is-done th, tr.is-done td:not(:first-child) {{ opacity: .45; }} tr.is-done th {{ text-decoration: line-through; }}
tr[hidden] {{ display: none; }}
code {{ padding: 1px 6px; border-radius: 5px; background: var(--surface); font-size: 12px; overflow-wrap: anywhere; }}
.pill {{ display: inline-block; padding: 1px 9px; border-radius: 99px; font-size: 11.5px; font-weight: 700; white-space: nowrap; }}
.pill--w {{ background: var(--warn-bg); color: var(--warn); }} .pill--o {{ background: var(--ok-bg); color: var(--ok); }} .pill--c {{ background: var(--c-bg); color: var(--accent); }}
.pr {{ display: inline-grid; place-items: center; width: 26px; height: 26px; border-radius: 8px; font-size: 13px; font-weight: 700; }}
.pr--h {{ background: var(--hi-bg); color: var(--hi); }} .pr--m {{ background: var(--warn-bg); color: var(--warn); }} .pr--l {{ background: var(--surface); color: var(--mid); }}
.tag {{ display: inline-block; padding: 1px 9px; border-radius: 6px; background: var(--surface); font-size: 12px; font-weight: 700; white-space: nowrap; }}
.ck {{ display: inline-flex; padding: 2px; cursor: pointer; }} .ck input {{ width: 20px; height: 20px; margin: 0; accent-color: var(--ok); cursor: pointer; }} .ck input:disabled {{ cursor: default; }}
.sr {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
a:focus-visible, button:focus-visible, input:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
@media (prefers-reduced-motion: reduce) {{ .bar i {{ transition: none; }} }}
</style>
<div class="wrap">
<p class="eyebrow">REPLACEMENT CHECKLIST · 2026.10.08</p>
<h1>画像・仮置き・文章の差し替え箇所</h1>
<p class="lead">新しいサイトの全ページ（トップ・下層・コース詳細13・法務3）を走査し、本番までに差し替える・確認するものを {len(ALL)} 項目にまとめました。各行の左のチェックは、このページを開いている全員で共有されます。同じ内容の CSV（replace-list.csv、担当・期限の列つき）もあります。</p>
<ul class="rule">
<li><b>{prio('高')} 公開の前に必ず</b>法律・信頼・購入の導線にかかわるもの。仮のまま公開すると、誤解やトラブル、売上の取りこぼしにつながる<div class="bar"><i id="b-高"></i></div><p class="cnt" id="n-高">0 / {n['高']} 完了</p></li>
<li><b>{prio('中')} 公開までに対応を推奨</b>仮のままでも動くが、質や信頼が下がるもの<div class="bar"><i id="b-中"></i></div><p class="cnt" id="n-中">0 / {n['中']} 完了</p></li>
<li><b>{prio('低')} 公開後でもよい</b>確認だけのもの、細かな表記<div class="bar"><i id="b-低"></i></div><p class="cnt" id="n-低">0 / {n['低']} 完了</p></li>
</ul>
<div class="key"><p><b>最初の一手</b>：T01（ヒーローの数字が根拠ページと食い違っている）は、情報を待たずにすぐ直せます。</p></div>
<div class="bar-tools" role="group" aria-label="表示の絞り込み"><button type="button" data-f="all" aria-pressed="true">すべて</button><button type="button" data-f="高" aria-pressed="false">高だけ</button><button type="button" data-f="open" aria-pressed="false">未完了だけ</button><a href="#img">画像</a><a href="#tmp">仮置き</a><a href="#txt">文章</a></div>
<p class="status" id="st">チェックの保存先に接続しています…</p>

<section id="img" aria-labelledby="h-img"><h2 id="h-img">画像（{len(IMG)}）</h2><p>差し替え＝仮のもの、確認＝このまま使えるか判断、確定＝このまま使う。</p>
<div class="tbl"><table>{head.format(c='状態', a='素材と、いまの中身', b='対応')}<tbody>{rows_i}</tbody></table></div></section>

<section id="tmp" aria-labelledby="h-tmp"><h2 id="h-tmp">仮置き（{len(TMP)}）</h2><p>サイト上でオレンジの印（要確認・仮の数字など）が付いている箇所、行き先のないリンク、送信されない見本のフォームです。</p>
<div class="tbl"><table>{head.format(c='分類', a='いまの表示', b='必要なもの')}<tbody>{rows_t}</tbody></table></div></section>

<section id="txt" aria-labelledby="h-txt"><h2 id="h-txt">文章（{len(TXT)}）</h2><p>今のサイト（theacademyjapan.org）から変えた主な文章、新しく書いた文章、本番前に書き換える仮の文章です。</p>
<div class="tbl"><table>{head.format(c='分類', a='今のサイト（以前の案）', b='新しいサイト')}<tbody>{rows_w}</tbody></table></div></section>
</div>
<script>
(() => {{
  const boxes = [...document.querySelectorAll('input[data-id]')];
  const rows = [...document.querySelectorAll('tr[data-id]')];
  const st = document.getElementById('st');
  let filter = 'all';
  const state = {{}};
  const paint = () => {{
    rows.forEach(r => {{ const id = r.dataset.id, done = !!state[id]; r.classList.toggle('is-done', done); r.querySelector('input').checked = done;
      r.hidden = (filter === '高' && r.dataset.p !== '高') || (filter === 'open' && done); }});
    for (const p of ['高', '中', '低']) {{ const all = rows.filter(r => r.dataset.p === p), d = all.filter(r => state[r.dataset.id]).length;
      document.getElementById('n-' + p).textContent = d + ' / ' + all.length + ' 完了'; document.getElementById('b-' + p).style.width = (all.length ? d / all.length * 100 : 0) + '%'; }}
  }};
  document.querySelectorAll('[data-f]').forEach(b => b.addEventListener('click', () => {{ filter = b.dataset.f; document.querySelectorAll('[data-f]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); paint(); }}));
  paint();
  (async () => {{
    const db = window.claude ? await window.claude.use('db') : null;
    if (!db) {{ st.textContent = 'チェックを保存するには、claude.ai にサインインしてこのページを開いてください（いまは表示だけです）。'; return; }}
    const col = db.collection('checks');
    col.onSnapshot(snap => {{ for (const k in state) delete state[k]; snap.docs.forEach(d => {{ const v = d.data(); if (v && v.done) state[d.id] = true; }}); paint(); }},
      () => {{ st.textContent = 'チェックの保存先に接続できませんでした。ページを開き直してください。'; }});
    const user = await window.claude.use('user');
    const canWrite = user ? (await user.can('data.write')) !== false : true;
    if (!canWrite) {{ st.textContent = '閲覧のみの権限のため、チェックは変更できません。'; return; }}
    boxes.forEach(b => {{ b.disabled = false; b.addEventListener('change', async () => {{
      const id = b.dataset.id, done = b.checked; state[id] = done || undefined; paint();
      try {{ await col.doc(id).set({{ done, at: new Date().toISOString() }}); st.textContent = '保存しました（' + id + '）'; }}
      catch (e) {{ state[id] = !done || undefined; paint(); st.textContent = '保存できませんでした（' + id + '）。権限を確認してください。'; }}
    }}); }});
    st.textContent = 'チェックは自動で保存され、このページを開いている全員に反映されます。';
  }})();
}})();
</script>'''
    open(os.path.join(DOCS, 'replace-list.html'), 'w').write(page)

write_csv(); write_html(); print('ok', len(IMG), len(TMP), len(TXT), {k: sum(1 for r in ALL if r[2] == k) for k in '高中低'})
