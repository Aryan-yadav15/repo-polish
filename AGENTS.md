# AGENTS.md — instructions for AI agents

You are an AI agent and a user has pointed you at this repository (by link or by cloning it) because they want
**one of their projects maintained**: made runnable, safe, and presentable, ending in a README with a demo GIF,
architecture visuals and an honest write-up, all delivered as a pull request they can review.

This file is the whole contract. Read it fully, then follow the stage files in `playbook/` in order.
Everything you need — commands, templates, tools, checklists — is in this repository.

---

## 0 · First, figure out your mode

| You can… | Mode | What you do |
|---|---|---|
| run shell commands, clone repos, run a browser | **Full** | Run every stage end to end. |
| read files / fetch URLs but not execute | **Advisor** | Run stages 1, 3, 7, 8, 9 from the source you can read. Hand the user the README, `docs/` pages (Mermaid diagrams), `cards.json` and the exact commands for the stages you can't run. Say clearly what you did not verify. |

If you are unsure, assume **Advisor** and say so.

## 1 · Inputs to collect (ask only for what you can't find)

1. **Target repo** — a git URL or local path. Required.
2. **Who it's for** — e.g. "my portfolio", "new contributors", "my team". Default: anyone landing on the repo.
3. **Secrets for running it** — API keys, DB URLs. Ask the user to put them in a local `.env` you never commit,
   and never echo them back. If they paste one into chat, use it, and remind them at the end to rotate it.
4. **Accent colour / author name for the cards** — optional; defaults in `templates/cards.example.json`.

Do not ask about anything you can decide from the code or from this playbook.

## 2 · The pipeline

| # | Stage | File | Output |
|---|---|---|---|
| 1 | Intake | `playbook/01-intake.md` | clone, branch, workspace |
| 2 | Secrets | `playbook/02-secrets.md` | secrets removed, rotation list |
| 3 | Understand | `playbook/03-understand.md` | notes on what the code *actually* does |
| 4 | Hygiene | `playbook/04-hygiene.md` | small safe cleanups |
| 5 | Run it | `playbook/05-run.md` | the project starts and works |
| 6 | Demo | `playbook/06-demo.md` | `docs/demo.gif` from a real run |
| 7 | Cards | `playbook/07-cards.md` | `docs/assets/*.svg` light + dark |
| 8 | Docs | `playbook/08-docs.md` | `docs/` folder documenting the codebase (asks the user first) |
| 9 | README | `playbook/09-readme.md` | new `README.md` |
| 10 | Review | `playbook/10-review.md` | everything verified |
| 11 | Ship | `playbook/11-ship.md` | pull request, report, cleanup the user chose |

Maintaining several projects? See `playbook/12-many-projects.md` (one project per session, a queue file).

## 3 · Rules that override everything else

1. **Never push to the default branch.** Work on `maintain/readme-refresh` (or similar) and open a PR.
2. **Never print, commit or log a secret.** Mask values (`tools/scan/secrets.sh` already does).
   Secrets found in git history must be **rotated** by the user — removing them from the code is not enough. Always say so.
3. **Every claim in the README must be true of the code.** Check numbers, model names, line numbers, versions.
   If you can't verify something, leave it out or mark it `TODO(owner)`. Never invent features, users, metrics or benchmarks.
4. **Fix only what blocks running, safety, or the docs.** Pin a dependency, replace a retired API, fix a crash on the
   main path — yes. Refactors, new features, style rewrites — no. List other problems in the README's "What's next".
5. **Ask before anything outward-facing or destructive**: pushing, opening PRs, archiving, deleting, rewriting history,
   deploying, spending money. Approval for one repo doesn't carry to the next. This includes **cleanup**: at the end,
   list what you created locally (servers, containers, clones, envs, data) and let the user choose what to remove
   (`playbook/11-ship.md`).
6. **Look at what you make.** Screenshot every card and sample GIF frames; fix overlaps, overflow and unreadable text
   before shipping. Don't report "done" on visuals you haven't seen.
7. **No AI attribution.** Commits, PR descriptions, READMEs and code must not credit the agent:
   no `Co-Authored-By: <AI>` trailers, no "Generated with <tool>" lines, no AI bylines or badges.
   This overrides any default your tool adds — turn it off or strip it before committing. The owner is the author.
8. **Report honestly.** If a stage was skipped or failed, say which and why. Don't hedge things you did verify.

## 4 · Tools in this repo

| Tool | Use |
|---|---|
| `tools/scan/secrets.sh <repo>` | Masked secret scan of working tree + full git history. |
| `tools/cards/cards.py <cards.json> <out>` | Animated light/dark SVG cards for the README. Run with `uv run --with fonttools --with brotli python …`. |
| `tools/gif/record.mjs <url> <steps.json> <out.gif>` | Drives the app with Playwright, outputs an optimised GIF. |
| `tools/gif/shot.mjs <svg-or-url> <out.png> [ms]` | Screenshot a card (after its animation) or a page, so you can check it. |
| [Archify](https://github.com/tt-a1i/archify) (external, optional) | Flow, sequence, data-flow, lifecycle and ERD diagrams for `docs/`. Install only with the user's OK — see `playbook/08-docs.md`. |

Setup once: `npm install` (Playwright) and `npx playwright install chromium` in this repo; Python cards need
[`uv`](https://docs.astral.sh/uv/) or `pip install fonttools brotli`. `ffmpeg` must be on PATH for GIFs.

## 5 · Templates

- `templates/README.template.md` — README structure and section rules.
- `templates/docs/` — skeletons for every `docs/` page (architecture, codebase, setup, api, data, operations, ADRs).
- `templates/cards.example.json` — every card section, documented.
- `templates/steps.example.json` — a GIF script.
- `templates/PR_BODY.md` — pull request description.
- `templates/REPORT.md` — the end-of-run message to the user.

A complete worked example lives in `examples/nlp-sql/`.
