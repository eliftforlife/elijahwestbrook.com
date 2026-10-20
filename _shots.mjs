// node _shots.mjs -> _shots/*.png (desktop + phone, full page) from the local server on :8811
import { createRequire } from 'module'; import fs from 'fs';
const require = createRequire(import.meta.url);
const pw = require('C:/Users/elift/Desktop/Eliftforlife youtube/14 failed businesses video/editor/main/node_modules/playwright');
fs.mkdirSync('_shots', { recursive: true });
const pages = process.argv.slice(2).length ? process.argv.slice(2) : ['/', '/studies/how-much-youtube-pays/', '/studies/best-time-to-post-on-youtube/'];
const b = await pw.chromium.launch();
for (const [name, vp] of [['desk', { width: 1280, height: 900 }], ['phone', { width: 390, height: 844 }]]) {
  const p = await b.newPage({ viewport: vp, deviceScaleFactor: 1 });
  for (const u of pages) { await p.goto('http://localhost:8811' + u, { waitUntil: 'networkidle' }); await p.waitForTimeout(500);
    await p.screenshot({ path: `_shots/${name}${u.replace(/\//g, '_') || '_'}.png`, fullPage: true }); }
  await p.close();
}
await b.close(); console.log(fs.readdirSync('_shots'));
