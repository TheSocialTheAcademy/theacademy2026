from common import *
import os; A = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets') + '/'
TXT = '<p class="k">THE ACADEMY · ONLINE LEARNING</p><p class="h">学んで、つくって、<br>次のキャリアへ。</p><p class="l">平日夜・週末の短い時間で、実務に直結するアウトプットを。</p><p class="b"><span class="p">無料で相談する</span><span>コースを探す</span></p>'
def pc(kind):
    if kind == 'A':
        return f'<div class="pc ha"><img class="bg" src="{A}hero.webp"><div class="fade"></div><div class="tx">{TXT}</div></div>'
    if kind == 'B':
        return (f'<div class="pc hb"><div class="tx">{TXT}</div><div class="ph"><img src="{A}hero.webp"></div>'
                f'<figure class="fl f1"><img src="{A}outcomes/sns-design.webp"><figcaption>作例｜SNS投稿デザイン</figcaption></figure>'
                f'<figure class="fl f2"><img src="{A}portfolio/hero-profile.webp"><figcaption>ポートフォリオに公開</figcaption></figure></div>')
    if kind == 'C':
        ims = ['outcomes/marketing-strategy.webp', 'outcomes/sns-design.webp', 'portfolio/show-featured-work.webp', 'outcomes/event-plan.webp', 'outcomes/english-presentation.webp', 'outcomes/ai-prompt.webp']
        return f'<div class="pc hc"><div class="tx">{TXT}</div><div class="col">' + ''.join(f'<div class="t t{i}"><img src="{A + s}"></div>' for i, s in enumerate(ims)) + '</div></div>'
    if kind == 'D':
        return (f'<div class="pc hd"><div class="tx">{TXT}</div><div class="win"><p class="bar"><span></span><span></span><span></span><em>theacademyjapan.org/portfolio/your-name</em></p><img src="{A}portfolio/sample-page.webp"></div>'
                f'<div class="steps"><span>学ぶ</span>→<span>つくる</span>→<span class="on">公開する</span></div></div>')
def sp(kind):
    vis = {'A': f'<img class="sv" src="{A}hero.webp" style="object-position:64% 25%">',
           'B': f'<div class="sv sb"><img src="{A}hero.webp"><figure><img src="{A}outcomes/sns-design.webp"></figure></div>',
           'C': f'<div class="sv sc">' + ''.join(f'<img src="{A + s}">' for s in ['outcomes/marketing-strategy.webp', 'outcomes/sns-design.webp', 'outcomes/event-plan.webp', 'outcomes/ai-prompt.webp']) + '</div>',
           'D': f'<div class="sv sd"><p class="bar"><span></span><span></span><span></span></p><img src="{A}portfolio/sample-page.webp"></div>'}[kind]
    return f'<div class="sp">{vis}<div class="stx">{TXT}</div></div>'
