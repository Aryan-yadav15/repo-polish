// Capture the diagram (just the SVG, at 2x) in light and dark: node capture.mjs <file.html> <out-prefix>
import { chromium } from 'playwright';

const [file, prefix] = process.argv.slice(2);
const b = await chromium.launch();
for (const theme of ['light', 'dark']) {
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2, colorScheme: theme, reducedMotion: 'reduce' });  // still frame: no marching dashes
  await p.goto('file://' + file);
  await p.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
  await p.waitForTimeout(1500);
  // crop to what is actually drawn (lanes, nodes, labels, legend) plus a margin
  const clip = await p.evaluate(() => {
    const svg = [...document.querySelectorAll('svg')].find(s => s.querySelector('g[data-node-id]'));
    const els = svg.querySelectorAll('[data-graph-role], g[data-node-id], g[data-legend], text, path[data-edge-id]');
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const e of els) {
      const r = e.getBoundingClientRect();
      if (!r.width && !r.height) continue;
      x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom);
    }
    const m = 24;
    return { x: Math.max(0, x0 - m), y: Math.max(0, y0 - m), width: x1 - x0 + 2 * m, height: y1 - y0 + 2 * m };
  });
  await p.screenshot({ path: `${prefix}-${theme}.png`, clip });
  await p.close();
}
await b.close();
console.log(`${prefix}-light.png, ${prefix}-dark.png`);
