# 6 · Demo GIF

**Goal:** a short, readable GIF of the real app doing its main job, under ~8 MB so GitHub renders it.

## Script the demo

Copy `templates/steps.example.json` and write 1–3 "moments" (the main feature, then the most visual one).
Steps run in order:

| Key | Does |
|---|---|
| `click` | click a selector |
| `fill` | `[selector, text]` — types it visibly |
| `press` | a key, e.g. `"Enter"` |
| `waitFor` | wait for a selector (e.g. `"text=Helena"`, `"canvas"`); `timeout` in ms |
| `scroll` | wheel by N px |
| `pause` | wait N ms (e.g. to respect an API rate limit) |
| `speed` | fast-forward everything this step waited on (×N) — use on AI/network waits |
| `wait` | hold after the step, ms (default 600) — give viewers time to read results |

Wait for something that only appears on **success** (a value from the correct answer), so a failed run can't
silently produce a GIF.

## Record

```bash
cd <this-repo>
W=1440 H=900 \
CROP='830:900:290:0' \
CSS='.particles,.sparkle{display:none!important}' \
GW=760 FPS=10 COLORS=128 \
node tools/gif/record.mjs http://localhost:3000 steps.json <project>/docs/demo.gif
```

- `W/H` viewport. `CROP=w:h:x:y` keeps just the main panel (find it from a screenshot via `tools/gif/shot.mjs`).
- `CSS` hides decoration that animates every frame (particles, shimmer). This is the single biggest size win.
- Size budget: ~8 MB. If over, lower `FPS` (8), `COLORS` (96) or `GW` (720) — in that order.

## Check it

Extract frames and look at them:

```bash
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 docs/demo.gif)
for f in 0.25 0.5 0.95; do ffmpeg -y -loglevel error -ss $(python3 -c "print($D*$f)") -i docs/demo.gif -frames:v 1 frame_$f.png; done
```

Text readable? Result visible long enough? No error toasts? No empty loading states?

**Done when:** the GIF shows a correct result, is ≤ ~8 MB, and you have looked at its frames.
Caption it in the README: what dataset it ran on, and that waits are sped up (if they are).
