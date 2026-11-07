// Usage: node gif/record.mjs <url> <steps.json> <out.gif>
// steps.json: [{"click":"text=Send"},{"fill":["textarea","Top 5 customers by spend"]},
//              {"press":"Enter"},{"waitFor":"text=SELECT","speed":4},{"wait":3000}]
// A step with "speed" fast-forwards the time spent on it (e.g. waiting for an LLM).
// Env: W/H viewport, CSS injected style, CROP=w:h:x:y, GW gif width, FPS, COLORS, KEEP=1 print video path.
import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';
import { readFileSync, mkdtempSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [url, stepsFile, out] = process.argv.slice(2);
const steps = JSON.parse(readFileSync(stepsFile, 'utf8'));
const dir = mkdtempSync(join(tmpdir(), 'gif-'));
const size = { width: +(process.env.W || 1280), height: +(process.env.H || 800) };
const fps = +(process.env.FPS || 10);

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: size, recordVideo: { dir, size } });
const page = await ctx.newPage();
const t0 = Date.now();
const now = () => (Date.now() - t0) / 1000;
await page.goto(url, { waitUntil: 'networkidle' });
// optional CSS to hide distracting decoration (e.g. particle effects) that bloats GIFs
if (process.env.CSS) await page.addStyleTag({ content: process.env.CSS });

const fast = []; // [start, end, speed] in seconds of video time
for (const s of steps) {
  const start = now();
  if (s.click) await page.click(s.click);
  if (s.fill) await page.fill(s.fill[0], '').then(() => page.type(s.fill[0], s.fill[1], { delay: 45 }));
  if (s.press) await page.keyboard.press(s.press);
  if (s.waitFor) await page.waitForSelector(s.waitFor, { timeout: s.timeout ?? 60000 });
  if (s.scroll) await page.mouse.wheel(0, s.scroll);
  if (s.pause) await page.waitForTimeout(s.pause); // e.g. wait out an API rate limit; pair with speed to cut it
  if (s.speed) fast.push([start, now(), s.speed]);
  await page.waitForTimeout(s.wait ?? 600);
}

const webm = await page.video().path();
await ctx.close();
await browser.close();
if (process.env.KEEP) console.log('video:', webm);

// build piecewise-speed segments covering the whole video
const segs = [];
let cur = 0;
for (const [a, b, sp] of fast) {
  if (a > cur) segs.push([cur, a, 1]);
  segs.push([a, b, sp]);
  cur = b;
}
segs.push([cur, null, 1]);
const parts = segs.map(([a, b, sp], i) =>
  `[0:v]trim=start=${a}${b ? `:end=${b}` : ''},setpts=(PTS-STARTPTS)/${sp}[s${i}]`).join(';');
const crop = process.env.CROP ? `crop=${process.env.CROP},` : '';
const chain = `${parts};${segs.map((_, i) => `[s${i}]`).join('')}concat=n=${segs.length}:v=1,` +
  `${crop}fps=${fps},scale=${process.env.GW || 1100}:-1:flags=lanczos`;
const palette = join(dir, 'palette.png');
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', webm, '-filter_complex',
  `${chain},palettegen=max_colors=${process.env.COLORS || 128}:stats_mode=diff`, palette]);
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', webm, '-i', palette, '-filter_complex',
  `${chain}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle`, out]);
console.log(`${out}  ${(statSync(out).size / 1e6).toFixed(1)} MB`);
