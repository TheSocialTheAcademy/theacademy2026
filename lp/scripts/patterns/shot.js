const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const [url,out,w,h]=process.argv.slice(2);const p=await b.newPage({viewport:{width:+w,height:+(h||900)}});await p.goto(url);await p.waitForTimeout(700);await p.screenshot({path:out,fullPage:!h});await b.close();})();
