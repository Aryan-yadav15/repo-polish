#!/usr/bin/env bash
# Usage: tools/scan/secrets.sh <repo-path>
# Finds likely secrets in the working tree AND in git history. Values are masked in the output,
# so it is safe to paste into an agent transcript. Exit code 1 if anything was found.
set -euo pipefail
cd "${1:-.}"

PATTERNS=(
  'AIza[0-9A-Za-z_-]{35}'                       # Google / Gemini / Firebase API key
  'sk-[A-Za-z0-9_-]{20,}'                       # OpenAI / Anthropic style keys
  'gsk_[A-Za-z0-9]{20,}'                        # Groq
  'ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,}'  # GitHub tokens
  'xox[baprs]-[A-Za-z0-9-]{10,}'                # Slack
  'AKIA[0-9A-Z]{16}'                            # AWS access key id
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'          # private keys
  '(postgres(ql)?|mysql|mongodb(\+srv)?|redis)://[^:/ "]+:[^@/ "]+@'  # DB URLs with passwords
  '(password|passwd|secret|api_key|apikey|token)["'"'"' ]*[:=] *["'"'"'][^"'"'"' ]{6,}["'"'"']'  # hardcoded assignments
)
re=$(IFS='|'; echo "${PATTERNS[*]}")
# keep file:line context, hide everything after the first 6 chars of each match
mask() { RE="$re" perl -pe 's/($ENV{RE})/substr($1,0,6)."***"/ge'; }

echo "== working tree =="
tree=$(git grep -nIE "$re" -- ':!*.lock' ':!package-lock.json' ':!*.min.js' ':!*example*' 2>/dev/null || true)
[ -n "$tree" ] && echo "$tree" | cut -c1-200 | mask || echo "clean"

echo "== git history (secrets here must be ROTATED even after removal) =="
hist=$(git log -p --all -G"$re" --format='commit %h %ad' --date=short 2>/dev/null | grep -E "^commit |^\+.*($re)" | grep -B1 -E '^\+' | grep -v '^--$' || true)
[ -n "$hist" ] && echo "$hist" | cut -c1-200 | mask || echo "clean"

[ -z "$tree$hist" ]
