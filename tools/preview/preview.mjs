// Usage: node tools/preview/preview.mjs <project-dir> <out-dir>
// Renders README.md and every docs/**/*.md as GitHub-style HTML pages in <out-dir> (nothing is written to the
// project). Links between .md files point at the rendered pages; images load from the project. Light/dark follows
// the OS, Mermaid blocks render, code blocks get a click-only copy button, and heading anchors use GitHub's slugs.
import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, dirname, resolve } from 'node:path';

const [projectArg, outArg] = process.argv.slice(2);
if (!projectArg || !outArg) { console.error('usage: preview.mjs <project-dir> <out-dir>'); process.exit(1); }
const project = resolve(projectArg);
const out = resolve(outArg);

const pages = [];
if (existsSync(join(project, 'README.md'))) pages.push('README.md');
const walk = (dir) => {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p);
    else if (name.endsWith('.md')) pages.push(relative(project, p));
  }
};
if (existsSync(join(project, 'docs'))) walk(join(project, 'docs'));

const page = (rel) => `<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>${rel} — preview</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown.min.css">
<style>
body{margin:0;background:#fff}@media (prefers-color-scheme:dark){body{background:#0d1117}}
.markdown-body{box-sizing:border-box;max-width:1012px;margin:0 auto;padding:32px 16px}
.bar{font:12px -apple-system,sans-serif;color:#57606a;max-width:1012px;margin:0 auto;padding:12px 16px 0}
.markdown-body pre{position:relative}
.copy-btn{position:absolute;top:8px;right:8px;opacity:0;transition:opacity .15s;border:1px solid #d0d7de;background:#f6f8fa;border-radius:6px;padding:4px 8px;font:12px -apple-system,sans-serif;cursor:pointer;color:#57606a}
.markdown-body pre:hover .copy-btn{opacity:1}
@media (prefers-color-scheme:dark){.copy-btn{background:#21262d;border-color:#30363d;color:#8b949e}.bar{color:#8b949e}}
</style></head><body>
<div class="bar">Local preview of <b>${rel}</b> · not GitHub · <a href="${relative(dirname(join(out, rel)), join(out, 'README.html'))}">README</a></div>
<article class="markdown-body" id="c"></article>
<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
const md = ${JSON.stringify(readFileSync(join(project, rel), 'utf8'))};
const srcDir = ${JSON.stringify('file://' + dirname(join(project, rel)) + '/')};
const esc = s => s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'})[c]);
// GitHub slug: lowercase, drop punctuation/symbols but keep spaces, then spaces -> dashes ("▸ See it" -> "-see-it")
const slug = t => t.toLowerCase().replace(/<[^>]+>/g, '').replace(/[^\\p{L}\\p{N}\\s_-]/gu, '').replace(/\\s/g, '-');
const r = new marked.Renderer();
r.code = (code, lang) => lang === 'mermaid' ? '<pre class="mermaid">' + esc(code) + '</pre>' : '<pre><code>' + esc(code) + '</code></pre>';
r.heading = (text, level, raw) => '<h' + level + ' id="' + slug(raw) + '">' + text + '</h' + level + '>';
const c = document.getElementById('c');
c.innerHTML = marked.parse(md, { renderer: r, gfm: true });
const isRel = u => u && !/^([a-z]+:|#|\\/)/i.test(u);
// images and non-markdown files load from the project; .md links go to the rendered page
c.querySelectorAll('img[src],source[srcset]').forEach(el => {
  const a = el.hasAttribute('src') ? 'src' : 'srcset';
  if (isRel(el.getAttribute(a))) el.setAttribute(a, new URL(el.getAttribute(a), srcDir).href);
});
c.querySelectorAll('a[href]').forEach(a => {
  const h = a.getAttribute('href');
  if (!isRel(h)) return;
  const [path, frag] = h.split('#');
  if (/\\.md$/i.test(path)) a.setAttribute('href', path.replace(/\\.md$/i, '.html') + (frag ? '#' + frag : ''));
  else if (/\\/$/.test(path)) a.setAttribute('href', path + 'README.html' + (frag ? '#' + frag : ''));
  else a.setAttribute('href', new URL(h, srcDir).href);
});
c.querySelectorAll('pre:not(.mermaid)').forEach(pre => {
  const b = document.createElement('button'); b.className = 'copy-btn'; b.textContent = 'Copy';
  b.onclick = () => navigator.clipboard.writeText(pre.querySelector('code').innerText)
    .then(() => { b.textContent = 'Copied'; setTimeout(() => b.textContent = 'Copy', 1200); });
  pre.appendChild(b);
});
mermaid.initialize({ startOnLoad: false, theme: matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'default' });
await mermaid.run({ querySelector: '.mermaid' });
if (location.hash) document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView();
</script></body></html>`;

for (const rel of pages) {
  const dest = join(out, rel.replace(/\.md$/i, '.html'));
  mkdirSync(dirname(dest), { recursive: true });
  writeFileSync(dest, page(rel));
}
console.log(`${pages.length} pages → ${join(out, 'README.html')}`);
