"""本編フレームワーク（思考フロー × スライド構成）。

『本編フレームワーク集』(docs/catalog/course-slide-templates.html C+節) の思考フローを、
1ブロックで **1チャプター分（10〜15枚規模）** へ一括展開する層。content.txt では
【本編:概念習得】 のように書き、フィールドを渡すだけで章扉＋本編が組める（coursegen が dispatch）。

■ 長尺化のしくみ（fan-out）
実コースは Chapter 10 × 15枚規模。固定枚数では足りないので、リスト系フィールドは
「項目の数だけ1枚ずつ」に展開する。マーケ講座の観察パターン（小扉→定義→各要素を1枚ずつ
→重要ポイント→事例に当てはめる）に対応：
  details = "指示=動詞で始める・対象を名詞で｜文脈=材料を構造化・NGを明示｜…"
    → 各要素が1枚ずつの詳細スライドになる（｜で要素、= の右を ・ で箇条書き）
  examples = "事例A=要点1・要点2｜事例B=…"  → 各事例が1枚ずつ
フィールドが無いページ／空のリストは自動スキップ。要素・事例を増やすほど厚くなる。
"""
import pages
import layouts
from slides import card, callout, textbox, add_icon, TEXT, TEXT_MUTED, PRIMARY


# ---------------------------------------------------------------- 共通ヘルパー
def _table(v):
    """"h1,h2,h3｜r1a,r1b,r1c｜…" → [[h1,h2,h3],[r1a,…],…]（｜で行・,でセル）。"""
    return [[c.strip() for c in str(row).split(",")] for row in pages._list(v)]


def _table_slide(prs, title, headers, rows, *, lead="", section="TABLE ／ 表"):
    """図解ライブラリの表（diagram_table）を1枚として置く。

    行数に応じて高さを詰め、間延びを防ぐ（文字と図表のバランス）。中央帯に配置。
    """
    from diagrams import diagram_table
    s = pages._body(prs, section, title)
    y = 4.2
    if lead:
        pages._lead(s, lead)
        y = 4.5
    # 行が少ないほど低く：ヘッダ1.0＋各行1.05、上限は本文ゾーン内
    h = min(8.2, 1.1 + (len(rows) + 1) * 1.05)
    diagram_table(s, pages.X0, y, pages.ZONE_W, h, headers=headers, rows=rows)
    return s


def _items(v):
    """"名=b1・b2｜名=b3" → [(名,[b1,b2]),(名,[b3])]。空/リストも許容。= 右は ・／ で箇条書き。"""
    out = []
    for it in pages._list(v):
        if isinstance(it, (list, tuple)):
            out.append((str(it[0]), [str(x) for x in it[1:]]))
            continue
        name, sep, rest = it.partition("=")
        bl = []
        if rest:
            for b in rest.replace("／", "・").replace("/", "・").split("・"):
                if b.strip():
                    bl.append(b.strip())
        out.append((name.strip(), bl))
    return out


def _detail_slide(prs, title, bullets, *, lead="", section="POINT ／ 詳細", icon=None):
    """タイトル＋（あれば）リード＋要点。要点3つ以下はカード横並び、多いときは箇条書き。

    icon は lead（サブタイトル）がある時だけ、その文章の左にインライン配置する
    （アイコンは強調したい文章の横に置く方針。浮いた配置はしない）。
    """
    s = pages._body(prs, section, title)
    lead_x = pages.X0
    if lead and icon:
        try:
            add_icon(s, icon, pages.X0, 3.02, size=0.66, color="#0141D4")
            lead_x = pages.X0 + 0.95
        except Exception:
            pass
    if lead:
        textbox(s, lead_x, 3.05, pages.ZONE_W - (lead_x - pages.X0), 0.62, [lead],
                size=11.5, color=TEXT)
    bl = [b for b in bullets if b]
    y0 = 4.6 if lead else 4.0
    if not bl:
        callout(s, pages.X0, y0, pages.ZONE_W, 1.4, title, accent=PRIMARY)
    elif len(bl) <= 3:
        n = len(bl); gap = 0.5; cw = (pages.ZONE_W - gap * (n - 1)) / n
        for i, b in enumerate(bl):
            card(s, pages.X0 + i * (cw + gap), y0, cw, 4.4, chip=str(i + 1), body=b)
    else:
        textbox(s, pages.X0, y0, pages.ZONE_W, 6.6, [f"・{b}" for b in bl],
                size=14, color=TEXT, line_spacing=1.85)
    return s


