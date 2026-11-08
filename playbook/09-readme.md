# 9 · README

**Goal:** a README that shows the project working in the first screen, explains how it's built, gets someone
running it in minutes, and is candid about its limits.

Start from `templates/README.template.md`. Order of sections:

1. **Hero card** (`<picture>` with light/dark sources) + a one-line nav.
2. **See it work** — the GIF, with a caption saying what it ran against.
3. **What you can do** — capabilities card (or a short list for small projects).
4. **How it works** — architecture card, flow card, decisions card, editor card;
   a detailed Mermaid sequence diagram inside `<details>` is a nice optional extra.
5. **Built with** — stack card.
6. **Run it** — prerequisites (with tested versions), terminal card, then **real fenced code blocks** with the commands.
7. **Project structure** — inside `<details>`.
8. **What's next** — honest limitations and the next fixes, from your stage 3 notes.

## Rules

- **Commands must be copyable.** Images can't be copied, so every command shown in the terminal card also appears
  in a fenced ```` ```bash ```` block. GitHub adds a copy button to each block, and selecting part of a block by hand
  still works normally. One block per terminal/process; no `$` or `❯` prompts inside blocks.
- Use `<picture><source media="(prefers-color-scheme: dark)" srcset="…-dark.svg"/><img src="…-light.svg" …/></picture>`
  for every card, with a real `alt` describing the content.
- Relative paths (`docs/assets/…`) so the README works on forks and branches.
- **Anchors:** GitHub drops symbols but keeps the space they leave, so `## ▸ See it work` becomes `#-see-it-work`
  (leading dash). Links to README sections from `docs/` must use that form: `../README.md#-whats-next`.
- No marketing filler ("enterprise-grade", "blazing fast", "revolutionary"). Specifics instead.
- Leave `TODO(owner)` for context only the owner knows (where/why it was built). Don't guess.
- Link into `docs/` (stage 8) instead of repeating it: the README stays a front page, `docs/` holds the detail.
- Keep existing long-form docs; move them into `docs/` or link them, never delete them.

**Done when:** the README renders (preview it — see stage 10), every image path exists, and every command block
works when pasted.
