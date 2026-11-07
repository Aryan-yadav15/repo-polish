# 3 · Understand

**Goal:** know what the project *actually* does, well enough to explain its architecture and defend its design.

Existing docs are often aspirational ("enterprise-grade", "production ready"). Trust the code.

Read, in this order:

1. Manifests: `package.json`, `requirements.txt` / `pyproject.toml`, `go.mod`, `Cargo.toml`, Dockerfiles, compose files.
2. Entry points: server `main`, app router / pages, CLI entry, background workers.
3. The main request path end to end: input → processing → storage/external APIs → output.
4. Configuration: env vars, settings classes, defaults.

Capture in your notes:

- **One sentence**: what a user gets from it.
- **Components** and how they talk (HTTP, SSE, WebSocket, queue, DB). This becomes the architecture card.
- **The main flow** as 4–6 steps. This becomes the flow card.
- **3–5 real design decisions** with the *why* — each must point to code (file + line). These become the decisions card.
- **One or two lines of code** that capture the core idea, with real line numbers. This becomes the editor card.
- **Known weaknesses** (security, scale, missing tests). These become "What's next".
- Counts you might quote (number of tools, rules, endpoints) — **compute them**, don't estimate.

**Done when:** you could explain the project in a two-minute interview and every point maps to a file.
