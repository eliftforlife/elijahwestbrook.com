// node _el.mjs <path> <css selector> <out.png> [width]  -> screenshot of one element (local docs server)
import { createRequire } from 'module'; import fs from 'fs'; import path from 'path'; import http from 'http';
const require = createRequire(import.meta.url);
const pw = require('C:/Users/elift/Desktop/Eliftforlife youtube/14 failed businesses video/editor/main/node_modules/playwright');
const T = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.png': 'image/png' };
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html'; const f = path.join('docs', p);
  if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': T[path.extname(f)] || 'application/octet-stream' }); r.end(fs.readFileSync(f)); }).listen(8817);
const [u, sel, out, w] = process.argv.slice(2);
const b = await pw.chromium.launch(); const p = await b.newPage({ viewport: { width: +(w || 1366), height: 900 } });
await p.goto('http://localhost:8817' + u); await p.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('in'))); await p.waitForTimeout(600);
await (await p.$(sel)).screenshot({ path: out }); await b.close(); srv.close(); console.log('ok');
