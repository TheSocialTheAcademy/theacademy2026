# 成果物のミニ模型（種類ごとに1つの型。em 単位で拡大縮小）
def mock(kind, items, col, title=''):
    bars = lambda n, w=(92, 78, 85, 60): ''.join(f'<i style="width:{w[i % len(w)]}%"></i>' for i in range(n))
    if kind == 'doc':
        sec = ''.join(f'<div class="mk-s"><b style="color:{col}">{i + 1:02d}</b><span>{t}</span><div class="mk-l">{bars(2)}</div></div>' for i, t in enumerate(items[:4]))
        return f'<div class="mk mk-doc"><div class="mk-pg mk-pg2"></div><div class="mk-pg"><p class="mk-t" style="border-color:{col}">{title}</p>{sec}</div></div>'
    if kind == 'phone':
        tiles = ''.join(f'<span style="background:{col}{a}"></span>' for a in ('', '33', '66', '22', '', '44'))
        lst = ''.join(f'<li><em style="background:{col}"></em>{t}</li>' for t in items[:4])
        return f'<div class="mk mk-ph"><div class="mk-phone"><div class="mk-bar" style="background:{col}"></div><div class="mk-tiles">{tiles}</div><ul>{lst}</ul></div></div>'
    if kind == 'sheet':
        hd = ''.join(f'<th style="background:{col}">{t}</th>' for t in items[:3])
        rows = ''.join('<tr>' + ''.join(f'<td><i style="width:{w}%"></i></td>' for w in ((70, 50, 85), (90, 60, 40), (55, 80, 65), (80, 45, 70))[r]) + '</tr>' for r in range(4))
        return f'<div class="mk mk-sh"><div class="mk-pg"><p class="mk-t" style="border-color:{col}">{title}</p><table>{"<tr>" + hd + "</tr>" + rows}</table><div class="mk-chart">' + ''.join(f'<span style="height:{h}%;background:{col}{a}"></span>' for h, a in ((40, '55'), (55, '77'), (48, '99'), (72, ''), (88, ''))) + '</div></div></div>'
    if kind == 'chat':
        msg = ''.join(f'<div class="mk-m {"me" if i % 2 else ""}"><em style="background:{col}"></em><p><b>{t}</b><i></i><i style="width:60%"></i></p></div>' for i, t in enumerate(items[:3]))
        return f'<div class="mk mk-ch"><div class="mk-pg"><p class="mk-win"><span></span><span></span><span></span><b style="color:{col}"># {title}</b></p>{msg}</div></div>'
    if kind == 'slide':
        dots = ''.join(f'<li><em style="background:{col}"></em>{t}</li>' for t in items[:3])
        return f'<div class="mk mk-sl"><div class="mk-pg mk-pg2"></div><div class="mk-pg"><p class="mk-k" style="color:{col}">PRESENTATION</p><p class="mk-h">{title}</p><ul>{dots}</ul><div class="mk-band" style="background:{col}"></div></div></div>'
MOCK_CSS = '''.mk{position:relative;width:100%;height:100%;font-size:var(--mk,10px)}.mk-pg{position:absolute;inset:6% 10% 6% 8%;background:#fff;border-radius:.6em;box-shadow:0 .4em 1.4em rgba(15,27,69,.10);padding:1.3em 1.4em;overflow:hidden}
.mk-pg2{transform:translate(1.4em,-.9em) rotate(3deg);opacity:.75}.mk-t{font-weight:900;font-size:1.25em;padding-bottom:.5em;border-bottom:.22em solid;margin-bottom:.7em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mk-s{display:grid;grid-template-columns:2.1em 1fr;column-gap:.4em;margin-bottom:.55em}.mk-s b{font-size:1.1em;font-weight:900;grid-row:span 2}.mk-s span{font-weight:700;font-size:1em;white-space:nowrap}
.mk-l i,.mk-sh td i,.mk-m i{display:block;height:.38em;border-radius:.2em;background:#DDE2EC;margin-top:.35em}
.mk-ph{display:grid;place-items:center}.mk-phone{width:46%;height:94%;background:#fff;border:.35em solid #0F1B45;border-radius:1.6em;overflow:hidden;box-shadow:0 .5em 1.6em rgba(15,27,69,.14)}
.mk-bar{height:2.2em}.mk-tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:.25em;padding:.4em}.mk-tiles span{aspect-ratio:1;border-radius:.2em}
.mk-ph ul{list-style:none;padding:.2em .7em}.mk-ph li{font-size:.95em;font-weight:700;display:flex;align-items:center;gap:.45em;padding:.32em 0;border-bottom:1px solid #EEF0F5;white-space:nowrap}.mk-ph li em,.mk-sl li em{width:.6em;height:.6em;border-radius:50%;flex:none}
.mk-sh table{width:100%;border-collapse:collapse;font-size:.85em}.mk-sh th{color:#fff;font-weight:700;padding:.35em .3em;text-align:left;white-space:nowrap;border:1px solid #fff}.mk-sh td{padding:.25em .3em;border:1px solid #E6E9F0}.mk-sh td i{margin:0}
.mk-chart{display:flex;align-items:flex-end;gap:.5em;height:4.6em;margin-top:.8em;border-bottom:1px solid #DDE2EC}.mk-chart span{flex:1;border-radius:.2em .2em 0 0}
.mk-win{display:flex;gap:.3em;align-items:center;margin-bottom:.8em}.mk-win span{width:.6em;height:.6em;border-radius:50%;background:#DDE2EC}.mk-win b{margin-left:.6em;font-size:1.05em}
.mk-m{display:flex;gap:.6em;margin-bottom:.75em}.mk-m em{width:2em;height:2em;border-radius:.5em;flex:none}.mk-m p{flex:1;background:#F4F6FA;border-radius:.6em;padding:.5em .7em}.mk-m b{font-size:.95em}.mk-m.me{flex-direction:row-reverse}.mk-m.me em{opacity:.45}
.mk-k{font-size:.8em;font-weight:700;letter-spacing:.14em}.mk-h{font-size:1.5em;font-weight:900;line-height:1.3;margin:.3em 0 .6em}.mk-sl ul{list-style:none}.mk-sl li{display:flex;align-items:center;gap:.5em;font-weight:700;font-size:1em;margin-bottom:.45em}
.mk-band{position:absolute;left:0;right:0;bottom:0;height:.6em}'''
