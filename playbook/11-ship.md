# 11 · Ship

**Goal:** a reviewable pull request, and a short honest report to the user.

## Commit

Commit in logical steps (docs, cards, fixes) with clear messages. Stage paths explicitly; don't `git add -A`
blindly — apps often rewrite local data files while running.

**No AI attribution** (AGENTS.md rule 7): no `Co-Authored-By` trailer naming an AI, and no "Generated with …"
line in commits or the PR body. Many agent tools add these by default — disable or remove them. Check before pushing:

```bash
git log <default-branch>..HEAD --format=%B | grep -iE 'co-authored-by|generated with' && echo "STRIP THESE FIRST"
```

## Ask, then push

Pushing is outward-facing. Ask the user before the first push for each project, then:

```bash
git push -u origin maintain/readme-refresh
gh pr create --base <default-branch> --title "docs: refreshed README, demo GIF, and fixes so it runs today" \
  --body-file pr_body.md
```

Fill `pr_body.md` from `templates/PR_BODY.md`. Without the `gh` CLI, give the user the compare URL:
`https://github.com/<owner>/<repo>/compare/<default-branch>...maintain/readme-refresh`.

Never merge it yourself unless the user says so.

## Report

Send the user a message following `templates/REPORT.md`: link, what changed, what was verified,
**secrets to rotate**, TODOs only they can fill, and anything you couldn't do.

## Clean up — ask, don't assume

Keep a list, from stage 1 on, of everything you created outside the project's git history: running servers,
containers, downloaded images, virtualenvs, `node_modules`, sample datasets, logs, `.env` files holding secrets,
and the working clone itself. At the end, show the user that list with sizes and **ask how they want to clean up**.
Never delete anything without their answer. Offer choices like:

| Option | What it removes | When it fits |
|---|---|---|
| **Keep everything running** | nothing | they want to try the app or review the PR locally |
| **Stop only** | servers and containers (`docker rm -f <name>`) | free the ports, keep files for a later session |
| **Full cleanup** | the above + clone, virtualenvs, `node_modules`, sample data, logs, images you pulled | the PR is all they need |
| **Custom** | whatever they pick from the list | anything else |

Before deleting, warn about anything that exists **only** locally — e.g. unpushed commits or a rewritten branch
not yet force-pushed — and say whether it can be recreated. Only remove images and containers **you** created;
check nothing else uses them (`docker ps -a --filter ancestor=<image>`). Confirm afterwards that the ports are
free and list what was removed and the space recovered.
