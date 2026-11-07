# 2 · Secrets

**Goal:** no secret in the working tree, and the user knows exactly which secrets to rotate.

Do this **before** reading the rest of the code. Public repos get scraped for keys within minutes.

```bash
<this-repo>/tools/scan/secrets.sh .
```

It prints masked matches in two sections:

- **working tree** — fix every real one now:
  - move the value to an environment variable (`process.env.X`, `os.environ["X"]`, Pydantic settings, …)
  - add a `.env.example` (or `.env.local.example`) with placeholder values, and make sure `.env*` is in `.gitignore`
  - replace hardcoded passwords in docs and tests with obvious placeholders (`postgres`, `your-api-key`)
- **git history** — removing these from the code does **not** remove them from history. Add each one to the
  rotation list for the report. Don't rewrite history unless the user explicitly asks; it breaks forks and clones.

False positives (placeholders, example values) are common. Judge each hit; don't "fix" `password = "changeme"` in a test fixture.

Verify:

```bash
<this-repo>/tools/scan/secrets.sh . | sed -n '/working tree/,/git history/p'   # should show only placeholders
```

**Done when:** the working-tree section is clean or only placeholders, `.env.example` exists if the app needs config,
and you have a rotation list (provider + where it was found, never the value).
