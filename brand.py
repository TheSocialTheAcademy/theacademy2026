"""brand.py — ブランド設定の単一ソース（ここを編集すればリブランドできる）。

色・フォント・既定雛形ファイル名をこの1ファイルに集約している。`slides.py` が
これを読み込んで再エクスポートするため、generate.py やスキルは
`from slides import PRIMARY, ...` で参照する。

定数名は「色相」ではなく「役割」で名付けてある（`PRIMARY` `SECONDARY`
`SUCCESS` `DANGER` …）。リブランドは **値（RGBColor）だけ** を差し替え、名前は
据え置く — こうすれば `PRIMARY` はリブランド後も一貫して「主色」を指し、参照側
（slides.py / スキル / サンプル）の import を変えずに済む。名前が色相を約束しない
ので、主色を青や緑に変えても `PRIMARY` のまま嘘にならない。
既定値は暖色オレンジ基調（`PRIMARY` = #EC6739）。

リブランド手順（詳細は docs/REBRAND.md）:
  1. 下の色・フォント・TEMPLATE を自社ブランドに書き換える
  2. `templates/` に自社雛形 .pptx を置き、TEMPLATE をそのファイル名にする
     （雛形は現雛形と同じレイアウト構成・プレースホルダを満たすこと）
"""
from pptx.dml.color import RGBColor

# ============================================================ ブランドカラー
# 役割ベースの定数名。値（RGBColor）だけを書き換え、名前は変えない（参照側が依存）。
# `add_icon()` の color= のみ hex 文字列、それ以外は RGBColor。
# The Academy Brand 2026 — Primary Blue 基調（役割名は据え置き・値のみ差し替え）
PRIMARY       = RGBColor(0x01, 0x41, 0xD4)   # Primary Blue 主色 / 見出しアクセント / CTA
PRIMARY_LIGHT = RGBColor(0xEE, 0xF2, 0xFD)   # 淡い主色 / 差し色（淡青）
SECONDARY     = RGBColor(0x00, 0x5B, 0xA3)   # Dark Navy 補色 / 信頼・構造
SUCCESS       = RGBColor(0x27, 0xAE, 0x60)   # Growth Green 成功・正解・完了
DANGER        = RGBColor(0xF7, 0x6B, 0x38)   # Energy Orange 注意・CTA（※赤は不使用）
HIGHLIGHT     = RGBColor(0x3E, 0x78, 0xFE)   # Light Blue 強調・学習アクセント
TEXT_MUTED    = RGBColor(0x67, 0x66, 0x88)   # Medium Gray 中立・サブテキスト
TEXT          = RGBColor(0x22, 0x22, 0x22)   # Dark Gray 本文テキスト
BORDER        = RGBColor(0xE6, 0xE6, 0xEA)   # 罫線
SURFACE       = RGBColor(0xF4, 0xF6, 0xFC)   # カード背景（淡青サーフェス）
WHITE         = RGBColor(0xFF, 0xFF, 0xFF)   # 反転テキスト・明色背景（絶対色）
BLACK         = RGBColor(0x00, 0x00, 0x00)   # 絶対色

# ============================================================ フォント
# 和文 JP_FONT は配布先に無いとフォールバックする（README / CLAUDE.md の落とし穴参照）。
# latin を変える場合、検査ゲートの幅計測がそのフォントを参照する点に注意。
FONT    = "Graphik"        # latin（英数字）ブランド正式フォント（~/Library/Fonts に導入済み・18ウェイト）。未導入環境では Inter/Arial へフォールバック
JP_FONT = "Hiragino Kaku Gothic ProN"   # 和文（ea/cs）ガイドライン primary（macOS標準）。代替 Noto Sans JP
JOSEFIN = "Josefin Sans"   # 表紙・章番号など装飾英字

# ============================================================ 既定雛形
# templates/ 配下の雛形 .pptx のファイル名。自社雛形に差し替えたらここを変更する。
# The Academy 版：オレンジ chrome をブルーに置換した雛形（サイズ・レイアウトは不変・色のみ）。
TEMPLATE = "スライド雛形_academy.pptx"

# ============================================================ アイコン
# ハウスアイコンセット（Iconify のプレフィックス）。add_icon には "ph:xxx" 形式で渡す。
# ガイドライン（公式 soco-st: 角丸・中線・ライン基調・親しみやすい）に最も近い Phosphor を採用。
# 検索: https://icon-sets.iconify.design/ph/ 。色は 1 アイコン 1 色（白地＝PRIMARY）。
ICON_SET = "ph"
