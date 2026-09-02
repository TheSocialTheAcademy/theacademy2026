"""content.txt → コース1本 を通し生成する薄いドライバ。

書式（テキスト1本でコース全体を記述）:

    # 行頭 # または // はコメント。空行は無視。
    【型キー】                      ← RENDERERS のキー（idx / 和名 / wf関数名）
    key: value                    ← そのページのフィールド。全角「：」も可
    goals: A｜B｜C                 ← 「｜」区切りは pages 側で list に正規化
    rows: 見出し=説明｜見出し=説明   ← 「=」ペアも pages 側で正規化
    |続き行                        ← 直前の value の続き（行頭 | で改行を連結）

各ブロックを順に `pages.render(prs, キー, フィールド)` へ渡すだけ。キーは 28 型でも
本編ワイヤー 50 型でも同じ経路で引ける（pages.RENDERERS）。標準フロー（HANDOFF §1.5）
に沿って、先頭ブロックを「コース表紙」にすると slide0 を書き換える形になる。

使い方:
    from coursegen import build_course
    build_course("content.txt", "output.pptx")            # 生成＋検査ゲート
    build_course("content.txt", "output.pptx", validate_gate=False)
"""
from pathlib import Path

import pages
import frameworks
from slides import (
    load_template, reset_to_cover_only, add_back_cover,
    finalize_page_numbers, validate,
)

_HEADER_OPEN, _HEADER_CLOSE = "【", "】"


def parse(text):
    """content テキストを [(型キー, フィールド dict), ...] に構文解析する。"""
    blocks = []
    key = None
    fields = {}
    last_field = None  # 直前に代入したフィールド名（行頭 | の続き行用）

    def flush():
        nonlocal key, fields
        if key is not None:
            blocks.append((key, fields))
        key, fields = None, {}

    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("//"):
            continue
        # ブロック見出し 【型キー】
        if stripped.startswith(_HEADER_OPEN) and _HEADER_CLOSE in stripped:
            flush()
            key = stripped[len(_HEADER_OPEN):stripped.index(_HEADER_CLOSE)].strip()
            last_field = None
            continue
        if key is None:
            continue  # 最初のブロック見出しより前の行は無視
        # 続き行（行頭 |）: 直前フィールドに改行連結
        if stripped.startswith("|") and last_field is not None:
            fields[last_field] = f"{fields[last_field]}\n{stripped[1:].strip()}"
            continue
        # key: value（半角 : / 全角 ：）
        sep_idx = _first_colon(stripped)
        if sep_idx is None:
            continue  # コロンの無い行はスキップ（緩く扱う）
        fkey = stripped[:sep_idx].strip()
        fval = stripped[sep_idx + 1:].strip()
        fields[fkey] = fval
        last_field = fkey
    flush()
    return blocks


def _first_colon(s):
    """半角 ':' か全角 '：' の先に現れる位置。無ければ None。"""
    cands = [s.index(c) for c in (":", "：") if c in s]
    return min(cands) if cands else None


def build_course(content, out, *, validate_gate=True, cover_lines=None):
    """content（パス or テキスト）から pptx を生成。末尾で検査ゲートを回す。

    先頭ブロックが「コース表紙(A1)」なら slide0 を書き換える（reset_to_cover_only で表紙のみ残す）。
    cover_lines を渡すと表紙ブロックが無い場合の既定表紙に使う。
    """
    text = content
    p = Path(str(content))
    if len(str(content)) < 4096 and p.exists():
        text = p.read_text(encoding="utf-8")

    blocks = parse(text)
    out = Path(out)

    prs = load_template()
    reset_to_cover_only(prs)
    if cover_lines is not None and not (blocks and _is_cover(blocks[0][0])):
        from slides import update_cover
        update_cover(prs.slides[0], lines=cover_lines)

    for key, fields in blocks:
        # 本編フレームワーク（1ブロック→複数ページ）は frameworks へ、それ以外は pages へ
        if frameworks.is_framework(key):
            frameworks.render(prs, key, fields)
        else:
            pages.render(prs, key, fields)

    add_back_cover(prs)
    finalize_page_numbers(prs, skip_first=True)
    prs.save(out)
    if validate_gate:
        validate(prs, out, render=True)
    return prs, blocks


def _is_cover(key):
    fn = pages.RENDERERS.get(key.strip())
    return fn is pages.course_cover


if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "content.txt"
    dst = sys.argv[2] if len(sys.argv) > 2 else "output.pptx"
    _, bl = build_course(src, dst)
    print(f"✅ {len(bl)} ブロック → {dst}")