row = lambda k: f'<div class="hrow"><div><p class="lbl">PC 1440px（縮小）</p>{pc(k)}</div><div><p class="lbl">スマホ 390px（縮小）</p>{sp(k)}</div></div>'
css = '''.hrow{display:grid;grid-template-columns:900px 290px;gap:40px;align-items:start}
.pc{position:relative;width:900px;height:470px;border-radius:12px;overflow:hidden;background:#fff;border:1px solid #E1E5EE}
.tx{position:absolute;left:48px;top:70px;width:410px;z-index:2}.k{font-size:9px;font-weight:700;letter-spacing:.16em;color:#0141D4}.h{font-size:36px;font-weight:900;line-height:1.3;margin:12px 0}.l{font-size:11.5px;font-weight:700;line-height:1.7}
.b{display:flex;gap:8px;margin-top:18px}.b span{font-size:11px;font-weight:700;padding:10px 18px;border-radius:6px;background:#fff;border:1px solid #E1E5EE}.b .p{background:#0141D4;color:#fff;border-color:#0141D4}
.ha .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 30%}.ha .fade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(255,255,255,.92) 0,rgba(255,255,255,.7) 40%,rgba(255,255,255,0) 62%)}
.hb .ph{position:absolute;right:0;top:0;width:52%;height:100%}.hb .ph img{width:100%;height:100%;object-fit:cover;object-position:60% 30%}
.fl{position:absolute;background:#fff;border-radius:10px;padding:6px;box-shadow:0 12px 30px rgba(15,27,69,.18);z-index:3}.fl img{display:block;width:100%;border-radius:6px}.fl figcaption{font-size:9.5px;font-weight:700;padding:5px 3px 1px;color:#0F1B45}
.f1{left:390px;bottom:40px;width:200px}.f2{right:28px;top:40px;width:150px}
.hc{background:#F7F8FB}.hc .col{position:absolute;right:-30px;top:-40px;width:470px;display:grid;grid-template-columns:1fr 1fr;gap:12px;transform:rotate(-6deg)}
.hc .t{background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 8px 22px rgba(15,27,69,.10);aspect-ratio:1.9/1}.hc .t img{width:100%;height:100%;object-fit:cover}.hc .t1,.hc .t3,.hc .t5{transform:translateY(40px)}
.hd{background:linear-gradient(180deg,#fff 0,#EEF3FF 100%)}.hd .win{position:absolute;right:36px;top:46px;width:430px;height:390px;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 14px 36px rgba(15,27,69,.14);border:1px solid #E1E5EE}
.bar{height:22px;background:#F1F3F8;display:flex;gap:5px;align-items:center;padding:0 9px}.bar span{width:6px;height:6px;border-radius:50%;background:#C8CEDB}.bar em{font-style:normal;font-size:8.5px;color:#676688;margin-left:10px;background:#fff;border-radius:4px;padding:1px 8px}
.hd .win img{width:100%;height:calc(100% - 22px);object-fit:cover;object-position:left top;display:block}.steps{position:absolute;left:48px;bottom:40px;display:flex;gap:6px;align-items:center;font-size:11px;font-weight:700;color:#676688;z-index:2}.steps span{background:#fff;border:1px solid #E1E5EE;padding:5px 11px;border-radius:999px}.steps .on{background:#0141D4;color:#fff;border-color:#0141D4}
.sp{width:290px;border-radius:14px;overflow:hidden;background:#fff;border:1px solid #E1E5EE}.sv{display:block;width:100%;height:200px;object-fit:cover}.stx{padding:16px 16px 20px}.stx .h{font-size:24px;margin:8px 0}.stx .b{flex-wrap:wrap}.stx .b span{padding:8px 12px}
.sb{position:relative}.sb>img{width:100%;height:100%;object-fit:cover;object-position:64% 25%}.sb figure{position:absolute;left:12px;bottom:-14px;width:120px;background:#fff;padding:4px;border-radius:8px;box-shadow:0 8px 20px rgba(15,27,69,.18)}.sb figure img{width:100%;display:block;border-radius:5px}
.sc{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:10px;background:#F7F8FB}.sc img{width:100%;aspect-ratio:1.9/1;object-fit:cover;border-radius:6px}
.sd{background:#EEF3FF;padding:14px 14px 0;overflow:hidden}.sd .bar{border-radius:8px 8px 0 0}.sd img{width:100%;display:block}
.cmp{width:100%;border-collapse:collapse;font-size:14px}.cmp th,.cmp td{border-bottom:1px solid #E6E9F0;padding:10px 12px;text-align:left}.cmp th{background:#F7F8FB;font-weight:700}'''
pats = [
 pat('H-A', 'いまの案（写真を全面に）', '学んでいる人の写真を全面に敷き、左に文字。温かさと「自分ごと」感が伝わります。', [('◎', '人の雰囲気・安心感'), ('△', '「つくる」「成果物」は写真だけでは伝わらない')], row('A')),
 pat('H-B', '写真＋浮かぶ成果物カード', 'いまの写真を右半分に収め、その手前に「作例」の成果物と、公開したポートフォリオを小さなカードで重ねます。キャッチコピーの「学んで、つくって」を絵で補います。写真は今のものを使えます。',
     [('◎', '人と成果物の両方が伝わる'), ('○', '今ある素材で作れる'), ('△', 'カードが多いとにぎやかになる（2枚まで）')], row('B'), True),
 pat('H-C', '成果物を並べる（人物なし）', '受講生がつくる成果物を斜めのタイルで並べます。「何ができるようになるか」が一番伝わりますが、人の温かさはなくなります。',
     [('◎', 'つくれるものの幅が伝わる'), ('△', '冷たい印象になりやすい'), ('△', '成果物の画像が増えるほど映える（今は6枚）')], row('C')),
 pat('H-D', 'ポートフォリオの画面を主役に', 'The Academy の一番の違い（学んだ成果を公開して次の機会につなげる）を、ポートフォリオの画面で見せます。下に「学ぶ→つくる→公開する」。',
     [('◎', 'ほかのスクールとの違いがはっきり'), ('△', '画面が小さいと中身が読めない'), ('△', 'ポートフォリオのページと見た目が重なる')], row('D')),
]
cmp = '<section class="pat"><h2>比べると</h2><table class="cmp"><tr><th></th><th>H-A 写真</th><th>H-B 写真＋成果物</th><th>H-C 成果物を並べる</th><th>H-D ポートフォリオ画面</th></tr>' + ''.join('<tr>' + ''.join(f'<{"th" if j == 0 else "td"}>{v}</{"th" if j == 0 else "td"}>' for j, v in enumerate(r)) + '</tr>' for r in [
 ('安心感・人の雰囲気', '◎', '◎', '△', '○'), ('「つくる」が伝わる', '△', '○', '◎', '◎'), ('ほかのスクールとの違い', '△', '○', '○', '◎'), ('今ある素材で作れる', '◎', '◎', '○', '◎'), ('ほかのページとの重なり', 'なし', 'なし', '学び方ページの作例と重なる', 'ポートフォリオのページと重なる')]) + '</table><p class="d" style="margin-top:14px">おすすめは <b>H-B</b>。いまの写真（安心感）を残したまま、コピーの「つくって」を成果物カードで補えます。メインの見た目がほかのページと重なりにくい点も H-C・H-D より有利です。</p></section>'
open('hero.html', 'w').write(board('トップのメイン画像　ほかのイメージ案', 'いまの案（H-A）に加えて、3つの方向を作りました。文字とボタンの位置・色はそのままで、右側の絵だけを変えています。', pats + [cmp], css))