def _subdoor(prs, label, title):
    """小扉（節の切り替え）。本文レイアウトに大きな見出しだけ置く軽い区切り。"""
    from pptx.enum.text import PP_ALIGN
    from diagrams import _tint
    s = pages._body(prs, label, title)
    shape = pages.shape_box if hasattr(pages, "shape_box") else None
    from slides import shape_box, WHITE
    from pptx.enum.shapes import MSO_SHAPE
    shape_box(s, MSO_SHAPE.RECTANGLE, pages.X0, 4.6, pages.ZONE_W, 4.6,
              fill=_tint(PRIMARY, 0.93), line=None)
    textbox(s, pages.X0 + 1.0, 6.2, pages.ZONE_W - 2.0, 1.8, [title], size=26,
            bold=True, color=PRIMARY, align=PP_ALIGN.CENTER, line_spacing=1.15)
    return s


# ============================================================ TF2 概念習得型
def teach_concept(prs, *, topic="この概念",
                  # 章扉（任意）。illust に soco-st 検索語を渡すと主役イラスト
                  num=None, course_name="", icon="ph:lightbulb", goals=None, illust=None,
                  # 1 What: 概念解説（定義＋部品フロー）
                  concept_title=None, concept_lead="", parts=None, concept_conclusion="",
                  # 2 構成要素を1枚ずつ（fan-out）: details="指示=動詞で始める・…｜文脈=…"
                  #   details_icons="ph:cursor-click｜ph:book-open｜…" で各詳細に ph: アイコン
                  details=None, details_icons=None, details_door="構成要素をひとつずつ",
                  details_section="ELEMENT ／ 構成要素",
                  # 3 Why: 動機づけ（why_icons で各カード見出しにアクセントアイコン）
                  why=None, why_title=None, why_lead="", why_conclusion="", why_icons=None,
                  # 4 構造（全体像）: ピラミッド/グループ
                  elements=None, elements_title=None, elements_kind="pyramid", elements_lead="",
                  # 4b グラフ（データ）: data="ラベル=値｜…"（円で構成比）／ 表: table="h1,h2｜a,b｜…"
                  data=None, data_chart="pie", data_title=None, data_lead="",
                  table=None, table_title=None, table_lead="",
                  # 4d ワイヤーフレーム型を差し込む: wf="W10=全体の構造｜W03=3つの根拠"
                  wf=None,
                  # 詳細スライドの構図をローテーションするか（同じ型を続けない）
                  rotate_layouts=True,
                  # 5 具体例を1枚ずつ（fan-out）: examples="事例A=要点1・要点2｜事例B=…"
                  examples=None, examples_door="事例で確かめる", examples_section="EXAMPLE ／ 具体例",
                  # （旧・単発の具体例も可）
                  scenario="", example_points=None, example_conclusion="",
                  # 6 よくある誤解
                  misconceptions=None, corrections=None, pitfalls_title=None, pitfalls_lead="",
                  # 7 応用・実践のヒントを1枚ずつ（任意 fan-out）
                  applications=None, applications_section="APPLY ／ 応用",
                  # 8 まとめ
                  summary_points=None, summary_title=None, summary_takeaway="",
                  # 小扉を出すか（長尺時の節切り替え）
                  subdoors=True,
                  **_):
    """TF2 概念習得型（What → Why → How）・長尺対応。

    章扉 → 概念(What) → 構成要素を1枚ずつ → 動機づけ(Why) → 構造(全体像)
      → 具体例を1枚ずつ → よくある誤解 → 応用 → まとめ。
    details / examples / applications は項目数だけ1枚ずつ展開（fan-out）。
    項目を増やすほど厚くなり、1チャプター15枚規模まで伸ばせる。
    """
    made = []
    door = subdoors

    def add(x):
        made.append(x)

    # 0 章扉（illust で soco-st 主役イラスト）
    if num is not None:
        add(pages.chapter_cover(prs, num=num, title=topic, course_name=course_name,
                                icon=icon, goals=goals or "", illust=illust))
    # 1 What ── 概念解説
    add(pages.concept(prs, title=concept_title or f"{topic}とは", lead=concept_lead,
                      flow=parts, conclusion=concept_conclusion))
    # 2 構成要素を1枚ずつ（構図をローテーション＝連続で同じ型にしない）
    ditems = _items(details)
    dicons = pages._list(details_icons)
    if ditems:
        if door and details_door:
            add(_subdoor(prs, details_section, details_door))
        for i, (name, bl) in enumerate(ditems):
            ttl = name or f"{topic}の要素"
            if rotate_layouts:
                add(layouts.rotate(i)(prs, section=details_section, title=ttl, bullets=bl))
            else:
                ic = dicons[i] if i < len(dicons) else None
                add(_detail_slide(prs, ttl, bl, section=details_section, icon=ic))
    # 3 Why ── 動機づけ（カード見出しにアイコン）
    if why:
        add(pages.motivation(prs, title=why_title or f"なぜ{topic}が重要か",
                             lead=why_lead, points=why, conclusion=why_conclusion,
                             icons=why_icons))
    # 4 構造（全体像）
    if elements:
        kw = {"lead": elements_lead, "title": elements_title or f"{topic}の全体像"}
        kw["groups" if elements_kind == "groups" else "pyramid"] = elements
        add(pages.structure(prs, **kw))
    # 4b グラフ（データ）── パターンライブラリのチャートを接続
    if data:
        cats, vals = [], []
        for name, val in pages._pairs(data):
            cats.append(name); vals.append(val)
        add(pages.data(prs, title=data_title or f"{topic}を数字で見る", lead=data_lead,
                       chart=data_chart, categories=cats, values=vals))
    # 4c 表 ── 図解ライブラリの diagram_table を接続
    if table:
        rows = _table(table)
        if rows:
            add(_table_slide(prs, table_title or f"{topic}の比較", rows[0], rows[1:],
                             lead=table_lead))
    # 4d ワイヤーフレーム50型を差し込む（wf="W10=全体の構造｜W03=3つの根拠"）
    for key, ttl in pages._pairs(wf):
        add(pages.render(prs, key, {"title": ttl} if ttl else {}))
    # 5 具体例を1枚ずつ（fan-out）＋（旧）単発
    eitems = _items(examples)
    if eitems:
        if door and examples_door:
            add(_subdoor(prs, examples_section, examples_door))
        for name, pts in eitems:
            add(pages.example(prs, title=name or f"{topic}の具体例",
                              points=pts, section=examples_section))
    if scenario or example_points:
        add(pages.example(prs, title=f"{topic}の具体例", scenario=scenario,
                          points=example_points, conclusion=example_conclusion))
    # 6 よくある誤解
    if misconceptions or corrections:
        add(pages.pitfalls(prs, title=pitfalls_title or f"{topic}のよくある誤解",
                           lead=pitfalls_lead, bad=misconceptions or [], good=corrections or []))
    # 7 応用・実践を1枚ずつ
    for name, bl in _items(applications):
        add(_detail_slide(prs, name or f"{topic}の応用", bl, section=applications_section))
    # 8 まとめ
    if summary_points:
        add(pages.summary(prs, title=summary_title or f"{topic}のまとめ",
                          points=summary_points, takeaway=summary_takeaway))
    return made


# ============================================================ ディスパッチャ
FRAMEWORKS = {
    "本編:概念習得": teach_concept, "概念習得": teach_concept,
    "概念習得型": teach_concept, "TF2": teach_concept,
}


def is_framework(key):
    return key.strip() in FRAMEWORKS


def render(prs, key, fields):
    """フレームワークキーで一括展開。返り値は作成したスライドのリスト。"""
    return FRAMEWORKS[key.strip()](prs, **fields)
