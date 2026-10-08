// gen_thumbs.py が書いた HTML から、コースごとのサムネイルを PNG で切り出す（webp への変換は thumbs_webp.py）
const { chromium } = require('playwright'); const fs = require('fs'); const os = require('os'); const path = require('path');
const J = JSON.parse(fs.readFileSync(process.env.TA_JOB || path.join(os.tmpdir(), 'ta_thumbs.json'), 'utf8'));  // TA_JOB で別の書き出し（記事のアイキャッチなど）にも使う
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 2 });
  await p.goto('file://' + J.html); await p.waitForTimeout(500); fs.mkdirSync(J.dir, { recursive: true });
  for (const s of J.slugs) await p.locator('#t-' + s).screenshot({ path: path.join(os.tmpdir(), `${J.prefix || 'ta_thumb_'}${s}.png`) });
  await b.close(); console.log('ok png', J.slugs.length); })();
