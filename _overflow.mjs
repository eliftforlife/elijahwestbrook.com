import { createRequire } from 'module'; import fs from 'fs'; import path from 'path'; import http from 'http';
const require = createRequire(import.meta.url);
const pw = require('C:/Users/elift/Desktop/Eliftforlife youtube/14 failed businesses video/editor/main/node_modules/playwright');
const T = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.png': 'image/png' };
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html'; const root = path.resolve('docs'); const f = path.resolve(root, '.' + p);
  if (!f.startsWith(root + path.sep)) { r.writeHead(403); return r.end(); }
  if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': T[path.extname(f)] || 'application/octet-stream' }); r.end(fs.readFileSync(f)); }).listen(8816, '127.0.0.1');
const b = await pw.chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 844 } });
for (const u of process.argv.slice(2)) { await p.goto('http://localhost:8816' + u); await p.waitForTimeout(800);
  console.log(u, JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > 392 && getComputedStyle(e).position !== 'fixed').slice(0, 6).map(e => e.tagName + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().right)))));
}
await b.close(); srv.close();
