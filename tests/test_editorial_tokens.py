"""統一トークン（editorial.py）の回帰テスト。

統一してよい7項目は「値を1箇所で決め、そこを通さないと描けない」状態でなければ
守られない。ここでは、
  - 罫線は RULE の5値以外を受け付けないこと
  - 注釈が全ページ同じ見え方（補助色・注釈級数）になること
  - 余白がグリッドと基準線の上で決まること
  - 本文の必要高さが検査ゲートと同じ計測で求まること（＝見切れない）
  - 編集トーンの機械チェックが効くこと
を確認する。
"""
import pytest

import editorial as ed
from slides import validate_fit


# ---------------------------------------------------------------- 罫線の太さ
def test_rule_accepts_only_registered_weights(body_slide):
    for name in ed.RULE:
        ed.rule(body_slide, 2.0, 5.0, 6.0, weight=name)
    with pytest.raises(ValueError):
        ed.rule(body_slide, 2.0, 6.0, 6.0, weight="fat")
    with pytest.raises(ValueError):
        ed.rule(body_slide, 2.0, 6.0, 6.0, weight=3.0)


def test_vrule_uses_same_weight_table(body_slide):
    ed.vrule(body_slide, 5.0, 4.0, 3.0, weight="structure")
    with pytest.raises(ValueError):
        ed.vrule(body_slide, 5.0, 4.0, 3.0, weight=0.9)


# ---------------------------------------------------------------- 注釈の扱い
def test_note_is_muted_and_small(body_slide):
    ed.note(body_slide, 1.07, 11.0, 8.0, ["出典：社内実績値"])
    runs = [r for sh in body_slide.shapes if sh.has_text_frame
            for p in sh.text_frame.paragraphs for r in p.runs]
    assert runs, "注釈が描かれていない"
    for r in runs:
        assert r.font.size.pt == ed.NOTE_SIZE
        assert r.font.color.rgb == ed.INK_SUB


def test_note_numbers_multiple_items(body_slide):
    ed.note(body_slide, 1.07, 10.5, 8.0, ["ひとつめ", "ふたつめ"])
    text = "\n".join(sh.text_frame.text for sh in body_slide.shapes
                     if sh.has_text_frame)
    assert f"{ed.NOTE_MARK}1 ひとつめ" in text
    assert f"{ed.NOTE_MARK}2 ふたつめ" in text


def test_note_of_single_item_has_no_number(body_slide):
    ed.note(body_slide, 1.07, 10.5, 8.0, ["ひとつだけ"])
    text = "\n".join(sh.text_frame.text for sh in body_slide.shapes
                     if sh.has_text_frame)
    assert f"{ed.NOTE_MARK} ひとつだけ" in text
    assert f"{ed.NOTE_MARK}1" not in text


# ---------------------------------------------------------------- 余白の感覚
def test_grid_spans_stay_inside_the_field():
    x0, w0 = ed.GRID.span(0, 12)
    assert x0 == pytest.approx(ed.FIELD["x"])
    assert x0 + w0 == pytest.approx(ed.FIELD["x"] + ed.FIELD["w"], abs=0.01)


def test_grid_split_is_asymmetric_and_gapped():
    (lx, lw), (rx, rw) = ed.GRID.split(7, 4)
    assert lw > rw                      # 非対称の段が作れる
    assert rx - (lx + lw) > 0           # 段のあいだに溝が空く


def test_grid_split_rejects_too_many_columns():
    with pytest.raises(ValueError):
        ed.GRID.split(7, 7)


def test_baseline_and_after_stay_on_the_grid():
    y = ed.baseline(3)
    assert y == pytest.approx(ed.FIELD["y"] + ed.BASE * 3)
    nxt = ed.after(y + 0.01)
    n = (nxt - ed.FIELD["y"]) / ed.BASE
    assert n == pytest.approx(round(n), abs=1e-6)
    assert nxt > y


# ---------------------------------------------------------------- 文字の必要高さ
def test_body_height_is_measured_not_guessed(prs, body_slide):
    lines = ["日本語の本文がそれなりの長さで折り返される場合でも、"
             "枠が足りずに末尾が切れてはいけない。"] * 3
    ed.body(body_slide, 1.07, 4.0, 10.0, lines, density="dense")
    codes = {v.code for v in validate_fit(prs)}
    assert "OVERFLOW_V" not in codes
    assert "OVERFLOW_H" not in codes


def test_body_steps_down_density_to_fit(body_slide):
    lines = ["収まるところまで密度を落とす。"] * 3
    sparse_size, sparse_ls = ed.DENSITY["sparse"]
    dense_size, dense_ls = ed.DENSITY["dense"]
    sparse_h = ed.fit_h(lines, 8.0, sparse_size, ls=sparse_ls)
    dense_h = ed.fit_h(lines, 8.0, dense_size, ls=dense_ls)
    assert dense_h < sparse_h
    ed.body(body_slide, 1.07, 4.0, 8.0, lines, density="sparse",
            fit_to=(sparse_h + dense_h) / 2)
    sizes = {r.font.size.pt for sh in body_slide.shapes if sh.has_text_frame
             for p in sh.text_frame.paragraphs for r in p.runs}
    assert sizes and max(sizes) < ed.DENSITY["sparse"][0]


def test_body_raises_when_it_cannot_fit(body_slide):
    with pytest.raises(ValueError):
        ed.body(body_slide, 1.07, 4.0, 6.0,
                ["どうやっても収まらない量の文章。"] * 12,
                density="sparse", fit_to=1.0)


# ---------------------------------------------------------------- 編集トーン
@pytest.mark.parametrize("bad", [
    "今すぐ買わないと手遅れになります",
    "絶対に成功します",
    "たった3日で誰でもできる",
    "すごい成果！！",
])
def test_tone_lint_catches_pressure_and_promises(bad):
    assert ed.tone_lint(bad), f"検出できていない: {bad}"


def test_tone_lint_passes_ordinary_editorial_copy():
    assert ed.tone_lint([
        "受講の成否を分けるのは、最初の3週間の設計だった。",
        "難易度そのものを下げる必要はない。",
    ]) == []
