// node make_assets.mjs -> assets/icon.png (512, black circle "E") + assets/og.png (1200x630 share card, banner look)
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const pw = require('C:/Users/elift/Desktop/Eliftforlife youtube/14 failed businesses video/editor/main/node_modules/playwright');
const F = `@font-face{font-family:I;font-weight:900;src:url('file:///C:/Users/elift/Desktop/Eliftforlife%20youtube/stream/overlay/fonts/inter-latin-900-normal.woff2')}
@font-face{font-family:I;font-weight:700;src:url('file:///C:/Users/elift/Desktop/Eliftforlife%20youtube/stream/overlay/fonts/inter-latin-700-normal.woff2')}`;
const b = await pw.chromium.launch({ args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 512, height: 512 } });
await p.setContent(`<style>${F}html,body{margin:0;background:transparent}div{width:512px;height:512px;border-radius:50%;background:#111;color:#fff;font:900 300px I;display:flex;align-items:center;justify-content:center;letter-spacing:-.02em}</style><div>E</div>`);
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
await p.screenshot({ path: 'assets/icon.png', omitBackground: true });
await p.setViewportSize({ width: 1200, height: 630 });
await p.setContent(`<style>${F}html,body{margin:0;width:1200px;height:630px;background:#fff;font-family:I;color:#111}
.w{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 90px}
h1{font-weight:900;font-size:112px;letter-spacing:-.045em;line-height:1;margin:0}
mark{background:#e8141c;color:#fff;border-radius:16px;padding:0 18px 8px}
p{font-weight:700;font-size:34px;color:#5f6368;margin:34px 0 0}
.n{position:absolute;left:90px;bottom:60px;display:flex;align-items:center;gap:16px;font-weight:900;font-size:32px}
.n i{width:52px;height:52px;border-radius:50%;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:28px}</style>
<div class="w"><h1>I study what <mark>works.</mark></h1><p>Free data on YouTube, ads, outreach and business.</p></div><div class="n"><i>E</i>elijahwestbrook.com</div>`);
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
await p.screenshot({ path: 'assets/og.png' });
await b.close(); console.log('assets done');
