# 10 · Review

**Goal:** catch mistakes before the user does.

## Preview the README

GitHub renders the README; locally, check that every referenced file exists and view the result:

```bash
grep -oE '(src|srcset)="[^"]+"' README.md | cut -d'"' -f2 | grep -v '^http' | while read f; do [ -f "$f" ] || echo "MISSING $f"; done
```

Then render a local GitHub-style preview of the README and every `docs/` page (working links, light/dark, Mermaid,
copy buttons) and open it — this is also what you show the user before asking to push:

```bash
node <this-repo>/tools/preview/preview.mjs <project> <preview-dir>     # prints the README page path
open <preview-dir>/README.html                                            # or xdg-open / start
node <this-repo>/tools/gif/shot.mjs "file://<preview-dir>/README.html" /tmp/readme.png 6000
```

Look at the screenshot. If image tools are unavailable to you, say the full-page view is unreviewed and let the
user's look at the preview be the check.
Cards below the fold only animate once scrolled into view; scroll before judging a blank card.

## Checklist

- [ ] Secret scan: working tree clean (`tools/scan/secrets.sh .`)
- [ ] No runtime artifacts staged (local DBs, caches the app rewrote, logs): `git status --short`
- [ ] App starts from a fresh clone with only the README's instructions
- [ ] Every number, model name, version and line number in the README and cards checked against the code/output
- [ ] Every card viewed in light **and** dark; GIF frames viewed; every docs diagram viewed
- [ ] `docs/`: links resolve and every env var the code reads is in `setup.md` (commands in `playbook/08-docs.md`)
- [ ] `docs/`: every path, endpoint and table mentioned exists; API examples came from the running app
- [ ] GIF ≤ ~8 MB; total `docs/assets` reasonable (< ~2 MB of SVG)
- [ ] All fixes listed for the PR body; all rotation-needed secrets listed for the report
- [ ] `TODO(owner)` markers listed for the report

**Done when:** every box is ticked or the exception is written down for the report.
