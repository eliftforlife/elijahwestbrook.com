// 11-07: screenshots with a built-in static server (no separate server process).  node _shots2.mjs <out folder> [paths...]
import { createRequire } from 'module'; import fs from 'fs'; import path from 'path'; import http from 'http';
const require = createRequire(import.meta.url);
const pw = require('C:/Users/elift/Desktop/Eliftforlife youtube/14 failed businesses video/editor/main/node_modules/playwright');
const OUT = process.argv[2] || '_shots'; fs.mkdirSync(OUT, { recursive: true });
const pages = process.argv.slice(3).length ? process.argv.slice(3) : ['/', '/ai-automation/', '/ai-automation/content-and-social-media/', '/automate/', '/studies/how-much-youtube-pays/'];
const T = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml' };
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html'; const root = path.resolve('docs'); const f = path.resolve(root, '.' + p);
  if (!f.startsWith(root + path.sep)) { r.writeHead(403); return r.end(); }
  if (!fs.existsSync(f) || !fs.statSync(f).isFile()) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': T[path.extname(f)] || 'application/octet-stream' }); r.end(fs.readFileSync(f)); }).listen(8815, '127.0.0.1');
const b = await pw.chromium.launch(); const errs = [];
for (const [name, vp] of [['desk', { width: 1366, height: 900 }], ['phone', { width: 390, height: 844 }]]) {
  const p = await b.newPage({ viewport: vp });
  p.on('console', m => { if (m.type() === 'error' && !/cloudflareinsights|fonts\.g|ERR_/.test(m.text())) errs.push(m.text()); });
  for (const u of pages) {
    await p.goto('http://localhost:8815' + u, { waitUntil: 'load' }); await p.waitForTimeout(800);
    const h = await p.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < h; y += 600) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(90); }
    await p.waitForTimeout(1300); await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300);
    const sw = await p.evaluate(() => document.documentElement.scrollWidth); if (sw > vp.width) errs.push(`${u} ${name}: sideways scroll ${sw}`);
    await p.screenshot({ path: `${OUT}/${name}${u.replace(/\//g, '_')}.png`, fullPage: true });
  }
  await p.close();
}
await b.close(); srv.close(); console.log(errs.length ? errs.join('\n') : 'no errors');
