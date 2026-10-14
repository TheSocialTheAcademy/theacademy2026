#!/usr/bin/env bash
# lp/ の各ページを生成し直す。トップ（lp-design.html）は手で編集し、ほかのページはここから作る。
# 使い方：bash lp/scripts/build.sh（どこから実行してもよい）
set -euo pipefail
cd "$(dirname "$0")"
for f in gen_courses gen_howto gen_portfolio gen_blog gen_beginners gen_extra gen_resources gen_evidence; do
  python3 "$f.py" > /dev/null
  echo "ok $f"
done
LEGAL_SITE=1 python3 gen_legal.py > /dev/null && echo "ok gen_legal"
python3 set_ogp.py > /dev/null && echo "ok set_ogp"
