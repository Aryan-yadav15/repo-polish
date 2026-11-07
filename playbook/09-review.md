# 9 · Review

**Goal:** catch mistakes before the user does.

## Preview the README

GitHub renders the README; locally, check that every referenced file exists and view the result:

```bash
grep -oE '(src|srcset)="[^"]+"' README.md | cut -d'"' -f2 | grep -v '^http' | while read f; do [ -f "$f" ] || echo "MISSING $f"; done
```

Then either push the branch and view it on GitHub (after the user approves the push), or render locally
with any GitHub-flavoured-markdown previewer and screenshot it with `tools/gif/shot.mjs`.
Cards below the fold only animate once scrolled into view; scroll before judging a blank card.

## Checklist

- [ ] Secret scan: working tree clean (`tools/scan/secrets.sh .`)
- [ ] No runtime artifacts staged (local DBs, caches the app rewrote, logs): `git status --short`
- [ ] App starts from a fresh clone with only the README's instructions
- [ ] Every number, model name, version and line number in the README and cards checked against the code/output
- [ ] Every card viewed in light **and** dark; GIF frames viewed
- [ ] GIF ≤ ~8 MB; total `docs/assets` reasonable (< ~2 MB of SVG)
- [ ] All fixes listed for the PR body; all rotation-needed secrets listed for the report
- [ ] `TODO(owner)` markers listed for the report

**Done when:** every box is ticked or the exception is written down for the report.
