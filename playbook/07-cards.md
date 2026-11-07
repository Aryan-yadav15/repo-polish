# 7 · Cards

**Goal:** designed, animated light/dark SVG visuals that replace plain tables and diagrams in the README.

Cards render inside GitHub's `<img>` sandbox: fonts are embedded and animation is SMIL, so no JavaScript or
external requests are needed at view time.

## Available cards

| Card | Section in `cards.json` | Replaces |
|---|---|---|
| hero | `hero` (required) | title + tagline + an animated "ask → result" demo + a facts strip |
| architecture | `arch` | a component diagram (client / server / data columns, animated data flow) |
| flow | `flow` | a numbered 4–6 step pipeline |
| capabilities | `capabilities` | a 2×2 "what you can do" table |
| decisions | `decisions` | a "why it's built this way" table |
| stack | `stack` | a tech-stack table, with [Simple Icons](https://simpleicons.org) logos by slug |
| terminal | `terminal` | a run-it terminal window (commands type in, output appears) |
| editor | `editor` | a code-editor window with real code, real line numbers and per-line notes |

Omit a section and that card isn't drawn. `templates/cards.example.json` documents every field;
`examples/nlp-sql/cards.json` is a full real config.

## Generate

```bash
cp <this-repo>/templates/cards.example.json <project>/docs/assets/cards.json   # then edit it
uv run --with fonttools --with brotli python <this-repo>/tools/cards/cards.py \
  <project>/docs/assets/cards.json <project>/docs/assets
```

Keep `cards.json` in the project, so the cards can be regenerated later.

## Content rules

- Everything on a card must be true. Demo rows in the hero should be **real output** from stage 5.
- Editor card: copy code verbatim from the file and use its real line numbers (`sed -n '100,110p' file`).
- Terminal card: output lines should match what the commands really print (versions, ports).
- Pick an accent per project (`accent.light` / `accent.dark`) — a darker shade for light mode, a brighter one for dark.

## Look at every card

```bash
for f in <project>/docs/assets/*.svg; do node <this-repo>/tools/gif/shot.mjs "$f" "/tmp/$(basename "$f" .svg).png" 7000; done
```

Open the PNGs. Check for: text running under other elements, content overflowing a box, numbers overlapping bars,
labels too long for their column. Shorten copy first; adjust layout constants in `cards.py` only if needed.

**Done when:** every card you use has been viewed in both light and dark and nothing overlaps or overflows.
