// Usage: node gif/shot.mjs <file.svg|url> <out.png> [waitMs]
import { chromium } from 'playwright';
const [src, out, wait = 6000] = process.argv.slice(2);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 1 });
await p.goto(src.startsWith('http') || src.startsWith('file') ? src : 'file://' + src);
await p.waitForTimeout(+wait);
const svg = src.endsWith('.svg') ? await p.$('svg') : null;
await (svg ?? p).screenshot({ path: out, ...(svg ? {} : { fullPage: true }) });
await b.close();
