# 4 · Hygiene

**Goal:** remove things that should never have been committed. Small and safe only.

Look for and untrack (`git rm -r --cached <path>`, then add to `.gitignore`):

- virtualenvs (`venv/`, `.venv/`, `env/`, `Lib/site-packages`), `node_modules/`
- build output (`dist/`, `build/`, `.next/`, `out/`, `__pycache__/`)
- logs, local databases, caches, `.DS_Store`
- editor folders (`.idea/`, `.vscode/` unless they hold shared config)

```bash
git ls-files | grep -E '(^|/)(\.?venv|node_modules|dist|build|\.next|__pycache__|logs?)/' | cut -d/ -f1-2 | sort -u
du -sh .git
```

Do **not** in this stage: reformat code, rename files, delete "unused" code, upgrade frameworks, or rewrite history.
Note candidates (unused components, duplicate files) for the README's "What's next" instead.

**Done when:** the repo contains only source, config and docs, and `.gitignore` covers what you removed.
