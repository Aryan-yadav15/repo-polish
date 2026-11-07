<!-- Cards are generated from docs/assets/cards.json with repo-polish (tools/cards/cards.py). Regenerate after editing it. -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/hero-dark.svg"/>
  <img src="docs/assets/hero-light.svg" width="100%" alt="PROJECT. TAGLINE. ONE-SENTENCE DESCRIPTION."/>
</picture>

<p align="center">
  <a href="#-see-it-work"><b>Demo</b></a> &nbsp;·&nbsp;
  <a href="#-how-it-works"><b>Architecture</b></a> &nbsp;·&nbsp;
  <a href="#-run-it"><b>Run it</b></a> &nbsp;·&nbsp;
  <a href="#-whats-next"><b>What's next</b></a>
</p>

<!-- TODO(owner): one line of context — where/why this was built -->

## ▸ See it work

<p align="center">
  <img src="docs/demo.gif" width="760" alt="DESCRIBE WHAT THE GIF SHOWS, STEP BY STEP"/>
</p>
<p align="center"><sub>Real run against DATASET · waits for the model are sped up</sub></p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/capabilities-dark.svg"/>
  <img src="docs/assets/capabilities-light.svg" width="100%" alt="LIST THE FOUR CAPABILITIES"/>
</picture>

## ▸ How it works

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/architecture-dark.svg"/>
  <img src="docs/assets/architecture-light.svg" width="100%" alt="DESCRIBE THE COMPONENTS AND HOW THEY CONNECT"/>
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/flow-dark.svg"/>
  <img src="docs/assets/flow-light.svg" width="100%" alt="LIST THE STEPS"/>
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/decisions-dark.svg"/>
  <img src="docs/assets/decisions-light.svg" width="100%" alt="LIST THE DECISIONS"/>
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/editor-dark.svg"/>
  <img src="docs/assets/editor-light.svg" width="100%" alt="DESCRIBE THE CODE SHOWN"/>
</picture>

<details>
<summary><b>Request sequence (detailed)</b></summary>

```mermaid
sequenceDiagram
    participant UI
    participant API
    participant DB
    UI->>API: request
    API->>DB: query
    DB-->>API: rows
    API-->>UI: response
```

</details>

## ▸ Built with

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/stack-dark.svg"/>
  <img src="docs/assets/stack-light.svg" width="100%" alt="LIST THE STACK"/>
</picture>

## ▸ Run it

You need RUNTIME VERSIONS (TESTED WITH …), SERVICES, and KEYS (WITH LINKS TO GET THEM).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/terminal-dark.svg"/>
  <img src="docs/assets/terminal-light.svg" width="100%" alt="DESCRIBE WHAT THE COMMANDS START"/>
</picture>

**Terminal 1 · backend** → http://localhost:8000

```bash
# the exact commands shown in the terminal card, one process per block, no prompts
```

**Terminal 2 · frontend** → http://localhost:3000

```bash
# …
```

<details>
<summary><b>Project structure</b></summary>

```
src/            what lives here
```

</details>

## ▸ What's next

- **AREA.** The honest limitation, and the fix you'd make.

<sub>More detail: LINKS TO EXISTING LONG-FORM DOCS</sub>
