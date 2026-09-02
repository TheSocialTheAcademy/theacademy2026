#!/usr/bin/env python3
"""参考デザインの閲覧ボードを生成する（Slideland風・タグ絞り込み）。

refs.json + inbox/画像 → board.html（社内閲覧専用・公開しない）。
標準ライブラリのみ。実行: .venv/bin/python3 refs/build_board.py

- 画像は data URI ではなく相対パス（inbox/…）で参照する＝他社スクショを
  ボードHTMLへ焼き込まない（再配布防止）。board.html は refs/ 内で開く。
- タグ（種類/業種/配色/テイスト/要素/蒸留状態）のチップで AND 絞り込み。
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFS = HERE / "refs.json"
OUT = HERE / "board.html"

AXES = [
    ("doc_type", "種類"),
    ("industry", "業種"),
    ("colors", "配色"),
    ("taste", "テイスト"),
    ("element", "要素"),
]


def load():
    if not REFS.exists():
        return []
    return json.loads(REFS.read_text(encoding="utf-8"))


def esc(s):
    return html.escape(str(s), quote=True)


def card(r):
    file = r.get("file") or ""
    img_path = f"inbox/{esc(file)}" if file else ""
    thumb = (f'<img loading="lazy" src="{img_path}" alt="{esc(r.get("title",""))}">'
             if file else '<div class="noimg">画像なし<br><span>inbox に追加</span></div>')
    chips = []
    for key, _ in AXES:
        for v in (r.get(key) or ([r[key]] if isinstance(r.get(key), str) and r.get(key) else [])):
            if v:
                chips.append(f'<span class="chip {key}">{esc(v)}</span>')
    done = (r.get("extract") == "done")
    status = ('<span class="chip status done">蒸留済</span>' if done
              else '<span class="chip status todo">未蒸留</span>')
    preset = (f'<a class="preset" href="{esc(r["preset"])}">→ {esc(r["preset"])}</a>'
              if r.get("preset") else "")
    src = r.get("source", "")
    note = esc(r.get("notes", ""))
    # data-* に全タグ値を格納（JSフィルタ用）
    data_attrs = " ".join(
        f'data-{k}="{esc("｜".join(r.get(k) or ([r[k]] if isinstance(r.get(k),str) and r.get(k) else [])))}"'
        for k, _ in AXES)
    data_attrs += f' data-status="{"done" if done else "todo"}"'
    return f"""    <article class="ref" {data_attrs}>
      <div class="thumb">{thumb}</div>
      <div class="meta">
        <div class="ttl">{esc(r.get('title','(無題)'))}</div>
        <div class="chips">{status}{''.join(chips)}</div>
        <p class="note">{note}</p>
        <div class="foot"><a class="src" href="{esc(src)}" target="_blank" rel="noopener">出典</a>{preset}</div>
      </div>
    </article>"""


def collect_values(refs):
    vals = {k: [] for k, _ in AXES}
    for r in refs:
        for k, _ in AXES:
            v = r.get(k)
            for x in (v or ([v] if isinstance(v, str) and v else [])):
                if x and x not in vals[k]:
                    vals[k].append(x)
    return vals


def filter_bar(vals):
    blocks = []
    for key, label in AXES:
        if not vals[key]:
            continue
        chips = "".join(
            f'<button class="f" data-axis="{key}" data-val="{esc(v)}">{esc(v)}</button>'
            for v in vals[key])
        blocks.append(f'<div class="fgroup"><span class="flabel">{label}</span>{chips}</div>')
    blocks.append(
        '<div class="fgroup"><span class="flabel">状態</span>'
        '<button class="f" data-axis="status" data-val="todo">未蒸留</button>'
        '<button class="f" data-axis="status" data-val="done">蒸留済</button></div>')
    return "\n".join(blocks)


def build():
    refs = load()
    vals = collect_values(refs)
    cards = "\n".join(card(r) for r in refs) or '<p class="empty">まだ参考がありません。inbox に画像を置き、refs.json に追記してください。</p>'
    doc = f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Academy｜参考デザインボード（社内専用）</title>
<style>
  :root{{--bg:#F4F6FC;--panel:#fff;--ink:#161A2E;--muted:#676688;--faint:#9A9AB2;
    --line:#E6E6EA;--accent:#0141D4;--accent-soft:#E9EEFC;--ok:#27AE60;--warn:#F76B38;
    --sans:"Hiragino Kaku Gothic ProN","Hiragino Sans",system-ui,-apple-system,sans-serif;
    --mono:ui-monospace,Menlo,Consolas,monospace;}}
  @media(prefers-color-scheme:dark){{:root{{--bg:#0B0F1F;--panel:#141931;--ink:#E9ECF7;
    --muted:#9FA0BE;--faint:#6C6D8C;--line:#242A47;--accent:#4E86FF;--accent-soft:#172248;}}}}
  *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}}
  .wrap{{max-width:1240px;margin:0 auto;padding:clamp(1.2rem,3vw,2.4rem)}}
  h1{{font-size:1.5rem;margin:0 0 .2rem;letter-spacing:-.01em}}
  .lede{{color:var(--muted);font-size:.9rem;margin:.2rem 0 0}}
  .warnbar{{margin:1rem 0;background:var(--accent-soft);border:1px solid color-mix(in srgb,var(--accent) 26%,transparent);
    border-radius:10px;padding:.6rem .9rem;font-size:.82rem;color:var(--ink)}}
  .filters{{display:flex;flex-direction:column;gap:.5rem;margin:1.1rem 0 1.4rem;padding:.9rem 1rem;
    background:var(--panel);border:1px solid var(--line);border-radius:12px}}
  .fgroup{{display:flex;flex-wrap:wrap;gap:.35rem;align-items:center}}
  .flabel{{font-family:var(--mono);font-size:.66rem;color:var(--faint);width:4.2em;flex:none;letter-spacing:.05em}}
  button.f{{font-family:var(--sans);font-size:.72rem;color:var(--muted);background:transparent;
    border:1px solid var(--line);border-radius:20px;padding:.16rem .6rem;cursor:pointer}}
  button.f:hover{{border-color:var(--accent);color:var(--accent)}}
  button.f.on{{background:var(--accent);border-color:var(--accent);color:#fff}}
  .bar2{{display:flex;gap:.6rem;align-items:center;margin-top:.2rem}}
  .count{{font-family:var(--mono);font-size:.72rem;color:var(--faint)}}
  .clear{{font-size:.72rem;color:var(--accent);background:none;border:0;cursor:pointer;text-decoration:underline}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem}}
  .ref{{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column}}
  .thumb{{aspect-ratio:16/10;background:var(--bg);display:flex;align-items:center;justify-content:center;border-bottom:1px solid var(--line)}}
  .thumb img{{width:100%;height:100%;object-fit:cover}}
  .noimg{{color:var(--faint);font-size:.8rem;text-align:center}} .noimg span{{font-size:.66rem}}
  .meta{{padding:.6rem .75rem .7rem;display:flex;flex-direction:column;gap:.4rem;flex:1}}
  .ttl{{font-weight:700;font-size:.9rem;line-height:1.25}}
  .chips{{display:flex;flex-wrap:wrap;gap:.25rem}}
  .chip{{font-size:.62rem;color:var(--muted);background:var(--bg);border:1px solid var(--line);border-radius:5px;padding:.05rem .35rem}}
  .chip.status.done{{color:#fff;background:var(--ok);border-color:var(--ok)}}
  .chip.status.todo{{color:var(--warn);border-color:var(--warn)}}
  .note{{font-size:.74rem;color:var(--muted);margin:.1rem 0 0;flex:1}}
  .foot{{display:flex;gap:.8rem;align-items:center;font-size:.72rem}}
  .src{{color:var(--accent)}} .preset{{color:var(--ok);font-family:var(--mono);font-size:.66rem}}
  .empty{{color:var(--muted)}}
  footer{{color:var(--faint);font-family:var(--mono);font-size:.7rem;margin-top:2rem;text-align:center}}
</style></head>
<body><div class="wrap">
  <h1>参考デザインボード</h1>
  <p class="lede">外部スライドの参考を種類・業種・配色・テイスト・要素で絞り込む。良いものは presets/ にテーマとして蒸留する。</p>
  <div class="warnbar">⚠️ <b>社内閲覧専用</b>。このボードと inbox の画像は公開・共有しない（他社資料の再配布防止）。取り込むのは配色・書体・余白・型の“原則”だけ。</div>
  <div class="filters">
{filter_bar(vals)}
    <div class="bar2"><span class="count" id="count"></span><button class="clear" id="clear">絞り込みを解除</button></div>
  </div>
  <div class="grid" id="grid">
{cards}
  </div>
  <footer>The Academy · 参考デザインボード（社内専用・build_board.py 自動生成） · {len(refs)} refs</footer>
</div>
<script>
  const active={{}};
  const grid=document.getElementById('grid');
  const cards=[...grid.querySelectorAll('.ref')];
  const count=document.getElementById('count');
  function apply(){{
    let shown=0;
    cards.forEach(c=>{{
      const ok=Object.entries(active).every(([axis,vals])=>{{
        if(!vals.size) return true;
        const have=(c.dataset[axis]||'').split('｜');
        return [...vals].every(v=>have.includes(v));
      }});
      c.style.display=ok?'':'none'; if(ok) shown++;
    }});
    count.textContent=shown+' / '+cards.length+' 件';
  }}
  document.querySelectorAll('button.f').forEach(b=>{{
    b.onclick=()=>{{
      const ax=b.dataset.axis, v=b.dataset.val;
      active[ax]=active[ax]||new Set();
      if(active[ax].has(v)){{active[ax].delete(v);b.classList.remove('on');}}
      else{{active[ax].add(v);b.classList.add('on');}}
      apply();
    }};
  }});
  document.getElementById('clear').onclick=()=>{{
    for(const k in active) active[k].clear();
    document.querySelectorAll('button.f.on').forEach(b=>b.classList.remove('on'));
    apply();
  }};
  apply();
</script>
</body></html>"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT}  ({len(refs)} refs)")


if __name__ == "__main__":
    build()
