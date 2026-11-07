# 1 · Intake

**Goal:** a clean working copy on a new branch, plus a place for notes.

```bash
WORK=~/maintain-work            # any scratch folder outside this repo
mkdir -p "$WORK" && cd "$WORK"
git clone <target-repo-url> project && cd project
git checkout -b maintain/readme-refresh
```

Then write down, in a scratch `NOTES.md` outside the repo (never commit it):

- default branch name, last commit date, primary language(s)
- any live deploy URL (repo "About" field, `package.json` `homepage`, Vercel/Netlify config) and whether it responds:
  `curl -s -o /dev/null -w '%{http_code}' -L <url>`
- what the current README says the project does (you will check this against the code in stage 3)

**Done when:** you're on the new branch with a clean `git status`, and you know whether a live deploy exists.
