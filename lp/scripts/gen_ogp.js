// gen_ogp.py が書いた HTML から OGP 画像を PNG で切り出す（jpg への変換は gen_ogp.py save）
const { chromium } = require('playwright'); const fs = require('fs'); const os = require('os'); const path = require('path');
const J = JSON.parse(fs.readFileSync(process.env.TA_JOB || path.join(os.tmpdir(), 'ta_ogp.json'), 'utf8'));
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1240, height: 900 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + J.html); await p.waitForTimeout(700);
  for (const s of J.slugs) await p.locator('#t-' + s).screenshot({ path: path.join(os.tmpdir(), `ta_ogp_${s}.png`) });
  await b.close(); console.log('ok png', J.slugs.length); })();
