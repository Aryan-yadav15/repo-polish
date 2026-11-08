# 5 · Run it

**Goal:** the project starts and its main feature works, on today's dependencies and APIs.

A README with a demo is only honest if the project runs. Expect breakage: dependencies drift and APIs change underneath every project.

## Set up

- Isolate dependencies outside the repo: `uv venv -p 3.12 ../.venv && VIRTUAL_ENV=../.venv uv pip install -r requirements.txt`,
  or `npm ci` / `npm install`.
- Use a runtime version the project's dependencies support. The newest Python or Node often lacks wheels/binaries
  (e.g. torch) — pick the newest version that works and **document it** in the README.
- Config goes in the git-ignored `.env` the user filled in. Never print it.

## Common breakage and the minimal fix

| Symptom | Usual cause | Fix |
|---|---|---|
| `ImportError` / missing attribute in a library | unpinned dependency jumped a major version | pin to the major the code was written for (`langchain>=0.3,<0.4`) and comment why |
| 404 / "model not found" from an AI API | model retired | switch to the current equivalent; verify by calling it |
| 429 / quota | free-tier limits (often per model, per minute *and* per day) | space out calls, or use another model; tell the user |
| Can't connect to DB | no local DB | run one in Docker from the official image (`postgres:16`, `mongo:7`) on a free port bound to `127.0.0.1`; load a public sample dataset or the project's seed/migrations |
| Crash on the main path | real bug | fix it if it's small and clearly a bug; note it in the PR |

Ask the user before running containers or anything that installs system-wide.

## Audit dependencies (report, don't fix)

Run the ecosystem's audit (`npm audit --omit=dev`, `pip-audit`, `cargo audit`, …) and record the counts by severity for
the report and the README's "What's next". Don't mass-upgrade to clear warnings — that's a separate, riskier change.
Fix one only if it's a direct dependency on the main path and the patch release is compatible.

## Prove it works

Exercise the main feature for real (UI or API) and check the output is **correct**, not just non-empty.
E.g. compare an AI-generated query result against the same query run directly on the database.

**Done when:** you've seen the main feature produce a correct result, and every fix you made is listed for the PR.
If it can't run (a third-party service shut down, private data unavailable), say so — stage 6 then uses screenshots of a
live deploy, or is skipped and the README says why.
