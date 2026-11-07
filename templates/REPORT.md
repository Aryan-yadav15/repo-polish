# End-of-run report (message to the user)

Keep it short. Lead with the result, then what needs them.

```
<Project> is done — PR: <link> (not merged).

⚠️ Rotate these, they're in git history: <provider + file, never the value>

What changed
- README: <cards used>, demo GIF (<what it shows>, <size>)
- Fixes so it runs today: <one line each>
- Cleanup: <secrets → env, untracked files>

Verified
- <main feature + how correctness was checked>
- Cards viewed in light/dark; GIF frames checked

Needs you
- TODO(owner): <items>
- <anything skipped and why>

Cleanup — what should I do with these?
  <servers/containers, clone, envs, data — with sizes>
  1) keep running  2) stop only  3) full cleanup  4) pick items
  (unpushed/local-only: <anything that would be lost>)
```
