# 画像パターン用の共通データ（色・アイコン・コース）
CAT = {'it': ('IT・デジタル', '#1E9E62', '#E9F7F0'), 'mk': ('マーケティング', '#E46A1F', '#FFF1E7'), 'en': ('英語・TOEIC', '#0141D4', '#EAF0FF'),
       'biz': ('ビジネス', '#6B4FD8', '#F0ECFF'), 'cr': ('クリエイティブ', '#D9467A', '#FDECF2'), 'ca': ('キャリア・学び方', '#0F1B45', '#EEF1F6')}
P = {  # 線アイコン（24×24）
 'palette': '<path d="M12 3a9 9 0 0 0 0 18c1.2 0 1.8-.9 1.4-1.9-.4-1 .3-2.1 1.4-2.1H17a4 4 0 0 0 4-4 9 9 0 0 0-9-10z"/><circle cx="7.5" cy="11" r="1.2"/><circle cx="10.5" cy="7" r="1.2"/><circle cx="15" cy="7.5" r="1.2"/>',
 'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1 7 17M17 7l2.1-2.1"/>',
 'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="m12 13 1 2 2 .3-1.5 1.4.4 2.1-1.9-1-1.9 1 .4-2.1L9 15.3l2-.3z"/>',
 'camera': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'chart': '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/><path d="M15 8h4v4"/>',
 'chat': '<path d="M12 3.5c5 0 9 3.2 9 7.2s-4 7.2-9 7.2c-.7 0-1.4-.1-2-.2L6 20l.6-3.6C4.4 15 3 13 3 10.7 3 6.7 7 3.5 12 3.5z"/><path d="M8 10h8M8 13h5"/>',
 'code': '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
 'mega': '<path d="M4 11v3a1 1 0 0 0 1 1h2l6 4V6L7 10H5a1 1 0 0 0-1 1z"/><path d="M17 9a4 4 0 0 1 0 6M19.5 6.5a8 8 0 0 1 0 11"/>',
 'spark': '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
 'head': '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>',
 'gantt': '<path d="M3 4v16h18"/><path d="M7 7h6M9 11h8M12 15h7"/>',
 'book': '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h7"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
}
def ic(k, cls='', sw=1.6): return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[k]}</svg>'
# slug, 表示名, cat, アイコン, レベル, 形式タグ, 成果物名, 成果物の種類, 中身（見出し）
C = [
 ('canva-basic', 'Canva初級', 'cr', 'palette', 'ベーシック', '全9章・約64分', 'SNS投稿・自己PRのデザインセット', 'phone', ['自己紹介バナー', 'SNS投稿画像', 'プレゼン資料']),
 ('slack-gas-task', 'Slack×GAS スマート管理ツール', 'it', 'gear', 'ツール', '仕様書つき', 'Slackで完結するタスク管理', 'chat', ['タスク登録', 'FAQ自動回答', 'ガントチャート']),
 ('event-design', 'イベントデザイン', 'biz', 'calendar', 'ベーシック', '全18章・約107分', 'イベント企画書・運営マニュアル', 'doc', ['目的と目標', '企画の詳細', '運営体制', '当日の進行', '振り返り']),
 ('instagram', 'インスタグラム', 'mk', 'camera', 'ベーシック', '全13章・約63分', 'Instagramアカウント戦略シート', 'phone', ['ペルソナ', 'テーマとトーン', 'ハッシュタグ', 'データ分析']),
 ('business-english', 'ビジネス英語初級', 'en', 'mail', 'ベーシック', '全7章・約46分', '英語の自己紹介・ビジネスメール文例集', 'doc', ['Self-introduction', 'Business email', 'LinkedIn profile', 'Sales email']),
 ('marketing-basic', 'マーケティング戦略基礎', 'mk', 'chart', 'ベーシック', '全6章・約75分', 'マーケティング戦略シート', 'sheet', ['市場分析', 'KGI・KSF・KPI', 'PDCA計画']),
 ('line-official', '公式LINE運用', 'it', 'chat', 'ベーシック', '全7章・約38分', '公式LINEの資料請求・予約の仕組み', 'phone', ['リッチメニュー', '資料請求', '自動返信', '予約受付']),
 ('automation', '自動化ツール開発', 'it', 'code', 'ベーシック', '全10章・約287分', 'GASで作るタスク管理ツール', 'sheet', ['スプレッドシート', 'メール通知', 'カレンダー連携']),
 ('sns-marketing', 'SNSマーケティング実践', 'mk', 'mega', 'プロ', '8週間', 'SNSキャンペーン企画書', 'doc', ['ペルソナ', '数値目標', '投稿計画', '振り返り']),
 ('ai-efficiency', '生成AI 業務改善', 'it', 'spark', 'プロ', '6週間', '業務改善の仕組み（AI活用）', 'chat', ['調査の自動化', '資料のたたき台', '定型業務']),
 ('toeic-700', 'TOEIC L&R 700点突破', 'en', 'head', 'プレミア', '3か月・全24回', '英語で伝える5分間プレゼン', 'slide', ['Opening', 'Main points', 'Closing']),
 ('chatgpt-basic', '初級編 ChatGPT', 'it', 'spark', 'ベーシック', '単発講座', '仕事で使えるプロンプト集', 'chat', ['議事録', 'メール', '企画のたたき台']),
 ('project-management', 'プロジェクトマネジメント', 'biz', 'gantt', 'ベーシック', '単発講座', 'プロジェクト計画書（WBS）', 'sheet', ['目的・範囲', 'WBS', 'スケジュール']),
]
BASE_CSS = '''*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Noto Sans JP',sans-serif;background:#E9ECF3;color:#0F1B45;padding:56px 60px 70px;width:1440px}
h1{font-size:34px;font-weight:900;letter-spacing:.02em}.lead{color:#676688;font-size:17px;margin:10px 0 0;line-height:1.7}
.pat{background:#fff;border-radius:18px;padding:30px 32px 32px;margin-top:34px}.pat h2{font-size:24px;font-weight:900;display:flex;gap:12px;align-items:center}
.pat h2 em{font-style:normal;background:#0141D4;color:#fff;font-size:16px;padding:4px 12px;border-radius:999px}.pat h2 .rec{background:#F76B38}
.pat .d{color:#4A4E6A;font-size:15px;line-height:1.75;margin:8px 0 18px}.pros{display:flex;gap:28px;font-size:14px;margin:0 0 20px;color:#4A4E6A;flex-wrap:wrap}
.pros b{color:#0F1B45}.lbl{font-size:12px;font-weight:700;color:#0141D4;letter-spacing:.08em;margin:0 0 8px}
.grid{display:grid;gap:18px}.cap{font-size:12.5px;color:#676688;margin-top:7px;line-height:1.5}'''
def board(title, lead, pats, css):
    return f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{BASE_CSS}{css}</style></head><body><h1>{title}</h1><p class="lead">{lead}</p>{"".join(pats)}</body></html>'
def pat(code, name, desc, pros, body, rec=False):
    pr = ''.join(f'<span><b>{k}</b> {v}</span>' for k, v in pros)
    return f'<section class="pat"><h2><em class="{"rec" if rec else ""}">{code}{"（おすすめ）" if rec else ""}</em>{name}</h2><p class="d">{desc}</p><div class="pros">{pr}</div>{body}</section>'
