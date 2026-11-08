# 8 · Docs

**Goal:** a `docs/` folder that lets a contributor — or the owner, months from now — understand and change the
code safely. The README is the front page for visitors; `docs/` is the manual for people working on the code.

## Ask first

Before writing, ask the user which they want:

1. **Full docs** — every page below that applies to this project.
2. **Essentials** — `codebase.md` + `setup.md` only.
3. **Skip** — README only.

If the project already has a `docs/` folder, say what's there and ask whether to **extend** it or **restructure** it.
Never delete existing docs; move or correct them, and say what changed.

## Pages

Use the skeletons in `templates/docs/`. Write only the pages the project needs — no empty or filler pages.

| Page | Contents | Include when |
|---|---|---|
| `docs/README.md` | index: what each page covers, suggested reading order | always (if writing docs) |
| `architecture.md` | components, how they communicate, main flows, key decisions (long form of the cards) | always |
| `codebase.md` | folder-by-folder map: what each module does, entry points, "where to start for X" | always |
| `setup.md` | full local setup; **configuration table** — env vars, or whatever the project uses instead (VS Code settings, CLI flags, config files): name · required/default · example · purpose · where it's read | always |
| `api.md` | endpoints / CLI commands / public functions, with real request + response examples | there is an API or CLI |
| `data.md` | schema, models, relationships, migrations, sample data | there is a database or persistent store |
| `operations.md` | deploy, per-environment config, logs, common failures and fixes | it is (or was) deployed |
| `decisions/NNNN-title.md` | one short ADR per significant choice: context, decision, consequences | 2+ decisions worth recording |

## Diagrams: use Archify for flow explanations

Whenever a page needs to **explain a flow** — a request path, a data pipeline, an agent/tool loop, a state
lifecycle, a sequence between services — or show a **schema** (ERD), use **[Archify](https://github.com/tt-a1i/archify)**:
an open-source (Apache-2.0) agent skill that turns a description or a repository into a validated, interactive diagram
(architecture, workflow, sequence, dataflow, lifecycle, ERD, class, tree, timeline, waterfall).

**Install (ask first).** Archify's own instructions require confirming scope with the user before installing.
Ask: install globally or for this project only, and for which agent. Then follow
<https://raw.githubusercontent.com/tt-a1i/archify/main/llms.txt> exactly — it lists, installs, then verifies with
`node <installed-path>/bin/archify.mjs doctor`. If the user declines, or you're in Advisor mode, use the
Mermaid fallback below.

**Already installed?** Check before installing (it may already be in the agent's skill list, globally or in
another project). If it is, tell the user where and which version, and ask whether to use it or install the scope
they picked. If Archify reports an update, relay it; don't update without being asked.

**Generate.** Ask Archify for the diagram the way its skill expects — describe what the reader needs to understand,
and for code-backed diagrams point it at the repository so nodes carry source evidence. Its `finalize` command
validates the result; a non-zero exit is never success. Keep each diagram's source and HTML in the project:

```
docs/diagrams/<name>.json        candidate source (regenerable)
docs/diagrams/<name>.html        interactive standalone diagram
docs/diagrams/<name>-light.png   static image for Markdown
docs/diagrams/<name>-dark.png
```

**Practical notes** (from real runs):

- **Keep receipts out of the repo.** `finalize` writes receipt JSON next to the output; pass `--out-dir <scratch>` where
  supported, and before committing keep only `<name>.json`, `<name>.html` and the PNGs in `docs/diagrams/`.
- **Browser gate needs Chrome.** If `browser-check` reports `viewer/chrome-unavailable`, point it at Playwright's
  Chromium: `export ARCHIFY_CHROME="$(node -e "console.log(require('playwright').chromium.executablePath())")"`
  (run from this repo after `npm install`).
- **Readability gates are strict.** Keep participant labels short (a word or two, ~12 characters) and put detail in the
  sublabel; keep the canvas width ≤ ~1080 so text isn't scaled below the minimum; merge minor return messages rather
  than stacking many. Read the diagnostic, fix that one thing, rerun — a non-zero exit is never success.
- **Types depend on version.** If the installed Archify lacks a type you need (e.g. ERD in older versions), use Mermaid
  for that diagram and say so.

**Embed.** GitHub does not render HTML inside Markdown, so embed the PNGs and link the interactive file:

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="diagrams/request-flow-dark.png"/>
  <img src="diagrams/request-flow-light.png" width="100%" alt="Request flow: browser → API → cache → database …"/>
</picture>

<sub>[Interactive version](diagrams/request-flow.html) — download and open in a browser to trace paths and see source links.</sub>
```

Get the PNGs from Archify's capture command, which renders light and dark screenshots
(`node <installed-path>/bin/archify.mjs visual-check docs/diagrams/<name>.html --summary --require-provenance --out-dir <tmp>`),
or with `tools/gif/shot.mjs` on the HTML. Crop to the diagram if needed. **Look at the images** before embedding.

**Mermaid fallback.** If Archify isn't available, write a fenced ```` ```mermaid ```` block (GitHub renders it).
Prefer `sequenceDiagram` for request flows, `flowchart` for pipelines, `stateDiagram-v2` for lifecycles, `erDiagram`
for schemas. Keep each under ~15 nodes; split rather than cram.

**Which diagrams.** One per real question a contributor would ask ("what happens when a request comes in?",
"how does data get from X to Y?", "what states can an order be in?"). Typical set: the main request flow in
`architecture.md`, an ERD in `data.md`, a lifecycle for any state machine. Don't diagram what a sentence explains.

## Rules

- **Generated from the code.** Every module, endpoint, env var and table comes from the source, with its file path
  (`src/api/routes.py:42`). Existing docs are a hint, not a source.
- **Examples are real.** Request/response examples in `api.md` come from calling the running app in stage 5;
  env var examples are placeholders, never real values.
- **Correct what's wrong.** If existing docs contradict the code, fix them and list the corrections for the PR.
- **Link, don't repeat.** README links into `docs/`; docs link to each other and to source files. One source of truth per fact.
- **Relative links** so docs work on forks, branches and GitHub's file browser.

## Verify

```bash
# every relative link and image in docs/ resolves
grep -rhoE '\]\(([^)#]+)|src="[^"]+"|srcset="[^"]+"' docs | sed -E 's/^\]\(|^src="|^srcset="|"$//g' | grep -v '^http' | sort -u \
  | while read p; do [ -e "docs/$p" ] || [ -e "$p" ] || echo "BROKEN $p"; done

# every env var the code reads appears in setup.md (adjust the pattern to the language; for settings-based
# projects such as VS Code extensions, compare contributes.configuration keys in package.json instead)
grep -rhoE 'process\.env\.[A-Z0-9_]+|os\.environ(\.get\(|\[)["'"'"'][A-Z0-9_]+|getenv\(["'"'"'][A-Z0-9_]+' --include='*.js' --include='*.ts' --include='*.py' --exclude-dir=node_modules --exclude-dir=.venv . \
  | grep -oE '[A-Z][A-Z0-9_]+$' | sort -u | while read v; do grep -q "$v" docs/setup.md || echo "UNDOCUMENTED $v"; done
```

**Done when:** the user's chosen pages exist, every path/endpoint/env var mentioned exists in the code, every flow
explanation has a diagram you've looked at, and links resolve.
