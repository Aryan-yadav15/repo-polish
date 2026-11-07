# 12 · Maintaining many projects

Doing all of a user's repositories in one sitting produces shallow work and blows through API quotas.
Do **one project per session** and keep state in a queue file in the user's workspace (not in this repo).

## Triage first

```bash
gh repo list <owner> --limit 500 --json name,isFork,isArchived,isPrivate,homepageUrl,pushedAt,primaryLanguage > repos.json
```

For each repo, record: README size (`gh api repos/<owner>/<repo>/readme -q .size`, 404 = none),
whether the homepage URL responds, last push. Default READMEs from scaffolding tools are ~1.3–1.5 KB.

Sort into tiers and confirm the tiers with the user:

- **Showcase** — full pipeline (all 11 stages).
- **Light** — short README, one screenshot or live link, secrets + hygiene only.
- **Archive candidates** — duplicates, empty repos, experiments the owner no longer needs. Never archive or delete without explicit approval.
- **Skip** — anything the user names as off-limits (e.g. production repos).

## Queue file

```markdown
# Queue
`[ ]` todo · `[~]` in progress · `[x]` done · `[-]` needs owner decision

## Showcase
- [x] project-a — PR #1. Rotate: Gemini key. TODO(owner): event name.
- [~] project-b — blocked: needs Stripe test key
- [ ] project-c — deploy 404
```

Each session: take the first `[ ]`, mark it `[~]`, run the pipeline, then mark `[x]` with the PR link and notes.

## Scheduling

Any of these works — pick what the user's tools support:

- the user starts a session when they have time: *"Run the next project in QUEUE.md using AGENTS.md from <this-repo-url>"*
- a scheduled/cloud agent run on a cron, if their agent platform supports it (it then can't ask questions,
  so it should skip projects that need secrets it doesn't have, and leave them `[-]`)
- a local scheduler (cron / launchd / Task Scheduler) invoking a headless agent CLI
