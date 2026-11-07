# Architecture

ONE PARAGRAPH: what the system does and its main parts.

## Components

| Component | Responsibility | Code |
|---|---|---|
| NAME | WHAT IT OWNS | [`path/`](../path/) |

## How they communicate

PROTOCOLS AND WHY (HTTP, SSE, WebSocket, queue, DB). Note anything synchronous vs asynchronous.

## Main flow: WHAT HAPPENS WHEN …

<!-- Archify diagram (see playbook/08-docs.md); Mermaid fallback if unavailable -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="diagrams/main-flow-dark.png"/>
  <img src="diagrams/main-flow-light.png" width="100%" alt="DESCRIBE THE FLOW STEP BY STEP"/>
</picture>

<sub>[Interactive version](diagrams/main-flow.html) — download and open in a browser.</sub>

1. STEP — [`file.py:LINE`](../file.py#LLINE)
2. STEP — …

## Key decisions

- **DECISION.** WHY, WITH A LINK TO THE CODE. ([ADR](decisions/0001-TITLE.md) if one exists)

## Known limits

- LIMIT AND ITS CONSEQUENCE.
